#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""可視化ツールの分割GeoJSONタイル（道路種別 × z/x/y）を単体でダウンロードする。

ロジックは census_converter/download.py に一本化し、本スクリプトは薄いラッパー。
通常はパイプライン統合版（`python run.py --year r03 --step download`）を使う。
保存先は data/{year}/geojson_tiles/。

    python scripts/download_geojson_tiles.py --year r03
    python scripts/download_geojson_tiles.py --year h27
"""
from __future__ import annotations
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from census_converter.config import load_config       # noqa: E402
from census_converter.download import download_geojson  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser(description="GeoJSONタイルのダウンロード")
    p.add_argument("--year", required=True, help="対象年度（r03 / h27）")
    p.add_argument("--force", action="store_true", help="既存ファイルも再取得する")
    args = p.parse_args()
    cfg = load_config(args.year)
    print(f"保存先: {cfg.tiles_dir}")
    download_geojson(cfg, skip_existing=not args.force)


if __name__ == "__main__":
    main()
