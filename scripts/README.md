# scripts/ — 個別ダウンロード / リリース補助スクリプト

- [個別ダウンロード](#個別ダウンロード) … 入力データを種別ごとに取り直す
- [リリース資産の組み立て](#リリース資産の組み立て) … 配布アセットと `SHA256SUMS.txt` を用意する

---

## 個別ダウンロード

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

---

## リリース資産の組み立て

`build_release_assets.py` は GitHub Releases 用のアセット一式と `SHA256SUMS.txt` をまとめて用意する。
`run.py --step all` で `data/{r03,h27}/output/` が揃っている状態で実行する。

```bash
python scripts/build_release_assets.py                          # dist/release/ に出力
python scripts/build_release_assets.py --dest /tmp/dist --tag data-v2
```

| アセット | 扱い |
|---|---|
| `<prefix>_qgis.zip` | **生成**（`generate_qgis_bundle.pack` を呼ぶ。GeoParquet同梱） |
| `<prefix>_jikantai.tar.gz` | **生成**（展開後 `jikantai/<year>/{01..47,index}.json`） |
| `<prefix>_converted.parquet` / `.pmtiles` | 置いてある場所のまま参照（数百MB〜なのでコピーしない） |
| `<prefix>_converted.qml` | `configs/qgis_styles/bundle/` から参照 |
| `SHA256SUMS.txt` | **生成**（上記10アセット全件） |

最後に `gh release upload <tag> --clobber ...` のコマンドを表示するので、内容を確認してから実行する
（スクリプト自身はアップロードしない）。

> [!IMPORTANT]
> `SHA256SUMS.txt` は**全アセットを一括アップロードする前提**で全件を書く。一部だけ差し替える運用では
> 公開中の他アセットのハッシュと食い違うため、その場合は公開中の `SHA256SUMS.txt` の該当行だけを直す。

zip は `ZIP_EPOCH`、tar.gz は mtime/uid/gid・gzipヘッダを固定しているので、同じ入力からは毎回同じ
ハッシュになる（再実行で確認済み）。ただし **`data-v1` で公開中の `*_jikantai.tar.gz` は本スクリプト
導入前に手作業で作ったもので、収録48ファイルはバイト一致するがアーカイブのバイト列は一致しない。**
