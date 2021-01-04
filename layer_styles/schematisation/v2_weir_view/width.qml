<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" labelsEnabled="1" simplifyAlgorithm="0" simplifyMaxScale="1" version="3.10.10-A Coruña" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="1e+08" simplifyDrawingTol="1" simplifyDrawingHints="1" maxScale="0" simplifyLocal="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 graduatedMethod="GraduatedSize" enableorderby="0" type="graduatedSymbol" attr="try(&#xd;&#xa;&#x9;coalesce(&#xd;&#xa;&#x9;&#x9;CASE WHEN def_shape = 1 THEN to_real(def_width)&#xd;&#xa;&#x9;&#x9;WHEN def_shape = 2 THEN to_real(def_width) &#xd;&#xa;&#x9;&#x9;WHEN def_shape = 3 THEN to_real(def_width)&#xd;&#xa;&#x9;&#x9;WHEN def_shape in (5, 6) THEN &#xd;&#xa;&#x9;&#x9;&#x9;to_real(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;array_first(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;string_to_array(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;def_width,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;' '&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;END, &#xd;&#xa; &#x9;&#x9;1&#xd;&#xa;&#x9;), &#xd;&#xa;&#x9;1&#xd;&#xa;)&#xd;&#xa;&#xd;&#xa;" symbollevels="0" forceraster="0">
    <ranges>
      <range upper="0.250000000000000" symbol="0" label="&lt; 0.25" lower="0.000000000000000" render="true"/>
      <range upper="0.500000000000000" symbol="1" label="0.25-0.5" lower="0.250000000000000" render="true"/>
      <range upper="0.750000000000000" symbol="2" label="0.5-0.75" lower="0.500000000000000" render="true"/>
      <range upper="1.000000000000000" symbol="3" label="0.75-1" lower="0.750000000000000" render="true"/>
      <range upper="1.500000000000000" symbol="4" label="1-1.5" lower="1.000000000000000" render="true"/>
      <range upper="2.000000000000000" symbol="5" label="1.5-2" lower="1.500000000000000" render="true"/>
      <range upper="3.000000000000000" symbol="6" label="2-3" lower="2.000000000000000" render="true"/>
      <range upper="4.000000000000000" symbol="7" label="3-4" lower="3.000000000000000" render="true"/>
      <range upper="5.000000000000000" symbol="8" label="4-5" lower="4.000000000000000" render="true"/>
      <range upper="99999.000000000000000" symbol="9" label=">5" lower="5.000000000000000" render="true"/>
    </ranges>
    <symbols>
      <symbol force_rhr="0" type="line" clip_to_extent="1" name="0" alpha="1">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="227,26,28,255" k="line_color"/>
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
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString" name="expression"/>
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
          <prop v="227,26,28,255" k="line_color"/>
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
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString" name="expression"/>
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
          <prop v="227,26,28,255" k="line_color"/>
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
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString" name="expression"/>
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
          <prop v="227,26,28,255" k="line_color"/>
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
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString" name="expression"/>
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
          <prop v="227,26,28,255" k="line_color"/>
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
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" clip_to_extent="1" name="5" alpha="1">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="227,26,28,255" k="line_color"/>
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
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" clip_to_extent="1" name="6" alpha="1">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="227,26,28,255" k="line_color"/>
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
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" clip_to_extent="1" name="7" alpha="1">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="227,26,28,255" k="line_color"/>
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
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" clip_to_extent="1" name="8" alpha="1">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="227,26,28,255" k="line_color"/>
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
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="line" clip_to_extent="1" name="9" alpha="1">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="227,26,28,255" k="line_color"/>
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
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString" name="expression"/>
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
          <prop v="227,26,28,255" k="line_color"/>
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
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="coalesce(scale_exp( to_real(&quot;def_width&quot;), 0.1, 1, 0.1, 3, 0.57), 0.4)" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <classificationMethod id="EqualInterval">
      <symmetricMode enabled="0" astride="0" symmetrypoint="0"/>
      <labelFormat trimtrailingzeroes="1" format="%1 - %2 " labelprecision="4"/>
      <extraInformation/>
    </classificationMethod>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="rule-based">
    <rules key="{2df5dcf5-102b-456f-8b72-1aa65f7687af}">
      <rule key="{d8bf76ec-1545-4bf8-b4a0-d9036a346472}" description="Crosssection" scalemaxdenom="10000">
        <settings calloutType="simple">
          <text-style fieldName="CASE WHEN def_shape = 1 THEN 'w: '||format_number(to_real(def_width),2) || ' (rect)'&#xd;&#xa;WHEN def_shape = 2 THEN 'Ø'||format_number(to_real(def_width),2) &#xd;&#xa;WHEN def_shape = 3 THEN 'w: ' || format_number(to_real(def_width),2) || ' (egg)'&#xd;&#xa;WHEN def_shape in (5, 6) THEN &#xd;&#xa;&#x9;'w: ' || &#xd;&#xa;&#x9;format_number(&#xd;&#xa;&#x9;&#x9;to_real(&#xd;&#xa;&#x9;&#x9;&#x9;array_first(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;string_to_array(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;def_width,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;' '&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;),&#xd;&#xa;&#x9;&#x9;2&#xd;&#xa;&#x9;) || ' (tab)'&#xd;&#xa;END" multilineHeight="1" fontKerning="1" fontSizeUnit="Point" fontFamily="MS Gothic" fontUnderline="0" fontLetterSpacing="0" fontItalic="0" blendMode="0" namedStyle="Regular" previewBkgrdColor="255,255,255,255" textColor="0,0,0,255" fontWordSpacing="0" isExpression="1" fontWeight="50" fontCapitals="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" useSubstitutions="0" fontSize="7" textOpacity="1" fontStrikeout="0" textOrientation="horizontal">
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
    <property key="dualview/previewExpressions" value="&quot;weir_display_name&quot;"/>
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
    <field name="weir_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_crest_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_crest_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="3" type="QString" name="3: broad crested"/>
              </Option>
              <Option type="Map">
                <Option value="4" type="QString" name="4: short crested"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_cross_section_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_sewerage">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_discharge_coefficient_positive">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_discharge_coefficient_negative">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_external">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_zoom_category">
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
    <field name="weir_friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_friction_type">
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
    <field name="weir_connection_node_start_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_connection_node_end_id">
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
                <Option value="1" type="QString" name="1: Rectangle"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: Circle"/>
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3: Egg"/>
              </Option>
              <Option type="Map">
                <Option value="5" type="QString" name="5: Tabulated rectangle"/>
              </Option>
              <Option type="Map">
                <Option value="6" type="QString" name="6: Tabulated trapezium"/>
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
    <alias index="1" field="weir_id" name=""/>
    <alias index="2" field="weir_display_name" name=""/>
    <alias index="3" field="weir_code" name=""/>
    <alias index="4" field="weir_crest_level" name=""/>
    <alias index="5" field="weir_crest_type" name=""/>
    <alias index="6" field="weir_cross_section_definition_id" name=""/>
    <alias index="7" field="weir_sewerage" name=""/>
    <alias index="8" field="weir_discharge_coefficient_positive" name=""/>
    <alias index="9" field="weir_discharge_coefficient_negative" name=""/>
    <alias index="10" field="weir_external" name=""/>
    <alias index="11" field="weir_zoom_category" name=""/>
    <alias index="12" field="weir_friction_value" name=""/>
    <alias index="13" field="weir_friction_type" name=""/>
    <alias index="14" field="weir_connection_node_start_id" name=""/>
    <alias index="15" field="weir_connection_node_end_id" name=""/>
    <alias index="16" field="def_id" name="id"/>
    <alias index="17" field="def_shape" name="shape"/>
    <alias index="18" field="def_width" name="width"/>
    <alias index="19" field="def_height" name="height"/>
    <alias index="20" field="def_code" name="code"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="ROWID" applyOnUpdate="0" expression=""/>
    <default field="weir_id" applyOnUpdate="0" expression=""/>
    <default field="weir_display_name" applyOnUpdate="0" expression=""/>
    <default field="weir_code" applyOnUpdate="0" expression=""/>
    <default field="weir_crest_level" applyOnUpdate="0" expression=""/>
    <default field="weir_crest_type" applyOnUpdate="0" expression=""/>
    <default field="weir_cross_section_definition_id" applyOnUpdate="0" expression=""/>
    <default field="weir_sewerage" applyOnUpdate="0" expression=""/>
    <default field="weir_discharge_coefficient_positive" applyOnUpdate="0" expression=""/>
    <default field="weir_discharge_coefficient_negative" applyOnUpdate="0" expression=""/>
    <default field="weir_external" applyOnUpdate="0" expression=""/>
    <default field="weir_zoom_category" applyOnUpdate="0" expression=""/>
    <default field="weir_friction_value" applyOnUpdate="0" expression=""/>
    <default field="weir_friction_type" applyOnUpdate="0" expression=""/>
    <default field="weir_connection_node_start_id" applyOnUpdate="0" expression=""/>
    <default field="weir_connection_node_end_id" applyOnUpdate="0" expression=""/>
    <default field="def_id" applyOnUpdate="0" expression=""/>
    <default field="def_shape" applyOnUpdate="0" expression=""/>
    <default field="def_width" applyOnUpdate="0" expression=""/>
    <default field="def_height" applyOnUpdate="0" expression=""/>
    <default field="def_code" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="ROWID" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="weir_id" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="weir_display_name" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="weir_code" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="weir_crest_level" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="weir_crest_type" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="weir_cross_section_definition_id" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="weir_sewerage" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="weir_discharge_coefficient_positive" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="weir_discharge_coefficient_negative" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="weir_external" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="weir_zoom_category" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="weir_friction_value" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="weir_friction_type" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="weir_connection_node_start_id" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="weir_connection_node_end_id" notnull_strength="0"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="def_id" notnull_strength="2"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="def_shape" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="def_width" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="def_height" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="def_code" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="ROWID" exp=""/>
    <constraint desc="" field="weir_id" exp=""/>
    <constraint desc="" field="weir_display_name" exp=""/>
    <constraint desc="" field="weir_code" exp=""/>
    <constraint desc="" field="weir_crest_level" exp=""/>
    <constraint desc="" field="weir_crest_type" exp=""/>
    <constraint desc="" field="weir_cross_section_definition_id" exp=""/>
    <constraint desc="" field="weir_sewerage" exp=""/>
    <constraint desc="" field="weir_discharge_coefficient_positive" exp=""/>
    <constraint desc="" field="weir_discharge_coefficient_negative" exp=""/>
    <constraint desc="" field="weir_external" exp=""/>
    <constraint desc="" field="weir_zoom_category" exp=""/>
    <constraint desc="" field="weir_friction_value" exp=""/>
    <constraint desc="" field="weir_friction_type" exp=""/>
    <constraint desc="" field="weir_connection_node_start_id" exp=""/>
    <constraint desc="" field="weir_connection_node_end_id" exp=""/>
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
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="&quot;weir_discharge_coefficient_negative&quot;">
    <columns>
      <column width="-1" type="field" hidden="0" name="ROWID"/>
      <column width="-1" type="field" hidden="0" name="def_id"/>
      <column width="-1" type="field" hidden="0" name="def_shape"/>
      <column width="-1" type="field" hidden="0" name="def_width"/>
      <column width="-1" type="field" hidden="0" name="def_height"/>
      <column width="-1" type="field" hidden="0" name="def_code"/>
      <column width="-1" type="actions" hidden="1"/>
      <column width="-1" type="field" hidden="0" name="weir_id"/>
      <column width="-1" type="field" hidden="0" name="weir_display_name"/>
      <column width="-1" type="field" hidden="0" name="weir_code"/>
      <column width="-1" type="field" hidden="0" name="weir_crest_level"/>
      <column width="-1" type="field" hidden="0" name="weir_crest_type"/>
      <column width="-1" type="field" hidden="0" name="weir_cross_section_definition_id"/>
      <column width="-1" type="field" hidden="0" name="weir_sewerage"/>
      <column width="-1" type="field" hidden="0" name="weir_discharge_coefficient_positive"/>
      <column width="-1" type="field" hidden="0" name="weir_discharge_coefficient_negative"/>
      <column width="-1" type="field" hidden="0" name="weir_external"/>
      <column width="-1" type="field" hidden="0" name="weir_zoom_category"/>
      <column width="-1" type="field" hidden="0" name="weir_friction_value"/>
      <column width="-1" type="field" hidden="0" name="weir_friction_type"/>
      <column width="-1" type="field" hidden="0" name="weir_connection_node_start_id"/>
      <column width="-1" type="field" hidden="0" name="weir_connection_node_end_id"/>
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
    <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="0" name="Weir view">
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="General">
        <attributeEditorField showLabel="1" index="1" name="weir_id"/>
        <attributeEditorField showLabel="1" index="2" name="weir_display_name"/>
        <attributeEditorField showLabel="1" index="3" name="weir_code"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Characteristics">
        <attributeEditorField showLabel="1" index="4" name="weir_crest_level"/>
        <attributeEditorField showLabel="1" index="5" name="weir_crest_type"/>
        <attributeEditorField showLabel="1" index="8" name="weir_discharge_coefficient_positive"/>
        <attributeEditorField showLabel="1" index="9" name="weir_discharge_coefficient_negative"/>
        <attributeEditorField showLabel="1" index="12" name="weir_friction_value"/>
        <attributeEditorField showLabel="1" index="13" name="weir_friction_type"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Cross section">
        <attributeEditorField showLabel="1" index="6" name="weir_cross_section_definition_id"/>
        <attributeEditorField showLabel="1" index="20" name="def_code"/>
        <attributeEditorField showLabel="1" index="17" name="def_shape"/>
        <attributeEditorField showLabel="1" index="18" name="def_width"/>
        <attributeEditorField showLabel="1" index="19" name="def_height"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Visualization">
        <attributeEditorField showLabel="1" index="7" name="weir_sewerage"/>
        <attributeEditorField showLabel="1" index="10" name="weir_external"/>
        <attributeEditorField showLabel="1" index="11" name="weir_zoom_category"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Connection nodes">
        <attributeEditorField showLabel="1" index="14" name="weir_connection_node_start_id"/>
        <attributeEditorField showLabel="1" index="15" name="weir_connection_node_end_id"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="ROWID" editable="1"/>
    <field name="def_code" editable="0"/>
    <field name="def_height" editable="0"/>
    <field name="def_id" editable="0"/>
    <field name="def_shape" editable="0"/>
    <field name="def_width" editable="0"/>
    <field name="orf_code" editable="1"/>
    <field name="orf_connection_node_end_id" editable="1"/>
    <field name="orf_connection_node_start_id" editable="1"/>
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
    <field name="weir_code" editable="1"/>
    <field name="weir_connection_node_end_id" editable="0"/>
    <field name="weir_connection_node_start_id" editable="0"/>
    <field name="weir_crest_level" editable="1"/>
    <field name="weir_crest_type" editable="1"/>
    <field name="weir_cross_section_definition_id" editable="1"/>
    <field name="weir_discharge_coefficient_negative" editable="1"/>
    <field name="weir_discharge_coefficient_positive" editable="1"/>
    <field name="weir_display_name" editable="1"/>
    <field name="weir_external" editable="1"/>
    <field name="weir_friction_type" editable="1"/>
    <field name="weir_friction_value" editable="1"/>
    <field name="weir_id" editable="1"/>
    <field name="weir_sewerage" editable="1"/>
    <field name="weir_zoom_category" editable="1"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="ROWID"/>
    <field labelOnTop="0" name="def_code"/>
    <field labelOnTop="0" name="def_height"/>
    <field labelOnTop="0" name="def_id"/>
    <field labelOnTop="0" name="def_shape"/>
    <field labelOnTop="0" name="def_width"/>
    <field labelOnTop="0" name="orf_code"/>
    <field labelOnTop="0" name="orf_connection_node_end_id"/>
    <field labelOnTop="0" name="orf_connection_node_start_id"/>
    <field labelOnTop="0" name="orf_crest_level"/>
    <field labelOnTop="0" name="orf_crest_type"/>
    <field labelOnTop="0" name="orf_cross_section_definition_id"/>
    <field labelOnTop="0" name="orf_discharge_coefficient_negative"/>
    <field labelOnTop="0" name="orf_discharge_coefficient_positive"/>
    <field labelOnTop="0" name="orf_display_name"/>
    <field labelOnTop="0" name="orf_friction_type"/>
    <field labelOnTop="0" name="orf_friction_value"/>
    <field labelOnTop="0" name="orf_id"/>
    <field labelOnTop="0" name="orf_max_capacity"/>
    <field labelOnTop="0" name="orf_sewerage"/>
    <field labelOnTop="0" name="orf_zoom_category"/>
    <field labelOnTop="0" name="weir_code"/>
    <field labelOnTop="0" name="weir_connection_node_end_id"/>
    <field labelOnTop="0" name="weir_connection_node_start_id"/>
    <field labelOnTop="0" name="weir_crest_level"/>
    <field labelOnTop="0" name="weir_crest_type"/>
    <field labelOnTop="0" name="weir_cross_section_definition_id"/>
    <field labelOnTop="0" name="weir_discharge_coefficient_negative"/>
    <field labelOnTop="0" name="weir_discharge_coefficient_positive"/>
    <field labelOnTop="0" name="weir_display_name"/>
    <field labelOnTop="0" name="weir_external"/>
    <field labelOnTop="0" name="weir_friction_type"/>
    <field labelOnTop="0" name="weir_friction_value"/>
    <field labelOnTop="0" name="weir_id"/>
    <field labelOnTop="0" name="weir_sewerage"/>
    <field labelOnTop="0" name="weir_zoom_category"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>"weir_display_name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
