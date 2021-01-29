<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyAlgorithm="0" simplifyDrawingTol="1" simplifyMaxScale="1" readOnly="0" maxScale="0" minScale="1e+08" hasScaleBasedVisibilityFlag="0" version="3.10.10-A Coruña" styleCategories="AllStyleCategories" labelsEnabled="1" simplifyDrawingHints="1" simplifyLocal="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" type="singleSymbol" forceraster="0" enableorderby="0">
    <symbols>
      <symbol name="0" type="line" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="227,26,28,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.66" k="line_width"/>
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
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" enabled="1" locked="0" class="MarkerLine">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="5" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="0" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="RenderMetersInMapUnits" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="firstvertex" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="1" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="weir_discharge_coefficient_negative = 0" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="offset" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="type" value="1" type="int"/>
                  <Option name="val" value="" type="QString"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="0.3333 * $length" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@0@1" type="marker" alpha="1" clip_to_extent="1" force_rhr="0">
            <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="line" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="227,26,28,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0.6" k="outline_width"/>
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
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="type" value="1" type="int"/>
                      <Option name="val" value="" type="QString"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="expression" value="" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer pass="0" enabled="1" locked="0" class="MarkerLine">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="5" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="0" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="RenderMetersInMapUnits" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="firstvertex" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="1" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="weir_discharge_coefficient_positive > 0&#xd;&#xa;AND weir_discharge_coefficient_negative = 0" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="offset" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="type" value="1" type="int"/>
                  <Option name="val" value="" type="QString"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="0.66 * $length" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@0@2" type="marker" alpha="1" clip_to_extent="1" force_rhr="0">
            <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="arrowhead" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="227,26,28,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0.6" k="outline_width"/>
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
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="type" value="1" type="int"/>
                      <Option name="val" value="" type="QString"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="expression" value="" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer pass="0" enabled="1" locked="0" class="MarkerLine">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="5" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="0" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="RenderMetersInMapUnits" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="firstvertex" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="1" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="weir_discharge_coefficient_positive = 0" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="offset" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="type" value="1" type="int"/>
                  <Option name="val" value="" type="QString"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="0.6667 * $length" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@0@3" type="marker" alpha="1" clip_to_extent="1" force_rhr="0">
            <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
              <prop v="180" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="line" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="227,26,28,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0.6" k="outline_width"/>
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
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="type" value="1" type="int"/>
                      <Option name="val" value="" type="QString"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="expression" value="" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer pass="0" enabled="1" locked="0" class="MarkerLine">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="5" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="0" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="RenderMetersInMapUnits" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="firstvertex" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="1" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="weir_discharge_coefficient_negative > 0&#xd;&#xa;AND weir_discharge_coefficient_positive = 0" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="offset" type="Map">
                  <Option name="active" value="false" type="bool"/>
                  <Option name="type" value="1" type="int"/>
                  <Option name="val" value="" type="QString"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="0.33 * $length" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@0@4" type="marker" alpha="1" clip_to_extent="1" force_rhr="0">
            <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
              <prop v="180" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="arrowhead" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="227,26,28,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0.6" k="outline_width"/>
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
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="type" value="1" type="int"/>
                      <Option name="val" value="" type="QString"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" value="false" type="bool"/>
                      <Option name="expression" value="" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer pass="0" enabled="1" locked="0" class="MarkerLine">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="3" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="0" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="MM" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="centralpoint" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@0@5" type="marker" alpha="1" clip_to_extent="1" force_rhr="0">
            <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="227,26,28,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="triangle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="0,0,0,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="3.4" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="size" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="if(@map_scale&lt;10000, 3.4,2)" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style fontCapitals="0" previewBkgrdColor="255,255,255,255" namedStyle="Regular" fontLetterSpacing="0" fontWeight="50" fieldName="coalesce(round(weir_crest_level, 2), 'NULL')" fontSize="8" blendMode="0" fontFamily="MS Gothic" fontStrikeout="0" fontSizeUnit="Point" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontUnderline="0" textOpacity="1" fontWordSpacing="0" textOrientation="horizontal" multilineHeight="1" textColor="227,26,28,255" fontItalic="0" useSubstitutions="0" isExpression="1" fontKerning="1">
        <text-buffer bufferDraw="1" bufferOpacity="1" bufferSize="0.7" bufferSizeUnits="MM" bufferNoFill="0" bufferJoinStyle="128" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferColor="255,255,255,255" bufferBlendMode="0"/>
        <background shapeOffsetUnit="MM" shapeBorderWidthUnit="MM" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeFillColor="255,255,255,255" shapeSizeType="0" shapeSVGFile="" shapeSizeUnit="MM" shapeRadiiX="0" shapeRadiiUnit="MM" shapeOffsetX="0" shapeJoinStyle="64" shapeBlendMode="0" shapeBorderColor="128,128,128,255" shapeSizeY="0" shapeOpacity="1" shapeOffsetY="0" shapeBorderWidth="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeType="0" shapeSizeX="0" shapeDraw="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiY="0" shapeRotation="0" shapeRotationType="0">
          <symbol name="markerSymbol" type="marker" alpha="1" clip_to_extent="1" force_rhr="0">
            <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="190,178,151,255" k="color"/>
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
      <placement quadOffset="2" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" centroidInside="0" yOffset="0" maxCurvedCharAngleOut="-25" overrunDistanceUnit="MM" xOffset="2" preserveRotation="0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorType="PointGeometry" placement="1" distUnits="MM" distMapUnitScale="3x:0,0,0,0,0,0" overrunDistance="0" placementFlags="2" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" repeatDistanceUnits="MM" repeatDistance="0" offsetType="0" maxCurvedCharAngleIn="25" layerType="LineGeometry" centroidWhole="0" fitInPolygonOnly="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" geometryGenerator="centroid($geometry)" rotationAngle="0" priority="5" dist="0" offsetUnits="MM" geometryGeneratorEnabled="1"/>
      <rendering maxNumLabels="2000" labelPerPart="0" minFeatureSize="0" obstacle="1" obstacleFactor="1" scaleMax="2500" upsidedownLabels="0" drawLabels="1" fontMaxPixelSize="10000" fontMinPixelSize="3" scaleMin="1" zIndex="0" limitNumLabels="0" obstacleType="0" scaleVisibility="1" mergeLines="0" fontLimitPixelSize="0" displayAll="1"/>
      <dd_properties>
        <Option type="Map">
          <Option name="name" value="" type="QString"/>
          <Option name="properties" type="Map">
            <Option name="Hali" type="Map">
              <Option name="active" value="true" type="bool"/>
              <Option name="expression" value="'Left'" type="QString"/>
              <Option name="type" value="3" type="int"/>
            </Option>
            <Option name="LabelRotation" type="Map">
              <Option name="active" value="false" type="bool"/>
              <Option name="type" value="1" type="int"/>
              <Option name="val" value="" type="QString"/>
            </Option>
            <Option name="PositionX" type="Map">
              <Option name="active" value="false" type="bool"/>
              <Option name="type" value="1" type="int"/>
              <Option name="val" value="" type="QString"/>
            </Option>
            <Option name="PositionY" type="Map">
              <Option name="active" value="false" type="bool"/>
              <Option name="type" value="1" type="int"/>
              <Option name="val" value="" type="QString"/>
            </Option>
            <Option name="Show" type="Map">
              <Option name="active" value="true" type="bool"/>
              <Option name="expression" value="intersects(transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;start_point( $geometry),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;  @map_crs  &#xd;&#xa;&#x9;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;&#x9;@map_extent&#xd;&#xa;)" type="QString"/>
              <Option name="type" value="3" type="int"/>
            </Option>
            <Option name="Vali" type="Map">
              <Option name="active" value="true" type="bool"/>
              <Option name="expression" value="'Top'" type="QString"/>
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
  </labeling>
  <customproperties>
    <property value="weir_display_name" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Pie">
    <DiagramCategory labelPlacementMethod="XHeight" enabled="0" sizeType="MM" diagramOrientation="Up" maxScaleDenominator="1e+08" minimumSize="0" height="15" lineSizeScale="3x:0,0,0,0,0,0" barWidth="5" penAlpha="255" sizeScale="3x:0,0,0,0,0,0" lineSizeType="MM" width="15" scaleBasedVisibility="0" penColor="#000000" scaleDependency="Area" backgroundColor="#ffffff" rotationOffset="270" backgroundAlpha="255" penWidth="0" minScaleDenominator="0" opacity="1">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute color="#000000" field="" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings zIndex="0" obstacle="0" dist="0" priority="0" showAll="1" placement="2" linePlacementFlags="2">
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
    <field name="weir_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_crest_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_crest_type">
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
    <field name="weir_cross_section_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_sewerage">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option name="CheckedState" value="1" type="QString"/>
            <Option name="UncheckedState" value="0" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_discharge_coefficient_positive">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_discharge_coefficient_negative">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_external">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option name="CheckedState" value="1" type="QString"/>
            <Option name="UncheckedState" value="0" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_zoom_category">
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
    <field name="weir_friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_friction_type">
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
    <field name="weir_connection_node_start_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_connection_node_end_id">
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
                <Option name="1: Rectangle" value="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="2: Circle" value="2" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="3: Egg" value="3" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="5: Tabulated rectangle" value="5" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="6: Tabulated trapezium" value="6" type="QString"/>
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
    <alias index="1" name="id" field="weir_id"/>
    <alias index="2" name="display_name" field="weir_display_name"/>
    <alias index="3" name="code" field="weir_code"/>
    <alias index="4" name="crest_level" field="weir_crest_level"/>
    <alias index="5" name="crest_type" field="weir_crest_type"/>
    <alias index="6" name="Cross_section_definition_id" field="weir_cross_section_definition_id"/>
    <alias index="7" name="sewerage" field="weir_sewerage"/>
    <alias index="8" name="discharge_coefficient_positive" field="weir_discharge_coefficient_positive"/>
    <alias index="9" name="discharge_coefficient_negative" field="weir_discharge_coefficient_negative"/>
    <alias index="10" name="external" field="weir_external"/>
    <alias index="11" name="zoom_category" field="weir_zoom_category"/>
    <alias index="12" name="friction_value" field="weir_friction_value"/>
    <alias index="13" name="friction_type" field="weir_friction_type"/>
    <alias index="14" name="connection_node_start_id" field="weir_connection_node_start_id"/>
    <alias index="15" name="connection_node_end_id" field="weir_connection_node_end_id"/>
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
    <default applyOnUpdate="0" expression="if(maximum(weir_id) is null,1, maximum(weir_id)+1)" field="weir_id"/>
    <default applyOnUpdate="0" expression="'new'" field="weir_display_name"/>
    <default applyOnUpdate="0" expression="'new'" field="weir_code"/>
    <default applyOnUpdate="0" expression="" field="weir_crest_level"/>
    <default applyOnUpdate="0" expression="4" field="weir_crest_type"/>
    <default applyOnUpdate="0" expression="" field="weir_cross_section_definition_id"/>
    <default applyOnUpdate="0" expression="" field="weir_sewerage"/>
    <default applyOnUpdate="0" expression="0.8" field="weir_discharge_coefficient_positive"/>
    <default applyOnUpdate="0" expression="0.8" field="weir_discharge_coefficient_negative"/>
    <default applyOnUpdate="0" expression="1" field="weir_external"/>
    <default applyOnUpdate="0" expression="2" field="weir_zoom_category"/>
    <default applyOnUpdate="0" expression="0.02" field="weir_friction_value"/>
    <default applyOnUpdate="0" expression="2" field="weir_friction_type"/>
    <default applyOnUpdate="0" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))) is null,'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))))" field="weir_connection_node_start_id"/>
    <default applyOnUpdate="0" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))) is null,'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))))" field="weir_connection_node_end_id"/>
    <default applyOnUpdate="0" expression="" field="def_id"/>
    <default applyOnUpdate="0" expression="" field="def_shape"/>
    <default applyOnUpdate="0" expression="" field="def_width"/>
    <default applyOnUpdate="0" expression="" field="def_height"/>
    <default applyOnUpdate="0" expression="" field="def_code"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="ROWID" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="weir_id" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="weir_display_name" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="weir_code" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="weir_crest_level" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="weir_crest_type" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="weir_cross_section_definition_id" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="weir_sewerage" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="weir_discharge_coefficient_positive" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="weir_discharge_coefficient_negative" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="weir_external" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="weir_zoom_category" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="weir_friction_value" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="weir_friction_type" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="weir_connection_node_start_id" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="weir_connection_node_end_id" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" field="def_id" constraints="1"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="def_shape" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="def_width" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="def_height" constraints="0"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="def_code" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="ROWID"/>
    <constraint desc="" exp="" field="weir_id"/>
    <constraint desc="" exp="" field="weir_display_name"/>
    <constraint desc="" exp="" field="weir_code"/>
    <constraint desc="" exp="" field="weir_crest_level"/>
    <constraint desc="" exp="" field="weir_crest_type"/>
    <constraint desc="" exp="" field="weir_cross_section_definition_id"/>
    <constraint desc="" exp="" field="weir_sewerage"/>
    <constraint desc="" exp="" field="weir_discharge_coefficient_positive"/>
    <constraint desc="" exp="" field="weir_discharge_coefficient_negative"/>
    <constraint desc="" exp="" field="weir_external"/>
    <constraint desc="" exp="" field="weir_zoom_category"/>
    <constraint desc="" exp="" field="weir_friction_value"/>
    <constraint desc="" exp="" field="weir_friction_type"/>
    <constraint desc="" exp="" field="weir_connection_node_start_id"/>
    <constraint desc="" exp="" field="weir_connection_node_end_id"/>
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
      <column name="weir_id" type="field" hidden="0" width="-1"/>
      <column name="weir_display_name" type="field" hidden="0" width="-1"/>
      <column name="weir_code" type="field" hidden="0" width="-1"/>
      <column name="weir_crest_level" type="field" hidden="0" width="-1"/>
      <column name="weir_crest_type" type="field" hidden="0" width="-1"/>
      <column name="weir_cross_section_definition_id" type="field" hidden="0" width="185"/>
      <column name="weir_sewerage" type="field" hidden="0" width="-1"/>
      <column name="weir_discharge_coefficient_positive" type="field" hidden="0" width="-1"/>
      <column name="weir_discharge_coefficient_negative" type="field" hidden="0" width="-1"/>
      <column name="weir_external" type="field" hidden="0" width="-1"/>
      <column name="weir_zoom_category" type="field" hidden="0" width="-1"/>
      <column name="weir_friction_value" type="field" hidden="0" width="-1"/>
      <column name="weir_friction_type" type="field" hidden="0" width="-1"/>
      <column name="weir_connection_node_start_id" type="field" hidden="0" width="-1"/>
      <column name="weir_connection_node_end_id" type="field" hidden="0" width="-1"/>
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
    <attributeEditorContainer name="Weir view" showLabel="1" columnCount="1" groupBox="0" visibilityExpression="" visibilityExpressionEnabled="0">
      <attributeEditorContainer name="General" showLabel="1" columnCount="1" groupBox="1" visibilityExpression="" visibilityExpressionEnabled="0">
        <attributeEditorField name="weir_id" showLabel="1" index="1"/>
        <attributeEditorField name="weir_display_name" showLabel="1" index="2"/>
        <attributeEditorField name="weir_code" showLabel="1" index="3"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Characteristics" showLabel="1" columnCount="1" groupBox="1" visibilityExpression="" visibilityExpressionEnabled="0">
        <attributeEditorField name="weir_crest_level" showLabel="1" index="4"/>
        <attributeEditorField name="weir_crest_type" showLabel="1" index="5"/>
        <attributeEditorField name="weir_discharge_coefficient_positive" showLabel="1" index="8"/>
        <attributeEditorField name="weir_discharge_coefficient_negative" showLabel="1" index="9"/>
        <attributeEditorField name="weir_friction_value" showLabel="1" index="12"/>
        <attributeEditorField name="weir_friction_type" showLabel="1" index="13"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Cross section" showLabel="1" columnCount="1" groupBox="1" visibilityExpression="" visibilityExpressionEnabled="0">
        <attributeEditorField name="weir_cross_section_definition_id" showLabel="1" index="6"/>
        <attributeEditorField name="def_code" showLabel="1" index="20"/>
        <attributeEditorField name="def_shape" showLabel="1" index="17"/>
        <attributeEditorField name="def_width" showLabel="1" index="18"/>
        <attributeEditorField name="def_height" showLabel="1" index="19"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Visualization" showLabel="1" columnCount="1" groupBox="1" visibilityExpression="" visibilityExpressionEnabled="0">
        <attributeEditorField name="weir_sewerage" showLabel="1" index="7"/>
        <attributeEditorField name="weir_external" showLabel="1" index="10"/>
        <attributeEditorField name="weir_zoom_category" showLabel="1" index="11"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Connection nodes" showLabel="1" columnCount="1" groupBox="1" visibilityExpression="" visibilityExpressionEnabled="0">
        <attributeEditorField name="weir_connection_node_start_id" showLabel="1" index="14"/>
        <attributeEditorField name="weir_connection_node_end_id" showLabel="1" index="15"/>
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
    <field name="ROWID" labelOnTop="0"/>
    <field name="def_code" labelOnTop="0"/>
    <field name="def_height" labelOnTop="0"/>
    <field name="def_id" labelOnTop="0"/>
    <field name="def_shape" labelOnTop="0"/>
    <field name="def_width" labelOnTop="0"/>
    <field name="weir_code" labelOnTop="0"/>
    <field name="weir_connection_node_end_id" labelOnTop="0"/>
    <field name="weir_connection_node_start_id" labelOnTop="0"/>
    <field name="weir_crest_level" labelOnTop="0"/>
    <field name="weir_crest_type" labelOnTop="0"/>
    <field name="weir_cross_section_definition_id" labelOnTop="0"/>
    <field name="weir_discharge_coefficient_negative" labelOnTop="0"/>
    <field name="weir_discharge_coefficient_positive" labelOnTop="0"/>
    <field name="weir_display_name" labelOnTop="0"/>
    <field name="weir_external" labelOnTop="0"/>
    <field name="weir_friction_type" labelOnTop="0"/>
    <field name="weir_friction_value" labelOnTop="0"/>
    <field name="weir_id" labelOnTop="0"/>
    <field name="weir_sewerage" labelOnTop="0"/>
    <field name="weir_zoom_category" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>"weir_display_name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
