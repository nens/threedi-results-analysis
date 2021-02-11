<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" minScale="1e+08" simplifyDrawingHints="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" simplifyMaxScale="1" simplifyAlgorithm="0" simplifyDrawingTol="1" readOnly="0" maxScale="0" version="3.10.10-A Coruña" labelsEnabled="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 attr="try(&#xd;&#xa;&#x9;coalesce(&#xd;&#xa;&#x9;&#x9;case &#xd;&#xa;&#x9;&#x9;&#x9;when def_shape = 1 then (to_real(&quot;def_width&quot;) + to_real(&quot;def_height&quot;))/2.0&#x9;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;&#x9;when def_shape = 2 then to_real(&quot;def_width&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;when def_shape = 3 then (to_real(&quot;def_width&quot;) + to_real(&quot;def_width&quot;)*1.5)/2.0&#xd;&#xa;&#x9;&#x9;&#x9;when def_shape in (5,6) then&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(def_width, ' ')))) &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;+&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;to_real(array_last(array_sort(string_to_array(def_height, ' '))))&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;) / 2.0&#xd;&#xa;&#x9;&#x9;&#x9;&#xd;&#xa;&#x9;&#x9;end, &#xd;&#xa; &#x9;&#x9;1&#xd;&#xa;&#x9;), &#xd;&#xa;&#x9;1&#xd;&#xa;)" symbollevels="0" graduatedMethod="GraduatedSize" type="graduatedSymbol" forceraster="0" enableorderby="0">
    <ranges>
      <range label="0 - 100" lower="0.000000000000000" symbol="0" render="true" upper="0.100000000000000"/>
      <range label="100 - 200" lower="0.100000000000000" symbol="1" render="true" upper="0.200000000000000"/>
      <range label="200 - 300" lower="0.200000000000000" symbol="2" render="true" upper="0.300000000000000"/>
      <range label="300 - 400" lower="0.300000000000000" symbol="3" render="true" upper="0.400000000000000"/>
      <range label="400 - 500" lower="0.400000000000000" symbol="4" render="true" upper="0.500000000000000"/>
      <range label="500 - 750" lower="0.500000000000000" symbol="5" render="true" upper="0.750000000000000"/>
      <range label="750 - 1000" lower="0.750000000000000" symbol="6" render="true" upper="1.000000000000000"/>
      <range label="1000 - 1250" lower="1.000000000000000" symbol="7" render="true" upper="1.250000000000000"/>
      <range label="1250 - 1500" lower="1.250000000000000" symbol="8" render="true" upper="1.500000000000000"/>
      <range label="> 1500" lower="1.500000000000000" symbol="9" render="true" upper="99999.000000000000000"/>
    </ranges>
    <symbols>
      <symbol force_rhr="0" type="line" alpha="1" name="0" clip_to_extent="1">
        <layer locked="0" enabled="1" class="SimpleLine" pass="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="101,101,101,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.1"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" alpha="1" name="1" clip_to_extent="1">
        <layer locked="0" enabled="1" class="SimpleLine" pass="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="101,101,101,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.422222"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" alpha="1" name="2" clip_to_extent="1">
        <layer locked="0" enabled="1" class="SimpleLine" pass="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="101,101,101,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.744444"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" alpha="1" name="3" clip_to_extent="1">
        <layer locked="0" enabled="1" class="SimpleLine" pass="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="101,101,101,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1.06667"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" alpha="1" name="4" clip_to_extent="1">
        <layer locked="0" enabled="1" class="SimpleLine" pass="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="101,101,101,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1.38889"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" alpha="1" name="5" clip_to_extent="1">
        <layer locked="0" enabled="1" class="SimpleLine" pass="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="101,101,101,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1.71111"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" alpha="1" name="6" clip_to_extent="1">
        <layer locked="0" enabled="1" class="SimpleLine" pass="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="101,101,101,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="2.03333"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" alpha="1" name="7" clip_to_extent="1">
        <layer locked="0" enabled="1" class="SimpleLine" pass="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="101,101,101,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="2.35556"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" alpha="1" name="8" clip_to_extent="1">
        <layer locked="0" enabled="1" class="SimpleLine" pass="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="101,101,101,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="2.67778"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" alpha="1" name="9" clip_to_extent="1">
        <layer locked="0" enabled="1" class="SimpleLine" pass="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="101,101,101,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="3"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol force_rhr="0" type="line" alpha="1" name="0" clip_to_extent="1">
        <layer locked="0" enabled="1" class="SimpleLine" pass="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="101,101,101,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.4"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <classificationMethod id="EqualInterval">
      <symmetricMode enabled="0" symmetrypoint="0" astride="0"/>
      <labelFormat labelprecision="4" trimtrailingzeroes="1" format="%1 - %2 "/>
      <extraInformation/>
    </classificationMethod>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="rule-based">
    <rules key="{8516845d-0642-4ee5-8878-fde9088a6339}">
      <rule description="Crosssection" key="{50ab6814-7b4a-443a-9ca2-9c094898acb9}" scalemaxdenom="10000">
        <settings calloutType="simple">
          <text-style fontCapitals="0" fieldName="CASE WHEN def_shape = 1 THEN 'rect '||round(def_width*1000)||'x'||round(def_height*1000) &#xd;&#xa;WHEN def_shape = 2 THEN 'Ø'||round(def_width*1000) &#xd;&#xa;WHEN def_shape = 3 THEN 'egg ' || round(def_width*1000) || '/' || round(def_width*1000*1.5,3) &#xd;&#xa;WHEN def_shape in (5, 6) THEN &#xd;&#xa;&#x9;'tab ' ||&#xd;&#xa;&#x9;round(array_last(array_sort(string_to_array(def_width, ' ')))*1000) ||&#xd;&#xa;&#x9;'/' || &#xd;&#xa;&#x9;round(array_last(array_sort(string_to_array(def_height, ' ')))*1000)&#xd;&#xa;END " fontStrikeout="0" isExpression="1" fontLetterSpacing="0" useSubstitutions="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" textColor="0,0,0,255" fontWeight="50" textOrientation="horizontal" fontItalic="0" multilineHeight="1" previewBkgrdColor="255,255,255,255" fontWordSpacing="0" fontSize="7" blendMode="0" fontUnderline="0" namedStyle="Regular" fontSizeUnit="Point" fontFamily="MS Gothic" textOpacity="1" fontKerning="1">
            <text-buffer bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferJoinStyle="128" bufferDraw="1" bufferNoFill="0" bufferBlendMode="0" bufferColor="255,255,255,255" bufferOpacity="1" bufferSizeUnits="MM" bufferSize="0.7"/>
            <background shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeJoinStyle="64" shapeRotation="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeX="0" shapeSizeY="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeSizeType="0" shapeSVGFile="" shapeOpacity="1" shapeOffsetUnit="MM" shapeRadiiX="0" shapeBorderWidth="0" shapeRotationType="0" shapeBorderColor="128,128,128,255" shapeOffsetY="0" shapeBorderWidthUnit="MM" shapeBlendMode="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeType="0" shapeRadiiY="0" shapeOffsetX="0" shapeFillColor="255,255,255,255" shapeSizeUnit="MM" shapeRadiiUnit="MM" shapeDraw="0">
              <symbol force_rhr="0" type="marker" alpha="1" name="markerSymbol" clip_to_extent="1">
                <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
                  <prop k="angle" v="0"/>
                  <prop k="color" v="133,182,111,255"/>
                  <prop k="horizontal_anchor_point" v="1"/>
                  <prop k="joinstyle" v="bevel"/>
                  <prop k="name" v="circle"/>
                  <prop k="offset" v="0,0"/>
                  <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="offset_unit" v="MM"/>
                  <prop k="outline_color" v="35,35,35,255"/>
                  <prop k="outline_style" v="solid"/>
                  <prop k="outline_width" v="0"/>
                  <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="outline_width_unit" v="MM"/>
                  <prop k="scale_method" v="diameter"/>
                  <prop k="size" v="2"/>
                  <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="size_unit" v="MM"/>
                  <prop k="vertical_anchor_point" v="1"/>
                  <data_defined_properties>
                    <Option type="Map">
                      <Option type="QString" name="name" value=""/>
                      <Option name="properties"/>
                      <Option type="QString" name="type" value="collection"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </background>
            <shadow shadowDraw="0" shadowOffsetAngle="135" shadowRadiusAlphaOnly="0" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowScale="100" shadowOffsetGlobal="1" shadowBlendMode="6" shadowUnder="0" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusUnit="MM" shadowOffsetUnit="MM" shadowOpacity="0.7" shadowColor="0,0,0,255" shadowRadius="1.5" shadowOffsetDist="1"/>
            <dd_properties>
              <Option type="Map">
                <Option type="QString" name="name" value=""/>
                <Option name="properties"/>
                <Option type="QString" name="type" value="collection"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format placeDirectionSymbol="0" wrapChar="" useMaxLineLengthForAutoWrap="1" reverseDirectionSymbol="0" plussign="0" decimals="3" autoWrapLength="0" addDirectionSymbol="0" multilineAlign="0" rightDirectionSymbol=">" formatNumbers="0" leftDirectionSymbol="&lt;"/>
          <placement placement="2" offsetType="0" yOffset="0" dist="0" offsetUnits="MapUnit" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" maxCurvedCharAngleOut="-25" repeatDistanceUnits="MM" distMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0" repeatDistance="0" xOffset="0" maxCurvedCharAngleIn="25" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" centroidWhole="0" centroidInside="0" distUnits="MM" layerType="LineGeometry" priority="5" preserveRotation="1" overrunDistance="0" overrunDistanceUnit="MM" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorType="PointGeometry" geometryGenerator="" placementFlags="9" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" rotationAngle="0" quadOffset="4" geometryGeneratorEnabled="0"/>
          <rendering drawLabels="1" upsidedownLabels="0" fontMinPixelSize="3" minFeatureSize="0" maxNumLabels="2000" mergeLines="0" obstacleType="0" labelPerPart="0" fontMaxPixelSize="10000" scaleVisibility="0" limitNumLabels="0" scaleMax="10000000" zIndex="0" obstacleFactor="1" displayAll="0" obstacle="1" scaleMin="1" fontLimitPixelSize="0"/>
          <dd_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="Color">
                  <Option type="bool" name="active" value="false"/>
                  <Option type="QString" name="expression" value="case &#xd;&#xa;when &quot;pipe_sewerage_type&quot; = 0 then '#ffaa00'&#xd;&#xa;when &quot;pipe_sewerage_type&quot; = 0 then '#55aaff'&#xd;&#xa;when &quot;pipe_sewerage_type&quot; = 0 then '#ff0000'&#xd;&#xa;when &quot;pipe_sewerage_type&quot; = 0 then '#999999'&#xd;&#xa;else '#000000'&#xd;&#xa;end"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option type="QString" name="anchorPoint" value="pole_of_inaccessibility"/>
              <Option type="Map" name="ddProperties">
                <Option type="QString" name="name" value=""/>
                <Option name="properties"/>
                <Option type="QString" name="type" value="collection"/>
              </Option>
              <Option type="bool" name="drawToAllParts" value="false"/>
              <Option type="QString" name="enabled" value="0"/>
              <Option type="QString" name="lineSymbol" value="&lt;symbol force_rhr=&quot;0&quot; type=&quot;line&quot; alpha=&quot;1&quot; name=&quot;symbol&quot; clip_to_extent=&quot;1&quot;>&lt;layer locked=&quot;0&quot; enabled=&quot;1&quot; class=&quot;SimpleLine&quot; pass=&quot;0&quot;>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option type=&quot;QString&quot; name=&quot;name&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;type&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
              <Option type="double" name="minLength" value="0"/>
              <Option type="QString" name="minLengthMapUnitScale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="minLengthUnit" value="MM"/>
              <Option type="double" name="offsetFromAnchor" value="0"/>
              <Option type="QString" name="offsetFromAnchorMapUnitScale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="offsetFromAnchorUnit" value="MM"/>
              <Option type="double" name="offsetFromLabel" value="0"/>
              <Option type="QString" name="offsetFromLabelMapUnitScale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="offsetFromLabelUnit" value="MM"/>
            </Option>
          </callout>
        </settings>
      </rule>
    </rules>
  </labeling>
  <customproperties>
    <property key="dualview/previewExpressions">
      <value>"ROWID"</value>
    </property>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Pie" attributeLegend="1">
    <DiagramCategory scaleBasedVisibility="0" backgroundAlpha="255" penWidth="0" sizeType="MM" penAlpha="255" scaleDependency="Area" rotationOffset="270" height="15" minScaleDenominator="0" maxScaleDenominator="1e+08" barWidth="5" labelPlacementMethod="XHeight" sizeScale="3x:0,0,0,0,0,0" lineSizeType="MM" opacity="1" enabled="0" minimumSize="0" penColor="#000000" width="15" backgroundColor="#ffffff" lineSizeScale="3x:0,0,0,0,0,0" diagramOrientation="Up">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" color="#000000" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings dist="0" obstacle="0" zIndex="0" placement="2" showAll="1" linePlacementFlags="2" priority="0">
    <properties>
      <Option type="Map">
        <Option type="QString" name="name" value=""/>
        <Option name="properties"/>
        <Option type="QString" name="type" value="collection"/>
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
    <field name="cul_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_calculation_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="100: embedded" value="100"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="101: isolated" value="101"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="102: connected" value="102"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="105: double connected" value="105"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_friction_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="1: Chèzy" value="1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="2: Manning" value="2"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_dist_calc_points">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_zoom_category">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="-1" value="-1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="0" value="0"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="1" value="1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="2" value="2"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="3" value="3"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="4" value="4"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="5" value="5"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_cross_section_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_discharge_coefficient_positive">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_discharge_coefficient_negative">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_invert_level_start_point">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_invert_level_end_point">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_connection_node_start_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_connection_node_end_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
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
                <Option type="QString" name="1: rectangle" value="1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="2: round" value="2"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="3: egg" value="3"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="5: tabulated rectangle" value="5"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="6: tabulated trapezium" value="6"/>
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
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_height">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="" field="ROWID"/>
    <alias index="1" name="id" field="cul_id"/>
    <alias index="2" name="display_name" field="cul_display_name"/>
    <alias index="3" name="code" field="cul_code"/>
    <alias index="4" name="calculation_type" field="cul_calculation_type"/>
    <alias index="5" name="friction_value" field="cul_friction_value"/>
    <alias index="6" name="friction_type" field="cul_friction_type"/>
    <alias index="7" name="dist_calc_points" field="cul_dist_calc_points"/>
    <alias index="8" name="zoom_category" field="cul_zoom_category"/>
    <alias index="9" name="cross_section_definition_id" field="cul_cross_section_definition_id"/>
    <alias index="10" name="discharge_coefficient_positive" field="cul_discharge_coefficient_positive"/>
    <alias index="11" name="discharge_coefficient_negative" field="cul_discharge_coefficient_negative"/>
    <alias index="12" name="invert_level_start_point" field="cul_invert_level_start_point"/>
    <alias index="13" name="invert_level_end_point" field="cul_invert_level_end_point"/>
    <alias index="14" name="connection_node_start_id" field="cul_connection_node_start_id"/>
    <alias index="15" name="connection_node_end_id" field="cul_connection_node_end_id"/>
    <alias index="16" name="id" field="def_id"/>
    <alias index="17" name="shape" field="def_shape"/>
    <alias index="18" name="width" field="def_width"/>
    <alias index="19" name="height" field="def_height"/>
    <alias index="20" name="code" field="def_code"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="ROWID"/>
    <default expression="if(maximum(cul_id) is null,1, maximum(cul_id)+1)" applyOnUpdate="0" field="cul_id"/>
    <default expression="'new'" applyOnUpdate="0" field="cul_display_name"/>
    <default expression="'new'" applyOnUpdate="0" field="cul_code"/>
    <default expression="101" applyOnUpdate="0" field="cul_calculation_type"/>
    <default expression="" applyOnUpdate="0" field="cul_friction_value"/>
    <default expression="2" applyOnUpdate="0" field="cul_friction_type"/>
    <default expression="10000" applyOnUpdate="0" field="cul_dist_calc_points"/>
    <default expression="3" applyOnUpdate="0" field="cul_zoom_category"/>
    <default expression="" applyOnUpdate="0" field="cul_cross_section_definition_id"/>
    <default expression="0.8" applyOnUpdate="0" field="cul_discharge_coefficient_positive"/>
    <default expression="0.8" applyOnUpdate="0" field="cul_discharge_coefficient_negative"/>
    <default expression="aggregate('v2_manhole_view','min',&quot;bottom_level&quot;, intersects($geometry,start_point(geometry(@parent)))) " applyOnUpdate="0" field="cul_invert_level_start_point"/>
    <default expression="aggregate('v2_manhole_view','min',&quot;bottom_level&quot;, intersects($geometry,end_point(geometry(@parent)))) " applyOnUpdate="0" field="cul_invert_level_end_point"/>
    <default expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))) is null, 'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))))" applyOnUpdate="0" field="cul_connection_node_start_id"/>
    <default expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))) is null, 'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))))" applyOnUpdate="0" field="cul_connection_node_end_id"/>
    <default expression="" applyOnUpdate="0" field="def_id"/>
    <default expression="" applyOnUpdate="0" field="def_shape"/>
    <default expression="" applyOnUpdate="0" field="def_width"/>
    <default expression="" applyOnUpdate="0" field="def_height"/>
    <default expression="" applyOnUpdate="0" field="def_code"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="ROWID"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_id"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_display_name"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_code"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_calculation_type"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_friction_value"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_friction_type"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_dist_calc_points"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_zoom_category"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_cross_section_definition_id"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_discharge_coefficient_positive"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_discharge_coefficient_negative"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_invert_level_start_point"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_invert_level_end_point"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="cul_connection_node_start_id"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="cul_connection_node_end_id"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="def_id"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="def_shape"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="def_width"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="def_height"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="def_code"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="ROWID"/>
    <constraint desc="" exp="" field="cul_id"/>
    <constraint desc="" exp="" field="cul_display_name"/>
    <constraint desc="" exp="" field="cul_code"/>
    <constraint desc="" exp="" field="cul_calculation_type"/>
    <constraint desc="" exp="" field="cul_friction_value"/>
    <constraint desc="" exp="" field="cul_friction_type"/>
    <constraint desc="" exp="" field="cul_dist_calc_points"/>
    <constraint desc="" exp="" field="cul_zoom_category"/>
    <constraint desc="" exp="" field="cul_cross_section_definition_id"/>
    <constraint desc="" exp="" field="cul_discharge_coefficient_positive"/>
    <constraint desc="" exp="" field="cul_discharge_coefficient_negative"/>
    <constraint desc="" exp="" field="cul_invert_level_start_point"/>
    <constraint desc="" exp="" field="cul_invert_level_end_point"/>
    <constraint desc="" exp="" field="cul_connection_node_start_id"/>
    <constraint desc="" exp="" field="cul_connection_node_end_id"/>
    <constraint desc="" exp="" field="def_id"/>
    <constraint desc="" exp="" field="def_shape"/>
    <constraint desc="" exp="" field="def_width"/>
    <constraint desc="" exp="" field="def_height"/>
    <constraint desc="" exp="" field="def_code"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortExpression="" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column type="field" name="ROWID" hidden="0" width="-1"/>
      <column type="field" name="cul_id" hidden="0" width="-1"/>
      <column type="field" name="cul_display_name" hidden="0" width="-1"/>
      <column type="field" name="cul_code" hidden="0" width="-1"/>
      <column type="field" name="cul_calculation_type" hidden="0" width="-1"/>
      <column type="field" name="cul_friction_value" hidden="0" width="-1"/>
      <column type="field" name="cul_friction_type" hidden="0" width="-1"/>
      <column type="field" name="cul_dist_calc_points" hidden="0" width="-1"/>
      <column type="field" name="cul_zoom_category" hidden="0" width="-1"/>
      <column type="field" name="cul_cross_section_definition_id" hidden="0" width="-1"/>
      <column type="field" name="cul_discharge_coefficient_positive" hidden="0" width="-1"/>
      <column type="field" name="cul_discharge_coefficient_negative" hidden="0" width="-1"/>
      <column type="field" name="cul_invert_level_start_point" hidden="0" width="-1"/>
      <column type="field" name="cul_invert_level_end_point" hidden="0" width="-1"/>
      <column type="field" name="cul_connection_node_start_id" hidden="0" width="-1"/>
      <column type="field" name="cul_connection_node_end_id" hidden="0" width="-1"/>
      <column type="field" name="def_id" hidden="0" width="-1"/>
      <column type="field" name="def_shape" hidden="0" width="-1"/>
      <column type="field" name="def_width" hidden="0" width="-1"/>
      <column type="field" name="def_height" hidden="0" width="-1"/>
      <column type="field" name="def_code" hidden="0" width="-1"/>
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
    <attributeEditorContainer groupBox="0" visibilityExpression="" showLabel="1" visibilityExpressionEnabled="0" columnCount="1" name="Culvert view">
      <attributeEditorContainer groupBox="1" visibilityExpression="" showLabel="1" visibilityExpressionEnabled="0" columnCount="1" name="General">
        <attributeEditorField showLabel="1" index="1" name="cul_id"/>
        <attributeEditorField showLabel="1" index="2" name="cul_display_name"/>
        <attributeEditorField showLabel="1" index="3" name="cul_code"/>
        <attributeEditorField showLabel="1" index="4" name="cul_calculation_type"/>
        <attributeEditorField showLabel="1" index="7" name="cul_dist_calc_points"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpression="" showLabel="1" visibilityExpressionEnabled="0" columnCount="1" name="Characteristics">
        <attributeEditorField showLabel="1" index="12" name="cul_invert_level_start_point"/>
        <attributeEditorField showLabel="1" index="13" name="cul_invert_level_end_point"/>
        <attributeEditorField showLabel="1" index="6" name="cul_friction_type"/>
        <attributeEditorField showLabel="1" index="5" name="cul_friction_value"/>
        <attributeEditorField showLabel="1" index="10" name="cul_discharge_coefficient_positive"/>
        <attributeEditorField showLabel="1" index="11" name="cul_discharge_coefficient_negative"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpression="" showLabel="1" visibilityExpressionEnabled="0" columnCount="1" name="Cross section definition">
        <attributeEditorField showLabel="1" index="9" name="cul_cross_section_definition_id"/>
        <attributeEditorField showLabel="1" index="20" name="def_code"/>
        <attributeEditorField showLabel="1" index="17" name="def_shape"/>
        <attributeEditorField showLabel="1" index="18" name="def_width"/>
        <attributeEditorField showLabel="1" index="19" name="def_height"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpression="" showLabel="1" visibilityExpressionEnabled="0" columnCount="1" name="Visualization">
        <attributeEditorField showLabel="1" index="8" name="cul_zoom_category"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpression="" showLabel="1" visibilityExpressionEnabled="0" columnCount="1" name="Connection nodes">
        <attributeEditorField showLabel="1" index="14" name="cul_connection_node_start_id"/>
        <attributeEditorField showLabel="1" index="15" name="cul_connection_node_end_id"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="ROWID"/>
    <field editable="1" name="cul_calculation_type"/>
    <field editable="1" name="cul_code"/>
    <field editable="0" name="cul_connection_node_end_id"/>
    <field editable="0" name="cul_connection_node_start_id"/>
    <field editable="1" name="cul_cross_section_definition_id"/>
    <field editable="1" name="cul_discharge_coefficient_negative"/>
    <field editable="1" name="cul_discharge_coefficient_positive"/>
    <field editable="1" name="cul_display_name"/>
    <field editable="1" name="cul_dist_calc_points"/>
    <field editable="1" name="cul_friction_type"/>
    <field editable="1" name="cul_friction_value"/>
    <field editable="1" name="cul_id"/>
    <field editable="1" name="cul_invert_level_end_point"/>
    <field editable="1" name="cul_invert_level_start_point"/>
    <field editable="1" name="cul_zoom_category"/>
    <field editable="0" name="def_code"/>
    <field editable="0" name="def_height"/>
    <field editable="0" name="def_id"/>
    <field editable="0" name="def_shape"/>
    <field editable="0" name="def_width"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="ROWID"/>
    <field labelOnTop="0" name="cul_calculation_type"/>
    <field labelOnTop="0" name="cul_code"/>
    <field labelOnTop="0" name="cul_connection_node_end_id"/>
    <field labelOnTop="0" name="cul_connection_node_start_id"/>
    <field labelOnTop="0" name="cul_cross_section_definition_id"/>
    <field labelOnTop="0" name="cul_discharge_coefficient_negative"/>
    <field labelOnTop="0" name="cul_discharge_coefficient_positive"/>
    <field labelOnTop="0" name="cul_display_name"/>
    <field labelOnTop="0" name="cul_dist_calc_points"/>
    <field labelOnTop="0" name="cul_friction_type"/>
    <field labelOnTop="0" name="cul_friction_value"/>
    <field labelOnTop="0" name="cul_id"/>
    <field labelOnTop="0" name="cul_invert_level_end_point"/>
    <field labelOnTop="0" name="cul_invert_level_start_point"/>
    <field labelOnTop="0" name="cul_zoom_category"/>
    <field labelOnTop="0" name="def_code"/>
    <field labelOnTop="0" name="def_height"/>
    <field labelOnTop="0" name="def_id"/>
    <field labelOnTop="0" name="def_shape"/>
    <field labelOnTop="0" name="def_width"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>"ROWID"</previewExpression>
  <mapTip>display_name</mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
