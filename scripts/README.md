# scripts/ — 個別ダウンロードスクリプト

道路交通センサスの入力データを**種別ごとに単体で取得**するためのスクリプト群。
ダウンロードのロジックは `census_converter/download.py` に一本化しており、
ここの各スクリプトはそれを呼ぶだけの薄いラッパー（実装の重複なし）。

通常は年度パイプラインでまとめて取得すれば足りる：

```bash
python run.py --year r03 --step download   # 3種すべてを取得
```

特定の種別だけ取り直したいときに個別スクリプトを使う。

| スクリプト | 取得対象 | 保存先 | 元データ（例: R03） |
|---|---|---|---|
| `download_geojson_tiles.py` | 分割GeoJSONタイル | `data/{year}/geojson_tiles/` | `census_visualizationR3/{道路種別}/{z}/{x}/{y}.geojson` |
| `download_kasho_csv.py` | 箇所別基本表 | `data/{year}/csv/kasho/` | `road/census/r3/data/csv/kasyo{NN}.csv` |
| `download_jikantai_csv.py` | 時間帯別交通量表 | `data/{year}/csv/jikantai/` | `road/census/r3/data/csv/zkntrf{NN}.csv` |

## 使い方

```bash
python scripts/download_kasho_csv.py     --year r03
python scripts/download_jikantai_csv.py  --year h27
python scripts/download_geojson_tiles.py --year r03

# 既存ファイルも再取得（既定は既存かつ非空をスキップ）
python scripts/download_kasho_csv.py --year r03 --force
```

- `--year`: `r03`（令和3年度）/ `h27`（平成27年度）。config は `configs/{year}.yaml` を参照。
- 時間帯別交通量表は `configs/{year}.yaml` の `jikantai_csv_url_template` が未設定なら取得しない。
- 時間帯別交通量表の位置づけ・ジオメトリ紐づけ設計は [../DESIGN.md](../DESIGN.md) §8 を参照。
