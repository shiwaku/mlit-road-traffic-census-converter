# mlit-road-traffic-census-converter

国土交通省「全国道路・街路交通情勢調査（道路交通センサス）一般交通量調査」の
GISデータを整形・クレンジングするコンバーター。

**方式A（可視化ツールのGeoJSON直ダウンロード方式）** を採用し、
可視化ツールから取得したGeoJSONに箇所別基本表CSVを紐づけて、
地図配信・分析向けのデータ（GeoJSON / FlatGeobuf / GeoParquet / PMTiles）を生成する。

対象年度: **H27（平成27年度）** / **R03（令和3年度）** / **R07（令和7年度・将来）**。
年度差分は `configs/{year}.yaml` に外出しし、共通エンジンで処理する。

> 設計の詳細は [DESIGN.md](DESIGN.md)、既存データの完全性検証は [VERIFICATION.md](VERIFICATION.md) を参照。
> 生成した PMTiles を可視化する Web ビューワは [`viewer/`](viewer/README.md)（Vite + TypeScript + MapLibre GL JS）。

---

## セットアップ

```bash
pip install -r requirements.txt
# 出力変換に GDAL(ogr2ogr) が必要。PMTiles出力には tippecanoe が必要。
```

## 使い方

```bash
# 全ステップ実行
python run.py --year r03 --step all

# 個別ステップ
python run.py --year r03 --step download
python run.py --year r03 --step merge,normalize,mergecsv,transform,join
python run.py --year r03 --step export --formats fgb,parquet,pmtiles
python run.py --year r03 --step verify

# H27 も同じインターフェース
python run.py --year h27 --step all
```

成果物は `data/{year}/output/` に出力される（`data/` は .gitignore 対象）。

### 個別ダウンロードスクリプト（`scripts/`）

`--step download` は3種（GeoJSONタイル・箇所別基本表・時間帯別交通量表）をまとめて取得するが、
種別ごとに取り直したい場合は `scripts/` の単体スクリプトを使う（ロジックは `download.py` に一本化した薄いラッパー）。

```bash
python scripts/download_geojson_tiles.py --year r03   # → data/r03/geojson_tiles/
python scripts/download_kasho_csv.py     --year r03   # → data/r03/csv/kasho/
python scripts/download_jikantai_csv.py  --year r03   # → data/r03/csv/jikantai/
# --force で既存ファイルも再取得
```

## パイプライン

| ステップ | モジュール | 処理 | 年度依存(config) |
|---|---|---|---|
| download | `download.py` | GeoJSONタイル + 箇所別基本表CSV + 時間帯別交通量表CSV を取得 | URL / タイル / 道路種別 / 県コード |
| merge | `merge_geojson.py` | 分割GeoJSONを1ファイルに結合 | — |
| normalize | `normalize_geometry.py` | LineString→MultiLineString統一 | — |
| mergecsv | `merge_csv.py` | 箇所別基本表CSV（`csv/kasho/`）を結合（文字コード自動判定・空行除去・キー0埋め） | key_zfill |
| transform | `transform_csv.py` | コード→ラベル変換 + 型キャスト | mappings / schema |
| join | `join.py` | `census` ⇔ `交通調査基本区間番号` で属性結合 | key列 / geojson_key_property |
| export | `export.py` | fgb / parquet / pmtiles 変換 | crs / output_basename |
| verify | `verify.py` | 紐づけ率・孤児タイル点検（オフライン） | — |

## 成果物

各年度のパイプライン実行で `data/{year}/output/` に以下を生成する（`data/` は .gitignore 対象＝GitHubには非公開）。

| 年度 | 形式 | ファイル名 | サイズ | 用途 |
|---|---|---|---|---|
| R03 | GeoJSON | `traffic_census_2021_converted.geojson` | 1.4GB | 汎用・中間 |
| R03 | GeoParquet | `traffic_census_2021_converted.parquet` | 95MB | QGIS・分析 |
| R03 | PMTiles | `traffic_census_2021_converted.pmtiles` | 655MB | MapLibre配信 |
| H27 | GeoJSON | `traffic_census_2015_converted.geojson` | 4.0GB | 汎用・中間 |
| H27 | GeoParquet | `traffic_census_2015_converted.parquet` | 111MB | QGIS・分析 |
| H27 | PMTiles | `traffic_census_2015_converted.pmtiles` | 521MB | MapLibre配信 |

- いずれも箇所別基本表を紐づけ済み（結合率 **100%**）。ファイル名の接尾辞は `output_suffix`（既定 `converted`）。
- **PMTiles** は `tippecanoe -Z4 -z14 -pk -pf`（`--no-tile-size-limit` / `--no-feature-limit`）で生成し、
  **featureを間引かず全保持**する（`--drop-densest-as-needed` は使わない）。
- 検証記録は [VERIFICATION.md](VERIFICATION.md)。R03は全件監査で実DL漏れ3件を回収済み。

### QGIS 主題図スタイル（QML）

GeoParquet を QGIS で主題図表示するための QML を [`configs/qgis_styles/`](configs/qgis_styles/) に用意。
[road-traffic-census-map-2021](https://github.com/shiwaku/road-traffic-census-map-2021) ビューワの
**5種類**（24時間交通量 / 混雑度 / 大型車混入率 / 混雑時旅行速度 / 昼間非混雑時旅行速度）に色分けを合わせており、
**R03（`traffic_census_2021_*`）・H27（`traffic_census_2015_*`）両年度分**を用意（計10ファイル）。
QGISでレイヤ→シンボロジ→「スタイルを読み込む」で `.qml` を適用（詳細は同フォルダのREADME）。

### 成果物サイズが年度で異なる理由

出力GeoJSON/GeoParquetのサイズは年度で大きく異なる（H27 ≫ R03）。これは**元データの線分分割の細かさ**による。
H27の元GeoJSONは LineString 優勢で1区間が多数の線分に分割されており（1区間あたり約6本、R03は約1.3本）、
紐づけ時に同じ属性が線分ごとに複製されるためファイルが膨らむ。区間数・情報量はむしろR03の方が多い。
詳細は [DESIGN.md 3.2](DESIGN.md) を参照。

> サイズに効くのは GeoJSON / GeoParquet。PMTiles は tippecanoe がズームごとに簡略化するため相対的に小さい。

## 新年度の追加（例: R07）

1. `configs/r07.yaml` の TODO を実データで確認して埋める（URL・タイル・0埋め要否）。
2. `configs/mappings/r07_mappings.yaml`（コード→ラベル）を用意。
3. `configs/schema/r07_schema.csv`（`Name,TypeName`）を用意。
4. `python run.py --year r07 --step all` を実行。

## ディレクトリ構成

```
mlit-road-traffic-census-converter/
├── README.md                 … 本ファイル
├── DESIGN.md                 … 設計書（§8: 時間帯別交通量表の連携検討）
├── VERIFICATION.md           … 完全性・紐づけ検証レポート
├── LICENSE                   … MIT（ソースコード）
├── requirements.txt
├── run.py                    … CLI（python run.py --year r03 --step all）
│
├── census_converter/         … 共通エンジン（年度非依存）
│   ├── config.py             … 年度config読込・作業パス解決
│   ├── download.py           … GeoJSONタイル / 箇所別基本表 / 時間帯別交通量表 のDL
│   ├── merge_geojson.py      … 分割GeoJSON結合
│   ├── normalize_geometry.py … LineString→MultiLineString統一
│   ├── merge_csv.py          … 箇所別基本表CSV結合（csv/kasho/）
│   ├── transform_csv.py      … コード→ラベル変換・型キャスト
│   ├── join.py               … census⇔交通調査基本区間番号 で属性結合
│   ├── export.py             … GeoParquet / PMTiles / FlatGeobuf 変換
│   └── verify.py             … 紐づけ率・孤児タイル点検（オフライン）
│
├── configs/                  … 年度ごとの差分
│   ├── h27.yaml / r03.yaml / r07.yaml
│   ├── mappings/             … コード→ラベル辞書
│   ├── schema/               … 年度別 項目名と型（Name,TypeName）
│   ├── tileindex/            … tileindex_zoomlevel_12.csv / KenCodeList.csv
│   └── qgis_styles/          … QGIS主題図QML（5種）＋generate_qml.py
│
├── scripts/                  … 個別ダウンロードスクリプト（download.py の薄いラッパー）
│   ├── download_geojson_tiles.py
│   ├── download_kasho_csv.py
│   └── download_jikantai_csv.py
│
└── data/                     … 入力・中間・成果物（.gitignore。詳細は data/README.md）
    └── {r03,h27}/
        ├── geojson_tiles/    … 【入力】分割GeoJSON
        ├── csv/
        │   ├── kasho/        … 【入力】箇所別基本表 kasyo{NN}.csv
        │   └── jikantai/     … 【入力】時間帯別交通量表 zkntrf{NN}.csv
        ├── work/             … 【中間】結合・正規化・変換の途中生成物
        └── output/           … 【成果物】traffic_census_{YYYY}_converted.*

（旧「H27… / R03… 」フォルダは旧コンバーターの保全用。.gitignore で追跡外）
```

> 時間帯別交通量表（`csv/jikantai/`）をジオメトリに紐づけ、Webマップで時間帯別グラフを表示する
> 拡張の検討は [DESIGN.md §8](DESIGN.md) を参照。

## ライセンス

- **本リポジトリのソースコード**: [MIT License](LICENSE)
- **入力・成果物データ**: 元データ（道路交通センサス）のライセンスに従う（下記）。データは本リポジトリに含めない。

## データ源・ライセンス

- 令和3年度: 箇所別基本表 <https://www.mlit.go.jp/road/census/r3/index.html> /
  可視化ツール <https://www.mlit.go.jp/road/ir/ir-data/census_visualizationR3/index.html>
- 平成27年度: 可視化ツール <https://www.mlit.go.jp/road/ir/ir-data/census_visualization2/index.html>
- 元データのライセンス: 国土交通省ウェブサイトの利用ルール ＝ **公共データ利用規約（第1.0版・PDL1.0）**（CC BY 4.0 互換）
  <https://www.mlit.go.jp/link.html>。利用時は **出典表示**（例:「出典：国土交通省ウェブサイト（URL）」）と、
  加工した場合は **加工した旨の明示** が必要（国が作成したかのような態様での公表は不可）。
- 関連: <https://github.com/shiwaku/road-traffic-census-map-2021> /
  <https://github.com/shiwaku/road-traffic-census-map-2015>

## 免責

- 本リポジトリのコード及び生成物は現状有姿（AS IS）で提供され、正確性・完全性・特定目的への
  適合性を保証しません。
- 本ツール及び生成データの利用により生じたいかなる損害についても、本リポジトリの作成者及び
  コントリビューターは一切の責任を負いません。
- 元データの利用条件（PDL1.0 の出典表示・加工明示）の遵守は、
  利用者ご自身の責任で確認・対応してください。
