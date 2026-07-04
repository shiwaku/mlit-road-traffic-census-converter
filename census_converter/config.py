"""年度設定（configs/{year}.yaml）の読み込みと作業パスの解決。"""
from __future__ import annotations
import os
from dataclasses import dataclass, field
from typing import Any
import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _resolve(path: str) -> str:
    """リポジトリルート基準の相対パスを絶対パスに解決。"""
    return path if os.path.isabs(path) else os.path.join(REPO_ROOT, path)


@dataclass
class Config:
    year: str
    label: str
    output_basename: str
    # download
    geojson_url_base: str
    kasho_csv_url_template: str
    road_types: list[str]
    tileindex: str
    ken_code_list: str
    request_timeout: tuple[float, float]
    request_sleep: float
    # csv
    key_column: str
    key_zfill: int
    csv_encodings: list[str]
    # transform
    mappings: dict[str, dict[str, str]]
    schema: dict[str, str]           # 列名 -> Integer/Real/String
    # join / export
    geojson_key_property: str
    crs: str | None
    # 出力ファイル名の接尾辞（例: traffic_census_2021_converted）
    output_suffix: str = "converted"
    # 作業ディレクトリ
    data_dir: str = field(default="")

    @property
    def tiles_dir(self) -> str: return os.path.join(self.data_dir, "geojson_tiles")

    @property
    def csv_dir(self) -> str: return os.path.join(self.data_dir, "csv")

    @property
    def work_dir(self) -> str: return os.path.join(self.data_dir, "work")

    @property
    def output_dir(self) -> str: return os.path.join(self.data_dir, "output")

    # 作業成果物の標準パス
    @property
    def merged_geojson(self) -> str:
        return os.path.join(self.work_dir, f"{self.year}_drm.geojson")

    @property
    def normalized_geojson(self) -> str:
        return os.path.join(self.work_dir, f"{self.year}_drm_multilinestring.geojson")

    @property
    def merged_csv(self) -> str:
        return os.path.join(self.work_dir, "kasho_merged.csv")

    @property
    def transformed_csv(self) -> str:
        return os.path.join(self.work_dir, "kasho_transformed.csv")

    @property
    def output_geojson(self) -> str:
        return os.path.join(self.output_dir, f"{self.output_basename}_{self.output_suffix}.geojson")


def load_config(year: str, data_root: str | None = None) -> Config:
    """configs/{year}.yaml を読み込み、参照ファイル（mappings/schema）も展開する。"""
    cfg_path = _resolve(os.path.join("configs", f"{year}.yaml"))
    if not os.path.exists(cfg_path):
        raise FileNotFoundError(f"設定ファイルが見つかりません: {cfg_path}")
    with open(cfg_path, encoding="utf-8") as f:
        raw: dict[str, Any] = yaml.safe_load(f)

    # mappings（コード->ラベル辞書）
    mappings: dict[str, dict[str, str]] = {}
    if raw.get("mappings"):
        with open(_resolve(raw["mappings"]), encoding="utf-8") as f:
            mappings = yaml.safe_load(f) or {}

    # schema（列名 -> 型）
    schema: dict[str, str] = {}
    if raw.get("schema_csv"):
        import csv as _csv
        with open(_resolve(raw["schema_csv"]), encoding="utf-8-sig", newline="") as f:
            r = _csv.reader(f)
            header = next(r, None)
            for row in r:
                if len(row) >= 2 and row[0]:
                    schema[row[0]] = row[1]

    to = raw.get("request_timeout", [3.0, 5.0])
    data_root = data_root or os.path.join(REPO_ROOT, "data")

    return Config(
        year=raw["year"],
        label=raw.get("label", raw["year"]),
        output_basename=raw.get("output_basename", f"traffic_census_{raw['year']}"),
        geojson_url_base=raw["geojson_url_base"].rstrip("/"),
        kasho_csv_url_template=raw["kasho_csv_url_template"],
        road_types=raw["road_types"],
        tileindex=_resolve(raw["tileindex"]),
        ken_code_list=_resolve(raw["ken_code_list"]),
        request_timeout=(float(to[0]), float(to[1])),
        request_sleep=float(raw.get("request_sleep", 0.1)),
        key_column=raw.get("key_column", "交通調査基本区間番号"),
        key_zfill=int(raw.get("key_zfill", 0)),
        csv_encodings=raw.get("csv_encodings", ["utf-8", "shift-jis", "cp932"]),
        mappings=mappings,
        schema=schema,
        geojson_key_property=raw.get("geojson_key_property", "census"),
        crs=raw.get("crs"),
        output_suffix=raw.get("output_suffix", "converted"),
        data_dir=os.path.join(data_root, raw["year"]),
    )


def ensure_dirs(cfg: Config) -> None:
    for d in (cfg.tiles_dir, cfg.csv_dir, cfg.work_dir, cfg.output_dir):
        os.makedirs(d, exist_ok=True)
