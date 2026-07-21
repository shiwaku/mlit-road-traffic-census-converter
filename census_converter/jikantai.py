"""ステップ: 時間帯別交通量表(zkntrf) → ビューワ用 県別JSON ルックアップ生成。

道路交通センサスの時間帯別交通量表(`zkntrf{NN}.csv`、県別 01–47)を、Webマップの
地物クリック時に引ける複合キー辞書(県別JSON)へ変換する（DESIGN §8, 案1=外部ルックアップ方式）。

- 結合キー: `都道府県指定市代表市コード` は持たず、時間帯別表のキーは
  複合キー `都道府県指定市コード` + `交通量調査単位区間番号`（＝交通量を実測した調査単位区間）。
  ジオメトリ(PMTiles)側もこの2列を保持しているため、PMTiles無改変でクリック時ルックアップできる。
- 粒度: 1調査単位区間 = 最大4行（上下{1,2}×車種{1=小型,2=大型}）。1観測値を複数の基本区間が共有する。
- 都道府県指定市コードは単一のzkntrfファイルにのみ出現する（跨がない）ため、
  クリック地物のコードから読むべき県別JSONが一意に決まる（NN = コード // 1000）。

出力: `data/{year}/output/jikantai/{NN}.json` と `index.json`。
"""
from __future__ import annotations
import csv
import glob
import json
import os

from .config import Config, ensure_dirs

# 結合キー列（両年度共通）
K_PREF = "都道府県指定市コード"
K_UNIT = "交通量調査単位区間番号"
K_DIR = "上り・下りの別"      # 1=上り, 2=下り
K_VEH = "車種区分"           # 1=小型, 2=大型
C_12H = "昼間１２時間自動車類交通量（台）"
C_24H = "２４時間自動車類交通量（台）"

# 時間帯列（表の並びは 7→…→23→0→…→6 の24列）。列名は「…／{全角時刻}時台」。
_HOUR_ORDER = list(range(7, 24)) + list(range(0, 7))  # 表の列順に対応する時刻
_FW = str.maketrans("0123456789", "０１２３４５６７８９")
def _hour_col(h: int) -> str:
    return f"時間帯別自動車類交通量（台／時）／{str(h).translate(_FW)}時台"

DIR_KEY = {"1": "up", "2": "down"}
VEH_KEY = {"1": "s", "2": "l"}


def _norm(v: str | None) -> str | None:
    """'10'/'10.0'/10 -> '10'（canonical int-string）。空は None。"""
    if v is None:
        return None
    s = str(v).strip()
    if s == "":
        return None
    try:
        return str(int(float(s)))
    except ValueError:
        return s


def _num(v: str | None):
    """整数化。空/非数値は None。"""
    if v is None:
        return None
    s = str(v).strip()
    if s == "":
        return None
    try:
        return int(float(s))
    except ValueError:
        return None


def _read_csv(path: str, encodings: list[str]) -> list[dict] | None:
    for enc in encodings:
        try:
            with open(path, encoding=enc, newline="") as f:
                return list(csv.DictReader(f))
        except UnicodeDecodeError:
            continue
    return None


def _empty_series() -> dict:
    return {"s": [None] * 24, "l": [None] * 24}


def _build_prefecture(rows: list[dict]) -> dict:
    """1県分のzkntrf行 → {"<pref>_<unit>": {up/down: {s,l}, t12, t24}}。"""
    # 表の列順→時刻(0-23)への並べ替えマップ
    hour_cols = [(_hour_col(h), h) for h in _HOUR_ORDER]
    units: dict[str, dict] = {}
    for r in rows:
        pref = _norm(r.get(K_PREF))
        unit = _norm(r.get(K_UNIT))
        if pref is None or unit is None:
            continue
        dk = DIR_KEY.get(str(r.get(K_DIR, "")).strip())
        vk = VEH_KEY.get(str(r.get(K_VEH, "")).strip())
        if dk is None or vk is None:
            continue
        key = f"{pref}_{unit}"
        u = units.setdefault(key, {"up": _empty_series(), "down": _empty_series(),
                                   "t12": {"s": None, "l": None}, "t24": {"s": None, "l": None}})
        arr = u[dk][vk]
        for col, h in hour_cols:
            arr[h] = _num(r.get(col))
        # t12/t24 は車種別に上り+下りを合算（1区間の上下計）。
        for tk, col in (("t12", C_12H), ("t24", C_24H)):
            v = _num(r.get(col))
            if v is not None:
                u[tk][vk] = (u[tk][vk] or 0) + v
    return units


def run(cfg: Config) -> str:
    ensure_dirs(cfg)
    files = sorted(glob.glob(os.path.join(cfg.jikantai_dir, "zkntrf*.csv")))
    if not files:
        raise FileNotFoundError(f"時間帯別交通量表CSVが見つかりません: {cfg.jikantai_dir}")

    out_dir = os.path.join(cfg.output_dir, "jikantai")
    os.makedirs(out_dir, exist_ok=True)

    index: dict[str, str] = {}   # 都道府県指定市コード -> NN
    total_units = 0
    for fp in files:
        nn = os.path.basename(fp)[6:8]  # zkntrf01.csv -> "01"
        rows = _read_csv(fp, cfg.csv_encodings)
        if rows is None:
            print(f"  警告: 文字コード判定失敗 {os.path.basename(fp)}", flush=True)
            continue
        units = _build_prefecture(rows)
        # コード -> NN 対応を記録（コードは単一ファイルにのみ出現する前提を検証）
        for r in rows:
            pref = _norm(r.get(K_PREF))
            if pref is None:
                continue
            if pref in index and index[pref] != nn:
                raise ValueError(
                    f"都道府県指定市コード {pref} が複数ファイルに出現 ({index[pref]}, {nn})")
            index[pref] = nn
        payload = {"year": cfg.year, "hours": list(range(24)), "units": units}
        with open(os.path.join(out_dir, f"{nn}.json"), "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
        total_units += len(units)
        print(f"  [{nn}] {len(rows):,}行 -> {len(units):,}区間", flush=True)

    with open(os.path.join(out_dir, "index.json"), "w", encoding="utf-8") as f:
        json.dump({"year": cfg.year, "pref_to_file": index}, f,
                  ensure_ascii=False, separators=(",", ":"))
    print(f"[jikantai] {len(files)}県 -> {total_units:,}区間 -> {out_dir}", flush=True)
    return out_dir
