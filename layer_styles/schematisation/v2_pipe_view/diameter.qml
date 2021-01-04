<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" labelsEnabled="1" simplifyAlgorithm="0" simplifyMaxScale="1" version="3.10.10-A Coruña" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="1e+08" simplifyDrawingTol="1" simplifyDrawingHints="1" maxScale="0" simplifyLocal="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" type="categorizedSymbol" attr="pipe_sewerage_type" symbollevels="0" forceraster="0">
    <categories>
      <category value="0" symbol="0" label="Combined sewer" render="true"/>
      <category value="1" symbol="1" label="Storm drain" render="true"/>
      <category value="2" symbol="2" label="Sanitary sewer" render="true"/>
      <category value="3" symbol="3" label="Transport" render="true"/>
      <category value="" symbol="4" label="Other" render="true"/>
    </categories>
    <symbols>
      <symbol force_rhr="0" type="line" clip_to_extent="1" name="0" alpha="1">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="255,170,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.4" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineStyle">
                  <Option value="false" type="bool" name="active"/>
                  <Option value="1" type="int" name="type"/>
                  <Option value="" type="QString" name="val"/>
                </Option>
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="try(&#xd;&#xa;&#x9;coalesce(&#xd;&#xa;&#x9;&#x9;scale_linear(&#xd;&#xa;&#x9;&#x9;&#x9;case &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape = 1 then (to_real(&quot;def_width&quot;) + to_real(&quot;def_height&quot;))/2.0&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape = 2 then to_real(&quot;def_width&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape = 3 then (to_real(&quot;def_width&quot;) + to_real(&quot;def_width&quot;)*1.5)/2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape in (5,6) then&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(def_width, ' ')))) &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;+&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(def_height, ' '))))&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;) / 2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;end&#xd;&#xa;&#x9;&#x9;&#x9;, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;1, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;3&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;1&#xd;&#xa;&#x9;), &#xd;&#xa;&#x9;1&#xd;&#xa;)" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" clip_to_extent="1" name="1" alpha="1">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="85,170,255,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.4" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineStyle">
                  <Option value="false" type="bool" name="active"/>
                  <Option value="1" type="int" name="type"/>
                  <Option value="" type="QString" name="val"/>
                </Option>
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="try(&#xd;&#xa;&#x9;coalesce(&#xd;&#xa;&#x9;&#x9;scale_linear(&#xd;&#xa;&#x9;&#x9;&#x9;case &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape = 1 then (to_real(&quot;def_width&quot;) + to_real(&quot;def_height&quot;))/2.0&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape = 2 then to_real(&quot;def_width&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape = 3 then (to_real(&quot;def_width&quot;) + to_real(&quot;def_width&quot;)*1.5)/2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape in (5,6) then&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(def_width, ' ')))) &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;+&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(def_height, ' '))))&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;) / 2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;end&#xd;&#xa;&#x9;&#x9;&#x9;, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;1, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;3&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;1&#xd;&#xa;&#x9;), &#xd;&#xa;&#x9;1&#xd;&#xa;)" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" clip_to_extent="1" name="2" alpha="1">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="255,0,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.4" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineStyle">
                  <Option value="false" type="bool" name="active"/>
                  <Option value="1" type="int" name="type"/>
                  <Option value="" type="QString" name="val"/>
                </Option>
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="try(&#xd;&#xa;&#x9;coalesce(&#xd;&#xa;&#x9;&#x9;scale_linear(&#xd;&#xa;&#x9;&#x9;&#x9;case &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape = 1 then (to_real(&quot;def_width&quot;) + to_real(&quot;def_height&quot;))/2.0&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape = 2 then to_real(&quot;def_width&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape = 3 then (to_real(&quot;def_width&quot;) + to_real(&quot;def_width&quot;)*1.5)/2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape in (5,6) then&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(def_width, ' ')))) &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;+&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(def_height, ' '))))&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;) / 2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;end&#xd;&#xa;&#x9;&#x9;&#x9;, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;1, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;3&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;1&#xd;&#xa;&#x9;), &#xd;&#xa;&#x9;1&#xd;&#xa;)" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" clip_to_extent="1" name="3" alpha="1">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="153,153,153,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.4" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineStyle">
                  <Option value="false" type="bool" name="active"/>
                  <Option value="1" type="int" name="type"/>
                  <Option value="" type="QString" name="val"/>
                </Option>
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="try(&#xd;&#xa;&#x9;coalesce(&#xd;&#xa;&#x9;&#x9;scale_linear(&#xd;&#xa;&#x9;&#x9;&#x9;case &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape = 1 then (to_real(&quot;def_width&quot;) + to_real(&quot;def_height&quot;))/2.0&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape = 2 then to_real(&quot;def_width&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape = 3 then (to_real(&quot;def_width&quot;) + to_real(&quot;def_width&quot;)*1.5)/2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape in (5,6) then&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(def_width, ' ')))) &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;+&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(def_height, ' '))))&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;) / 2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;end&#xd;&#xa;&#x9;&#x9;&#x9;, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;1, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;3&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;1&#xd;&#xa;&#x9;), &#xd;&#xa;&#x9;1&#xd;&#xa;)" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" clip_to_extent="1" name="4" alpha="1">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.4" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineStyle">
                  <Option value="false" type="bool" name="active"/>
                  <Option value="1" type="int" name="type"/>
                  <Option value="" type="QString" name="val"/>
                </Option>
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="try(&#xd;&#xa;&#x9;coalesce(&#xd;&#xa;&#x9;&#x9;scale_linear(&#xd;&#xa;&#x9;&#x9;&#x9;case &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape = 1 then (to_real(&quot;def_width&quot;) + to_real(&quot;def_height&quot;))/2.0&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape = 2 then to_real(&quot;def_width&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape = 3 then (to_real(&quot;def_width&quot;) + to_real(&quot;def_width&quot;)*1.5)/2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape in (5,6) then&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(def_width, ' ')))) &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;+&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(def_height, ' '))))&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;) / 2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;end&#xd;&#xa;&#x9;&#x9;&#x9;, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;1, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;3&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;1&#xd;&#xa;&#x9;), &#xd;&#xa;&#x9;1&#xd;&#xa;)" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol force_rhr="0" type="line" clip_to_extent="1" name="0" alpha="1">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="255,170,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.4" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineStyle">
                  <Option value="false" type="bool" name="active"/>
                  <Option value="1" type="int" name="type"/>
                  <Option value="" type="QString" name="val"/>
                </Option>
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="try(&#xd;&#xa;&#x9;coalesce(&#xd;&#xa;&#x9;&#x9;scale_linear(&#xd;&#xa;&#x9;&#x9;&#x9;case &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape = 1 then (to_real(&quot;def_width&quot;) + to_real(&quot;def_height&quot;))/2.0&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape = 2 then to_real(&quot;def_width&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape = 3 then (to_real(&quot;def_width&quot;) + to_real(&quot;def_width&quot;)*1.5)/2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;when def_shape in (5,6) then&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(def_width, ' ')))) &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;+&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(def_height, ' '))))&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;) / 2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;end&#xd;&#xa;&#x9;&#x9;&#x9;, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;1, &#xd;&#xa;&#x9;&#x9;&#x9;0.1, &#xd;&#xa;&#x9;&#x9;&#x9;3&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;1&#xd;&#xa;&#x9;), &#xd;&#xa;&#x9;1&#xd;&#xa;)" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="rule-based">
    <rules key="{f96c9462-acd1-4f75-a1c0-20d60925c082}">
      <rule key="{df0dd273-dca4-4022-8a02-3291064ec155}" description="Crosssection" scalemaxdenom="5000">
        <settings calloutType="simple">
          <text-style fieldName="CASE WHEN def_shape = 1 THEN 'rect '||round(def_width*1000)||'x'||round(def_height*1000) &#xd;&#xa;WHEN def_shape = 2 THEN 'Ø'||round(def_width*1000) &#xd;&#xa;WHEN def_shape = 3 THEN 'egg ' || round(def_width*1000) || '/' || round(def_width*1000*1.5,3) &#xd;&#xa;WHEN def_shape in (5, 6) THEN &#xd;&#xa;&#x9;'tab ' ||&#xd;&#xa;&#x9;round(array_last(array_sort(string_to_array(def_width, ' ')))*1000) ||&#xd;&#xa;&#x9;'/' || &#xd;&#xa;&#x9;round(array_last(array_sort(string_to_array(def_height, ' ')))*1000)&#xd;&#xa;END " multilineHeight="1" fontKerning="1" fontSizeUnit="Point" fontFamily="MS Gothic" fontUnderline="0" fontLetterSpacing="0" fontItalic="0" blendMode="0" namedStyle="Regular" previewBkgrdColor="255,255,255,255" textColor="0,0,0,255" fontWordSpacing="0" isExpression="1" fontWeight="50" fontCapitals="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" useSubstitutions="0" fontSize="7" textOpacity="1" fontStrikeout="0" textOrientation="horizontal">
            <text-buffer bufferSize="0.7" bufferColor="255,255,255,255" bufferJoinStyle="128" bufferOpacity="1" bufferBlendMode="0" bufferNoFill="0" bufferDraw="1" bufferSizeUnits="MM" bufferSizeMapUnitScale="3x:0,0,0,0,0,0"/>
            <background shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiX="0" shapeJoinStyle="64" shapeSizeY="0" shapeBorderColor="128,128,128,255" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeRotationType="0" shapeOffsetY="0" shapeSizeX="0" shapeDraw="0" shapeFillColor="255,255,255,255" shapeBorderWidthUnit="MM" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeType="0" shapeBorderWidth="0" shapeOffsetX="0" shapeSizeUnit="MM" shapeRadiiY="0" shapeType="0" shapeOpacity="1" shapeBlendMode="0" shapeSVGFile="" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetUnit="MM" shapeRadiiUnit="MM" shapeRotation="0">
              <symbol force_rhr="0" type="marker" clip_to_extent="1" name="markerSymbol" alpha="1">
                <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
                  <prop v="0" k="angle"/>
                  <prop v="133,182,111,255" k="color"/>
                  <prop v="1" k="horizontal_anchor_point"/>
                  <prop v="bevel" k="joinstyle"/>
                  <prop v="circle" k="name"/>
                  <prop v="0,0" k="offset"/>
                  <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
                  <prop v="MM" k="offset_unit"/>
                  <prop v="35,35,35,255" k="outline_color"/>
                  <prop v="solid" k="outline_style"/>
                  <prop v="0" k="outline_width"/>
                  <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
                  <prop v="MM" k="outline_width_unit"/>
                  <prop v="diameter" k="scale_method"/>
                  <prop v="2" k="size"/>
                  <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
                  <prop v="MM" k="size_unit"/>
                  <prop v="1" k="vertical_anchor_point"/>
                  <data_defined_properties>
                    <Option type="Map">
                      <Option value="" type="QString" name="name"/>
                      <Option name="properties"/>
                      <Option value="collection" type="QString" name="type"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </background>
            <shadow shadowOffsetGlobal="1" shadowOffsetUnit="MM" shadowRadiusUnit="MM" shadowOffsetAngle="135" shadowRadiusAlphaOnly="0" shadowUnder="0" shadowRadius="1.5" shadowScale="100" shadowOffsetDist="1" shadowBlendMode="6" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.7" shadowColor="0,0,0,255" shadowDraw="0"/>
            <dd_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format wrapChar="" leftDirectionSymbol="&lt;" multilineAlign="0" formatNumbers="0" autoWrapLength="0" plussign="0" addDirectionSymbol="0" rightDirectionSymbol=">" reverseDirectionSymbol="0" placeDirectionSymbol="0" useMaxLineLengthForAutoWrap="1" decimals="3"/>
          <placement placement="2" repeatDistanceUnits="MM" distUnits="MM" maxCurvedCharAngleOut="-25" maxCurvedCharAngleIn="25" offsetType="0" centroidInside="0" overrunDistance="0" quadOffset="4" geometryGeneratorType="PointGeometry" repeatDistance="0" layerType="LineGeometry" yOffset="0" geometryGenerator="" fitInPolygonOnly="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" preserveRotation="1" xOffset="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" distMapUnitScale="3x:0,0,0,0,0,0" priority="5" rotationAngle="0" centroidWhole="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" overrunDistanceUnit="MM" geometryGeneratorEnabled="0" dist="0" offsetUnits="MapUnit" placementFlags="9"/>
          <rendering obstacle="1" upsidedownLabels="0" displayAll="0" scaleMin="1" scaleVisibility="0" limitNumLabels="0" scaleMax="10000000" fontMinPixelSize="3" drawLabels="1" maxNumLabels="2000" fontLimitPixelSize="0" minFeatureSize="0" labelPerPart="0" obstacleFactor="1" mergeLines="0" obstacleType="0" fontMaxPixelSize="10000" zIndex="0"/>
          <dd_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="Color">
                  <Option value="false" type="bool" name="active"/>
                  <Option value="case &#xd;&#xa;when &quot;pipe_sewerage_type&quot; = 0 then '#ffaa00'&#xd;&#xa;when &quot;pipe_sewerage_type&quot; = 0 then '#55aaff'&#xd;&#xa;when &quot;pipe_sewerage_type&quot; = 0 then '#ff0000'&#xd;&#xa;when &quot;pipe_sewerage_type&quot; = 0 then '#999999'&#xd;&#xa;else '#000000'&#xd;&#xa;end" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option value="pole_of_inaccessibility" type="QString" name="anchorPoint"/>
              <Option type="Map" name="ddProperties">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
              <Option value="false" type="bool" name="drawToAllParts"/>
              <Option value="0" type="QString" name="enabled"/>
              <Option value="&lt;symbol force_rhr=&quot;0&quot; type=&quot;line&quot; clip_to_extent=&quot;1&quot; name=&quot;symbol&quot; alpha=&quot;1&quot;>&lt;layer enabled=&quot;1&quot; class=&quot;SimpleLine&quot; locked=&quot;0&quot; pass=&quot;0&quot;>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; type=&quot;QString&quot; name=&quot;name&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; type=&quot;QString&quot; name=&quot;type&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString" name="lineSymbol"/>
              <Option value="0" type="double" name="minLength"/>
              <Option value="3x:0,0,0,0,0,0" type="QString" name="minLengthMapUnitScale"/>
              <Option value="MM" type="QString" name="minLengthUnit"/>
              <Option value="0" type="double" name="offsetFromAnchor"/>
              <Option value="3x:0,0,0,0,0,0" type="QString" name="offsetFromAnchorMapUnitScale"/>
              <Option value="MM" type="QString" name="offsetFromAnchorUnit"/>
              <Option value="0" type="double" name="offsetFromLabel"/>
              <Option value="3x:0,0,0,0,0,0" type="QString" name="offsetFromLabelMapUnitScale"/>
              <Option value="MM" type="QString" name="offsetFromLabelUnit"/>
            </Option>
          </callout>
        </settings>
      </rule>
    </rules>
  </labeling>
  <customproperties>
    <property key="dualview/previewExpressions" value="ROWID"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Pie">
    <DiagramCategory labelPlacementMethod="XHeight" diagramOrientation="Up" penWidth="0" sizeScale="3x:0,0,0,0,0,0" scaleDependency="Area" lineSizeType="MM" lineSizeScale="3x:0,0,0,0,0,0" backgroundColor="#ffffff" minScaleDenominator="0" backgroundAlpha="255" penColor="#000000" minimumSize="0" enabled="0" sizeType="MM" maxScaleDenominator="1e+08" scaleBasedVisibility="0" height="15" rotationOffset="270" barWidth="5" opacity="1" penAlpha="255" width="15">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute field="" color="#000000" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings dist="0" linePlacementFlags="2" obstacle="0" zIndex="0" priority="0" placement="2" showAll="1">
    <properties>
      <Option type="Map">
        <Option value="" type="QString" name="name"/>
        <Option name="properties"/>
        <Option value="collection" type="QString" name="type"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="ROWID">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="pipe_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_profile_num">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_sewerage_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="0: mixed"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1: rain water"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: dry weather flow"/>
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3: transport"/>
              </Option>
              <Option type="Map">
                <Option value="4" type="QString" name="4: spillway"/>
              </Option>
              <Option type="Map">
                <Option value="5" type="QString" name="5: sinker"/>
              </Option>
              <Option type="Map">
                <Option value="6" type="QString" name="6: storage"/>
              </Option>
              <Option type="Map">
                <Option value="7" type="QString" name="7: storage tank"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_calculation_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="0: embedded"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1: isolated"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: connected"/>
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3: broad crest"/>
              </Option>
              <Option type="Map">
                <Option value="4" type="QString" name="4: short crest"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_invert_level_start_point">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_invert_level_end_point">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_cross_section_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_friction_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="1" type="QString" name="1: Chèzy"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: Manning"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_dist_calc_points">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_material">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="0: concrete"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1: pvc"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: gres"/>
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3: cast iron"/>
              </Option>
              <Option type="Map">
                <Option value="4" type="QString" name="4: brickwork"/>
              </Option>
              <Option type="Map">
                <Option value="5" type="QString" name="5: HPE"/>
              </Option>
              <Option type="Map">
                <Option value="6" type="QString" name="6: HDPE"/>
              </Option>
              <Option type="Map">
                <Option value="7" type="QString" name="7: plate iron"/>
              </Option>
              <Option type="Map">
                <Option value="8" type="QString" name="8: steel"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_pipe_quality">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="pipe_original_length">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_zoom_category">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="-1" type="QString" name="-1"/>
              </Option>
              <Option type="Map">
                <Option value="0" type="QString" name="0"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2"/>
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3"/>
              </Option>
              <Option type="Map">
                <Option value="4" type="QString" name="4"/>
              </Option>
              <Option type="Map">
                <Option value="5" type="QString" name="5"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_connection_node_start_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_connection_node_end_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_shape">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="1" type="QString" name="1: rectangle"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: round"/>
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3: egg"/>
              </Option>
              <Option type="Map">
                <Option value="5" type="QString" name="5: tabulated rectangle"/>
              </Option>
              <Option type="Map">
                <Option value="6" type="QString" name="6: tabulated trapezium"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_width">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_height">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" field="ROWID" name=""/>
    <alias index="1" field="pipe_id" name="id"/>
    <alias index="2" field="pipe_display_name" name="display_name"/>
    <alias index="3" field="pipe_code" name="code"/>
    <alias index="4" field="pipe_profile_num" name="profile_num"/>
    <alias index="5" field="pipe_sewerage_type" name="sewerage_type"/>
    <alias index="6" field="pipe_calculation_type" name="calculation_type"/>
    <alias index="7" field="pipe_invert_level_start_point" name="invert_level_start_point"/>
    <alias index="8" field="pipe_invert_level_end_point" name="invert_level_end_point"/>
    <alias index="9" field="pipe_cross_section_definition_id" name="cross_section_definition_id"/>
    <alias index="10" field="pipe_friction_value" name="friction_value"/>
    <alias index="11" field="pipe_friction_type" name="friction_type"/>
    <alias index="12" field="pipe_dist_calc_points" name="dist_calc_points"/>
    <alias index="13" field="pipe_material" name="material"/>
    <alias index="14" field="pipe_pipe_quality" name=""/>
    <alias index="15" field="pipe_original_length" name="original_length"/>
    <alias index="16" field="pipe_zoom_category" name="zoom_category"/>
    <alias index="17" field="pipe_connection_node_start_id" name="connection_node_start_id"/>
    <alias index="18" field="pipe_connection_node_end_id" name="connection_node_end_id"/>
    <alias index="19" field="def_id" name="id"/>
    <alias index="20" field="def_shape" name="shape"/>
    <alias index="21" field="def_width" name="width"/>
    <alias index="22" field="def_height" name="height"/>
    <alias index="23" field="def_code" name="code"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="ROWID" applyOnUpdate="0" expression=""/>
    <default field="pipe_id" applyOnUpdate="0" expression="if(maximum(pipe_id) is null,1, maximum(pipe_id)+1)"/>
    <default field="pipe_display_name" applyOnUpdate="0" expression="'new'"/>
    <default field="pipe_code" applyOnUpdate="0" expression="'new'"/>
    <default field="pipe_profile_num" applyOnUpdate="0" expression=""/>
    <default field="pipe_sewerage_type" applyOnUpdate="0" expression=""/>
    <default field="pipe_calculation_type" applyOnUpdate="0" expression="1"/>
    <default field="pipe_invert_level_start_point" applyOnUpdate="0" expression="aggregate('v2_manhole_view','mean',&quot;bottom_level&quot;, intersects($geometry,start_point(geometry(@parent))))"/>
    <default field="pipe_invert_level_end_point" applyOnUpdate="0" expression="aggregate('v2_manhole_view','mean',&quot;bottom_level&quot;, intersects($geometry,end_point(geometry(@parent))))"/>
    <default field="pipe_cross_section_definition_id" applyOnUpdate="0" expression=""/>
    <default field="pipe_friction_value" applyOnUpdate="0" expression=""/>
    <default field="pipe_friction_type" applyOnUpdate="0" expression="2"/>
    <default field="pipe_dist_calc_points" applyOnUpdate="0" expression="10000"/>
    <default field="pipe_material" applyOnUpdate="0" expression=""/>
    <default field="pipe_pipe_quality" applyOnUpdate="0" expression=""/>
    <default field="pipe_original_length" applyOnUpdate="0" expression=""/>
    <default field="pipe_zoom_category" applyOnUpdate="0" expression="2"/>
    <default field="pipe_connection_node_start_id" applyOnUpdate="0" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))) is null, 'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))))"/>
    <default field="pipe_connection_node_end_id" applyOnUpdate="0" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))) is null, 'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))))"/>
    <default field="def_id" applyOnUpdate="0" expression=""/>
    <default field="def_shape" applyOnUpdate="0" expression=""/>
    <default field="def_width" applyOnUpdate="0" expression=""/>
    <default field="def_height" applyOnUpdate="0" expression=""/>
    <default field="def_code" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="ROWID" notnull_strength="0"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="pipe_id" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="pipe_display_name" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="pipe_code" notnull_strength="2"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="pipe_profile_num" notnull_strength="0"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="pipe_sewerage_type" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="pipe_calculation_type" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="pipe_invert_level_start_point" notnull_strength="2"/>
    <constraint constraints="5" unique_strength="0" exp_strength="2" field="pipe_invert_level_end_point" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="pipe_cross_section_definition_id" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="pipe_friction_value" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="pipe_friction_type" notnull_strength="2"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="pipe_dist_calc_points" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="pipe_material" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="pipe_pipe_quality" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="pipe_original_length" notnull_strength="0"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="pipe_zoom_category" notnull_strength="2"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="pipe_connection_node_start_id" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="pipe_connection_node_end_id" notnull_strength="0"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="def_id" notnull_strength="2"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="def_shape" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="def_width" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="def_height" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="def_code" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="ROWID" exp=""/>
    <constraint desc="" field="pipe_id" exp=""/>
    <constraint desc="" field="pipe_display_name" exp=""/>
    <constraint desc="" field="pipe_code" exp=""/>
    <constraint desc="" field="pipe_profile_num" exp=""/>
    <constraint desc="" field="pipe_sewerage_type" exp=""/>
    <constraint desc="" field="pipe_calculation_type" exp=""/>
    <constraint desc="" field="pipe_invert_level_start_point" exp=""/>
    <constraint desc="" field="pipe_invert_level_end_point" exp="&quot;invert_level_end_point&quot; is not null"/>
    <constraint desc="" field="pipe_cross_section_definition_id" exp=""/>
    <constraint desc="" field="pipe_friction_value" exp=""/>
    <constraint desc="" field="pipe_friction_type" exp=""/>
    <constraint desc="" field="pipe_dist_calc_points" exp=""/>
    <constraint desc="" field="pipe_material" exp=""/>
    <constraint desc="" field="pipe_pipe_quality" exp=""/>
    <constraint desc="" field="pipe_original_length" exp=""/>
    <constraint desc="" field="pipe_zoom_category" exp=""/>
    <constraint desc="" field="pipe_connection_node_start_id" exp=""/>
    <constraint desc="" field="pipe_connection_node_end_id" exp=""/>
    <constraint desc="" field="def_id" exp=""/>
    <constraint desc="" field="def_shape" exp=""/>
    <constraint desc="" field="def_width" exp=""/>
    <constraint desc="" field="def_height" exp=""/>
    <constraint desc="" field="def_code" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column width="-1" type="field" hidden="0" name="ROWID"/>
      <column width="-1" type="field" hidden="0" name="pipe_id"/>
      <column width="-1" type="field" hidden="0" name="pipe_display_name"/>
      <column width="-1" type="field" hidden="0" name="pipe_code"/>
      <column width="-1" type="field" hidden="0" name="pipe_profile_num"/>
      <column width="-1" type="field" hidden="0" name="pipe_sewerage_type"/>
      <column width="-1" type="field" hidden="0" name="pipe_calculation_type"/>
      <column width="-1" type="field" hidden="0" name="pipe_invert_level_start_point"/>
      <column width="-1" type="field" hidden="0" name="pipe_invert_level_end_point"/>
      <column width="-1" type="field" hidden="0" name="pipe_cross_section_definition_id"/>
      <column width="-1" type="field" hidden="0" name="pipe_friction_value"/>
      <column width="-1" type="field" hidden="0" name="pipe_friction_type"/>
      <column width="-1" type="field" hidden="0" name="pipe_dist_calc_points"/>
      <column width="-1" type="field" hidden="0" name="pipe_material"/>
      <column width="-1" type="field" hidden="0" name="pipe_original_length"/>
      <column width="-1" type="field" hidden="0" name="pipe_zoom_category"/>
      <column width="-1" type="field" hidden="0" name="pipe_connection_node_start_id"/>
      <column width="-1" type="field" hidden="0" name="pipe_connection_node_end_id"/>
      <column width="-1" type="field" hidden="0" name="def_id"/>
      <column width="-1" type="field" hidden="0" name="def_shape"/>
      <column width="-1" type="field" hidden="0" name="def_width"/>
      <column width="-1" type="field" hidden="0" name="def_height"/>
      <column width="-1" type="field" hidden="0" name="def_code"/>
      <column width="-1" type="actions" hidden="1"/>
      <column width="-1" type="field" hidden="0" name="pipe_pipe_quality"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1">.</editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath>.</editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
Formulieren van QGIS mogen een functie van Python hebben die wordt aangeroepen wanneer het formulier wordt geopend.

Gebruik deze functie om extra logica aan uw formulieren toe te voegen.

Voer de naam van de functie in in het veld "Python Init functie".
Een voorbeeld volgt:
"""
from PyQt4.QtGui import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="0" name="Pipe view">
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="General">
        <attributeEditorField showLabel="1" index="1" name="pipe_id"/>
        <attributeEditorField showLabel="1" index="2" name="pipe_display_name"/>
        <attributeEditorField showLabel="1" index="3" name="pipe_code"/>
        <attributeEditorField showLabel="1" index="6" name="pipe_calculation_type"/>
        <attributeEditorField showLabel="1" index="12" name="pipe_dist_calc_points"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Characteristics">
        <attributeEditorField showLabel="1" index="7" name="pipe_invert_level_start_point"/>
        <attributeEditorField showLabel="1" index="8" name="pipe_invert_level_end_point"/>
        <attributeEditorField showLabel="1" index="10" name="pipe_friction_value"/>
        <attributeEditorField showLabel="1" index="11" name="pipe_friction_type"/>
        <attributeEditorField showLabel="1" index="13" name="pipe_material"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Cross section definition">
        <attributeEditorField showLabel="1" index="9" name="pipe_cross_section_definition_id"/>
        <attributeEditorField showLabel="1" index="20" name="def_shape"/>
        <attributeEditorField showLabel="1" index="21" name="def_width"/>
        <attributeEditorField showLabel="1" index="22" name="def_height"/>
        <attributeEditorField showLabel="1" index="23" name="def_code"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Visualization">
        <attributeEditorField showLabel="1" index="5" name="pipe_sewerage_type"/>
        <attributeEditorField showLabel="1" index="16" name="pipe_zoom_category"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Connection nodes">
        <attributeEditorField showLabel="1" index="17" name="pipe_connection_node_start_id"/>
        <attributeEditorField showLabel="1" index="18" name="pipe_connection_node_end_id"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="ROWID" editable="1"/>
    <field name="def_code" editable="0"/>
    <field name="def_height" editable="0"/>
    <field name="def_id" editable="1"/>
    <field name="def_shape" editable="0"/>
    <field name="def_width" editable="0"/>
    <field name="pipe_calculation_type" editable="1"/>
    <field name="pipe_code" editable="1"/>
    <field name="pipe_connection_node_end_id" editable="0"/>
    <field name="pipe_connection_node_start_id" editable="0"/>
    <field name="pipe_cross_section_definition_id" editable="1"/>
    <field name="pipe_display_name" editable="1"/>
    <field name="pipe_dist_calc_points" editable="1"/>
    <field name="pipe_friction_type" editable="1"/>
    <field name="pipe_friction_value" editable="1"/>
    <field name="pipe_id" editable="1"/>
    <field name="pipe_invert_level_end_point" editable="1"/>
    <field name="pipe_invert_level_start_point" editable="1"/>
    <field name="pipe_material" editable="1"/>
    <field name="pipe_original_length" editable="1"/>
    <field name="pipe_pipe_quality" editable="1"/>
    <field name="pipe_profile_num" editable="1"/>
    <field name="pipe_sewerage_type" editable="1"/>
    <field name="pipe_zoom_category" editable="1"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="ROWID"/>
    <field labelOnTop="0" name="def_code"/>
    <field labelOnTop="0" name="def_height"/>
    <field labelOnTop="0" name="def_id"/>
    <field labelOnTop="0" name="def_shape"/>
    <field labelOnTop="0" name="def_width"/>
    <field labelOnTop="0" name="pipe_calculation_type"/>
    <field labelOnTop="0" name="pipe_code"/>
    <field labelOnTop="0" name="pipe_connection_node_end_id"/>
    <field labelOnTop="0" name="pipe_connection_node_start_id"/>
    <field labelOnTop="0" name="pipe_cross_section_definition_id"/>
    <field labelOnTop="0" name="pipe_display_name"/>
    <field labelOnTop="0" name="pipe_dist_calc_points"/>
    <field labelOnTop="0" name="pipe_friction_type"/>
    <field labelOnTop="0" name="pipe_friction_value"/>
    <field labelOnTop="0" name="pipe_id"/>
    <field labelOnTop="0" name="pipe_invert_level_end_point"/>
    <field labelOnTop="0" name="pipe_invert_level_start_point"/>
    <field labelOnTop="0" name="pipe_material"/>
    <field labelOnTop="0" name="pipe_original_length"/>
    <field labelOnTop="0" name="pipe_pipe_quality"/>
    <field labelOnTop="0" name="pipe_profile_num"/>
    <field labelOnTop="0" name="pipe_sewerage_type"/>
    <field labelOnTop="0" name="pipe_zoom_category"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>"ROWID"</previewExpression>
  <mapTip>display_name</mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
