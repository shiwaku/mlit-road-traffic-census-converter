#!/usr/bin/env python3
"""MLIT 道路交通センサス コンバーター CLI。

例:
  python run.py --year r03 --step all
  python run.py --year h27 --step download
  python run.py --year r03 --step merge,normalize,mergecsv,transform,join,export
  python run.py --year r03 --step verify
"""
from __future__ import annotations
import argparse
import sys

from census_converter import (
    config, download, merge_geojson, normalize_geometry,
    merge_csv, transform_csv, join, export, verify, jikantai,
)

# ステップ名 -> 実行関数
STEPS = ["download", "merge", "normalize", "mergecsv", "transform", "join", "export", "jikantai", "verify"]
ALL_PIPELINE = ["download", "merge", "normalize", "mergecsv", "transform", "join", "export", "jikantai", "verify"]


def run_step(name: str, cfg: config.Config, formats: tuple[str, ...]) -> None:
    print(f"\n===== [{cfg.year}] step: {name} =====", flush=True)
    if name == "download":
        download.run(cfg)
    elif name == "merge":
        merge_geojson.run(cfg)
    elif name == "normalize":
        normalize_geometry.run(cfg)
    elif name == "mergecsv":
        merge_csv.run(cfg)
    elif name == "transform":
        transform_csv.run(cfg)
    elif name == "join":
        join.run(cfg)
    elif name == "export":
        export.run(cfg, formats=formats)
    elif name == "jikantai":
        jikantai.run(cfg)
    elif name == "verify":
        verify.run(cfg)
    else:
        raise ValueError(f"未知のステップ: {name}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="MLIT 道路交通センサス コンバーター")
    ap.add_argument("--year", required=True, help="対象年度 (configs/{year}.yaml)")
    ap.add_argument("--step", default="all",
                    help=f"実行ステップ（カンマ区切り、または all）。選択肢: {','.join(STEPS)}")
    ap.add_argument("--formats", default="fgb,parquet",
                    help="export形式（fgb,parquet,pmtiles）")
    ap.add_argument("--data-root", default=None, help="作業ルート（既定: ./data）")
    args = ap.parse_args(argv)

    cfg = config.load_config(args.year, data_root=args.data_root)
    config.ensure_dirs(cfg)

    steps = ALL_PIPELINE if args.step == "all" else [s.strip() for s in args.step.split(",")]
    bad = [s for s in steps if s not in STEPS]
    if bad:
        ap.error(f"未知のステップ: {bad}")
    formats = tuple(s.strip() for s in args.formats.split(",") if s.strip())

    print(f"対象: {cfg.label} ({cfg.year})  作業ディレクトリ: {cfg.data_dir}")
    for s in steps:
        run_step(s, cfg, formats)
    print("\n完了。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
