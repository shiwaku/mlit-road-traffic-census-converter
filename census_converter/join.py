"""ステップ6: GeoJSON に箇所別基本表を紐づけ。

元スクリプト(5_drm_add_kasho_v3.py)相当。
GeoJSON属性 `census` ⇔ CSV `交通調査基本区間番号` をキーに、CSVの全列をpropertiesへ付与。
schema に従い Integer/Real 列は JSON数値（非文字列）、空値は null として出力する。
"""
from __future__ import annotations
import json

import pandas as pd

from .config import Config, ensure_dirs


def _typed_index(cfg: Config) -> dict[str, dict]:
    """transformed_csv を key列->{列: 型付き値} の辞書に変換。"""
    df = pd.read_csv(cfg.transformed_csv, dtype=str, na_filter=False)
    schema = cfg.schema
    index: dict[str, dict] = {}
    for row in df.to_dict(orient="records"):
        rec = {}
        for col, val in row.items():
            typ = schema.get(col)
            if typ in ("Integer", "Real"):
                if val == "" or val is None:
                    rec[col] = None
                else:
                    try:
                        rec[col] = int(val) if typ == "Integer" else float(val)
                    except ValueError:
                        # 例: Integerだが小数文字列 -> floatを試す
                        try:
                            rec[col] = float(val)
                        except ValueError:
                            rec[col] = None
            else:
                rec[col] = val
        index[row[cfg.key_column]] = rec
    return index


def run(cfg: Config, input_geojson: str | None = None) -> str:
    ensure_dirs(cfg)
    src = input_geojson or cfg.normalized_geojson
    csv_index = _typed_index(cfg)
    print(f"[join] CSV {len(csv_index):,} 区間を読み込み", flush=True)

    with open(src, encoding="utf-8") as f:
        geojson = json.load(f)

    key_prop = cfg.geojson_key_property
    feats = geojson["features"]
    matched = 0
    for feat in feats:
        props = feat.setdefault("properties", {})
        rec = csv_index.get(str(props.get(key_prop)))
        if rec:
            props.update(rec)
            matched += 1

    out = cfg.output_geojson
    with open(out, "w", encoding="utf-8") as f:
        f.write('{\n"type": "FeatureCollection",\n')
        if geojson.get("crs") is not None:
            f.write('"crs": ' + json.dumps(geojson["crs"], ensure_ascii=False) + ',\n')
        f.write('"features": [\n')
        for i, feat in enumerate(feats):
            f.write(json.dumps(feat, ensure_ascii=False))
            f.write(",\n" if i < len(feats) - 1 else "\n")
        f.write("]\n}\n")

    rate = matched / len(feats) * 100 if feats else 0
    print(f"[join] {matched:,}/{len(feats):,} features に属性付与 ({rate:.2f}%) -> {out}",
          flush=True)
    return out
