"""MLIT 道路交通センサス コンバーター（方式A: 可視化ツールのGeoJSON直DL）。

年度非依存の共通エンジン。年度ごとの差分は configs/{year}.yaml に外出しする。
パイプライン: download -> merge_geojson -> normalize_geometry
              -> merge_csv -> transform_csv -> join -> export（+ verify）
"""
__all__ = [
    "config", "download", "merge_geojson", "normalize_geometry",
    "merge_csv", "transform_csv", "join", "export", "verify",
]
