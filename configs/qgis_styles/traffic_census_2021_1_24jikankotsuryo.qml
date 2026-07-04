<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.34.0" styleCategories="Symbology">
  <renderer-v2 type="RuleRenderer" symbollevels="0" enableorderby="0" forceraster="0" referencescale="-1">
    <rules key="{root}">
      <rule symbol="0" filter="&quot;道路種別&quot; = &#x27;3：一般国道&#x27; AND &quot;管理区分&quot; &lt;&gt; &#x27;1：国土交通大臣&#x27; AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; IS NOT NULL" label="一般国道（直轄外）"/>
      <rule symbol="1" filter="&quot;道路種別&quot; = &#x27;3：一般国道&#x27; AND &quot;管理区分&quot; = &#x27;1：国土交通大臣&#x27; AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; IS NOT NULL" label="一般国道（直轄）"/>
      <rule symbol="2" filter="&quot;道路種別&quot; = &#x27;1：高速自動車国道&#x27; AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; IS NOT NULL" label="高速自動車国道"/>
      <rule symbol="3" filter="&quot;道路種別&quot; = &#x27;2：都市高速道路&#x27; AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; IS NOT NULL" label="都市高速道路"/>
      <rule symbol="4" filter="&quot;道路種別&quot; IN (&#x27;4：主要地方道（都道府県道）&#x27;,&#x27;5：主要地方道（指定市市道）&#x27;) AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; IS NOT NULL" label="主要地方道"/>
      <rule symbol="5" filter="&quot;道路種別&quot; IN (&#x27;6：一般都道府県道&#x27;,&#x27;7：指定市の一般市道&#x27;) AND &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; IS NOT NULL" label="一般都道府県道・市道"/>
    </rules>
    <symbols>
      <symbol name="0" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
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
            <Option name="line_color" type="QString" value="255,0,255,255,rgb:1.000000,0.000000,1.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.66"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        <data_defined_properties>
          <Option type="Map">
            <Option name="properties" type="Map">
              <Option name="line_width" type="Map">
                <Option name="active" type="bool" value="true"/>
                <Option name="expression" type="QString" value="CASE WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 5000 THEN 0.3 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 10000 THEN 0.6 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 20000 THEN 1.2 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 40000 THEN 2.4 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 80000 THEN 3.6 ELSE 4.8 END"/>
                <Option name="type" type="int" value="3"/>
              </Option>
            </Option>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="1" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
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
            <Option name="line_color" type="QString" value="255,7,7,255,rgb:1.000000,0.027451,0.027451,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.66"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        <data_defined_properties>
          <Option type="Map">
            <Option name="properties" type="Map">
              <Option name="line_width" type="Map">
                <Option name="active" type="bool" value="true"/>
                <Option name="expression" type="QString" value="CASE WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 5000 THEN 0.3 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 10000 THEN 0.6 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 20000 THEN 1.2 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 40000 THEN 2.4 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 80000 THEN 3.6 ELSE 4.8 END"/>
                <Option name="type" type="int" value="3"/>
              </Option>
            </Option>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="2" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
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
            <Option name="line_color" type="QString" value="0,0,255,255,rgb:0.000000,0.000000,1.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.66"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        <data_defined_properties>
          <Option type="Map">
            <Option name="properties" type="Map">
              <Option name="line_width" type="Map">
                <Option name="active" type="bool" value="true"/>
                <Option name="expression" type="QString" value="CASE WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 5000 THEN 0.3 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 10000 THEN 0.6 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 20000 THEN 1.2 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 40000 THEN 2.4 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 80000 THEN 3.6 ELSE 4.8 END"/>
                <Option name="type" type="int" value="3"/>
              </Option>
            </Option>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="3" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
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
            <Option name="line_color" type="QString" value="0,0,119,255,rgb:0.000000,0.000000,0.466667,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.66"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        <data_defined_properties>
          <Option type="Map">
            <Option name="properties" type="Map">
              <Option name="line_width" type="Map">
                <Option name="active" type="bool" value="true"/>
                <Option name="expression" type="QString" value="CASE WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 5000 THEN 0.3 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 10000 THEN 0.6 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 20000 THEN 1.2 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 40000 THEN 2.4 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 80000 THEN 3.6 ELSE 4.8 END"/>
                <Option name="type" type="int" value="3"/>
              </Option>
            </Option>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="4" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
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
            <Option name="line_color" type="QString" value="0,116,0,255,rgb:0.000000,0.454902,0.000000,1"/>
            <Option name="line_style" type="QString" value="solid"/>
            <Option name="line_width" type="QString" value="0.66"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        <data_defined_properties>
          <Option type="Map">
            <Option name="properties" type="Map">
              <Option name="line_width" type="Map">
                <Option name="active" type="bool" value="true"/>
                <Option name="expression" type="QString" value="CASE WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 5000 THEN 0.3 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 10000 THEN 0.6 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 20000 THEN 1.2 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 40000 THEN 2.4 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 80000 THEN 3.6 ELSE 4.8 END"/>
                <Option name="type" type="int" value="3"/>
              </Option>
            </Option>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="5" type="line" alpha="1" clip_to_extent="1" frame_rate="10" force_rhr="0" is_animated="0">
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
            <Option name="line_width" type="QString" value="0.66"/>
            <Option name="line_width_unit" type="QString" value="MM"/>
            <Option name="offset" type="QString" value="0"/>
            <Option name="offset_unit" type="QString" value="MM"/>
            <Option name="ring_filter" type="QString" value="0"/>
            <Option name="trim_distance_end" type="QString" value="0"/>
            <Option name="trim_distance_start" type="QString" value="0"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
            <Option name="width_map_unit_scale" type="QString" value="3x:0,0,0,0,0,0"/>
          </Option>
        <data_defined_properties>
          <Option type="Map">
            <Option name="properties" type="Map">
              <Option name="line_width" type="Map">
                <Option name="active" type="bool" value="true"/>
                <Option name="expression" type="QString" value="CASE WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 5000 THEN 0.3 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 10000 THEN 0.6 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 20000 THEN 1.2 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 40000 THEN 2.4 WHEN &quot;２４時間自動車類交通量（上下合計）／合計（台）&quot; &lt; 80000 THEN 3.6 ELSE 4.8 END"/>
                <Option name="type" type="int" value="3"/>
              </Option>
            </Option>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <layerGeometryType>1</layerGeometryType>
</qgis>
