"""ステップ4: 都道府県別 箇所別基本表CSV を結合。

元スクリプト(3_kasho_csv_merge.py)相当。
- 文字コードを自動判定（csv_encodings を順に試行）
- 全列空白の行を除去
- キー列(交通調査基本区間番号)を必要に応じ zfill（H27対策）
"""
from __future__ import annotations
import glob
import os

import numpy as np
import pandas as pd

from .config import Config, ensure_dirs


def _read_any(path: str, encodings: list[str]) -> pd.DataFrame | None:
    for enc in encodings:
        try:
            return pd.read_csv(path, encoding=enc, dtype=str)
        except UnicodeDecodeError:
            continue
    return None


def run(cfg: Config) -> str:
    ensure_dirs(cfg)
    files = sorted(glob.glob(os.path.join(cfg.kasho_dir, "*.csv")))
    if not files:
        raise FileNotFoundError(f"箇所別基本表CSVが見つかりません: {cfg.kasho_dir}")

    frames = []
    for fp in files:
        df = _read_any(fp, cfg.csv_encodings)
        if df is None:
            print(f"  警告: 文字コード判定失敗 {os.path.basename(fp)}", flush=True)
            continue
        if cfg.key_zfill and cfg.key_column in df.columns:
            df[cfg.key_column] = df[cfg.key_column].str.zfill(cfg.key_zfill)
        frames.append(df)

    merged = pd.concat(frames, ignore_index=True)
    # 全列空白/NaN の行を除去
    merged = merged.replace(r"^\s*$", np.nan, regex=True).dropna(how="all")

    out = cfg.merged_csv
    merged.to_csv(out, index=False, encoding="utf-8")
    print(f"[merge_csv] {len(files)} ファイル -> {len(merged):,} 行 -> {out}", flush=True)
    return out
