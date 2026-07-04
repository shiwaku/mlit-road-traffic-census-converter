# QGIS スタイル（主題図 QML）

GeoParquet を QGIS で表示するための主題図スタイル。
[road-traffic-census-map-2021](https://github.com/shiwaku/road-traffic-census-map-2021) ビューワの
**5種類の主題図**に色分け・区分を合わせている。

**R03・H27 両年度分**を用意（ファイル名の接頭辞で区別）:
- R03（令和3年度）: `traffic_census_2021_*` → `data/r03/output/traffic_census_2021_converted.parquet` 用
- H27（平成27年度）: `traffic_census_2015_*` → `data/h27/output/traffic_census_2015_converted.parquet` 用

区分・色は両年度で共通。列名は旅行速度のみ年度差があり `generate_qml.py` が吸収する
（道路種別・管理区分のラベル書式、24時間交通量・混雑度・大型車混入率の列名は両年度で同一）。

| QML | 主題図 | 分類 | 色 |
|---|---|---|---|
| `..._1_24jikankotsuryo.qml` | 24時間交通量(全車上下計) | 色=道路種別 / 線幅=交通量6段階(5千/1万/2万/4万/8万)。入れ子ルール(色6×幅6=36)で線幅を静的に指定 | 高速=青, 一般国道=赤(直轄外=マゼンタ), 主要地方道=緑, 都道府県道・市道=暗赤 |
| `..._2_konzatsudo.qml` | 混雑度 | <1.0 / 1.0–1.25 / 1.25–1.75 / ≥1.75 | 緑→黄→橙→赤 |
| `..._3_ogatashakonnyuritsu.qml` | 大型車混入率(%) | <10 / 10–15 / 15–20 / ≥20 | 緑→黄→橙→赤 |
| `..._4_konzatsuji.qml` | 混雑時旅行速度 | min(上り,下り) を <10/…/≥50 の6段階 | 赤→橙→黄→緑→水→青 |
| `..._5_hikonzatsuji.qml` | 昼間非混雑時旅行速度 | 同上（非混雑時速度） | 赤→橙→黄→緑→水→青 |

## 使い方（QGIS）

1. 対象年度の GeoParquet（R03: `traffic_census_2021_converted.parquet` /
   H27: `traffic_census_2015_converted.parquet`）を QGIS に追加。
2. レイヤを右クリック → プロパティ → シンボロジ → 画面下の「スタイル ▾」→「スタイルを読み込む…」
   で、その年度の接頭辞に合った `.qml` を選択。
3. 主題図を切り替えるときは別の `.qml` を読み込む。

## 再生成

```bash
python configs/qgis_styles/generate_qml.py
```

区分値・色は `generate_qml.py` 冒頭の定義を編集して調整する。

## 実装メモ（QGISの落とし穴）

- **線幅の data-defined は「スタイルを読み込む」で反映されない場合がある。** 24時間交通量図は当初、
  ルール(色=道路種別)＋データ定義式で線幅を変えていたが、幅が一律のままになった。このため
  **入れ子ルール（親=道路種別で色、子=交通量ビンで静的な線幅）** に変更し、DDに依存しない実装にした。
- **速度図の分類式は `min()`/`max()` を使う。** QGISの式に `least()`/`greatest()` は無く、
  使うと「式が不正です」となり全フィーチャが未分類＝非表示になる（混雑時・非混雑時旅行速度図で発生）。
