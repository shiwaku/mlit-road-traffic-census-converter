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
                width_expr: str | None = None, level: int = 0) -> str:
    """SimpleLine シンボル1個のXML。width_expr指定時はデータ定義で線幅を上書き。
    level は symbol levels 有効時の描画順（pass）。大きいほど後＝前面に描画される。"""
    dd = ""
    if width_expr:
        dd = f"""
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
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
        <layer class="SimpleLine" enabled="1" locked="0" pass="{level}">
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


def rule_qml_nested(groups: list[tuple[str, str, tuple[int, int, int]]],
                    bins: list[tuple[str, str, float]]) -> str:
    """入れ子RuleRenderer。groups=[(親ラベル, 親filter=色分類, rgb)]、
    bins=[(子ラベル, 子filter=幅分類, width_mm)]。各葉に静的な色・幅のシンボルを割当てる
    （データ定義に依存せず確実に線幅が変わる）。色=親グループ / 幅=子ビン。"""
    rules_xml, syms_xml = [], []
    idx = 0
    ng = len(groups)
    for gi, (glab, gfilt, rgb) in enumerate(groups):
        # symbol levels: 道路種別クラスが高いグループ(=groups先頭)ほど level を大きくし前面に描画。
        # groups は高位クラス順(高速→…→市道)に並べる前提。level = ng-1-gi。
        level = ng - 1 - gi
        child_xml = []
        for bi, (blab, bfilt, wmm) in enumerate(bins):
            child_xml.append(
                f'        <rule key="{{r{gi}_{idx}}}" symbol="{idx}" '
                f'filter="{esc(bfilt)}" label="{esc(blab)}"/>')
            syms_xml.append(line_symbol(str(idx), rgb, wmm, level=level))
            idx += 1
        rules_xml.append(
            f'      <rule key="{{g{gi}}}" filter="{esc(gfilt)}" label="{esc(glab)}">\n'
            + "\n".join(child_xml) + "\n      </rule>")
    return f"""<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="{QGIS_VERSION}" styleCategories="Symbology">
  <renderer-v2 type="RuleRenderer" symbollevels="1" enableorderby="0" forceraster="0" referencescale="-1">
    <rules key="{{root}}">
{chr(10).join(rules_xml)}
    </rules>
    <symbols>
{chr(10).join(syms_xml)}
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
    # QGISの式関数は min()/max()（least()/greatest() は存在せず「式が不正です」になる）
    return f'min(coalesce({q(up)}, {BIG}), coalesce({q(dn)}, {BIG}))'


def main():
    files = {}

    # 1) 24時間交通量: 色=道路種別（親ルール） / 線幅=交通量6段階（子ルール・静的幅）
    #    ※ data-defined 線幅はQGISの Load Style で適用されないため、幅は静的値を持つ
    #      入れ子ルールで表現する（色×幅=6×6のシンボル）。
    V = q(F_24H)
    road_groups = [
        ('高速自動車国道', f"{q(F_ROADTYPE)} = '1：高速自動車国道'", (0, 0, 255)),
        ('都市高速道路', f"{q(F_ROADTYPE)} = '2：都市高速道路'", (0, 0, 119)),
        ('一般国道（直轄）', f"{q(F_ROADTYPE)} = '3：一般国道' AND {q(F_KANRI)} = '1：国土交通大臣'",
         (255, 7, 7)),
        ('一般国道（直轄外）', f"{q(F_ROADTYPE)} = '3：一般国道' AND {q(F_KANRI)} <> '1：国土交通大臣'",
         (255, 0, 255)),
        ('主要地方道', f"{q(F_ROADTYPE)} IN ('4：主要地方道（都道府県道）','5：主要地方道（指定市市道）')",
         (0, 116, 0)),
        ('一般都道府県道・市道', f"{q(F_ROADTYPE)} IN ('6：一般都道府県道','7：指定市の一般市道')",
         (116, 0, 0)),
    ]
    vol_bins = [
        ('〜5千台', f"{V} < 5000", 0.3),
        ('5千〜1万台', f"{V} >= 5000 AND {V} < 10000", 0.6),
        ('1万〜2万台', f"{V} >= 10000 AND {V} < 20000", 1.2),
        ('2万〜4万台', f"{V} >= 20000 AND {V} < 40000", 2.4),
        ('4万〜8万台', f"{V} >= 40000 AND {V} < 80000", 3.6),
        ('8万台〜', f"{V} >= 80000", 4.8),
    ]
    files["traffic_census_2021_1_24jikankotsuryo.qml"] = rule_qml_nested(road_groups, vol_bins)

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
