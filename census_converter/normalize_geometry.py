"""ステップ3: LineString を MultiLineString に統一。

元スクリプト(2_toMultiLineString.py)相当。元データは両ジオメトリが混在するため、
MultiLineStringに揃えることで下流処理・タイル化を安定させる。
features を1行1featureで書き出す（下流のjoinがストリーム処理しやすい形）。
"""
from __future__ import annotations
import json

from .config import Config, ensure_dirs


def run(cfg: Config, input_geojson: str | None = None) -> str:
    ensure_dirs(cfg)
    src = input_geojson or cfg.merged_geojson
    with open(src, encoding="utf-8") as f:
        data = json.load(f)

    converted = 0
    for feat in data["features"]:
        geom = feat.get("geometry") or {}
        if geom.get("type") == "LineString":
            geom["type"] = "MultiLineString"
            geom["coordinates"] = [geom["coordinates"]]
            converted += 1

    out = cfg.normalized_geojson
    with open(out, "w", encoding="utf-8") as f:
        f.write('{\n"type": "FeatureCollection",\n')
        if data.get("crs") is not None:
            f.write('"crs": ' + json.dumps(data["crs"], ensure_ascii=False) + ',\n')
        f.write('"features": [\n')
        feats = data["features"]
        for i, feat in enumerate(feats):
            f.write(json.dumps(feat, ensure_ascii=False, separators=(", ", ": ")))
            f.write(",\n" if i < len(feats) - 1 else "\n")
        f.write("]\n}\n")

    print(f"[normalize_geometry] LineString->MultiLineString {converted:,} 件 -> {out}", flush=True)
    return out
