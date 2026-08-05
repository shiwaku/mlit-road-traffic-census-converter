# -*- coding: utf-8 -*-
"""GeoParquet と一緒に配布する QGIS 同梱物（サイドカーQML / QLR / QGZ）を生成する。

生成物は `bundle/` に出力し、GitHub Releases で GeoParquet と同じフォルダに置く想定:

  <output_basename>_converted.qml   既定スタイル（サイドカー）。parquetと同名・同階層に置くと
                                    QGISがレイヤ追加時に自動適用する（中身=24時間交通量図）
  <prefix>_N_<theme>.qlr            レイヤ定義。1ファイルD&Dでスタイル適用済みレイヤを1テーマ追加
  <prefix>.qgz                      5主題図＋地理院淡色（背景）をまとめたQGISプロジェクト

スタイル本体は generate_qml.py の出力をそのまま埋め込むため、色・区分は主題図QMLと常に一致する
（QMLを直したら本スクリプトを再実行すれば同梱物にも伝播する）。

datasource は相対パス（`./<file>.parquet`）。QGISは QLR/QGZ 自身の位置を基準に解決するので、
**同梱物と parquet は同一フォルダに置く**必要がある（リリースを丸ごとダウンロードした状態が該当）。

XML の細部は、実際に動いている
[mlit-urban-planning-converter](https://github.com/shiwaku/mlit-urban-planning-converter)
の `src/tosiko_pmtiles/qgis_project.py`（QGIS 3.34 の実出力合わせ）に倣っている。手書きの
最小構成では「プロジェクトCRSがCRSなし」「背景地図が描かれない」になったため、実物合わせが確実。
落とし穴は本ファイル内および README の実装メモを参照。

使い方:
    python configs/qgis_styles/generate_qgis_bundle.py
    python configs/qgis_styles/generate_qgis_bundle.py --install-to-data  # data/<year>/output/ にも配置
    python configs/qgis_styles/generate_qgis_bundle.py --pack /tmp/dist   # リリース用ZIPを作る
"""
import argparse
import os
import shutil
import warnings
import zipfile
from xml.sax.saxutils import escape, quoteattr

from generate_qml import QGIS_VERSION, YEARS, build_year

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
BUNDLE_DIR = os.path.join(OUT_DIR, "bundle")
REPO_ROOT = os.path.dirname(os.path.dirname(OUT_DIR))

# 主題図の並び順と表示名。キーは generate_qml.py が出す QML ファイル名の中間部分。
THEMES = [
    ("1_24jikankotsuryo", "24時間交通量（全車上下計）"),
    ("2_konzatsudo", "混雑度"),
    ("3_ogatashakonnyuritsu", "大型車混入率（％）"),
    ("4_konzatsuji", "混雑時旅行速度"),
    ("5_hikonzatsuji", "昼間非混雑時旅行速度"),
]
# サイドカーQML（レイヤ追加時に自動適用される既定スタイル）に採用する主題図。
DEFAULT_THEME = "1_24jikankotsuryo"

# 年度メタ。epsg は元データのCRS（configs/*.yaml が crs: null =再投影しないため元CRSが残る）。
YEAR_META = {
    "r03": {"era": "R03", "wareki": "令和3年度", "epsg": 4612},
    # H27元データは crs メンバーなし = GeoJSONの既定である WGS84。
    "h27": {"era": "H27", "wareki": "平成27年度", "epsg": 4326},
}

# 初期表示範囲（データCRS=経緯度）。日本全体が入る範囲。
DEFAULT_EXTENT = (122.0, 20.0, 154.0, 46.0)

# 背景地図（地理院タイル 淡色地図）。XYZタイルなので座標系は常に Web メルカトル。
BASEMAP_NAME = "地理院タイル 淡色地図"
BASEMAP_ID = "gsi_pale_basemap"
BASEMAP_URL = "https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png"
BASEMAP_EPSG = 3857
_WEB_MERCATOR_MAX = 20037508.342789244
BASEMAP_EXTENT = (-_WEB_MERCATOR_MAX, -_WEB_MERCATOR_MAX, _WEB_MERCATOR_MAX, _WEB_MERCATOR_MAX)

ATTRIBUTION = "背景地図: 地理院タイル（淡色地図） / データ: 国土交通省 道路交通センサス"
# ZIP内のタイムスタンプは固定する（実行時刻を入れると中身が同じでもバイト列が変わり、
# bundle/ をコミット対象にしている都合で毎回空の差分が出る）。
ZIP_EPOCH = (1980, 1, 1, 0, 0, 0)


def style_body(qml: str) -> str:
    """主題図QMLの <qgis> 直下（renderer-v2 と layerGeometryType）を取り出す。

    どちらの要素も maplayer の子として有効なので、そのまま QLR / QGZ に埋め込める。
    """
    head_end = qml.index("\n", qml.index("<qgis ")) + 1
    return qml[head_end:qml.rindex("</qgis>")].rstrip("\n")


def reindent(xml: str, extra: str = "  ") -> str:
    """QML由来のXMLを maplayer 直下の深さに合わせて字下げする。"""
    return "\n".join(extra + line for line in xml.splitlines())


def srs_xml(epsg: int, pad: str = "      ") -> str:
    """<spatialrefsys>。proj4 / WKT は pyproj から引く（geopandas 経由で既に依存）。

    背景地図（XYZタイル）は EPSG:3857 で、データ側の経緯度とは別に書き出す必要がある。
    ここを取り違えるとメートル値が度として扱われ、レイヤが画面上のどこにも出てこない。
    """
    from pyproj import CRS

    crs = CRS.from_epsg(epsg)
    with warnings.catch_warnings():
        # proj4化で情報が落ちうるという一般的な警告。扱うのは経緯度とWebメルカトルなので
        # 落ちるものは無い。QGISの旧バージョン互換のため proj4 も併記する。
        warnings.simplefilter("ignore", UserWarning)
        proj4 = crs.to_proj4()
    acronym = "longlat" if crs.is_geographic else dict(
        p.split("=", 1) for p in proj4.split() if "=" in p).get("+proj", "")
    return (
        f'{pad}<spatialrefsys nativeFormat="Wkt">\n'
        f'{pad}  <wkt>{escape(crs.to_wkt())}</wkt>\n'
        f'{pad}  <proj4>{escape(proj4)}</proj4>\n'
        f'{pad}  <srsid>{epsg}</srsid>\n'
        f'{pad}  <srid>{epsg}</srid>\n'
        f'{pad}  <authid>EPSG:{epsg}</authid>\n'
        f'{pad}  <description>{escape(crs.name)}</description>\n'
        f'{pad}  <projectionacronym>{escape(acronym)}</projectionacronym>\n'
        f'{pad}  <ellipsoidacronym>{ellipsoid_authid(epsg)}</ellipsoidacronym>\n'
        f'{pad}  <geographicflag>{"true" if crs.is_geographic else "false"}</geographicflag>\n'
        f'{pad}</spatialrefsys>'
    )


def ellipsoid_authid(epsg: int) -> str:
    """楕円体のEPSGコード（GRS80=EPSG:7019 / WGS84=EPSG:7030）。"""
    from pyproj import CRS

    crs = CRS.from_epsg(epsg)
    ident = (crs.ellipsoid.to_json_dict().get("id") or {}) if crs.ellipsoid else {}
    if ident.get("authority") and ident.get("code"):
        return f"{ident['authority']}:{ident['code']}"
    return "NONE"


def extent_xml(box: tuple, pad: str, tag: str = "extent") -> str:
    return (f'{pad}<{tag}>\n'
            f'{pad}  <xmin>{box[0]!r}</xmin>\n'
            f'{pad}  <ymin>{box[1]!r}</ymin>\n'
            f'{pad}  <xmax>{box[2]!r}</xmax>\n'
            f'{pad}  <ymax>{box[3]!r}</ymax>\n'
            f'{pad}</{tag}>')


def vector_maplayer(layer_id: str, name: str, source: str, style: str, epsg: int,
                    pad: str = "    ") -> str:
    """スタイル適用済みベクタレイヤの <maplayer>。"""
    return (
        f'{pad}<maplayer type="vector" geometry="Line" wkbType="MultiLineString" '
        f'hasScaleBasedVisibilityFlag="0" minScale="1e+08" maxScale="0" '
        f'simplifyDrawingHints="1" simplifyDrawingTol="1" simplifyLocal="1" simplifyMaxScale="1" '
        f'simplifyAlgorithm="0" readOnly="0" labelsEnabled="0" symbologyReferenceScale="-1" '
        f'styleCategories="AllStyleCategories" autoRefreshMode="Disabled" autoRefreshTime="0">\n'
        f'{extent_xml(DEFAULT_EXTENT, pad + "  ")}\n'
        f'{extent_xml(DEFAULT_EXTENT, pad + "  ", tag="wgs84extent")}\n'
        f'{pad}  <id>{escape(layer_id)}</id>\n'
        f'{pad}  <datasource>{escape(source)}</datasource>\n'
        f'{pad}  <layername>{escape(name)}</layername>\n'
        f'{pad}  <srs>\n{srs_xml(epsg, pad + "    ")}\n{pad}  </srs>\n'
        f'{pad}  <provider encoding="UTF-8">ogr</provider>\n'
        f'{reindent(style, pad)}\n'
        f'{pad}  <layerOpacity>1</layerOpacity>\n'
        f'{pad}  <blendMode>0</blendMode>\n'
        f'{pad}  <featureBlendMode>0</featureBlendMode>\n'
        f'{pad}</maplayer>'
    )


def basemap_datasource() -> str:
    """XYZレイヤの datasource。QGIS 3.34 の出力と同じ並び・同じ encode。

    - URIは `http-header:referer=&type=xyz&url=…&zmax=18&zmin=0`。3.34の出力に
      `crs` と `format` は無い（`type=xyz` ではプロバイダ側が EPSG:3857 に固定するので
      `crs` は効かない。値を持たない `format` はURIのパースを壊しうるので書かない）
    - `url` は percent encode する（`{z}` → `%7Bz%7D`）
    """
    return ("http-header:referer=&type=xyz&url="
            + BASEMAP_URL.replace("{", "%7B").replace("}", "%7D")
            + "&zmax=18&zmin=0")


def basemap_maplayer(pad: str = "    ") -> str:
    """地理院タイル（淡色地図）の XYZ ラスタレイヤ。

    手書きの最小構成では「読み込めても描画されない」ため、動いているプロジェクトの
    <maplayer> を写している。extent（Webメルカトル全球）・wgs84extent・noData・flags・
    temporal・customproperties・pipe（resampling〜resamplingStage）まで揃えるのが要点。
    """
    return (
        f'{pad}<maplayer type="raster" hasScaleBasedVisibilityFlag="0" minScale="1e+08" '
        f'maxScale="0" styleCategories="AllStyleCategories" autoRefreshMode="Disabled" '
        f'autoRefreshTime="0" refreshOnNotifyEnabled="0" refreshOnNotifyMessage="" '
        f'legendPlaceholderImage="">\n'
        f'{extent_xml(BASEMAP_EXTENT, pad + "  ")}\n'
        f'{pad}  <wgs84extent>\n'
        f'{pad}    <xmin>-180</xmin>\n'
        f'{pad}    <ymin>-85.05112877980660357</ymin>\n'
        f'{pad}    <xmax>180</xmax>\n'
        f'{pad}    <ymax>85.05112877980660357</ymax>\n'
        f'{pad}  </wgs84extent>\n'
        f'{pad}  <id>{BASEMAP_ID}</id>\n'
        f'{pad}  <datasource>{escape(basemap_datasource())}</datasource>\n'
        f'{pad}  <keywordList>\n{pad}    <value></value>\n{pad}  </keywordList>\n'
        f'{pad}  <layername>{escape(BASEMAP_NAME)}</layername>\n'
        f'{pad}  <srs>\n{srs_xml(BASEMAP_EPSG, pad + "    ")}\n{pad}  </srs>\n'
        f'{pad}  <provider>wms</provider>\n'
        f'{pad}  <noData>\n'
        f'{pad}    <noDataList bandNo="1" useSrcNoData="0"/>\n'
        f'{pad}  </noData>\n'
        f'{pad}  <map-layer-style-manager current="default">\n'
        f'{pad}    <map-layer-style name="default"/>\n'
        f'{pad}  </map-layer-style-manager>\n'
        f'{pad}  <metadataUrls/>\n'
        f'{pad}  <flags>\n'
        f'{pad}    <Identifiable>1</Identifiable>\n'
        f'{pad}    <Removable>1</Removable>\n'
        f'{pad}    <Searchable>1</Searchable>\n'
        f'{pad}    <Private>0</Private>\n'
        f'{pad}  </flags>\n'
        f'{pad}  <temporal bandNumber="1" fetchMode="0" enabled="0" mode="0">\n'
        f'{pad}    <fixedRange>\n{pad}      <start></start>\n{pad}      <end></end>\n'
        f'{pad}    </fixedRange>\n'
        f'{pad}  </temporal>\n'
        f'{pad}  <customproperties>\n'
        f'{pad}    <Option type="Map">\n'
        f'{pad}      <Option type="QString" name="identify/format" value="Undefined"/>\n'
        f'{pad}    </Option>\n'
        f'{pad}  </customproperties>\n'
        f'{pad}  <pipe>\n'
        f'{pad}    <provider>\n'
        f'{pad}      <resampling maxOversampling="2" zoomedInResamplingMethod="nearestNeighbour" '
        f'enabled="false" zoomedOutResamplingMethod="nearestNeighbour"/>\n'
        f'{pad}    </provider>\n'
        f'{pad}    <rasterrenderer type="singlebandcolordata" alphaBand="-1" opacity="1" '
        f'nodataColor="" band="1">\n'
        f'{pad}      <rasterTransparency/>\n'
        f'{pad}      <minMaxOrigin>\n'
        f'{pad}        <limits>None</limits>\n'
        f'{pad}        <extent>WholeRaster</extent>\n'
        f'{pad}        <statAccuracy>Estimated</statAccuracy>\n'
        f'{pad}        <cumulativeCutLower>0.02</cumulativeCutLower>\n'
        f'{pad}        <cumulativeCutUpper>0.98</cumulativeCutUpper>\n'
        f'{pad}        <stdDevFactor>2</stdDevFactor>\n'
        f'{pad}      </minMaxOrigin>\n'
        f'{pad}    </rasterrenderer>\n'
        f'{pad}    <brightnesscontrast contrast="0" gamma="1" brightness="0"/>\n'
        f'{pad}    <huesaturation colorizeBlue="128" colorizeStrength="100" grayscaleMode="0" '
        f'invertColors="0" saturation="0" colorizeOn="0" colorizeRed="255" colorizeGreen="128"/>\n'
        f'{pad}    <rasterresampler maxOversampling="2"/>\n'
        f'{pad}    <resamplingStage>resamplingFilter</resamplingStage>\n'
        f'{pad}  </pipe>\n'
        f'{pad}  <blendMode>0</blendMode>\n'
        f'{pad}</maplayer>'
    )


def tree_layer(layer_id: str, name: str, checked: bool, pad: str,
               source: str = "", provider_key: str = "") -> str:
    """レイヤツリーの1行。背景地図は実出力と同じく source / providerKey を埋める
    （データ側のベクタレイヤは空でも id で解決される）。"""
    return (f'{pad}<layer-tree-layer id={quoteattr(layer_id)} name={quoteattr(name)} '
            f'source="{escape(source)}" providerKey="{provider_key}" '
            f'checked="{"Qt::Checked" if checked else "Qt::Unchecked"}" expanded="0">\n'
            f'{pad}  <customproperties/>\n'
            f'{pad}</layer-tree-layer>')


def build_qlr(layer_id: str, name: str, source: str, style: str, epsg: int) -> str:
    """1テーマ分のレイヤ定義ファイル（.qlr）。"""
    return (
        "<!DOCTYPE qgis-layer-definition>\n"
        f"<!-- {name}: 道路交通センサス GeoParquet のレイヤ定義（スタイル適用済み）。\n"
        "     https://github.com/shiwaku/mlit-road-traffic-census-converter が生成。\n"
        "     *.parquet と同じフォルダに置いてから QGIS にドラッグ&ドロップすること。 -->\n"
        "<qlr>\n"
        "  <layer-tree-group>\n"
        f'{tree_layer(layer_id, name, True, "    ")}\n'
        "  </layer-tree-group>\n"
        "  <maplayers>\n"
        f"{vector_maplayer(layer_id, name, source, style, epsg)}\n"
        "  </maplayers>\n"
        "</qlr>\n"
    )


def build_qgs(title: str, layers: list, epsg: int) -> str:
    """5主題図＋背景をまとめたプロジェクト本体（.qgs）。

    layers=[(layer_id, 表示名, datasource, styleXML)]。先頭（=24時間交通量図）のみ表示ON。
    """
    srs = srs_xml(epsg, "    ")
    tree = "\n".join(
        tree_layer(lid, name, checked=(i == 0), pad="    ")
        for i, (lid, name, _src, _st) in enumerate(layers))
    tree += "\n" + tree_layer(BASEMAP_ID, BASEMAP_NAME, True, "    ",
                              source=basemap_datasource(), provider_key="wms")
    maplayers = "\n".join(vector_maplayer(lid, name, src, st, epsg)
                          for lid, name, src, st in layers)
    maplayers += "\n" + basemap_maplayer()
    order = "\n".join(f'    <layer id={quoteattr(lid)}/>' for lid, _n, _s, _st in layers)
    order += f'\n    <layer id={quoteattr(BASEMAP_ID)}/>'
    return (
        "<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>\n"
        f'<qgis version="{QGIS_VERSION}" projectname={quoteattr(title)}>\n'
        f'  <title>{escape(title)}</title>\n'
        '  <homePath path=""/>\n'
        f'  <projectCrs>\n{srs}\n  </projectCrs>\n'
        '  <layer-tree-group>\n'
        f'{tree}\n'
        '    <custom-order enabled="0"/>\n'
        '  </layer-tree-group>\n'
        '  <mapcanvas name="theMapCanvas" annotationsVisible="1">\n'
        '    <units>degrees</units>\n'
        f'{extent_xml(DEFAULT_EXTENT, "    ")}\n'
        f'    <destinationsrs>\n{srs}\n    </destinationsrs>\n'
        '  </mapcanvas>\n'
        '  <projectlayers>\n'
        f'{maplayers}\n'
        '  </projectlayers>\n'
        '  <layerorder>\n'
        f'{order}\n'
        '  </layerorder>\n'
        '  <properties>\n'
        '    <Paths>\n'
        '      <Absolute type="bool">false</Absolute>\n'
        '    </Paths>\n'
        # QGISは ProjectionsEnabled が1でないと <projectCrs> を読まない
        # （qgsproject.cpp: readNumEntry("SpatialRefSys","/ProjectionsEnabled",0) が偽なら
        # projectCrs ノードを見にいかない）。これが無いとプロジェクトCRSが「CRSなし」になり、
        # 投影変換ができず EPSG:3857 の背景地図が描かれない。今回まさにこれで踏んだ。
        '    <SpatialRefSys>\n'
        '      <ProjectionsEnabled type="int">1</ProjectionsEnabled>\n'
        '    </SpatialRefSys>\n'
        # 計測用の楕円体。未設定だと QgsProject::ellipsoid() が "NONE" を返し、経緯度のまま
        # 平面計算されて距離・面積が度単位の無意味な値になる。
        '    <Measure>\n'
        f'      <Ellipsoid type="QString">{ellipsoid_authid(epsg)}</Ellipsoid>\n'
        '    </Measure>\n'
        '    <Measurement>\n'
        '      <AreaUnits type="QString">m2</AreaUnits>\n'
        '      <DistanceUnits type="QString">meters</DistanceUnits>\n'
        '    </Measurement>\n'
        '    <CopyrightLabel>\n'
        '      <Enabled type="bool">true</Enabled>\n'
        f'      <Label type="QString">{escape(ATTRIBUTION)}</Label>\n'
        '      <Placement type="int">3</Placement>\n'
        '      <MarginH type="int">2</MarginH>\n'
        '      <MarginV type="int">2</MarginV>\n'
        '      <FontName type="QString">Sans Serif</FontName>\n'
        '      <FontSize type="int">9</FontSize>\n'
        '      <Color type="QString">#000000</Color>\n'
        '    </CopyrightLabel>\n'
        '  </properties>\n'
        f'  <projectMetadata>\n    <title>{escape(title)}</title>\n'
        f'    <abstract>{escape(ATTRIBUTION)}</abstract>\n    <links/>\n  </projectMetadata>\n'
        '</qgis>\n'
    )


def zip_one(name: str, data: bytes) -> bytes:
    """1ファイルだけを含むZIP（.qgz は .qgs を1つ含むZIP）。日時は固定。"""
    import io

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        info = zipfile.ZipInfo(name, date_time=ZIP_EPOCH)
        info.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(info, data)
    return buf.getvalue()


def build_all() -> dict:
    """bundle/ に置くファイル名 -> バイト列。"""
    out = {}
    for year, ycfg in YEARS.items():
        meta = YEAR_META[year]
        pre = ycfg["prefix"]
        epsg = meta["epsg"]
        qmls = build_year(ycfg)
        # layername は付けない（Parquetのレイヤ名はファイル基底名。付けると取り違えの元）
        source = f"./{pre}_converted.parquet"

        # 1) サイドカーQML: parquetと同名にするとQGISが自動適用する既定スタイル
        out[f"{pre}_converted.qml"] = qmls[f"{pre}_{DEFAULT_THEME}.qml"].encode("utf-8")

        # 2) テーマごとの QLR
        layers = []
        for key, label in THEMES:
            style = style_body(qmls[f"{pre}_{key}.qml"])
            name = f'{meta["era"]} {label}'
            layer_id = f"{pre}_{key}"
            out[f"{pre}_{key}.qlr"] = build_qlr(
                layer_id, name, source, style, epsg).encode("utf-8")
            layers.append((layer_id, name, source, style))

        # 3) 5主題図まとめのプロジェクト
        title = f'道路交通センサス {meta["era"]}（{meta["wareki"]}）主題図'
        out[f"{pre}.qgz"] = zip_one(f"{pre}.qgs", build_qgs(title, layers, epsg).encode("utf-8"))
    return out


README_TXT = """道路交通センサス GeoParquet — QGIS スタイル同梱物（{era} / {wareki}）

■ 置き場所（重要）
  この中のファイルは {parquet} と「同じフォルダ」に展開してください。
  .qgz / .qlr はデータソースを相対パスで持つため、別フォルダだとレイヤが見つかりません。

■ 使い方（3通り。お好みで）
  1) {prefix}.qgz をダブルクリック
     → 5主題図＋地理院淡色の背景がセットで開きます。レイヤのチェックで主題図を切り替え。
  2) {prefix}_N_*.qlr を QGIS にドラッグ&ドロップ
     → その主題図1つが、スタイル適用済みのレイヤとして追加されます。
  3) {parquet} をそのままドラッグ&ドロップ
     → 同じフォルダに {basename}.qml があれば、24時間交通量図が自動で適用されます。
        別の主題図にするには レイヤのプロパティ → シンボロジ → 「スタイル ▾」→「スタイルを読み込む」
        から {prefix}_N_*.qml を選択してください。

■ 収録する主題図（5種）
  1 24時間交通量（全車上下計）  色=道路種別 / 線幅=交通量6段階
  2 混雑度                      <1.0 / 1.0-1.25 / 1.25-1.75 / >=1.75
  3 大型車混入率（％）          <10 / 10-15 / 15-20 / >=20
  4 混雑時旅行速度              min(上り,下り) を <10 ... >=50 の6段階
  5 昼間非混雑時旅行速度        同上（非混雑時速度）

■ 座標系
  データ: EPSG:{epsg}（元データのまま）。背景の地理院タイルは EPSG:3857。
  プロジェクトは EPSG:{epsg} で開き、背景地図はQGISがオンザフライ変換して重ねます。

■ 動作条件
  GeoParquet の読み込みには GDAL の Parquet ドライバが必要です（QGIS 3.28 以降を推奨）。
  QGIS の「ヘルプ → QGISについて」で GDAL のバージョンを確認できます。
  ブラウザパネルに .parquet が現れない場合は、Parquet ドライバを含むビルドを使ってください。

■ 出典
  データ: 国土交通省 道路交通センサス（{wareki}）
  背景地図: 地理院タイル（淡色地図） https://maps.gsi.go.jp/development/ichiran.html

■ 再生成
  python configs/qgis_styles/generate_qml.py           # 主題図QML
  python configs/qgis_styles/generate_qgis_bundle.py   # 本同梱物（QML/QLR/QGZ）
  https://github.com/shiwaku/mlit-road-traffic-census-converter
"""


def pack(dest_dir: str, files: dict) -> None:
    """年度ごとに リリース添付用ZIP を作る（qgz + qlr + 主題図qml + README）。"""
    os.makedirs(dest_dir, exist_ok=True)
    for year, ycfg in YEARS.items():
        meta = YEAR_META[year]
        pre = ycfg["prefix"]
        zip_path = os.path.join(dest_dir, f"{pre}_qgis.zip")
        with zipfile.ZipFile(zip_path, "w") as z:
            def add(name: str, data: bytes) -> None:
                info = zipfile.ZipInfo(name, date_time=ZIP_EPOCH)
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, data)

            add("README.txt", README_TXT.format(
                era=meta["era"], wareki=meta["wareki"], prefix=pre, epsg=meta["epsg"],
                parquet=f"{pre}_converted.parquet",
                basename=f"{pre}_converted").encode("utf-8"))
            for name, data in sorted(files.items()):
                if name.startswith(pre):
                    add(name, data)
            for key, _label in THEMES:  # 主題図QML（手動読み込み用）
                qml = f"{pre}_{key}.qml"
                with open(os.path.join(OUT_DIR, qml), "rb") as f:
                    add(qml, f.read())
        with zipfile.ZipFile(zip_path) as z:
            print(f"パック: {zip_path} ({os.path.getsize(zip_path):,} bytes / "
                  f"{len(z.namelist())} files)")


def main():
    ap = argparse.ArgumentParser(description="QGIS同梱物（QML/QLR/QGZ）を生成する")
    ap.add_argument("--install-to-data", action="store_true",
                    help="data/<year>/output/ が存在すればそこにも配置する（ローカル確認用）")
    ap.add_argument("--pack", metavar="DIR",
                    help="リリース添付用の <prefix>_qgis.zip を DIR に作る")
    args = ap.parse_args()

    os.makedirs(BUNDLE_DIR, exist_ok=True)
    files = build_all()
    for name, data in sorted(files.items()):
        with open(os.path.join(BUNDLE_DIR, name), "wb") as f:
            f.write(data)
        print(f"生成: bundle/{name} ({len(data):,} bytes)")

    if args.install_to_data:
        for year, ycfg in YEARS.items():
            dest = os.path.join(REPO_ROOT, "data", year, "output")
            if not os.path.isdir(dest):
                print(f"skip: {dest} が無い（先に run.py で出力してください）")
                continue
            for name in sorted(files):
                if name.startswith(ycfg["prefix"]):
                    shutil.copy2(os.path.join(BUNDLE_DIR, name), os.path.join(dest, name))
                    print(f"配置: data/{year}/output/{name}")

    if args.pack:
        pack(args.pack, files)


if __name__ == "__main__":
    main()
