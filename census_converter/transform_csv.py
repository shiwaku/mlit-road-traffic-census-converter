"""ステップ5: コード値→ラベル変換 + 型キャスト。

元スクリプト(4_kasho_csv_convert.py)相当だが、年度依存を config に外出し:
- mappings: {列名: {コード: ラベル}} でコード列をラベル化
- schema:   {列名: Integer|Real|String} で数値列を型変換
"""
from __future__ import annotations

import pandas as pd

from .config import Config, ensure_dirs


def run(cfg: Config, input_csv: str | None = None) -> str:
    ensure_dirs(cfg)
    src = input_csv or cfg.merged_csv
    df = pd.read_csv(src, dtype=str, na_filter=False)

    # コード -> ラベル
    applied = 0
    for col, mapping in cfg.mappings.items():
        if col in df.columns:
            # マッピングに無い値は元の値を保持
            df[col] = df[col].map(lambda v, m=mapping: m.get(v, v))
            applied += 1
        else:
            print(f"  警告: mappings対象列がCSVに無い: {col}", flush=True)

    # 型キャスト（schema）
    cast_int = cast_real = 0
    for col, typ in cfg.schema.items():
        if col not in df.columns:
            continue
        if typ == "Integer":
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
            cast_int += 1
        elif typ == "Real":
            df[col] = pd.to_numeric(df[col], errors="coerce")
            cast_real += 1

    out = cfg.transformed_csv
    df.to_csv(out, index=False)
    print(f"[transform_csv] label列 {applied} / Integer {cast_int} / Real {cast_real} -> {out}",
          flush=True)
    return out
