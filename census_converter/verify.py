"""検証ステップ: 紐づけ率・孤児タイル・未マッチ内訳をオフラインで点検。

VERIFICATION.md の手順を再現可能な形で組み込んだもの。サーバアクセスは行わない。
"""
from __future__ import annotations
import collections
import csv
import glob
import os
import re

from .config import Config

_CENSUS_RE = re.compile(rb'"census":\s*"([0-9]+)"')


def _geojson_census_counts(path: str, key_prop: str = "census") -> collections.Counter:
    pat = re.compile(('"%s":\\s*"([0-9]+)"' % re.escape(key_prop)).encode())
    counts: collections.Counter = collections.Counter()
    with open(path, "rb") as f:
        for line in f:
            for m in pat.finditer(line):
                counts[m.group(1).decode()] += 1
    return counts


def _csv_keys(path: str, key_column: str) -> collections.Counter:
    csv.field_size_limit(1 << 30)
    counts: collections.Counter = collections.Counter()
    with open(path, encoding="utf-8", newline="") as f:
        r = csv.reader(f)
        header = next(r)
        ki = header.index(key_column)
        for row in r:
            if row and len(row) > ki:
                counts[row[ki]] += 1
    return counts


def check_join(cfg: Config, geojson: str | None = None, csv_path: str | None = None) -> dict:
    """census ⇔ key の双方向マッチ率を測る。"""
    geojson = geojson or cfg.merged_geojson
    csv_path = csv_path or cfg.transformed_csv
    geo = _geojson_census_counts(geojson, cfg.geojson_key_property)
    keys = _csv_keys(csv_path, cfg.key_column)
    geo_u, csv_u = set(geo), set(keys)
    geo_total = sum(geo.values())
    feat_matched = sum(v for k, v in geo.items() if k in csv_u)
    res = {
        "geojson_features": geo_total,
        "geojson_unique": len(geo_u),
        "csv_rows": sum(keys.values()),
        "csv_unique": len(csv_u),
        "matched_unique": len(geo_u & csv_u),
        "geojson_only": len(geo_u - csv_u),
        "csv_only": len(csv_u - geo_u),
        "feature_join_rate": (feat_matched / geo_total * 100) if geo_total else 0.0,
    }
    print("[verify.join]")
    for k, v in res.items():
        print(f"  {k}: {v:,}" if isinstance(v, int) else f"  {k}: {v:.2f}")
    return res


def check_tiles(cfg: Config, tiles_dir: str | None = None) -> dict:
    """DL済みタイルが tileindex 内か（孤児検査）、indexカバー率。"""
    tiles_dir = tiles_dir or cfg.tiles_dir
    idx = set()
    with open(cfg.tileindex, newline="") as f:
        for row in csv.reader(f):
            if len(row) >= 3 and row[0].strip().isdigit():
                idx.add((row[2], row[0], row[1]))  # z,x,y
    covered = set()
    orphan = 0
    for fn in os.listdir(tiles_dir):
        if not fn.endswith(".geojson"):
            continue
        p = fn[:-8].split("_")
        key = (p[-3], p[-2], p[-1])
        if key in idx:
            covered.add(key)
        else:
            orphan += 1
    res = {
        "index_tiles": len(idx),
        "covered_tiles": len(covered),
        "coverage_pct": len(covered) / len(idx) * 100 if idx else 0.0,
        "orphan_files": orphan,
    }
    print("[verify.tiles]")
    for k, v in res.items():
        print(f"  {k}: {v:,}" if isinstance(v, int) else f"  {k}: {v:.2f}")
    return res


def run(cfg: Config) -> dict:
    out = {}
    if os.path.isdir(cfg.tiles_dir) and glob.glob(os.path.join(cfg.tiles_dir, "*.geojson")):
        out["tiles"] = check_tiles(cfg)
    if os.path.exists(cfg.merged_geojson) and os.path.exists(cfg.transformed_csv):
        out["join"] = check_join(cfg)
    return out
