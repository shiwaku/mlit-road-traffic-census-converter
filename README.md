# mlit-road-traffic-census-converter

国土交通省「全国道路・街路交通情勢調査（道路交通センサス）一般交通量調査」の
GISデータを整形・クレンジングするコンバーター。

**方式A（可視化ツールのGeoJSON直ダウンロード方式）** を採用し、
可視化ツールから取得したGeoJSONに箇所別基本表CSVを紐づけて、
地図配信・分析向けのデータ（GeoJSON / FlatGeobuf / GeoParquet / PMTiles）を生成する。

対象年度: **H27（平成27年度）** / **R03（令和3年度）** / **R07（令和7年度・将来）**。
年度差分は `configs/{year}.yaml` に外出しし、共通エンジンで処理する。

> 設計の詳細は [DESIGN.md](DESIGN.md)、既存データの完全性検証は [VERIFICATION.md](VERIFICATION.md) を参照。

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

## パイプライン

| ステップ | モジュール | 処理 | 年度依存(config) |
|---|---|---|---|
| download | `download.py` | GeoJSONタイル + 箇所別基本表CSV を取得 | URL / タイル / 道路種別 / 県コード |
| merge | `merge_geojson.py` | 分割GeoJSONを1ファイルに結合 | — |
| normalize | `normalize_geometry.py` | LineString→MultiLineString統一 | — |
| mergecsv | `merge_csv.py` | 県別CSV結合（文字コード自動判定・空行除去・キー0埋め） | key_zfill |
| transform | `transform_csv.py` | コード→ラベル変換 + 型キャスト | mappings / schema |
| join | `join.py` | `census` ⇔ `交通調査基本区間番号` で属性結合 | key列 / geojson_key_property |
| export | `export.py` | fgb / parquet / pmtiles 変換 | crs / output_basename |
| verify | `verify.py` | 紐づけ率・孤児タイル点検（オフライン） | — |

## 成果物のサイズについて

出力GeoJSONのサイズは年度で大きく異なる（例: R03 ≈ 1.4GB、H27 ≈ 4.3GB）。
これは**元データの線分分割の細かさ**の違いによる。H27の元GeoJSONは LineString 優勢で
1区間が多数の線分に分割されており（1区間あたり約6本）、紐づけ時に同じ属性が線分ごとに
複製されるためファイルが膨らむ。区間数・情報量はむしろR03の方が多い。詳細は
[DESIGN.md 3.2](DESIGN.md) を参照。

> サイズに効くのは GeoJSON / GeoParquet のみ。PMTiles は tippecanoe が結合・簡略化するため影響は小さい。

## 新年度の追加（例: R07）

1. `configs/r07.yaml` の TODO を実データで確認して埋める（URL・タイル・0埋め要否）。
2. `configs/mappings/r07_mappings.yaml`（コード→ラベル）を用意。
3. `configs/schema/r07_schema.csv`（`Name,TypeName`）を用意。
4. `python run.py --year r07 --step all` を実行。

## ディレクトリ構成

```
census_converter/     共通エンジン（年度非依存）
configs/              年度別config・mappings・schema・tileindex
run.py                CLI
data/                 作業・成果物（.gitignore）
legacy: 既存の「H27/R03 …」フォルダは旧コンバーターの保全（.gitignore）
```

## データ源・ライセンス

- 令和3年度: 箇所別基本表 <https://www.mlit.go.jp/road/census/r3/index.html> /
  可視化ツール <https://www.mlit.go.jp/road/ir/ir-data/census_visualizationR3/index.html>
- 平成27年度: 可視化ツール <https://www.mlit.go.jp/road/ir/ir-data/census_visualization2/index.html>
- 元データのライセンス: 政府標準利用規約（第2.0版）準拠 <https://www.mlit.go.jp/link.html>
- 関連: <https://github.com/shiwaku/road-traffic-census-map-2021> /
  <https://github.com/shiwaku/road-traffic-census-map-2015>

## 免責

利用者が当該データを用いて行う一切の行為について、作者は責任を負いません。
