"""ステップ7: 出力形式変換（FlatGeobuf / GeoParquet / PMTiles）。

元の ogr2ogr / tippecanoe 手順相当。外部コマンド（ogr2ogr, tippecanoe）を呼び出す。
crs 指定がある場合は ogr2ogr の -t_srs で再投影する。
"""
from __future__ import annotations
import os
import shutil
import subprocess

from .config import Config, ensure_dirs


def _run(cmd: list[str]) -> None:
    print("  $ " + " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def to_fgb(cfg: Config, src_geojson: str | None = None) -> str:
    if not shutil.which("ogr2ogr"):
        raise RuntimeError("ogr2ogr が見つかりません（GDALをインストールしてください）")
    src = src_geojson or cfg.output_geojson
    dst = os.path.join(cfg.output_dir, f"{cfg.output_basename}_convert.fgb")
    cmd = ["ogr2ogr", "-f", "FlatGeobuf"]
    if cfg.crs:
        cmd += ["-t_srs", cfg.crs]
    cmd += [dst, src]
    _run(cmd)
    return dst


def to_parquet(cfg: Config, src_fgb: str | None = None) -> str:
    if not shutil.which("ogr2ogr"):
        raise RuntimeError("ogr2ogr が見つかりません（GDALをインストールしてください）")
    src = src_fgb or os.path.join(cfg.output_dir, f"{cfg.output_basename}_convert.fgb")
    dst = os.path.join(cfg.output_dir, f"{cfg.output_basename}_convert.parquet")
    _run(["ogr2ogr", "-f", "Parquet", dst, src])
    return dst


def to_pmtiles(cfg: Config, src_geojson: str | None = None,
               min_zoom: int = 4, max_zoom: int = 14) -> str:
    if not shutil.which("tippecanoe"):
        raise RuntimeError("tippecanoe が見つかりません")
    src = src_geojson or cfg.output_geojson
    dst = os.path.join(cfg.output_dir, f"{cfg.output_basename}_convert.pmtiles")
    _run(["tippecanoe", "-o", dst, "-Z", str(min_zoom), "-z", str(max_zoom),
          "--drop-densest-as-needed", "--force", src])
    return dst


def run(cfg: Config, formats: tuple[str, ...] = ("fgb", "parquet")) -> None:
    ensure_dirs(cfg)
    fgb = None
    if "fgb" in formats or "parquet" in formats:
        fgb = to_fgb(cfg)
    if "parquet" in formats:
        to_parquet(cfg, fgb)
    if "pmtiles" in formats:
        to_pmtiles(cfg)
    print("[export] 完了", flush=True)
