<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" labelsEnabled="1" simplifyAlgorithm="0" simplifyMaxScale="1" version="3.10.10-A Coruña" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="1e+08" simplifyDrawingTol="1" simplifyDrawingHints="1" maxScale="0" simplifyLocal="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" type="singleSymbol" symbollevels="0" forceraster="0">
    <symbols>
      <symbol force_rhr="0" type="line" clip_to_extent="1" name="0" alpha="1">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="51,160,44,255" k="line_color"/>
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
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer enabled="1" class="MarkerLine" locked="0" pass="0">
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
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="orf_discharge_coefficient_negative = 0" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="offset">
                  <Option value="false" type="bool" name="active"/>
                  <Option value="1" type="int" name="type"/>
                  <Option value="" type="QString" name="val"/>
                </Option>
                <Option type="Map" name="offsetAlongLine">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="0.3333 * $length" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" type="marker" clip_to_extent="1" name="@0@1" alpha="1">
            <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
              <prop v="0" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="line" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="51,160,44,255" k="outline_color"/>
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
                  <Option value="" type="QString" name="name"/>
                  <Option type="Map" name="properties">
                    <Option type="Map" name="angle">
                      <Option value="false" type="bool" name="active"/>
                      <Option value="1" type="int" name="type"/>
                      <Option value="" type="QString" name="val"/>
                    </Option>
                    <Option type="Map" name="enabled">
                      <Option value="true" type="bool" name="active"/>
                      <Option value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;" type="QString" name="expression"/>
                      <Option value="3" type="int" name="type"/>
                    </Option>
                    <Option type="Map" name="size">
                      <Option value="false" type="bool" name="active"/>
                      <Option value="" type="QString" name="expression"/>
                      <Option value="3" type="int" name="type"/>
                    </Option>
                  </Option>
                  <Option value="collection" type="QString" name="type"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer enabled="1" class="MarkerLine" locked="0" pass="0">
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
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="orf_discharge_coefficient_positive > 0&#xd;&#xa;AND orf_discharge_coefficient_negative = 0" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="offset">
                  <Option value="false" type="bool" name="active"/>
                  <Option value="1" type="int" name="type"/>
                  <Option value="" type="QString" name="val"/>
                </Option>
                <Option type="Map" name="offsetAlongLine">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="0.66 * $length" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" type="marker" clip_to_extent="1" name="@0@2" alpha="1">
            <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
              <prop v="0" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="arrowhead" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="51,160,44,255" k="outline_color"/>
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
                  <Option value="" type="QString" name="name"/>
                  <Option type="Map" name="properties">
                    <Option type="Map" name="angle">
                      <Option value="false" type="bool" name="active"/>
                      <Option value="1" type="int" name="type"/>
                      <Option value="" type="QString" name="val"/>
                    </Option>
                    <Option type="Map" name="enabled">
                      <Option value="true" type="bool" name="active"/>
                      <Option value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;" type="QString" name="expression"/>
                      <Option value="3" type="int" name="type"/>
                    </Option>
                    <Option type="Map" name="size">
                      <Option value="false" type="bool" name="active"/>
                      <Option value="" type="QString" name="expression"/>
                      <Option value="3" type="int" name="type"/>
                    </Option>
                  </Option>
                  <Option value="collection" type="QString" name="type"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer enabled="1" class="MarkerLine" locked="0" pass="0">
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
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="orf_discharge_coefficient_positive = 0" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="offset">
                  <Option value="false" type="bool" name="active"/>
                  <Option value="1" type="int" name="type"/>
                  <Option value="" type="QString" name="val"/>
                </Option>
                <Option type="Map" name="offsetAlongLine">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="0.6667 * $length" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" type="marker" clip_to_extent="1" name="@0@3" alpha="1">
            <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
              <prop v="180" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="line" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="51,160,44,255" k="outline_color"/>
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
                  <Option value="" type="QString" name="name"/>
                  <Option type="Map" name="properties">
                    <Option type="Map" name="angle">
                      <Option value="false" type="bool" name="active"/>
                      <Option value="1" type="int" name="type"/>
                      <Option value="" type="QString" name="val"/>
                    </Option>
                    <Option type="Map" name="enabled">
                      <Option value="true" type="bool" name="active"/>
                      <Option value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;" type="QString" name="expression"/>
                      <Option value="3" type="int" name="type"/>
                    </Option>
                    <Option type="Map" name="size">
                      <Option value="false" type="bool" name="active"/>
                      <Option value="" type="QString" name="expression"/>
                      <Option value="3" type="int" name="type"/>
                    </Option>
                  </Option>
                  <Option value="collection" type="QString" name="type"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer enabled="1" class="MarkerLine" locked="0" pass="0">
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
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="orf_discharge_coefficient_negative > 0&#xd;&#xa;AND orf_discharge_coefficient_positive = 0" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="offset">
                  <Option value="false" type="bool" name="active"/>
                  <Option value="1" type="int" name="type"/>
                  <Option value="" type="QString" name="val"/>
                </Option>
                <Option type="Map" name="offsetAlongLine">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="0.33 * $length" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" type="marker" clip_to_extent="1" name="@0@4" alpha="1">
            <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
              <prop v="180" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="arrowhead" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="51,160,44,255" k="outline_color"/>
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
                  <Option value="" type="QString" name="name"/>
                  <Option type="Map" name="properties">
                    <Option type="Map" name="angle">
                      <Option value="false" type="bool" name="active"/>
                      <Option value="1" type="int" name="type"/>
                      <Option value="" type="QString" name="val"/>
                    </Option>
                    <Option type="Map" name="enabled">
                      <Option value="true" type="bool" name="active"/>
                      <Option value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;" type="QString" name="expression"/>
                      <Option value="3" type="int" name="type"/>
                    </Option>
                    <Option type="Map" name="size">
                      <Option value="false" type="bool" name="active"/>
                      <Option value="" type="QString" name="expression"/>
                      <Option value="3" type="int" name="type"/>
                    </Option>
                  </Option>
                  <Option value="collection" type="QString" name="type"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer enabled="1" class="MarkerLine" locked="0" pass="0">
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
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" type="marker" clip_to_extent="1" name="@0@5" alpha="1">
            <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
              <prop v="0" k="angle"/>
              <prop v="51,160,44,255" k="color"/>
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
                  <Option value="" type="QString" name="name"/>
                  <Option name="properties"/>
                  <Option value="collection" type="QString" name="type"/>
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
      <text-style fieldName="coalesce(round(orf_crest_level, 2), 'NULL')" multilineHeight="1" fontKerning="1" fontSizeUnit="Point" fontFamily="MS Shell Dlg 2" fontUnderline="0" fontLetterSpacing="0" fontItalic="0" blendMode="0" namedStyle="Standaard" previewBkgrdColor="255,255,255,255" textColor="51,160,44,255" fontWordSpacing="0" isExpression="1" fontWeight="50" fontCapitals="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" useSubstitutions="0" fontSize="8" textOpacity="1" fontStrikeout="0" textOrientation="horizontal">
        <text-buffer bufferSize="0.7" bufferColor="255,255,255,255" bufferJoinStyle="128" bufferOpacity="1" bufferBlendMode="0" bufferNoFill="0" bufferDraw="1" bufferSizeUnits="MM" bufferSizeMapUnitScale="3x:0,0,0,0,0,0"/>
        <background shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiX="0" shapeJoinStyle="64" shapeSizeY="0" shapeBorderColor="128,128,128,255" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeRotationType="0" shapeOffsetY="0" shapeSizeX="0" shapeDraw="0" shapeFillColor="255,255,255,255" shapeBorderWidthUnit="MM" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeType="0" shapeBorderWidth="0" shapeOffsetX="0" shapeSizeUnit="MM" shapeRadiiY="0" shapeType="0" shapeOpacity="1" shapeBlendMode="0" shapeSVGFile="" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetUnit="MM" shapeRadiiUnit="MM" shapeRotation="0">
          <symbol force_rhr="0" type="marker" clip_to_extent="1" name="markerSymbol" alpha="1">
            <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
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
      <placement placement="1" repeatDistanceUnits="MM" distUnits="MM" maxCurvedCharAngleOut="-25" maxCurvedCharAngleIn="25" offsetType="0" centroidInside="0" overrunDistance="0" quadOffset="2" geometryGeneratorType="PointGeometry" repeatDistance="0" layerType="LineGeometry" yOffset="0" geometryGenerator="centroid($geometry)" fitInPolygonOnly="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" preserveRotation="0" xOffset="2" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" distMapUnitScale="3x:0,0,0,0,0,0" priority="5" rotationAngle="0" centroidWhole="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" overrunDistanceUnit="MM" geometryGeneratorEnabled="1" dist="0" offsetUnits="MM" placementFlags="2"/>
      <rendering obstacle="1" upsidedownLabels="0" displayAll="1" scaleMin="1" scaleVisibility="1" limitNumLabels="0" scaleMax="2500" fontMinPixelSize="3" drawLabels="1" maxNumLabels="2000" fontLimitPixelSize="0" minFeatureSize="0" labelPerPart="0" obstacleFactor="1" mergeLines="0" obstacleType="0" fontMaxPixelSize="10000" zIndex="0"/>
      <dd_properties>
        <Option type="Map">
          <Option value="" type="QString" name="name"/>
          <Option type="Map" name="properties">
            <Option type="Map" name="Hali">
              <Option value="true" type="bool" name="active"/>
              <Option value="'Left'" type="QString" name="expression"/>
              <Option value="3" type="int" name="type"/>
            </Option>
            <Option type="Map" name="LabelRotation">
              <Option value="false" type="bool" name="active"/>
              <Option value="1" type="int" name="type"/>
              <Option value="" type="QString" name="val"/>
            </Option>
            <Option type="Map" name="PositionX">
              <Option value="false" type="bool" name="active"/>
              <Option value="1" type="int" name="type"/>
              <Option value="" type="QString" name="val"/>
            </Option>
            <Option type="Map" name="PositionY">
              <Option value="false" type="bool" name="active"/>
              <Option value="1" type="int" name="type"/>
              <Option value="" type="QString" name="val"/>
            </Option>
            <Option type="Map" name="Show">
              <Option value="true" type="bool" name="active"/>
              <Option value="intersects(transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;start_point( $geometry),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;  @map_crs  &#xd;&#xa;&#x9;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;&#x9;@map_extent&#xd;&#xa;)" type="QString" name="expression"/>
              <Option value="3" type="int" name="type"/>
            </Option>
            <Option type="Map" name="Vali">
              <Option value="true" type="bool" name="active"/>
              <Option value="'Top'" type="QString" name="expression"/>
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
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory labelPlacementMethod="XHeight" diagramOrientation="Up" penWidth="0" sizeScale="3x:0,0,0,0,0,0" scaleDependency="Area" lineSizeType="MM" lineSizeScale="3x:0,0,0,0,0,0" backgroundColor="#ffffff" minScaleDenominator="0" backgroundAlpha="255" penColor="#000000" minimumSize="0" enabled="0" sizeType="MM" maxScaleDenominator="1e+08" scaleBasedVisibility="0" height="15" rotationOffset="270" barWidth="5" opacity="1" penAlpha="255" width="15">
      <fontProperties style="" description="MS Shell Dlg 2,7.8,-1,5,50,0,0,0,0,0"/>
      <attribute field="" color="#000000" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings dist="0" linePlacementFlags="18" obstacle="0" zIndex="0" priority="0" placement="2" showAll="1">
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
    <field name="orf_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_max_capacity">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_crest_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_sewerage">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_cross_section_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_friction_type">
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
    <field name="orf_discharge_coefficient_positive">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_discharge_coefficient_negative">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_zoom_category">
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
    <field name="orf_crest_type">
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
    <field name="orf_connection_node_start_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_connection_node_end_id">
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
    <alias index="1" field="orf_id" name=""/>
    <alias index="2" field="orf_display_name" name=""/>
    <alias index="3" field="orf_code" name=""/>
    <alias index="4" field="orf_max_capacity" name=""/>
    <alias index="5" field="orf_crest_level" name=""/>
    <alias index="6" field="orf_sewerage" name=""/>
    <alias index="7" field="orf_cross_section_definition_id" name=""/>
    <alias index="8" field="orf_friction_value" name=""/>
    <alias index="9" field="orf_friction_type" name=""/>
    <alias index="10" field="orf_discharge_coefficient_positive" name=""/>
    <alias index="11" field="orf_discharge_coefficient_negative" name=""/>
    <alias index="12" field="orf_zoom_category" name=""/>
    <alias index="13" field="orf_crest_type" name=""/>
    <alias index="14" field="orf_connection_node_start_id" name=""/>
    <alias index="15" field="orf_connection_node_end_id" name=""/>
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
    <default field="orf_id" applyOnUpdate="0" expression=""/>
    <default field="orf_display_name" applyOnUpdate="0" expression=""/>
    <default field="orf_code" applyOnUpdate="0" expression=""/>
    <default field="orf_max_capacity" applyOnUpdate="0" expression=""/>
    <default field="orf_crest_level" applyOnUpdate="0" expression=""/>
    <default field="orf_sewerage" applyOnUpdate="0" expression=""/>
    <default field="orf_cross_section_definition_id" applyOnUpdate="0" expression=""/>
    <default field="orf_friction_value" applyOnUpdate="0" expression=""/>
    <default field="orf_friction_type" applyOnUpdate="0" expression=""/>
    <default field="orf_discharge_coefficient_positive" applyOnUpdate="0" expression=""/>
    <default field="orf_discharge_coefficient_negative" applyOnUpdate="0" expression=""/>
    <default field="orf_zoom_category" applyOnUpdate="0" expression=""/>
    <default field="orf_crest_type" applyOnUpdate="0" expression=""/>
    <default field="orf_connection_node_start_id" applyOnUpdate="0" expression=""/>
    <default field="orf_connection_node_end_id" applyOnUpdate="0" expression=""/>
    <default field="def_id" applyOnUpdate="0" expression=""/>
    <default field="def_shape" applyOnUpdate="0" expression=""/>
    <default field="def_width" applyOnUpdate="0" expression=""/>
    <default field="def_height" applyOnUpdate="0" expression=""/>
    <default field="def_code" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="ROWID" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="orf_id" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="orf_display_name" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="orf_code" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="orf_max_capacity" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="orf_crest_level" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="orf_sewerage" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="orf_cross_section_definition_id" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="orf_friction_value" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="orf_friction_type" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="orf_discharge_coefficient_positive" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="orf_discharge_coefficient_negative" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="orf_zoom_category" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="orf_crest_type" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="orf_connection_node_start_id" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="orf_connection_node_end_id" notnull_strength="0"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="def_id" notnull_strength="2"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="def_shape" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="def_width" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="def_height" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="def_code" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="ROWID" exp=""/>
    <constraint desc="" field="orf_id" exp=""/>
    <constraint desc="" field="orf_display_name" exp=""/>
    <constraint desc="" field="orf_code" exp=""/>
    <constraint desc="" field="orf_max_capacity" exp=""/>
    <constraint desc="" field="orf_crest_level" exp=""/>
    <constraint desc="" field="orf_sewerage" exp=""/>
    <constraint desc="" field="orf_cross_section_definition_id" exp=""/>
    <constraint desc="" field="orf_friction_value" exp=""/>
    <constraint desc="" field="orf_friction_type" exp=""/>
    <constraint desc="" field="orf_discharge_coefficient_positive" exp=""/>
    <constraint desc="" field="orf_discharge_coefficient_negative" exp=""/>
    <constraint desc="" field="orf_zoom_category" exp=""/>
    <constraint desc="" field="orf_crest_type" exp=""/>
    <constraint desc="" field="orf_connection_node_start_id" exp=""/>
    <constraint desc="" field="orf_connection_node_end_id" exp=""/>
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
      <column width="-1" type="field" hidden="0" name="orf_id"/>
      <column width="-1" type="field" hidden="0" name="orf_display_name"/>
      <column width="-1" type="field" hidden="0" name="orf_code"/>
      <column width="-1" type="field" hidden="0" name="orf_max_capacity"/>
      <column width="-1" type="field" hidden="0" name="orf_crest_level"/>
      <column width="-1" type="field" hidden="0" name="orf_sewerage"/>
      <column width="-1" type="field" hidden="0" name="orf_cross_section_definition_id"/>
      <column width="-1" type="field" hidden="0" name="orf_friction_value"/>
      <column width="-1" type="field" hidden="0" name="orf_friction_type"/>
      <column width="-1" type="field" hidden="0" name="orf_discharge_coefficient_positive"/>
      <column width="-1" type="field" hidden="0" name="orf_discharge_coefficient_negative"/>
      <column width="-1" type="field" hidden="0" name="orf_zoom_category"/>
      <column width="-1" type="field" hidden="0" name="orf_crest_type"/>
      <column width="-1" type="field" hidden="0" name="orf_connection_node_start_id"/>
      <column width="-1" type="field" hidden="0" name="orf_connection_node_end_id"/>
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
        <attributeEditorField showLabel="1" index="-1" name="weir_id"/>
        <attributeEditorField showLabel="1" index="-1" name="weir_display_name"/>
        <attributeEditorField showLabel="1" index="-1" name="weir_code"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Characteristics">
        <attributeEditorField showLabel="1" index="-1" name="weir_crest_level"/>
        <attributeEditorField showLabel="1" index="-1" name="weir_crest_type"/>
        <attributeEditorField showLabel="1" index="-1" name="weir_discharge_coefficient_positive"/>
        <attributeEditorField showLabel="1" index="-1" name="weir_discharge_coefficient_negative"/>
        <attributeEditorField showLabel="1" index="-1" name="weir_friction_value"/>
        <attributeEditorField showLabel="1" index="-1" name="weir_friction_type"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Cross section">
        <attributeEditorField showLabel="1" index="-1" name="weir_cross_section_definition_id"/>
        <attributeEditorField showLabel="1" index="20" name="def_code"/>
        <attributeEditorField showLabel="1" index="17" name="def_shape"/>
        <attributeEditorField showLabel="1" index="18" name="def_width"/>
        <attributeEditorField showLabel="1" index="19" name="def_height"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Visualization">
        <attributeEditorField showLabel="1" index="-1" name="weir_sewerage"/>
        <attributeEditorField showLabel="1" index="-1" name="weir_external"/>
        <attributeEditorField showLabel="1" index="-1" name="weir_zoom_category"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Connection nodes">
        <attributeEditorField showLabel="1" index="-1" name="weir_connection_node_start_id"/>
        <attributeEditorField showLabel="1" index="-1" name="weir_connection_node_end_id"/>
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
