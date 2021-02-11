<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyAlgorithm="0" simplifyDrawingTol="1" simplifyMaxScale="1" readOnly="0" maxScale="0" minScale="0" hasScaleBasedVisibilityFlag="0" version="3.10.10-A Coruña" styleCategories="AllStyleCategories" labelsEnabled="1" simplifyDrawingHints="1" simplifyLocal="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" type="graduatedSymbol" forceraster="0" graduatedMethod="GraduatedSize" attr="try(&#xd;&#xa;&#x9;coalesce(&#xd;&#xa;&#x9;&#x9;case &#xd;&#xa;&#x9;&#x9;&#x9;when def_shape = 1 then (to_real(&quot;def_width&quot;) + to_real(&quot;def_height&quot;))/2.0&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;when def_shape = 2 then to_real(&quot;def_width&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;when def_shape = 3 then (to_real(&quot;def_width&quot;) + to_real(&quot;def_width&quot;)*1.5)/2.0&#xd;&#xa;&#x9;&#x9;&#x9;when def_shape in (5,6) then&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(def_width, ' ')))) &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;+&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(def_height, ' '))))&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;) / 2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;end, &#xd;&#xa; &#x9;&#x9;1&#xd;&#xa;&#x9;), &#xd;&#xa;&#x9;1&#xd;&#xa;)" enableorderby="0">
    <ranges>
      <range lower="0.000000000000000" render="true" symbol="0" upper="0.100000000000000" label="0 - 100"/>
      <range lower="0.100000000000000" render="true" symbol="1" upper="0.200000000000000" label="100 - 200"/>
      <range lower="0.200000000000000" render="true" symbol="2" upper="0.300000000000000" label="200 - 300"/>
      <range lower="0.300000000000000" render="true" symbol="3" upper="0.400000000000000" label="300 - 400"/>
      <range lower="0.400000000000000" render="true" symbol="4" upper="0.500000000000000" label="400 - 500"/>
      <range lower="0.500000000000000" render="true" symbol="5" upper="0.750000000000000" label="500 - 750"/>
      <range lower="0.750000000000000" render="true" symbol="6" upper="1.000000000000000" label="750 - 1000"/>
      <range lower="1.000000000000000" render="true" symbol="7" upper="1.250000000000000" label="1000 - 1250"/>
      <range lower="1.250000000000000" render="true" symbol="8" upper="1.500000000000000" label="1250 - 1500"/>
      <range lower="1.500000000000000" render="true" symbol="9" upper="99999.000000000000000" label="> 1500"/>
    </ranges>
    <symbols>
      <symbol name="0" type="line" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="51,160,44,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.1" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="1" type="line" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="51,160,44,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.422222" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="2" type="line" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="51,160,44,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.744444" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="3" type="line" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="51,160,44,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="1.06667" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="4" type="line" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="51,160,44,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="1.38889" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="5" type="line" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="51,160,44,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="1.71111" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="6" type="line" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="51,160,44,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="2.03333" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="7" type="line" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="51,160,44,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="2.35556" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="8" type="line" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="51,160,44,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="2.67778" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="9" type="line" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="51,160,44,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="3" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol name="0" type="line" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="51,160,44,255" k="line_color"/>
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
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="outlineWidth" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <classificationMethod id="EqualInterval">
      <symmetricMode enabled="0" astride="0" symmetrypoint="0"/>
      <labelFormat format="%1 - %2 " labelprecision="4" trimtrailingzeroes="1"/>
      <extraInformation/>
    </classificationMethod>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="rule-based">
    <rules key="{ccad5221-04d0-49f8-aa02-51c047a2c035}">
      <rule key="{a9529068-4689-4cd9-a0ed-d401f29bf8ed}" scalemaxdenom="10000" description="Crosssection">
        <settings calloutType="simple">
          <text-style fontCapitals="0" previewBkgrdColor="255,255,255,255" namedStyle="Regular" fontLetterSpacing="0" fontWeight="50" fieldName="CASE WHEN def_shape = 1 THEN 'rect '||round(def_width*1000)||'x'||round(def_height*1000) &#xd;&#xa;WHEN def_shape = 2 THEN 'Ø'||round(def_width*1000) &#xd;&#xa;WHEN def_shape = 3 THEN 'egg ' || round(def_width*1000) || '/' || round(def_width*1000*1.5,3) &#xd;&#xa;WHEN def_shape in (5, 6) THEN &#xd;&#xa;&#x9;'tab ' ||&#xd;&#xa;&#x9;round(array_last(array_sort(string_to_array(def_width, ' ')))*1000) ||&#xd;&#xa;&#x9;'/' || &#xd;&#xa;&#x9;round(array_last(array_sort(string_to_array(def_height, ' ')))*1000)&#xd;&#xa;END " fontSize="7" blendMode="0" fontFamily="MS Gothic" fontStrikeout="0" fontSizeUnit="Point" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontUnderline="0" textOpacity="1" fontWordSpacing="0" textOrientation="horizontal" multilineHeight="1" textColor="0,0,0,255" fontItalic="0" useSubstitutions="0" isExpression="1" fontKerning="1">
            <text-buffer bufferDraw="1" bufferOpacity="1" bufferSize="0.7" bufferSizeUnits="MM" bufferNoFill="0" bufferJoinStyle="128" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferColor="255,255,255,255" bufferBlendMode="0"/>
            <background shapeOffsetUnit="MM" shapeBorderWidthUnit="MM" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeFillColor="255,255,255,255" shapeSizeType="0" shapeSVGFile="" shapeSizeUnit="MM" shapeRadiiX="0" shapeRadiiUnit="MM" shapeOffsetX="0" shapeJoinStyle="64" shapeBlendMode="0" shapeBorderColor="128,128,128,255" shapeSizeY="0" shapeOpacity="1" shapeOffsetY="0" shapeBorderWidth="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeType="0" shapeSizeX="0" shapeDraw="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiY="0" shapeRotation="0" shapeRotationType="0">
              <symbol name="markerSymbol" type="marker" alpha="1" clip_to_extent="1" force_rhr="0">
                <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
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
                      <Option name="name" value="" type="QString"/>
                      <Option name="properties"/>
                      <Option name="type" value="collection" type="QString"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </background>
            <shadow shadowOffsetGlobal="1" shadowOffsetAngle="135" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusAlphaOnly="0" shadowDraw="0" shadowBlendMode="6" shadowColor="0,0,0,255" shadowOffsetUnit="MM" shadowRadius="1.5" shadowOpacity="0.7" shadowScale="100" shadowUnder="0" shadowOffsetDist="1" shadowRadiusUnit="MM" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format useMaxLineLengthForAutoWrap="1" reverseDirectionSymbol="0" multilineAlign="0" addDirectionSymbol="0" formatNumbers="0" wrapChar="" autoWrapLength="0" leftDirectionSymbol="&lt;" placeDirectionSymbol="0" plussign="0" decimals="3" rightDirectionSymbol=">"/>
          <placement quadOffset="4" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" centroidInside="0" yOffset="0" maxCurvedCharAngleOut="-25" overrunDistanceUnit="MM" xOffset="0" preserveRotation="1" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorType="PointGeometry" placement="2" distUnits="MM" distMapUnitScale="3x:0,0,0,0,0,0" overrunDistance="0" placementFlags="9" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" repeatDistanceUnits="MM" repeatDistance="0" offsetType="0" maxCurvedCharAngleIn="25" layerType="LineGeometry" centroidWhole="0" fitInPolygonOnly="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" geometryGenerator="" rotationAngle="0" priority="5" dist="0" offsetUnits="MapUnit" geometryGeneratorEnabled="0"/>
          <rendering maxNumLabels="2000" labelPerPart="0" minFeatureSize="0" obstacle="1" obstacleFactor="1" scaleMax="10000000" upsidedownLabels="0" drawLabels="1" fontMaxPixelSize="10000" fontMinPixelSize="3" scaleMin="1" zIndex="0" limitNumLabels="0" obstacleType="0" scaleVisibility="0" mergeLines="0" fontLimitPixelSize="0" displayAll="0"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="Color" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="expression" value="case &#xd;&#xa;when &quot;pipe_sewerage_type&quot; = 0 then '#ffaa00'&#xd;&#xa;when &quot;pipe_sewerage_type&quot; = 0 then '#55aaff'&#xd;&#xa;when &quot;pipe_sewerage_type&quot; = 0 then '#ff0000'&#xd;&#xa;when &quot;pipe_sewerage_type&quot; = 0 then '#999999'&#xd;&#xa;else '#000000'&#xd;&#xa;end" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option name="anchorPoint" value="pole_of_inaccessibility" type="QString"/>
              <Option name="ddProperties" type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
              <Option name="drawToAllParts" value="false" type="bool"/>
              <Option name="enabled" value="0" type="QString"/>
              <Option name="lineSymbol" value="&lt;symbol name=&quot;symbol&quot; type=&quot;line&quot; alpha=&quot;1&quot; clip_to_extent=&quot;1&quot; force_rhr=&quot;0&quot;>&lt;layer pass=&quot;0&quot; enabled=&quot;1&quot; locked=&quot;0&quot; class=&quot;SimpleLine&quot;>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString"/>
              <Option name="minLength" value="0" type="double"/>
              <Option name="minLengthMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="minLengthUnit" value="MM" type="QString"/>
              <Option name="offsetFromAnchor" value="0" type="double"/>
              <Option name="offsetFromAnchorMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offsetFromAnchorUnit" value="MM" type="QString"/>
              <Option name="offsetFromLabel" value="0" type="double"/>
              <Option name="offsetFromLabelMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offsetFromLabelUnit" value="MM" type="QString"/>
            </Option>
          </callout>
        </settings>
      </rule>
    </rules>
  </labeling>
  <customproperties>
    <property value="ROWID" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory labelPlacementMethod="XHeight" enabled="0" sizeType="MM" diagramOrientation="Up" maxScaleDenominator="1e+08" minimumSize="0" height="15" lineSizeScale="3x:0,0,0,0,0,0" barWidth="5" penAlpha="255" sizeScale="3x:0,0,0,0,0,0" lineSizeType="MM" width="15" scaleBasedVisibility="0" penColor="#000000" scaleDependency="Area" backgroundColor="#ffffff" rotationOffset="270" backgroundAlpha="255" penWidth="0" minScaleDenominator="0" opacity="1">
      <fontProperties style="" description="MS Shell Dlg 2,7.8,-1,5,50,0,0,0,0,0"/>
      <attribute color="#000000" field="" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings zIndex="0" obstacle="0" dist="0" priority="0" showAll="1" placement="2" linePlacementFlags="18">
    <properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties"/>
        <Option name="type" value="collection" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
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
    <field name="orf_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_max_capacity">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_crest_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_sewerage">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option name="CheckedState" value="1" type="QString"/>
            <Option name="UncheckedState" value="0" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_cross_section_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_friction_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="1: Chèzy" value="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="2: Manning" value="2" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_discharge_coefficient_positive">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_discharge_coefficient_negative">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_zoom_category">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="-1" value="-1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="0" value="0" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="1" value="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="2" value="2" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="3" value="3" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="4" value="4" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="5" value="5" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_crest_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="3: broad crested" value="3" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="4: short crested" value="4" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_connection_node_start_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_connection_node_end_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_shape">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="1: rectangle" value="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="2: round" value="2" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="3: egg" value="3" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="5: tabulated rectangle" value="5" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="6: tabulated trapezium" value="6" type="QString"/>
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
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_height">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="" field="ROWID"/>
    <alias index="1" name="id" field="orf_id"/>
    <alias index="2" name="display_name" field="orf_display_name"/>
    <alias index="3" name="code" field="orf_code"/>
    <alias index="4" name="max_capacity" field="orf_max_capacity"/>
    <alias index="5" name="crest_level" field="orf_crest_level"/>
    <alias index="6" name="sewerage" field="orf_sewerage"/>
    <alias index="7" name="cross_section_definition_id" field="orf_cross_section_definition_id"/>
    <alias index="8" name="friction_value" field="orf_friction_value"/>
    <alias index="9" name="friction_type" field="orf_friction_type"/>
    <alias index="10" name="discharge_coefficient_positive" field="orf_discharge_coefficient_positive"/>
    <alias index="11" name="discharge_coefficient_negative" field="orf_discharge_coefficient_negative"/>
    <alias index="12" name="zoom_category" field="orf_zoom_category"/>
    <alias index="13" name="crest_type" field="orf_crest_type"/>
    <alias index="14" name="connection_node_start_id" field="orf_connection_node_start_id"/>
    <alias index="15" name="connection_node_end_id" field="orf_connection_node_end_id"/>
    <alias index="16" name="id" field="def_id"/>
    <alias index="17" name="shape" field="def_shape"/>
    <alias index="18" name="width" field="def_width"/>
    <alias index="19" name="height" field="def_height"/>
    <alias index="20" name="code" field="def_code"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" expression="" field="ROWID"/>
    <default applyOnUpdate="0" expression="if(maximum(orf_id) is null,1, maximum(orf_id)+1)" field="orf_id"/>
    <default applyOnUpdate="0" expression="'new'" field="orf_display_name"/>
    <default applyOnUpdate="0" expression="'new'" field="orf_code"/>
    <default applyOnUpdate="0" expression="" field="orf_max_capacity"/>
    <default applyOnUpdate="0" expression="" field="orf_crest_level"/>
    <default applyOnUpdate="0" expression="" field="orf_sewerage"/>
    <default applyOnUpdate="0" expression="" field="orf_cross_section_definition_id"/>
    <default applyOnUpdate="0" expression="0.02" field="orf_friction_value"/>
    <default applyOnUpdate="0" expression="2" field="orf_friction_type"/>
    <default applyOnUpdate="0" expression="0.8" field="orf_discharge_coefficient_positive"/>
    <default applyOnUpdate="0" expression="0.8" field="orf_discharge_coefficient_negative"/>
    <default applyOnUpdate="0" expression="3" field="orf_zoom_category"/>
    <default applyOnUpdate="0" expression="4" field="orf_crest_type"/>
    <default applyOnUpdate="0" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))) is null, 'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))))" field="orf_connection_node_start_id"/>
    <default applyOnUpdate="0" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))) is null, 'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))))" field="orf_connection_node_end_id"/>
    <default applyOnUpdate="0" expression="" field="def_id"/>
    <default applyOnUpdate="0" expression="" field="def_shape"/>
    <default applyOnUpdate="0" expression="" field="def_width"/>
    <default applyOnUpdate="0" expression="" field="def_height"/>
    <default applyOnUpdate="0" expression="" field="def_code"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="ROWID" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="orf_id" constraints="1"/>
    <constraint exp_strength="2" unique_strength="0" notnull_strength="2" field="orf_display_name" constraints="5"/>
    <constraint exp_strength="2" unique_strength="0" notnull_strength="2" field="orf_code" constraints="5"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="orf_max_capacity" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="orf_crest_level" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="orf_sewerage" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="orf_cross_section_definition_id" constraints="1"/>
    <constraint exp_strength="2" unique_strength="0" notnull_strength="2" field="orf_friction_value" constraints="5"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="orf_friction_type" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="orf_discharge_coefficient_positive" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="orf_discharge_coefficient_negative" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="orf_zoom_category" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="orf_crest_type" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="orf_connection_node_start_id" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="orf_connection_node_end_id" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="def_id" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="def_shape" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="def_width" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="def_height" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="def_code" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="ROWID"/>
    <constraint desc="" exp="" field="orf_id"/>
    <constraint desc="" exp="&quot;orf_display_name&quot; is not null" field="orf_display_name"/>
    <constraint desc="" exp="&quot;orf_code&quot; is not null&#xd;&#xa;" field="orf_code"/>
    <constraint desc="" exp="" field="orf_max_capacity"/>
    <constraint desc="" exp="" field="orf_crest_level"/>
    <constraint desc="" exp="" field="orf_sewerage"/>
    <constraint desc="" exp="" field="orf_cross_section_definition_id"/>
    <constraint desc="" exp="&quot;orf_friction_value&quot; is not null" field="orf_friction_value"/>
    <constraint desc="" exp="" field="orf_friction_type"/>
    <constraint desc="" exp="" field="orf_discharge_coefficient_positive"/>
    <constraint desc="" exp="" field="orf_discharge_coefficient_negative"/>
    <constraint desc="" exp="" field="orf_zoom_category"/>
    <constraint desc="" exp="" field="orf_crest_type"/>
    <constraint desc="" exp="" field="orf_connection_node_start_id"/>
    <constraint desc="" exp="" field="orf_connection_node_end_id"/>
    <constraint desc="" exp="" field="def_id"/>
    <constraint desc="" exp="" field="def_shape"/>
    <constraint desc="" exp="" field="def_width"/>
    <constraint desc="" exp="" field="def_height"/>
    <constraint desc="" exp="" field="def_code"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column name="ROWID" type="field" hidden="0" width="-1"/>
      <column name="orf_id" type="field" hidden="0" width="-1"/>
      <column name="orf_display_name" type="field" hidden="0" width="-1"/>
      <column name="orf_code" type="field" hidden="0" width="-1"/>
      <column name="orf_max_capacity" type="field" hidden="0" width="-1"/>
      <column name="orf_crest_level" type="field" hidden="0" width="-1"/>
      <column name="orf_sewerage" type="field" hidden="0" width="-1"/>
      <column name="orf_cross_section_definition_id" type="field" hidden="0" width="-1"/>
      <column name="orf_friction_value" type="field" hidden="0" width="-1"/>
      <column name="orf_friction_type" type="field" hidden="0" width="-1"/>
      <column name="orf_discharge_coefficient_positive" type="field" hidden="0" width="-1"/>
      <column name="orf_discharge_coefficient_negative" type="field" hidden="0" width="-1"/>
      <column name="orf_zoom_category" type="field" hidden="0" width="-1"/>
      <column name="orf_crest_type" type="field" hidden="0" width="-1"/>
      <column name="orf_connection_node_start_id" type="field" hidden="0" width="-1"/>
      <column name="orf_connection_node_end_id" type="field" hidden="0" width="-1"/>
      <column name="def_id" type="field" hidden="0" width="-1"/>
      <column name="def_shape" type="field" hidden="0" width="-1"/>
      <column name="def_width" type="field" hidden="0" width="-1"/>
      <column name="def_height" type="field" hidden="0" width="-1"/>
      <column name="def_code" type="field" hidden="0" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
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
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from PyQt4.QtGui import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer name="Orifice view" showLabel="1" columnCount="1" groupBox="0" visibilityExpression="" visibilityExpressionEnabled="0">
      <attributeEditorContainer name="General" showLabel="1" columnCount="1" groupBox="1" visibilityExpression="" visibilityExpressionEnabled="0">
        <attributeEditorField name="orf_id" showLabel="1" index="1"/>
        <attributeEditorField name="orf_display_name" showLabel="1" index="2"/>
        <attributeEditorField name="orf_code" showLabel="1" index="3"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Characteristics" showLabel="1" columnCount="1" groupBox="1" visibilityExpression="" visibilityExpressionEnabled="0">
        <attributeEditorField name="orf_crest_level" showLabel="1" index="5"/>
        <attributeEditorField name="orf_crest_type" showLabel="1" index="13"/>
        <attributeEditorField name="orf_friction_value" showLabel="1" index="8"/>
        <attributeEditorField name="orf_friction_type" showLabel="1" index="9"/>
        <attributeEditorField name="orf_discharge_coefficient_positive" showLabel="1" index="10"/>
        <attributeEditorField name="orf_discharge_coefficient_negative" showLabel="1" index="11"/>
        <attributeEditorField name="orf_max_capacity" showLabel="1" index="4"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Visualization" showLabel="1" columnCount="1" groupBox="1" visibilityExpression="" visibilityExpressionEnabled="0">
        <attributeEditorField name="orf_sewerage" showLabel="1" index="6"/>
        <attributeEditorField name="orf_zoom_category" showLabel="1" index="12"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Cross section" showLabel="1" columnCount="1" groupBox="1" visibilityExpression="" visibilityExpressionEnabled="0">
        <attributeEditorField name="orf_cross_section_definition_id" showLabel="1" index="7"/>
        <attributeEditorField name="def_shape" showLabel="1" index="17"/>
        <attributeEditorField name="def_width" showLabel="1" index="18"/>
        <attributeEditorField name="def_height" showLabel="1" index="19"/>
        <attributeEditorField name="def_code" showLabel="1" index="20"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Connection nodes" showLabel="1" columnCount="1" groupBox="1" visibilityExpression="" visibilityExpressionEnabled="0">
        <attributeEditorField name="orf_connection_node_start_id" showLabel="1" index="14"/>
        <attributeEditorField name="orf_connection_node_end_id" showLabel="1" index="15"/>
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
    <field name="orf_code" editable="1"/>
    <field name="orf_connection_node_end_id" editable="0"/>
    <field name="orf_connection_node_start_id" editable="0"/>
    <field name="orf_crest_level" editable="1"/>
    <field name="orf_crest_type" editable="1"/>
    <field name="orf_cross_section_definition_id" editable="1"/>
    <field name="orf_discharge_coefficient_negative" editable="1"/>
    <field name="orf_discharge_coefficient_positive" editable="1"/>
    <field name="orf_display_name" editable="1"/>
    <field name="orf_friction_type" editable="1"/>
    <field name="orf_friction_value" editable="1"/>
    <field name="orf_id" editable="1"/>
    <field name="orf_max_capacity" editable="1"/>
    <field name="orf_sewerage" editable="1"/>
    <field name="orf_zoom_category" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="ROWID" labelOnTop="0"/>
    <field name="def_code" labelOnTop="0"/>
    <field name="def_height" labelOnTop="0"/>
    <field name="def_id" labelOnTop="0"/>
    <field name="def_shape" labelOnTop="0"/>
    <field name="def_width" labelOnTop="0"/>
    <field name="orf_code" labelOnTop="0"/>
    <field name="orf_connection_node_end_id" labelOnTop="0"/>
    <field name="orf_connection_node_start_id" labelOnTop="0"/>
    <field name="orf_crest_level" labelOnTop="0"/>
    <field name="orf_crest_type" labelOnTop="0"/>
    <field name="orf_cross_section_definition_id" labelOnTop="0"/>
    <field name="orf_discharge_coefficient_negative" labelOnTop="0"/>
    <field name="orf_discharge_coefficient_positive" labelOnTop="0"/>
    <field name="orf_display_name" labelOnTop="0"/>
    <field name="orf_friction_type" labelOnTop="0"/>
    <field name="orf_friction_value" labelOnTop="0"/>
    <field name="orf_id" labelOnTop="0"/>
    <field name="orf_max_capacity" labelOnTop="0"/>
    <field name="orf_sewerage" labelOnTop="0"/>
    <field name="orf_zoom_category" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>"ROWID"</previewExpression>
  <mapTip>weir_display_name</mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
