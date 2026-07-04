#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""時間帯別交通量表（zkntrf{NN}.csv, 都道府県 01-47）を単体でダウンロードする。

ロジックは census_converter/download.py に一本化し、本スクリプトは薄いラッパー。
通常はパイプライン統合版（`python run.py --year r03 --step download`）で
geojson_tiles + kasho + jikantai をまとめて取得できるが、時間帯別交通量表だけを
取り直したい場合にこれを使う。保存先は data/{year}/csv/jikantai/（DESIGN.md §8）。

    python scripts/download_jikantai_csv.py --year r03
    python scripts/download_jikantai_csv.py --year h27
"""
from __future__ import annotations
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from census_converter.config import load_config          # noqa: E402
from census_converter.download import download_jikantai_csv  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser(description="時間帯別交通量表CSVのダウンロード")
    p.add_argument("--year", required=True, help="対象年度（r03 / h27）")
    p.add_argument("--force", action="store_true", help="既存ファイルも再取得する")
    args = p.parse_args()
    cfg = load_config(args.year)
    if not cfg.jikantai_csv_url_template:
        sys.exit(f"[{args.year}] 時間帯別交通量表URL(jikantai_csv_url_template)が未設定です")
    print(f"保存先: {cfg.jikantai_dir}")
    download_jikantai_csv(cfg, skip_existing=not args.force)


if __name__ == "__main__":
    main()
