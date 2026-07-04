"""ステップ2: 分割GeoJSONタイルを1ファイルにマージ。

元スクリプト(1_geojson_merge.py)は geopandas を使っていたが、数万タイルでは低速。
ここでは JSON を直接ストリーム結合する（座標を完全保持・高速・破損ファイルをスキップ）。
crs は年度内で一貫しているため、最初に読めたタイルの crs を採用する。
"""
from __future__ import annotations
import glob
import json
import os

from .config import Config, ensure_dirs


def _peek_crs(files: list[str]):
    """最初に正常に読めたタイルの crs を返す（無ければ None）。"""
    for fp in files:
        try:
            with open(fp, encoding="utf-8") as f:
                data = json.load(f)
            return data.get("crs")
        except (ValueError, UnicodeDecodeError):
            continue
    return None


def run(cfg: Config, tiles_dir: str | None = None) -> str:
    ensure_dirs(cfg)
    src_dir = tiles_dir or cfg.tiles_dir
    files = sorted(glob.glob(os.path.join(src_dir, "*.geojson")))
    if not files:
        raise FileNotFoundError(f"タイルが見つかりません: {src_dir}")
    print(f"[merge_geojson] {len(files):,} タイルを結合中...", flush=True)

    crs = _peek_crs(files)
    out = cfg.merged_geojson
    n_feat = 0
    n_skip = 0
    first = True
    with open(out, "w", encoding="utf-8") as w:
        w.write('{\n"type": "FeatureCollection",\n')
        if crs is not None:
            w.write('"crs": ' + json.dumps(crs, ensure_ascii=False) + ",\n")
        w.write('"features": [\n')
        for i, fp in enumerate(files, 1):
            try:
                with open(fp, encoding="utf-8") as f:
                    data = json.load(f)
            except (ValueError, UnicodeDecodeError):
                n_skip += 1
                continue
            for feat in data.get("features", []):
                w.write("" if first else ",\n")
                w.write(json.dumps(feat, ensure_ascii=False))
                first = False
                n_feat += 1
            if i % 3000 == 0:
                print(f"  {i:,}/{len(files):,}  features={n_feat:,} skip={n_skip}", flush=True)
        w.write("\n]\n}\n")

    print(f"[merge_geojson] {n_feat:,} features / crs={_crs_name(crs)} / skip={n_skip} -> {out}",
          flush=True)
    return out


def _crs_name(crs) -> str:
    if not crs:
        return "なし(WGS84)"
    try:
        return crs["properties"]["name"]
    except Exception:
        return "指定あり"
