# 道路交通センサス コンバーター 再整理 設計案

MLIT（国土交通省）道路交通センサス（全国道路・街路交通情勢調査 一般交通量調査）の
GISデータを整形・クレンジングするコンバーターの再整理設計。

- 対象年度: **H27（平成27年度）** / **R03（令和3年度）** / **R07（令和7年度・将来）**
- 主軸: **方式A（可視化ツールのGeoJSON直ダウンロード方式）**
- 作成日: 2026-07-04

---

## 1. 背景・現状

過去のコンバーターは 4フォルダ・約23GB・約11万ファイル で、大半が中間生成物
（分割GeoJSON / PBF / fgb 等）。処理ロジックは実質 **2方式** に集約される。

### 方式A：可視化ツール方式（採用）

MLIT可視化ツールから **GeoJSONを直接ダウンロード** し、箇所別基本表CSVを紐づける5段パイプライン。

```
DL: census_*_geojson_dl.py（道路種別 × タイル）
    census_*_kasho_csv_dl.py（県別CSV 01-47）
 1_geojson_merge.py       … 分割GeoJSONを1ファイルに結合
 2_toMultiLineString.py   … LineString → MultiLineString に統一
 3_kasho_csv_merge.py     … 県別CSVを結合（文字コード自動判定・空行除去）
 4_kasho_csv_convert.py   … コード値 → ラベル変換 + 数値型キャスト
 5_drm_add_kasho.py       … census ⇔ 交通調査基本区間番号 でGeoJSONに属性結合
 → ogr2ogr で fgb / parquet 化、tippecanoe で pmtiles 化
```

対象: H27・R03 の2世代（コードはほぼ同一、差分は年度固有の列名・コード辞書・URLのみ）。

### 方式B：国土交通プラットフォーム方式（不採用／参考保存）

```
census_h27_pbf_dl.py            … ベクトルタイル（PBF）をDL
batch_convert_pbf_to_geojson.sh … tippecanoe-decode + jq でGeoJSON化
traffic_census_2015_converter.py… 属性文字列クレンジング（「（推定値）」「,」除去等）
 → ogr2ogr で parquet 化
```

**不採用理由**: PBF（ベクトルタイル）はタイル内座標系に量子化されており、
`tippecanoe-decode` で緯度経度に戻しても元の座標精度が復元できず、
折れ線がタイルグリッドにスナップして劣化する。方式Aは元の緯度経度がそのまま
入っているため座標精度で優位。将来の代替手段として `legacy/` に参考保存する。

---

## 2. 方針

- **方式A（GeoJSON直DL）を正式・推奨パスとする。** H27も方式Aの成果物を正とする。
- **年度で変わる部分を config に外出し**し、処理の骨格（エンジン）は共通化する。
- **R03の設計（スキーマCSV駆動の型変換）を標準**とし、H27はconfig側で吸収する。
- **R07公開時は config を1枚追加するだけ**で回せる形にする（同形式のGeoJSON配布を想定）。

---

## 3. 年度差分（config化する項目）

| 差分項目 | H27 | R03 | R07（予想） |
|---|---|---|---|
| GeoJSON DL URL ベース | `census_visualization2` | `census_visualizationR3` | `census_visualizationR7`？ |
| 箇所別基本表CSV URL | `road/census/h27/data/csv/kasyo{ken}.csv` | `road/census/r3/data/csv/kasyo{ken}.csv` | `road/census/r7/data/csv/`？ |
| タイルインデックス | zoomlevel_12 | zoomlevel_12 | 12（想定） |
| 道路種別 | drm10 / drm20 / drm31 / drm32 / drm40_50 / drm60_70 | 同左 | 同左（想定） |
| 区間番号キーの0埋め | あり（11桁 zfill） | なし | 要確認 |
| コード→ラベル辞書 | 単方向列 | 上り／下り 分離列 | 要確認 |
| 型スキーマ | コード内 default 処理 | `CSV項目名と型.csv` で駆動 | 同形式を想定 |
| 実数キャスト対象列 | 少 | 多（旅行速度／幅員構成／安全施設／交差点密度 等） | 要確認 |
| 紐づけキー | GeoJSON属性 `census` ⇔ CSV `交通調査基本区間番号` | 同左 | 同左（想定） |

### 3.1 元GeoJSON（DL直後のタイル）の実データ比較

`geojson_2/drm*_*.geojson`（H27: 255ファイル/5,140 features、R03: 54ファイル/374 features）を
横断調査した結果、元データには以下の違いがある。

| 項目 | H27（可視化ツール） | R03（可視化ツール） |
|---|---|---|
| properties キー | `census`, `color`, **`kanri`, `roadtype`, `keycode`**（5キー） | **`census`, `color`（2キーのみ）** |
| crs メンバー | **なし**（GeoJSON仕様上 WGS84/CRS84 扱い） | **あり**（`EPSG:4612` = JGD2000 地理座標） |
| color 値域 | 10,20,31,32,40,50,60,70（8種） | 10,31,32,40,60（サンプル範囲） |
| geometry | LineString + MultiLineString 混在（LineString優勢） | LineString + MultiLineString 混在 |
| census キー | 11桁文字列（0埋め済み） | 11桁文字列（0埋め済み） |

**再整理への影響:**

1. **属性の持ち方が違う（最重要）** — H27 は GeoJSON 自体に `kanri`（管理区分）・`roadtype`
   （道路種別）を冗長に持つが、R03 は削ぎ落とされ詳細属性はすべて箇所別基本表CSVの紐づけで付与する。
   → エンジンは「GeoJSON側は `census`/`color` のみ信頼し、実質属性はCSV結合で付与」に統一する。
   H27 の `kanri`/`roadtype` は無視／上書きされるため実害なし。
2. **crs の有無** — R03 は `EPSG:4612`(JGD2000)、H27 は crs 無し(=CRS84/WGS84)。実用上ほぼ同座標だが
   nominal には測地系が異なる。出力 crs の統一方針（例: 全て EPSG:4326 に寄せる／元のまま）を
   config で扱えるようにしておく。
3. **census キーの0埋め** — 元GeoJSONは両年度とも11桁で揃っている。0埋め差分が問題になるのは
   箇所別基本表CSV側（H27のCSVは先頭ゼロが落ちるため `zfill(11)` が必要）。
   → 0埋めは「CSV読み込み時にキー列へ適用」として config 化する。
4. **geometry 混在** — 両年度とも LineString/MultiLineString 混在のため、MultiLineString への
   正規化（`2_toMultiLineString` 相当）は両年度で必要（共通処理）。

**結論:** 構造差はすべて config と CSV結合ロジックで吸収可能。方式Aの統合設計は問題なく成立する。

### 3.2 成果物GeoJSONのサイズ差（H27 ≫ R03）

新エンジンで生成した成果物GeoJSONは、年度でサイズが大きく異なる。

| | feature数 | ユニークcensus区間 | feat/census | 属性数/feature | 出力GeoJSON |
|---|---|---|---|---|---|
| R03 (2021) | 127,363 | 99,064 | 1.29 | 161 | 1.41GB |
| H27 (2015) | 559,414 | 94,175 | 5.94 | 124 | 4.25GB |

**原因は「元データの線分分割の細かさ」である。**

- 区間数（census）は両年度でほぼ同じ（約94〜99千）＝道路網の規模は同程度。
- H27の元GeoJSONは **LineString優勢** で、1区間が多数の短い線分に分割されている（feat/census ≈ 5.9）。
  R03は MultiLineString にまとまっている（≈ 1.3）。→ H27の feature 数は R03 の約4.4倍。
- 箇所別基本表の紐づけでは、**同一censusを持つ全featureに同じ属性（約120〜160列）が丸ごと複製**される。
  H27は1区間を約6本に分けているため、同じ属性ブロックを約6回書き込む（R03は約1.3回）。
- 結果、属性列数は H27(124) < R03(161) にもかかわらず、feature数（＝属性の重複量）の多さが勝って、
  H27のGeoJSONは R03 の約3倍になる。

**影響と対処:**
- ファイルサイズに効くのは GeoJSON / GeoParquet のみ。**PMTiles化には実質影響しない**
  （tippecanoe が結合・簡略化するため）。
- H27のGeoJSONを軽量化したい場合は、同一censusの連続線分を MultiLineString に統合（dissolve）する
  後処理を挟む選択肢がある（現状は元データの分割を保持している）。

---

## 4. ディレクトリ構成（実装済み）

```
mlit-road-traffic-census-converter/
├── README.md                    … 全体説明・使い方・成果物一覧
├── DESIGN.md                    … 本設計書
├── VERIFICATION.md              … 完全性・紐づけ検証レポート
├── requirements.txt             … geopandas, pandas, requests, PyYAML
├── .gitignore                   … data/ と旧フォルダを除外
│
├── census_converter/            … 共通エンジン（年度非依存）
│   ├── __init__.py
│   ├── config.py                … 年度config読込・作業パス解決
│   ├── download.py              … GeoJSONタイル + 箇所別基本表CSV のDL
│   ├── merge_geojson.py         … 分割GeoJSONをJSONストリーム結合（破損スキップ）
│   ├── normalize_geometry.py    … LineString → MultiLineString 統一
│   ├── merge_csv.py             … 県別CSV結合（文字コード自動判定・空行除去・キー0埋め）
│   ├── transform_csv.py         … コード→ラベル変換 + 型キャスト（config駆動）
│   ├── join.py                  … census ⇔ 区間番号 でGeoJSONに属性結合
│   ├── export.py                … parquet(geopandas) / pmtiles(tippecanoe -pk -pf) / fgb(ogr2ogr)
│   └── verify.py                … 紐づけ率・孤児タイル点検（オフライン）
│
├── configs/                     … 年度ごとの差分だけ
│   ├── h27.yaml / r03.yaml / r07.yaml（R07はテンプレート）
│   ├── mappings/                … コード→ラベル辞書（h27_mappings.yaml, r03_mappings.yaml）
│   ├── schema/                  … 年度別の項目名と型（h27_schema.csv, r03_schema.csv）
│   └── tileindex/               … tileindex_zoomlevel_12.csv, KenCodeList.csv
│
├── scripts/                     … 個別ダウンロードスクリプト（download.py の薄いラッパー）
│   ├── download_geojson_tiles.py   … GeoJSONタイル単体DL
│   ├── download_kasho_csv.py       … 箇所別基本表CSV単体DL
│   └── download_jikantai_csv.py    … 時間帯別交通量表CSV単体DL（§8）
│
├── run.py                       … CLI: `python run.py --year r03 --step all`
│
├── data/                        … 入力・中間・成果物（.gitignore 対象。data/README.md に構成説明）
│   └── {r03,h27}/
│       ├── geojson_tiles/       … 【入力】分割GeoJSON（道路種別×タイル）
│       ├── csv/                 … 【入力】CSVを種別ごとに格納
│       │   ├── kasho/           …   箇所別基本表 kasyo{NN}.csv（merge_csvが全結合する対象）
│       │   └── jikantai/        …   時間帯別交通量表 zkntrf{NN}.csv（スキーマ別のため分離／§8）
│       ├── work/                … 【中間】結合・正規化・変換の途中生成物
│       └── output/              … 【成果物】traffic_census_{YYYY}_converted.*
│       ※ 入力は実ファイルで自己完結。旧フォルダに依存しない
│
└── （旧フォルダ）H27… / R03… … 旧コンバーターの保全（.gitignore、削除可）
```

- 出力ファイル名の接尾辞は config の `output_suffix`（既定 `converted`）で可変。
  例: `traffic_census_2021_converted.geojson`。

---

## 5. 共通エンジンの処理段（パイプライン）

| # | モジュール | 処理内容 | 年度依存（config） |
|---|---|---|---|
| 1 | `download.py` | GeoJSONタイル（道路種別×タイル）と箇所別基本表CSV（県別）をDL | URL / タイルインデックス / 道路種別 / 県コード |
| 2 | `merge_geojson.py` | 分割GeoJSONをJSONストリームで結合（高速・破損ファイルはスキップ） | なし |
| 3 | `normalize_geometry.py` | LineString → MultiLineString に統一 | なし |
| 4 | `merge_csv.py` | 県別CSVを結合（utf-8/shift-jis/cp932 自動判定、空行除去、キー0埋め） | 0埋め桁数 |
| 5 | `transform_csv.py` | コード値→ラベル変換、Integer/Real 型キャスト | コード辞書 / 型スキーマ |
| 6 | `join.py` | GeoJSON属性 `census` ⇔ CSV `交通調査基本区間番号` で属性結合 | キー列名 |
| 7 | `export.py` | GeoParquet(geopandas) / PMTiles(tippecanoe `-Z4 -z14 -pk -pf`) / fgb(ogr2ogr) | 出力名 |
| ✓ | `verify.py` | 紐づけ率・孤児タイル点検（オフライン、サーバ不使用） | なし |

### CLI 例

```bash
# 全ステップ実行
python run.py --year r03 --step all

# 個別ステップ実行
python run.py --year h27 --step download
python run.py --year r03 --step merge,normalize,mergecsv,transform,join,verify
python run.py --year r03 --step export --formats parquet,pmtiles
```

> PMTilesは `-pk`(`--no-tile-size-limit`) `-pf`(`--no-feature-limit`) で生成し、**featureを間引かず全保持**する。

---

## 6. 決定事項（確定済み）

1. **入力データの配置** … 入力（GeoJSONタイル・CSV）は `data/{年度}/` に**実ファイルで集約**し自己完結化。
   旧フォルダには依存しない。`data/` は .gitignore でGitHub非公開。旧23GBフォルダは保全（削除可）。
2. **公開** … `_convert` 系の成果物は非公開（`data/`）。**コード/configのみGitHub公開**
   （<https://github.com/shiwaku/mlit-road-traffic-census-converter>）。
3. **出力ファイル名** … 接尾辞を `_converted` に統一（`output_suffix`）。
4. **PMTiles** … `-pk -pf` で間引かず全feature保持（間引き版は不採用）。
5. **DL完全性** … 全件監査を実施。R03は実漏れ3件を回収、H27の1件はサーバ破損ファイルで除外
   （[VERIFICATION.md](VERIFICATION.md)）。
6. **R07** … 公開後に実URL・スキーマを確認して `configs/r07.yaml` 他を確定（テンプレート済み）。

---

## 7. データ源・ライセンス

- 令和3年度: 箇所別基本表 <https://www.mlit.go.jp/road/census/r3/index.html> /
  可視化ツール <https://www.mlit.go.jp/road/ir/ir-data/census_visualizationR3/index.html>
- 平成27年度: 可視化ツール <https://www.mlit.go.jp/road/ir/ir-data/census_visualization2/index.html>
- ライセンス: 政府標準利用規約（第2.0版）準拠 <https://www.mlit.go.jp/link.html>
- 関連リポジトリ: <https://github.com/shiwaku/road-traffic-census-map-2021> /
  <https://github.com/shiwaku/road-traffic-census-map-2015>

---

## 8. 時間帯別交通量表の連携（拡張検討）

R03 census ページには箇所別基本表(`kasyo{ken}.csv`)に加えて **時間帯別交通量表**
(`zkntrf{ken}.csv`、県別 01–47) が公開されている。これをジオメトリ／PMTilesに紐づけて、
Webマップ上で地物クリック時に**時間帯別交通量のグラフ**を表示できるかを検証した（2026-07-05、北海道 kasyo01/zkntrf01 で実証）。

### 8.1 結論：可能。ただし2段階結合が必要

時間帯別交通量表には **`交通調査基本区間番号`（ジオメトリの結合キー）が無い**。
キーは複合キー `都道府県指定市コード` + `交通量調査単位区間番号`（＝**調査単位区間**＝交通量を実測した単位）。

一方、箇所別基本表は両方のキーを持つため橋渡しになる：

```
ジオメトリ ──census──▶ 箇所別基本表 ──(交通量／都道府県指定市コード ＋ 交通量／調査単位区間番号)──▶ 時間帯別交通量表
```

実測した結合率（箇所別基本表の全基本区間が時間帯別表にヒットするか）：**4,800 / 4,883 = 98.3%**（北海道）。
未ヒット約1.7%は zkntrf 側に存在しない調査単位区間。

### 8.2 キーの粒度差（N対1）

`交通調査基本区間番号` と `調査単位区間` は**別概念で1対1ではない**。基本区間のほうが細かい。

| 概念 | 意味 | 北海道での個数 |
|---|---|---|
| `交通調査基本区間番号`（11桁） | 道路網の最小区間＝ジオメトリ1本 | 4,883 |
| `都道府県指定市コード` + `調査単位区間番号` | 交通量を実測した観測区間 | 2,582 |

1調査単位区間に属する基本区間数の分布（北海道）：1本=1,339 / 2本=694 / 3本=283 / 4本=140 / 5本=68 / 6本以上=58+。
→ 約半数は偶然1対1だが、残りは **1つの観測値を複数のジオメトリ区間が共有** する構造。
時間帯別表も同じ観測単位なので、**同じグラフが複数の基本区間に複製付与**される（センサスの仕様）。

### 8.3 時間帯別交通量表の構造

- 1調査単位区間 = **4行**（`上り・下りの別` {1,2} × `車種区分` {1=小型, 2=大型}）。一部2行。
- 時間帯列は `時間帯別自動車類交通量（台／時）／７時台` … `／６時台` の **7時始まり24列**（7→23→0→6の順、ソート注意）。
- 加えて `昼間１２時間自動車類交通量（台）` / `２４時間自動車類交通量（台）` を保持。
- グラフは「方向別・車種別の4系列」または合算で描く設計を先に決める必要あり。

### 8.4 Webマップ連携の構成案

**現行PMTilesは連携キーを既に保持している**（出力168列中に `交通量／都道府県指定市コード`・
`交通量／調査単位区間番号` が残存）。したがってPMTilesを作り直さずクリック時ルックアップが可能。

- **案1: 外部ルックアップ方式（推奨）** — PMTilesはそのまま。時間帯別データを
  複合キー辞書（`{"都道府県指定市コード_調査単位区間番号": {上り:{小型:[24値],大型:[…]}, 下り:{…}}}`）
  として県別JSONで持ち、クリック時に地物プロパティのキーで引いて Chart.js / Vega-Lite で描画。
  県別に遅延ロードすればペイロード軽量。686MBのPMTilesを太らせずに済む。
- **案2: 焼き込み方式** — 時間帯別を集約(24列)ないし上下×車種×24(最大96列)で各地物に付与してから
  tippecanoe。自己完結・追加fetch不要だがPMTiles肥大・観測値の複製冗長・1地物あたりプロパティ量制約。

### 8.5 実装状況

- **DL: 実装済み** — `configs/{r03,h27}.yaml` に `jikantai_csv_url_template`（`.../data/csv/zkntrf{ken}.csv`）を
  追加し、`download.py` に `download_jikantai_csv()` を実装。`--step download` で geojson_tiles + csv + jikantai を
  まとめて取得する。保存先は `data/{year}/csv/jikantai/zkntrf{NN}.csv`（箇所別基本表 `csv/kasho/` とは
  スキーマが異なるため別サブディレクトリ）。**R03・H27とも全国47県取得済み**（各約26MB、欠落0）。
  H27の時間帯別表もキー構造は同一（`都道府県指定市コード` + `交通量調査単位区間番号`）。
  単体取得用に `scripts/download_jikantai_csv.py`（census_converter非依存のスタンドアロン版）も保存。
- **変換/連携: 未着手** — 「zkntrf → Webマップが直接読める県別JSON（複合キー→時間帯配列）に変換するステップ」
  を追加する。まず全国47県で結合率を確認してから持ち方（案1/案2）を確定する。
