# 道路交通センサスマップ（ビューワ）

道路交通センサス（**令和3年度=2021 / 平成27年度=2015**）の変換済み PMTiles を
Web 地図で可視化するビューワ。**Vite + TypeScript + MapLibre GL JS + PMTiles** 構成。

親プロジェクト（`mlit-road-traffic-census-converter`）が生成した PMTiles を消費する。

## 機能

- **年度切替**（令和3年度 / 平成27年度）
- **5つの主題図**
  - 24時間交通量（全車上下計） — 道路種別で色分け・交通量で線幅
  - 混雑度 / 大型車混入率 — 値で段階色分け（＋昼間12時間交通量ラベル）
  - 混雑時 / 昼間非混雑時 旅行速度 — 上り・下りの遅い方で段階色分け
- 空中写真（地理院シームレス）の重ね合わせ＋不透明度スライダー
- テーマ連動の凡例、道路クリックで属性ポップアップ
- ナビ / 全画面 / 現在地 / スケールコントロール、URL ハッシュ同期

## セットアップ

```bash
cd viewer
npm install
```

## 開発（ローカルの PMTiles を使用）

親リポジトリの `data/{r03,h27}/output/*.pmtiles` が存在する前提。
Vite の開発サーバが Range 対応でローカル配信するため、`public/` へのコピーは不要。

```bash
npm run dev
# → http://localhost:5173
```

配信マッピング（`vite.config.ts`）:

| URL パス | 実ファイル |
| --- | --- |
| `/pmtiles/r03.pmtiles` | `../data/r03/output/traffic_census_2021_converted.pmtiles` |
| `/pmtiles/h27.pmtiles` | `../data/h27/output/traffic_census_2015_converted.pmtiles` |

## ビルド / 本番デプロイ

PMTiles（数百MB）は Git に含められないため、**外部ホスト**（HTTP Range 対応必須：
レンタルサーバ / S3 / Cloudflare R2 等）へアップロードし、URL を環境変数で指定する。

```bash
cp .env.example .env
# .env を編集して VITE_PMTILES_R03_URL / VITE_PMTILES_H27_URL を設定
npm run build          # tsc 型チェック + vite build → dist/
npm run preview        # dist/ の確認
```

`dist/` を GitHub Pages 等へ配置する（`base: './'` 設定済みでサブパス配信可）。

## 構成

```
src/
  main.ts              エントリ（protocol登録・状態管理・イベント配線）
  config/
    years.ts           年度定義（source-layer / PMTiles URL / 速度列名 / ポップアップ項目）
    themes.ts          テーマ登録
  map/
    createMap.ts       地図＋コントロール
    basemap.ts         空中写真 raster
    sources.ts         両年度 PMTiles source
    roadStyle.ts       共通式（道路種別カラー / 交通量→線幅 / フィルタ）
    renderTheme.ts     年度・テーマのレイヤ差し替え
  themes/              5テーマの buildLayers（+ helpers）
  ui/                  controlPanel / legend / opacitySlider / popup
```

## データの出典・ライセンス

本ビューワが表示するデータは道路交通センサス（国土交通省）の変換物で、
**公共データ利用規約（PDL1.0）** の下で提供される。出典・利用条件は
[国土交通省の公表ページ](https://www.mlit.go.jp/road/census/)および
[リンク・著作権・免責事項](https://www.mlit.go.jp/link.html)に従うこと。
再配布・ベクトルタイル配信を行う場合は、最新の利用条件を必ず確認すること。
