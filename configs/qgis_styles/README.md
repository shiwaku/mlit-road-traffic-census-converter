# QGIS スタイル（主題図 QML）

GeoParquet（`traffic_census_2021_converted.parquet`）を QGIS で表示するための主題図スタイル。
[road-traffic-census-map-2021](https://github.com/shiwaku/road-traffic-census-map-2021) ビューワの
**5種類の主題図**に色分け・区分を合わせている。

| QML | 主題図 | 分類 | 色 |
|---|---|---|---|
| `..._1_24jikankotsuryo.qml` | 24時間交通量(全車上下計) | 色=道路種別 / 線幅=交通量6段階(5千/1万/2万/4万/8万) | 高速=青, 一般国道=赤(直轄外=マゼンタ), 主要地方道=緑, 都道府県道・市道=暗赤 |
| `..._2_konzatsudo.qml` | 混雑度 | <1.0 / 1.0–1.25 / 1.25–1.75 / ≥1.75 | 緑→黄→橙→赤 |
| `..._3_ogatashakonnyuritsu.qml` | 大型車混入率(%) | <10 / 10–15 / 15–20 / ≥20 | 緑→黄→橙→赤 |
| `..._4_konzatsuji.qml` | 混雑時旅行速度 | min(上り,下り) を <10/…/≥50 の6段階 | 赤→橙→黄→緑→水→青 |
| `..._5_hikonzatsuji.qml` | 昼間非混雑時旅行速度 | 同上（非混雑時速度） | 赤→橙→黄→緑→水→青 |

## 使い方（QGIS）

1. `data/r03/output/traffic_census_2021_converted.parquet` を QGIS に追加。
2. レイヤを右クリック → プロパティ → シンボロジ → 画面下の「スタイル ▾」→「スタイルを読み込む…」
   で目的の `.qml` を選択。
3. 主題図を切り替えるときは別の `.qml` を読み込む。

> 対象は R03（令和3年度）の列名。H27 は列名体系が異なるため、そのままでは適用不可
> （H27用は `generate_qml.py` のフィールド名を差し替えて再生成すれば作成可能）。

## 再生成

```bash
python configs/qgis_styles/generate_qml.py
```

区分値・色は `generate_qml.py` 冒頭の定義を編集して調整する。
