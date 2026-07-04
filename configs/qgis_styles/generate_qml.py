# -*- coding: utf-8 -*-
"""road-traffic-census-map-2021 ビューワの5主題図に対応する QGIS QML(スタイル)を生成する。

対象レイヤ: GeoParquet（R03: traffic_census_2021_converted.parquet）
出力: 各主題図ごとに .qml を1ファイル生成（QGIS 3.x）。
  Layer Properties → Symbology → Load Style で読み込む。
"""
import html
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
QGIS_VERSION = "3.34.0"

# フィールド名
F_ROADTYPE = "道路種別"
F_KANRI = "管理区分"
F_24H = "２４時間自動車類交通量（上下合計）／合計（台）"
F_KONZATSUDO = "混雑度"
F_OGATA = "昼間１２時間大型車混入率（％）"
F_KZ_UP = "朝夕（混雑時）／上り／旅行速度／合計（ｋｍ／ｈ）"
F_KZ_DN = "朝夕（混雑時）／下り／旅行速度／合計（ｋｍ／ｈ）"
F_HK_UP = "昼間（非混雑時）／上り／旅行速度／合計（ｋｍ／ｈ）"
F_HK_DN = "昼間（非混雑時）／下り／旅行速度／合計（ｋｍ／ｈ）"


def esc(s: str) -> str:
    """XML属性値エスケープ。"""
    return html.escape(str(s), quote=True)


def qcolor(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f"{r},{g},{b},255,rgb:{r/255:.6f},{g/255:.6f},{b/255:.6f},1"


def line_symbol(name: str, rgb: tuple[int, int, int], width_mm: float,
                width_expr: str | None = None) -> str:
    """SimpleLine シンボル1個のXML。width_expr指定時はデータ定義で線幅を上書き。"""
    dd = ""
    if width_expr:
        dd = f"""
        <data_defined_properties>
          <Option type="Map">
            <Option name="properties" type="Map">
              <Option name="line_width" type="Map">
                <Option name="active" type="bool" value="true"/>
                <Option name="expression" type="QString" value="{esc(width_expr)}"/>
                <Option name="type" type="int" value="3"/>
              </Option>
            </Option>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>"""
    return f"""      <symbol name="{name}" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="0">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="{qcolor(rgb)}"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="{width_mm}"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>{dd}
        </layer>
      </symbol>"""


def graduated_qml(attr: str, ranges: list[tuple[float, float, tuple[int, int, int], str]],
                  width_mm: float = 0.66) -> str:
    """graduatedSymbol レンダラのQML。ranges=[(lower,upper,rgb,label)]。"""
    range_xml = "\n".join(
        f'      <range lower="{lo:.6f}" upper="{hi:.6f}" render="true" symbol="{i}" label="{esc(lab)}"/>'
        for i, (lo, hi, _rgb, lab) in enumerate(ranges))
    sym_xml = "\n".join(line_symbol(str(i), rgb, width_mm)
                        for i, (_lo, _hi, rgb, _lab) in enumerate(ranges))
    src_sym = line_symbol("0", ranges[0][2], width_mm)
    return f"""<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="{QGIS_VERSION}" styleCategories="Symbology">
  <renderer-v2 type="graduatedSymbol" attr="{esc(attr)}" graduatedMethod="GraduatedColor" symbollevels="0" enableorderby="0" forceraster="0" referencescale="-1">
    <ranges>
{range_xml}
    </ranges>
    <symbols>
{sym_xml}
    </symbols>
    <source-symbol>
{src_sym}
    </source-symbol>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <layerGeometryType>1</layerGeometryType>
</qgis>
"""


def rule_qml(rules: list[tuple[str, tuple[int, int, int], str]], width_expr: str) -> str:
    """RuleRenderer のQML。rules=[(filter, rgb, label)]、線幅はwidth_exprでデータ定義。"""
    rule_xml = "\n".join(
        f'      <rule symbol="{i}" filter="{esc(filt)}" label="{esc(lab)}"/>'
        for i, (filt, _rgb, lab) in enumerate(rules))
    sym_xml = "\n".join(line_symbol(str(i), rgb, 0.66, width_expr=width_expr)
                        for i, (_filt, rgb, _lab) in enumerate(rules))
    return f"""<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="{QGIS_VERSION}" styleCategories="Symbology">
  <renderer-v2 type="RuleRenderer" symbollevels="0" enableorderby="0" forceraster="0" referencescale="-1">
    <rules key="{{root}}">
{rule_xml}
    </rules>
    <symbols>
{sym_xml}
    </symbols>
  </renderer-v2>
  <layerGeometryType>1</layerGeometryType>
</qgis>
"""


# 色定義
GREEN = (0, 152, 0)
YELLOW = (255, 210, 0)
ORANGE = (255, 127, 0)
RED = (255, 0, 0)
LBLUE = (0, 191, 255)
BLUE = (0, 63, 255)
BIG = 999999.0

# 速度テーマの共通区分（min(上り,下り)）
SPEED_RANGES = lambda: [
    (0.0, 10.0, RED, "0 – 10 km/h"),
    (10.0, 20.0, ORANGE, "10 – 20 km/h"),
    (20.0, 30.0, YELLOW, "20 – 30 km/h"),
    (30.0, 40.0, GREEN, "30 – 40 km/h"),
    (40.0, 50.0, LBLUE, "40 – 50 km/h"),
    (50.0, BIG, BLUE, "50 km/h 以上"),
]


def q(f):  # 式内のフィールド参照
    return f'"{f}"'


def speed_attr(up, dn):
    return f'least(coalesce({q(up)}, {BIG}), coalesce({q(dn)}, {BIG}))'


def main():
    files = {}

    # 1) 24時間交通量: 色=道路種別 / 線幅=交通量6段階
    width_expr = (
        f'CASE '
        f'WHEN {q(F_24H)} < 5000 THEN 0.3 '
        f'WHEN {q(F_24H)} < 10000 THEN 0.6 '
        f'WHEN {q(F_24H)} < 20000 THEN 1.2 '
        f'WHEN {q(F_24H)} < 40000 THEN 2.4 '
        f'WHEN {q(F_24H)} < 80000 THEN 3.6 '
        f'ELSE 4.8 END'
    )
    nn = f'{q(F_24H)} IS NOT NULL'
    rules = [
        (f'{q(F_ROADTYPE)} = \'3：一般国道\' AND {q(F_KANRI)} <> \'1：国土交通大臣\' AND {nn}',
         (255, 0, 255), '一般国道（直轄外）'),
        (f'{q(F_ROADTYPE)} = \'3：一般国道\' AND {q(F_KANRI)} = \'1：国土交通大臣\' AND {nn}',
         (255, 7, 7), '一般国道（直轄）'),
        (f'{q(F_ROADTYPE)} = \'1：高速自動車国道\' AND {nn}', (0, 0, 255), '高速自動車国道'),
        (f'{q(F_ROADTYPE)} = \'2：都市高速道路\' AND {nn}', (0, 0, 119), '都市高速道路'),
        (f'{q(F_ROADTYPE)} IN (\'4：主要地方道（都道府県道）\',\'5：主要地方道（指定市市道）\') AND {nn}',
         (0, 116, 0), '主要地方道'),
        (f'{q(F_ROADTYPE)} IN (\'6：一般都道府県道\',\'7：指定市の一般市道\') AND {nn}',
         (116, 0, 0), '一般都道府県道・市道'),
    ]
    files["traffic_census_2021_1_24jikankotsuryo.qml"] = rule_qml(rules, width_expr)

    # 2) 混雑度（フィールド分類）
    files["traffic_census_2021_2_konzatsudo.qml"] = graduated_qml(F_KONZATSUDO, [
        (0.0, 1.0, GREEN, "0 – 1.0"),
        (1.0, 1.25, YELLOW, "1.0 – 1.25"),
        (1.25, 1.75, ORANGE, "1.25 – 1.75"),
        (1.75, BIG, RED, "1.75 以上"),
    ])

    # 3) 大型車混入率（フィールド分類）
    files["traffic_census_2021_3_ogatashakonnyuritsu.qml"] = graduated_qml(F_OGATA, [
        (0.0, 10.0, GREEN, "0 – 10 %"),
        (10.0, 15.0, YELLOW, "10 – 15 %"),
        (15.0, 20.0, ORANGE, "15 – 20 %"),
        (20.0, BIG, RED, "20 % 以上"),
    ])

    # 4) 混雑時旅行速度
    files["traffic_census_2021_4_konzatsuji.qml"] = graduated_qml(
        speed_attr(F_KZ_UP, F_KZ_DN), SPEED_RANGES())

    # 5) 昼間非混雑時旅行速度
    files["traffic_census_2021_5_hikonzatsuji.qml"] = graduated_qml(
        speed_attr(F_HK_UP, F_HK_DN), SPEED_RANGES())

    for name, content in files.items():
        path = os.path.join(OUT_DIR, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("生成:", name)


if __name__ == "__main__":
    main()
