"""ステップ2: 分割GeoJSONタイルを1ファイルにマージ。

元スクリプト(1_geojson_merge.py)相当。geopandasで全タイルを読み込み結合する。
"""
from __future__ import annotations
import glob
import os

import pandas as pd
import geopandas as gpd

from .config import Config, ensure_dirs


def run(cfg: Config) -> str:
    ensure_dirs(cfg)
    files = sorted(glob.glob(os.path.join(cfg.tiles_dir, "*.geojson")))
    if not files:
        raise FileNotFoundError(f"タイルが見つかりません: {cfg.tiles_dir}")
    print(f"[merge_geojson] {len(files):,} タイルを読み込み中...", flush=True)

    frames = []
    for i, fp in enumerate(files, 1):
        try:
            frames.append(gpd.read_file(fp))
        except Exception as e:
            print(f"  警告: 読み込み失敗 {os.path.basename(fp)}: {e}", flush=True)
        if i % 2000 == 0:
            print(f"  {i:,}/{len(files):,}", flush=True)

    gdf = gpd.GeoDataFrame(pd.concat(frames, ignore_index=True))
    out = cfg.merged_geojson
    gdf.to_file(out, driver="GeoJSON")
    print(f"[merge_geojson] {len(gdf):,} features -> {out}", flush=True)
    return out
