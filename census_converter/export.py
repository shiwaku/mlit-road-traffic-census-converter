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
    dst = os.path.join(cfg.output_dir, f"{cfg.output_basename}_{cfg.output_suffix}.fgb")
    cmd = ["ogr2ogr", "-f", "FlatGeobuf"]
    if cfg.crs:
        cmd += ["-t_srs", cfg.crs]
    cmd += [dst, src]
    _run(cmd)
    return dst


def to_parquet(cfg: Config, src_geojson: str | None = None) -> str:
    """GeoParquet を生成。GDALのParquetドライバが無い環境でも動くよう geopandas を使う。"""
    dst = os.path.join(cfg.output_dir, f"{cfg.output_basename}_{cfg.output_suffix}.parquet")
    src = src_geojson or cfg.output_geojson
    import geopandas as gpd
    print(f"  読み込み中: {src}", flush=True)
    gdf = gpd.read_file(src)
    print(f"  {len(gdf):,} features -> GeoParquet 書き出し中...", flush=True)
    gdf.to_parquet(dst)
    return dst


# PMTiles生成プロファイル
#   a: 混雑タイルでfeatureを間引く（軽量・俯瞰で欠落あり）＝既定
#   b: -pk(--no-tile-size-limit) -pf(--no-feature-limit) で上限撤廃し全feature保持（間引きなし）
PMTILES_PROFILES = {
    "a": {"suffix": "", "flags": ["--drop-densest-as-needed"]},
    "b": {"suffix": "_full", "flags": ["-pk", "-pf"]},
}


def to_pmtiles(cfg: Config, src_geojson: str | None = None,
               min_zoom: int = 4, max_zoom: int = 14, profile: str = "a") -> str:
    if not shutil.which("tippecanoe"):
        raise RuntimeError("tippecanoe が見つかりません")
    if profile not in PMTILES_PROFILES:
        raise ValueError(f"未知のPMTilesプロファイル: {profile}（a|b）")
    prof = PMTILES_PROFILES[profile]
    src = src_geojson or cfg.output_geojson
    dst = os.path.join(
        cfg.output_dir,
        f"{cfg.output_basename}_{cfg.output_suffix}{prof['suffix']}.pmtiles")
    _run(["tippecanoe", "-o", dst, "-Z", str(min_zoom), "-z", str(max_zoom),
          "-l", cfg.output_basename, *prof["flags"], "--force", src])
    return dst


def run(cfg: Config, formats: tuple[str, ...] = ("parquet", "pmtiles"),
        pmtiles_profiles: tuple[str, ...] = ("a",)) -> None:
    ensure_dirs(cfg)
    if "fgb" in formats:
        print("[export] FlatGeobuf 生成", flush=True)
        to_fgb(cfg)
    if "parquet" in formats:
        print("[export] GeoParquet 生成", flush=True)
        to_parquet(cfg)
    if "pmtiles" in formats:
        for prof in pmtiles_profiles:
            print(f"[export] PMTiles 生成（profile {prof}）", flush=True)
            to_pmtiles(cfg, profile=prof)
    print("[export] 完了", flush=True)
