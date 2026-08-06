# QGIS スタイル（主題図 QML / QLR / QGZ）

GeoParquet を QGIS で表示するための主題図スタイル。QML（スタイル単体）に加え、
ダウンロードしただけでスタイルが当たる QLR・QGZ を [`bundle/`](bundle/) に用意している（後述）。
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

## 同梱物（`bundle/`）— ダウンロードしただけでスタイルが当たる形

上の手順（手動で「スタイルを読み込む」）を省けるように、`bundle/` に**リリース配布用の3形式**を
`generate_qgis_bundle.py` で生成している。スタイル本体は上表のQMLをそのまま埋め込むので、
QMLを直して両スクリプトを再実行すれば同梱物にも自動で伝播する（色・区分の二重管理は無い）。

| ファイル | 数 | 使い方 | 得られるもの |
|---|---|---|---|
| `<prefix>.qgz` | 2（年度別） | ダブルクリックで開く | 5主題図＋地理院淡色（背景）が一括。レイヤのチェックで切替 |
| `<prefix>_N_<theme>.qlr` | 10（5主題図×2年度） | QGISへドラッグ&ドロップ | その主題図1つがスタイル適用済みレイヤとして追加 |
| `<prefix>_converted.qml` | 2（年度別） | parquetと同じフォルダに置くだけ | parquet追加時にQGISが既定スタイルとして自動適用（中身=24時間交通量図） |

> **前提**: `.qgz` / `.qlr` は datasource を相対パス（`./<prefix>_converted.parquet`）で持ち、
> QGIS はそれを**ファイル自身の位置**を基準に解決する。したがって同梱物と GeoParquet は
> **同一フォルダ**に置く必要がある。サイドカーQMLも「parquetと同名・同階層」が自動適用の条件。
> リリース用ZIP（`--pack`）は GeoParquet を同梱するので、解凍しただけでこの条件を満たす。
> `bundle/` から個別に取り出して使う場合は、自分で parquet と並べる。

プロジェクトCRSはデータと同じ（R03=EPSG:4612 / H27=EPSG:4326、`<units>degrees</units>`）。
背景の地理院タイルはXYZなのでレイヤ側に EPSG:3857 と全球extentを持たせ、QGISがオンザフライ変換して重ねる。

XMLの細部は、実際に配布・動作している
[mlit-urban-planning-converter](https://github.com/shiwaku/mlit-urban-planning-converter)
の `src/tosiko_pmtiles/qgis_project.py`（QGIS 3.34の実出力合わせ）に倣っている。
背景地図レイヤは属性・子要素までそちらと一致させてある。

```bash
python configs/qgis_styles/generate_qgis_bundle.py                  # bundle/ を生成
python configs/qgis_styles/generate_qgis_bundle.py --install-to-data # data/<year>/output/ にも配置
python configs/qgis_styles/generate_qgis_bundle.py --pack /tmp/dist  # リリース添付用ZIPを作る
```

`--install-to-data` はローカルで `run.py` 実行後の `data/{r03,h27}/output/` に同梱物をコピーする
（parquetと並ぶので、そのまま `.qgz` を開いて確認できる）。

`--pack` は `<prefix>_qgis.zip`（14ファイル = **GeoParquet** + qgz + qlr5 + 主題図qml5 + サイドカーqml
+ README.txt）を作る。**GeoParquet を同梱するのが要点**で、これにより利用者は
「zipをダウンロード → 解凍 → `.qgz` を開く」だけで済み、解凍先を parquet に合わせる必要がなくなる
（そこを間違えるとレイヤが「利用不可」になるのが最大の躓きどころだった）。
同梱元は `data/<year>/output/<prefix>_converted.parquet` なので、事前に
`python run.py --year {r03,h27} --step all` が必要（無い場合はエラーで停止する）。
サイズは R03 約81MB / H27 約99MB（parquetは内部圧縮済みだが deflate でさらに15〜19%縮む）。

## 再生成

```bash
python configs/qgis_styles/generate_qml.py           # 主題図QML（10ファイル）
python configs/qgis_styles/generate_qgis_bundle.py   # 同梱物（bundle/）
```

**2つは必ずセットで実行する。** `generate_qml.py` だけ実行して `generate_qgis_bundle.py` を忘れると、
QMLは新しいのに `bundle/` の `.qlr` / `.qgz` に埋め込まれたスタイルが古いまま残り、
「色・区分は常に一致」という前提が崩れる。

この取り違えは [`.github/workflows/check-qgis-styles.yml`](../../.github/workflows/check-qgis-styles.yml)
が検知する（両方を再生成して `git diff --exit-code`。出力は `ZIP_EPOCH` 固定で再現的なので、
再生成漏れがあるときだけ差分が出る）。CIが赤くなったら上の2コマンドを実行して差分をコミットすればよい。

区分値・色は `generate_qml.py` 冒頭の定義を編集して調整する。**QMLを変えたら
`generate_qgis_bundle.py` も再実行**すること（`bundle/` に埋め込まれたスタイルを更新するため）。

## 実装メモ（QGISの落とし穴）

- **線幅の data-defined は「スタイルを読み込む」で反映されない場合がある。** 24時間交通量図は当初、
  ルール(色=道路種別)＋データ定義式で線幅を変えていたが、幅が一律のままになった。このため
  **入れ子ルール（親=道路種別で色、子=交通量ビンで静的な線幅）** に変更し、DDに依存しない実装にした。
- **速度図の分類式は `min()`/`max()` を使う。** QGISの式に `least()`/`greatest()` は無く、
  使うと「式が不正です」となり全フィーチャが未分類＝非表示になる（混雑時・非混雑時旅行速度図で発生）。
- **`bundle/` の相対パスはファイル自身の位置基準。** `.qgz` は `<properties><Paths><Absolute>false`、
  `.qlr` は QGIS が読み込み元パスで解決する。同梱物を parquet と別フォルダに置くとレイヤが
  「利用不可」になる。これは案内文でカバーしきれない類の失敗なので、リリース用ZIPには
  **GeoParquet 自体を入れて構造的に防いでいる**（`pack()`）。ZIPはフラット構造のままにしており、
  Windows/macOS の既定の展開がZIP名のフォルダを作るため、結果として1フォルダに揃う。
- **`<properties><SpatialRefSys><ProjectionsEnabled>1` が無いと `<projectCrs>` が読まれない。**
  QGISは `readNumEntry("SpatialRefSys","/ProjectionsEnabled",0)` が偽ならprojectCrsノードを
  見にいかない（qgsproject.cpp）。**プロジェクトCRSが「CRSなし」になり、投影変換ができないので
  EPSG:3857の背景地図も描かれない**という2症状が同時に出る。初版でまさにこれを踏んだ。
- **背景地図（XYZ）は実出力を写す。** 手書きの最小構成では読み込めても描画されなかった。要点は
  URIを `http-header:referer=&type=xyz&url=…（{z}はpercent encode）&zmax=18&zmin=0` にすること、
  レイヤのCRSとextentを **EPSG:3857・Webメルカトル全球**で書くこと（プロジェクトの経緯度を
  流用するとメートル値が度として扱われ、どこにも出てこない）、`<extent>`／`<wgs84extent>`／
  `<noData>`／`<flags>`／`<temporal>`／`<customproperties>`／`<pipe>` を省かないこと。
- **datasource に `|layername=` は付けない。** Parquetのレイヤ名はファイル基底名で決まるため、
  付けると取り違えの元になるだけ（参考実装も付けていない）。
- **GeoParquet の読み込みには GDAL の Parquet ドライバが必要。** 無いビルドではブラウザパネルに
  `.parquet` が出ないため、スタイル以前にデータが開けない。
