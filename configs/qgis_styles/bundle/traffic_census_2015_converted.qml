<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.34.0" styleCategories="Symbology">
  <renderer-v2 type="RuleRenderer" symbollevels="1" enableorderby="0" forceraster="0" referencescale="-1">
    <rules key="{root}">
      <rule key="{g0}" filter="&quot;道路種別&quot; = &#x27;1：高速自動車国道&#x27;" label="高速自動車国道">
        <rule key="{r0_0}" symbol="0" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 5000" label="〜5千台"/>
        <rule key="{r0_1}" symbol="1" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 5000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 10000" label="5千〜1万台"/>
        <rule key="{r0_2}" symbol="2" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 10000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 20000" label="1万〜2万台"/>
        <rule key="{r0_3}" symbol="3" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 20000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 40000" label="2万〜4万台"/>
        <rule key="{r0_4}" symbol="4" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 40000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 80000" label="4万〜8万台"/>
        <rule key="{r0_5}" symbol="5" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 80000" label="8万台〜"/>
      </rule>
      <rule key="{g1}" filter="&quot;道路種別&quot; = &#x27;2：都市高速道路&#x27;" label="都市高速道路">
        <rule key="{r1_6}" symbol="6" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 5000" label="〜5千台"/>
        <rule key="{r1_7}" symbol="7" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 5000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 10000" label="5千〜1万台"/>
        <rule key="{r1_8}" symbol="8" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 10000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 20000" label="1万〜2万台"/>
        <rule key="{r1_9}" symbol="9" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 20000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 40000" label="2万〜4万台"/>
        <rule key="{r1_10}" symbol="10" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 40000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 80000" label="4万〜8万台"/>
        <rule key="{r1_11}" symbol="11" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 80000" label="8万台〜"/>
      </rule>
      <rule key="{g2}" filter="&quot;道路種別&quot; = &#x27;3：一般国道&#x27; AND &quot;管理区分&quot; = &#x27;1：国土交通大臣&#x27;" label="一般国道（直轄）">
        <rule key="{r2_12}" symbol="12" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 5000" label="〜5千台"/>
        <rule key="{r2_13}" symbol="13" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 5000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 10000" label="5千〜1万台"/>
        <rule key="{r2_14}" symbol="14" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 10000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 20000" label="1万〜2万台"/>
        <rule key="{r2_15}" symbol="15" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 20000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 40000" label="2万〜4万台"/>
        <rule key="{r2_16}" symbol="16" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 40000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 80000" label="4万〜8万台"/>
        <rule key="{r2_17}" symbol="17" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 80000" label="8万台〜"/>
      </rule>
      <rule key="{g3}" filter="&quot;道路種別&quot; = &#x27;3：一般国道&#x27; AND &quot;管理区分&quot; &lt;&gt; &#x27;1：国土交通大臣&#x27;" label="一般国道（直轄外）">
        <rule key="{r3_18}" symbol="18" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 5000" label="〜5千台"/>
        <rule key="{r3_19}" symbol="19" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 5000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 10000" label="5千〜1万台"/>
        <rule key="{r3_20}" symbol="20" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 10000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 20000" label="1万〜2万台"/>
        <rule key="{r3_21}" symbol="21" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 20000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 40000" label="2万〜4万台"/>
        <rule key="{r3_22}" symbol="22" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 40000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 80000" label="4万〜8万台"/>
        <rule key="{r3_23}" symbol="23" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 80000" label="8万台〜"/>
      </rule>
      <rule key="{g4}" filter="&quot;道路種別&quot; IN (&#x27;4：主要地方道（都道府県道）&#x27;,&#x27;5：主要地方道（指定市市道）&#x27;)" label="主要地方道">
        <rule key="{r4_24}" symbol="24" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 5000" label="〜5千台"/>
        <rule key="{r4_25}" symbol="25" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 5000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 10000" label="5千〜1万台"/>
        <rule key="{r4_26}" symbol="26" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 10000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 20000" label="1万〜2万台"/>
        <rule key="{r4_27}" symbol="27" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 20000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 40000" label="2万〜4万台"/>
        <rule key="{r4_28}" symbol="28" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 40000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 80000" label="4万〜8万台"/>
        <rule key="{r4_29}" symbol="29" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 80000" label="8万台〜"/>
      </rule>
      <rule key="{g5}" filter="&quot;道路種別&quot; IN (&#x27;6：一般都道府県道&#x27;,&#x27;7：指定市の一般市道&#x27;)" label="一般都道府県道・市道">
        <rule key="{r5_30}" symbol="30" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 5000" label="〜5千台"/>
        <rule key="{r5_31}" symbol="31" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 5000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 10000" label="5千〜1万台"/>
        <rule key="{r5_32}" symbol="32" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 10000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 20000" label="1万〜2万台"/>
        <rule key="{r5_33}" symbol="33" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 20000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 40000" label="2万〜4万台"/>
        <rule key="{r5_34}" symbol="34" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 40000 AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 80000" label="4万〜8万台"/>
        <rule key="{r5_35}" symbol="35" filter="&quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &gt;= 80000" label="8万台〜"/>
      </rule>
    </rules>
    <symbols>
      <symbol name="0" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="5">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="0,0,255,255,rgb:0.000000,0.000000,1.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.3"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="1" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="5">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="0,0,255,255,rgb:0.000000,0.000000,1.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.6"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="2" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="5">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="0,0,255,255,rgb:0.000000,0.000000,1.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="1.2"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="3" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="5">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="0,0,255,255,rgb:0.000000,0.000000,1.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="2.4"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="4" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="5">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="0,0,255,255,rgb:0.000000,0.000000,1.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="3.6"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="5" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="5">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="0,0,255,255,rgb:0.000000,0.000000,1.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="4.8"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="6" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="4">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="0,0,119,255,rgb:0.000000,0.000000,0.466667,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.3"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="7" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="4">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="0,0,119,255,rgb:0.000000,0.000000,0.466667,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.6"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="8" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="4">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="0,0,119,255,rgb:0.000000,0.000000,0.466667,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="1.2"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="9" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="4">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="0,0,119,255,rgb:0.000000,0.000000,0.466667,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="2.4"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="10" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="4">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="0,0,119,255,rgb:0.000000,0.000000,0.466667,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="3.6"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="11" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="4">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="0,0,119,255,rgb:0.000000,0.000000,0.466667,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="4.8"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="12" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="3">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="255,7,7,255,rgb:1.000000,0.027451,0.027451,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.3"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="13" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="3">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="255,7,7,255,rgb:1.000000,0.027451,0.027451,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.6"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="14" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="3">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="255,7,7,255,rgb:1.000000,0.027451,0.027451,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="1.2"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="15" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="3">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="255,7,7,255,rgb:1.000000,0.027451,0.027451,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="2.4"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="16" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="3">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="255,7,7,255,rgb:1.000000,0.027451,0.027451,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="3.6"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="17" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="3">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="255,7,7,255,rgb:1.000000,0.027451,0.027451,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="4.8"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="18" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="2">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="255,0,255,255,rgb:1.000000,0.000000,1.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.3"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="19" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="2">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="255,0,255,255,rgb:1.000000,0.000000,1.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.6"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="20" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="2">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="255,0,255,255,rgb:1.000000,0.000000,1.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="1.2"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="21" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="2">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="255,0,255,255,rgb:1.000000,0.000000,1.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="2.4"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="22" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="2">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="255,0,255,255,rgb:1.000000,0.000000,1.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="3.6"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="23" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="2">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="255,0,255,255,rgb:1.000000,0.000000,1.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="4.8"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="24" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="1">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="0,116,0,255,rgb:0.000000,0.454902,0.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.3"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="25" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="1">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="0,116,0,255,rgb:0.000000,0.454902,0.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.6"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="26" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="1">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="0,116,0,255,rgb:0.000000,0.454902,0.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="1.2"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="27" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="1">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="0,116,0,255,rgb:0.000000,0.454902,0.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="2.4"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="28" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="1">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="0,116,0,255,rgb:0.000000,0.454902,0.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="3.6"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="29" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
        <layer class="SimpleLine" enabled="1" locked="0" pass="1">
          <Option type="Map">
            <Option name="align_dash_pattern" type="QString" value="0"/>
            <Option name="capstyle" type="QString" value="round"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="customdash_unit" type="QString" value="MM"/>
            <Option name="dash_pattern_offset" type="QString" value="0"/>
            <Option name="dash_pattern_offset_unit" type="QString" value="MM"/>
            <Option name="draw_inside_polygon" type="QString" value="0"/>
            <Option name="joinstyle" type="QString" value="round"/>
            <Option name="line_color" type="QString" value="0,116,0,255,rgb:0.000000,0.454902,0.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="4.8"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="30" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
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
            <Option name="line_color" type="QString" value="116,0,0,255,rgb:0.454902,0.000000,0.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.3"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="31" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
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
            <Option name="line_color" type="QString" value="116,0,0,255,rgb:0.454902,0.000000,0.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.6"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="32" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
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
            <Option name="line_color" type="QString" value="116,0,0,255,rgb:0.454902,0.000000,0.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="1.2"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="33" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
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
            <Option name="line_color" type="QString" value="116,0,0,255,rgb:0.454902,0.000000,0.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="2.4"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="34" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
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
            <Option name="line_color" type="QString" value="116,0,0,255,rgb:0.454902,0.000000,0.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="3.6"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="35" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
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
            <Option name="line_color" type="QString" value="116,0,0,255,rgb:0.454902,0.000000,0.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="4.8"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <layerGeometryType>1</layerGeometryType>
</qgis>
