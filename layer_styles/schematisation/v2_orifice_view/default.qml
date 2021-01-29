<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.10.10-A Coruña" simplifyMaxScale="1" labelsEnabled="0" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" readOnly="0" minScale="1e+08" simplifyAlgorithm="0" maxScale="0" simplifyDrawingHints="1" simplifyLocal="1" simplifyDrawingTol="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" enableorderby="0" type="singleSymbol" forceraster="0">
    <symbols>
      <symbol alpha="1" name="0" force_rhr="0" clip_to_extent="1" type="line">
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" enabled="1" class="MarkerLine" locked="0">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="orf_discharge_coefficient_negative = 0"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="offset" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="type" type="int" value="1"/>
                  <Option name="val" type="QString" value=""/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="0.3333 * $length"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol alpha="1" name="@0@1" force_rhr="0" clip_to_extent="1" type="marker">
            <layer pass="0" enabled="1" class="SimpleMarker" locked="0">
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
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="type" type="int" value="1"/>
                      <Option name="val" type="QString" value=""/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value=""/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                  </Option>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer pass="0" enabled="1" class="MarkerLine" locked="0">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="orf_discharge_coefficient_positive > 0&#xd;&#xa;AND orf_discharge_coefficient_negative = 0"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="offset" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="type" type="int" value="1"/>
                  <Option name="val" type="QString" value=""/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="0.66 * $length"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol alpha="1" name="@0@2" force_rhr="0" clip_to_extent="1" type="marker">
            <layer pass="0" enabled="1" class="SimpleMarker" locked="0">
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
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="type" type="int" value="1"/>
                      <Option name="val" type="QString" value=""/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value=""/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                  </Option>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer pass="0" enabled="1" class="MarkerLine" locked="0">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="orf_discharge_coefficient_positive = 0"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="offset" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="type" type="int" value="1"/>
                  <Option name="val" type="QString" value=""/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="0.6667 * $length"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol alpha="1" name="@0@3" force_rhr="0" clip_to_extent="1" type="marker">
            <layer pass="0" enabled="1" class="SimpleMarker" locked="0">
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
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="type" type="int" value="1"/>
                      <Option name="val" type="QString" value=""/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value=""/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                  </Option>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer pass="0" enabled="1" class="MarkerLine" locked="0">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="orf_discharge_coefficient_negative > 0&#xd;&#xa;AND orf_discharge_coefficient_positive = 0"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="offset" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="type" type="int" value="1"/>
                  <Option name="val" type="QString" value=""/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="0.33 * $length"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol alpha="1" name="@0@4" force_rhr="0" clip_to_extent="1" type="marker">
            <layer pass="0" enabled="1" class="SimpleMarker" locked="0">
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
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="type" type="int" value="1"/>
                      <Option name="val" type="QString" value=""/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value=""/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                  </Option>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer pass="0" enabled="1" class="MarkerLine" locked="0">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol alpha="1" name="@0@5" force_rhr="0" clip_to_extent="1" type="marker">
            <layer pass="0" enabled="1" class="SimpleMarker" locked="0">
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
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties" type="Map">
                    <Option name="fillColor" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="type" type="int" value="1"/>
                      <Option name="val" type="QString" value=""/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="if(@map_scale&lt;10000, 3.4,2)"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                  </Option>
                  <Option name="type" type="QString" value="collection"/>
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
      <text-style fontWordSpacing="0" fontSize="8" fontSizeUnit="Point" blendMode="0" isExpression="1" fieldName="coalesce(round(weir_crest_level, 2), 'NULL')" fontFamily="MS Shell Dlg 2" multilineHeight="1" textOrientation="horizontal" fontWeight="50" textColor="227,26,28,255" fontKerning="1" fontItalic="0" previewBkgrdColor="255,255,255,255" namedStyle="Standaard" fontStrikeout="0" textOpacity="1" fontCapitals="0" fontUnderline="0" useSubstitutions="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontLetterSpacing="0">
        <text-buffer bufferSize="0.7" bufferNoFill="0" bufferOpacity="1" bufferColor="255,255,255,255" bufferSizeUnits="MM" bufferBlendMode="0" bufferDraw="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferJoinStyle="128"/>
        <background shapeOpacity="1" shapeBorderColor="128,128,128,255" shapeOffsetX="0" shapeType="0" shapeFillColor="255,255,255,255" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetY="0" shapeSizeUnit="MM" shapeBorderWidth="0" shapeBlendMode="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeRotation="0" shapeRadiiY="0" shapeSVGFile="" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeY="0" shapeDraw="0" shapeRadiiX="0" shapeSizeType="0" shapeBorderWidthUnit="MM" shapeRotationType="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetUnit="MM" shapeRadiiUnit="MM" shapeJoinStyle="64" shapeSizeX="0">
          <symbol alpha="1" name="markerSymbol" force_rhr="0" clip_to_extent="1" type="marker">
            <layer pass="0" enabled="1" class="SimpleMarker" locked="0">
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
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties"/>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </background>
        <shadow shadowOffsetAngle="135" shadowRadiusUnit="MM" shadowScale="100" shadowDraw="0" shadowUnder="0" shadowBlendMode="6" shadowRadiusAlphaOnly="0" shadowOffsetDist="1" shadowColor="0,0,0,255" shadowOffsetGlobal="1" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetUnit="MM" shadowRadius="1.5" shadowOpacity="0.7"/>
        <dd_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format addDirectionSymbol="0" rightDirectionSymbol=">" useMaxLineLengthForAutoWrap="1" plussign="0" autoWrapLength="0" decimals="3" multilineAlign="0" placeDirectionSymbol="0" reverseDirectionSymbol="0" formatNumbers="0" wrapChar="" leftDirectionSymbol="&lt;"/>
      <placement repeatDistance="0" overrunDistanceUnit="MM" geometryGenerator="centroid($geometry)" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" placementFlags="2" yOffset="0" overrunDistance="0" dist="0" placement="1" offsetUnits="MM" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" preserveRotation="0" maxCurvedCharAngleOut="-25" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" priority="5" centroidInside="0" layerType="LineGeometry" xOffset="2" geometryGeneratorEnabled="1" offsetType="0" centroidWhole="0" rotationAngle="0" distUnits="MM" repeatDistanceUnits="MM" distMapUnitScale="3x:0,0,0,0,0,0" quadOffset="2" maxCurvedCharAngleIn="25" geometryGeneratorType="PointGeometry"/>
      <rendering obstacle="1" scaleMin="1" fontLimitPixelSize="0" limitNumLabels="0" obstacleType="0" displayAll="1" labelPerPart="0" scaleVisibility="1" fontMaxPixelSize="10000" drawLabels="1" minFeatureSize="0" upsidedownLabels="0" zIndex="0" obstacleFactor="1" maxNumLabels="2000" mergeLines="0" fontMinPixelSize="3" scaleMax="2500"/>
      <dd_properties>
        <Option type="Map">
          <Option name="name" type="QString" value=""/>
          <Option name="properties" type="Map">
            <Option name="Hali" type="Map">
              <Option name="active" type="bool" value="true"/>
              <Option name="expression" type="QString" value="'Left'"/>
              <Option name="type" type="int" value="3"/>
            </Option>
            <Option name="LabelRotation" type="Map">
              <Option name="active" type="bool" value="false"/>
              <Option name="type" type="int" value="1"/>
              <Option name="val" type="QString" value=""/>
            </Option>
            <Option name="PositionX" type="Map">
              <Option name="active" type="bool" value="false"/>
              <Option name="type" type="int" value="1"/>
              <Option name="val" type="QString" value=""/>
            </Option>
            <Option name="PositionY" type="Map">
              <Option name="active" type="bool" value="false"/>
              <Option name="type" type="int" value="1"/>
              <Option name="val" type="QString" value=""/>
            </Option>
            <Option name="Show" type="Map">
              <Option name="active" type="bool" value="true"/>
              <Option name="expression" type="QString" value="intersects(transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;start_point( $geometry),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;  @map_crs  &#xd;&#xa;&#x9;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;&#x9;@map_extent&#xd;&#xa;)"/>
              <Option name="type" type="int" value="3"/>
            </Option>
            <Option name="Vali" type="Map">
              <Option name="active" type="bool" value="true"/>
              <Option name="expression" type="QString" value="'Top'"/>
              <Option name="type" type="int" value="3"/>
            </Option>
          </Option>
          <Option name="type" type="QString" value="collection"/>
        </Option>
      </dd_properties>
      <callout type="simple">
        <Option type="Map">
          <Option name="anchorPoint" type="QString" value="pole_of_inaccessibility"/>
          <Option name="ddProperties" type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
          <Option name="drawToAllParts" type="bool" value="false"/>
          <Option name="enabled" type="QString" value="0"/>
          <Option name="lineSymbol" type="QString" value="&lt;symbol alpha=&quot;1&quot; name=&quot;symbol&quot; force_rhr=&quot;0&quot; clip_to_extent=&quot;1&quot; type=&quot;line&quot;>&lt;layer pass=&quot;0&quot; enabled=&quot;1&quot; class=&quot;SimpleLine&quot; locked=&quot;0&quot;>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; type=&quot;QString&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; type=&quot;QString&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
          <Option name="minLength" type="double" value="0"/>
          <Option name="minLengthMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
          <Option name="minLengthUnit" type="QString" value="MM"/>
          <Option name="offsetFromAnchor" type="double" value="0"/>
          <Option name="offsetFromAnchorMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
          <Option name="offsetFromAnchorUnit" type="QString" value="MM"/>
          <Option name="offsetFromLabel" type="double" value="0"/>
          <Option name="offsetFromLabelMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
          <Option name="offsetFromLabelUnit" type="QString" value="MM"/>
        </Option>
      </callout>
    </settings>
  </labeling>
  <customproperties>
    <property key="dualview/previewExpressions" value="&quot;ROWID&quot;"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Pie" attributeLegend="1">
    <DiagramCategory sizeScale="3x:0,0,0,0,0,0" minScaleDenominator="0" height="15" sizeType="MM" penWidth="0" penColor="#000000" rotationOffset="270" width="15" scaleDependency="Area" lineSizeType="MM" labelPlacementMethod="XHeight" diagramOrientation="Up" enabled="0" lineSizeScale="3x:0,0,0,0,0,0" barWidth="5" backgroundColor="#ffffff" backgroundAlpha="255" maxScaleDenominator="1e+08" scaleBasedVisibility="0" opacity="1" penAlpha="255" minimumSize="0">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute color="#000000" field="" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings placement="2" priority="0" zIndex="0" obstacle="0" dist="0" showAll="1" linePlacementFlags="2">
    <properties>
      <Option type="Map">
        <Option name="name" type="QString" value=""/>
        <Option name="properties"/>
        <Option name="type" type="QString" value="collection"/>
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
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_max_capacity">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_crest_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_sewerage">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option name="CheckedState" type="QString" value="1"/>
            <Option name="UncheckedState" type="QString" value="0"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_cross_section_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
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
                <Option name="1: Chèzy" type="QString" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="2: Manning" type="QString" value="2"/>
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
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_discharge_coefficient_negative">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
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
                <Option name="-1" type="QString" value="-1"/>
              </Option>
              <Option type="Map">
                <Option name="0" type="QString" value="0"/>
              </Option>
              <Option type="Map">
                <Option name="1" type="QString" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="2" type="QString" value="2"/>
              </Option>
              <Option type="Map">
                <Option name="3" type="QString" value="3"/>
              </Option>
              <Option type="Map">
                <Option name="4" type="QString" value="4"/>
              </Option>
              <Option type="Map">
                <Option name="5" type="QString" value="5"/>
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
                <Option name="3: broad crested" type="QString" value="3"/>
              </Option>
              <Option type="Map">
                <Option name="4: short crested" type="QString" value="4"/>
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
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_connection_node_end_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
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
                <Option name="1: rectangle" type="QString" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="2: round" type="QString" value="2"/>
              </Option>
              <Option type="Map">
                <Option name="3: egg" type="QString" value="3"/>
              </Option>
              <Option type="Map">
                <Option name="5: tabulated rectangle" type="QString" value="5"/>
              </Option>
              <Option type="Map">
                <Option name="6: tabulated trapezium" type="QString" value="6"/>
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
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_height">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="ROWID" index="0"/>
    <alias name="id" field="orf_id" index="1"/>
    <alias name="display_name" field="orf_display_name" index="2"/>
    <alias name="code" field="orf_code" index="3"/>
    <alias name="max_capacity" field="orf_max_capacity" index="4"/>
    <alias name="crest_level" field="orf_crest_level" index="5"/>
    <alias name="sewerage" field="orf_sewerage" index="6"/>
    <alias name="cross_section_definition_id" field="orf_cross_section_definition_id" index="7"/>
    <alias name="friction_value" field="orf_friction_value" index="8"/>
    <alias name="friction_type" field="orf_friction_type" index="9"/>
    <alias name="discharge_coefficient_positive" field="orf_discharge_coefficient_positive" index="10"/>
    <alias name="discharge_coefficient_negative" field="orf_discharge_coefficient_negative" index="11"/>
    <alias name="zoom_category" field="orf_zoom_category" index="12"/>
    <alias name="crest_type" field="orf_crest_type" index="13"/>
    <alias name="connection_node_start_id" field="orf_connection_node_start_id" index="14"/>
    <alias name="connection_node_end_id" field="orf_connection_node_end_id" index="15"/>
    <alias name="id" field="def_id" index="16"/>
    <alias name="shape" field="def_shape" index="17"/>
    <alias name="width" field="def_width" index="18"/>
    <alias name="height" field="def_height" index="19"/>
    <alias name="code" field="def_code" index="20"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" field="ROWID" applyOnUpdate="0"/>
    <default expression="if(maximum(orf_id) is null,1, maximum(orf_id)+1)" field="orf_id" applyOnUpdate="0"/>
    <default expression="'new'" field="orf_display_name" applyOnUpdate="0"/>
    <default expression="'new'" field="orf_code" applyOnUpdate="0"/>
    <default expression="" field="orf_max_capacity" applyOnUpdate="0"/>
    <default expression="" field="orf_crest_level" applyOnUpdate="0"/>
    <default expression="" field="orf_sewerage" applyOnUpdate="0"/>
    <default expression="" field="orf_cross_section_definition_id" applyOnUpdate="0"/>
    <default expression="0.02" field="orf_friction_value" applyOnUpdate="0"/>
    <default expression="2" field="orf_friction_type" applyOnUpdate="0"/>
    <default expression="0.8" field="orf_discharge_coefficient_positive" applyOnUpdate="0"/>
    <default expression="0.8" field="orf_discharge_coefficient_negative" applyOnUpdate="0"/>
    <default expression="3" field="orf_zoom_category" applyOnUpdate="0"/>
    <default expression="4" field="orf_crest_type" applyOnUpdate="0"/>
    <default expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))) is null, 'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))))" field="orf_connection_node_start_id" applyOnUpdate="0"/>
    <default expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))) is null, 'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))))" field="orf_connection_node_end_id" applyOnUpdate="0"/>
    <default expression="" field="def_id" applyOnUpdate="0"/>
    <default expression="" field="def_shape" applyOnUpdate="0"/>
    <default expression="" field="def_width" applyOnUpdate="0"/>
    <default expression="" field="def_height" applyOnUpdate="0"/>
    <default expression="" field="def_code" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint constraints="0" unique_strength="0" field="ROWID" notnull_strength="0" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" field="orf_id" notnull_strength="2" exp_strength="0"/>
    <constraint constraints="5" unique_strength="0" field="orf_display_name" notnull_strength="2" exp_strength="2"/>
    <constraint constraints="5" unique_strength="0" field="orf_code" notnull_strength="2" exp_strength="2"/>
    <constraint constraints="0" unique_strength="0" field="orf_max_capacity" notnull_strength="0" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" field="orf_crest_level" notnull_strength="2" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="orf_sewerage" notnull_strength="0" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" field="orf_cross_section_definition_id" notnull_strength="2" exp_strength="0"/>
    <constraint constraints="5" unique_strength="0" field="orf_friction_value" notnull_strength="2" exp_strength="2"/>
    <constraint constraints="1" unique_strength="0" field="orf_friction_type" notnull_strength="2" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" field="orf_discharge_coefficient_positive" notnull_strength="2" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" field="orf_discharge_coefficient_negative" notnull_strength="2" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" field="orf_zoom_category" notnull_strength="2" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" field="orf_crest_type" notnull_strength="2" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" field="orf_connection_node_start_id" notnull_strength="2" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" field="orf_connection_node_end_id" notnull_strength="2" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" field="def_id" notnull_strength="2" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="def_shape" notnull_strength="0" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="def_width" notnull_strength="0" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="def_height" notnull_strength="0" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" field="def_code" notnull_strength="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="ROWID" exp=""/>
    <constraint desc="" field="orf_id" exp=""/>
    <constraint desc="" field="orf_display_name" exp="&quot;orf_display_name&quot; is not null"/>
    <constraint desc="" field="orf_code" exp="&quot;orf_code&quot; is not null&#xd;&#xa;"/>
    <constraint desc="" field="orf_max_capacity" exp=""/>
    <constraint desc="" field="orf_crest_level" exp=""/>
    <constraint desc="" field="orf_sewerage" exp=""/>
    <constraint desc="" field="orf_cross_section_definition_id" exp=""/>
    <constraint desc="" field="orf_friction_value" exp="&quot;orf_friction_value&quot; is not null"/>
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
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="&quot;orf_discharge_coefficient_negative&quot;">
    <columns>
      <column name="ROWID" type="field" width="-1" hidden="0"/>
      <column name="orf_id" type="field" width="-1" hidden="0"/>
      <column name="orf_display_name" type="field" width="-1" hidden="0"/>
      <column name="orf_code" type="field" width="-1" hidden="0"/>
      <column name="orf_max_capacity" type="field" width="-1" hidden="0"/>
      <column name="orf_crest_level" type="field" width="-1" hidden="0"/>
      <column name="orf_sewerage" type="field" width="-1" hidden="0"/>
      <column name="orf_cross_section_definition_id" type="field" width="-1" hidden="0"/>
      <column name="orf_friction_value" type="field" width="-1" hidden="0"/>
      <column name="orf_friction_type" type="field" width="-1" hidden="0"/>
      <column name="orf_discharge_coefficient_positive" type="field" width="-1" hidden="0"/>
      <column name="orf_discharge_coefficient_negative" type="field" width="-1" hidden="0"/>
      <column name="orf_zoom_category" type="field" width="-1" hidden="0"/>
      <column name="orf_crest_type" type="field" width="-1" hidden="0"/>
      <column name="orf_connection_node_start_id" type="field" width="-1" hidden="0"/>
      <column name="orf_connection_node_end_id" type="field" width="-1" hidden="0"/>
      <column name="def_id" type="field" width="-1" hidden="0"/>
      <column name="def_shape" type="field" width="-1" hidden="0"/>
      <column name="def_width" type="field" width="-1" hidden="0"/>
      <column name="def_height" type="field" width="-1" hidden="0"/>
      <column name="def_code" type="field" width="-1" hidden="0"/>
      <column type="actions" width="-1" hidden="1"/>
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
    <attributeEditorContainer columnCount="1" name="Orifice view" visibilityExpression="" groupBox="0" visibilityExpressionEnabled="0" showLabel="1">
      <attributeEditorContainer columnCount="1" name="General" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="orf_id" index="1" showLabel="1"/>
        <attributeEditorField name="orf_display_name" index="2" showLabel="1"/>
        <attributeEditorField name="orf_code" index="3" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" name="Characteristics" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="orf_crest_level" index="5" showLabel="1"/>
        <attributeEditorField name="orf_crest_type" index="13" showLabel="1"/>
        <attributeEditorField name="orf_friction_value" index="8" showLabel="1"/>
        <attributeEditorField name="orf_friction_type" index="9" showLabel="1"/>
        <attributeEditorField name="orf_discharge_coefficient_positive" index="10" showLabel="1"/>
        <attributeEditorField name="orf_discharge_coefficient_negative" index="11" showLabel="1"/>
        <attributeEditorField name="orf_max_capacity" index="4" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" name="Visualization" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="orf_sewerage" index="6" showLabel="1"/>
        <attributeEditorField name="orf_zoom_category" index="12" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" name="Cross section" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="orf_cross_section_definition_id" index="7" showLabel="1"/>
        <attributeEditorField name="def_shape" index="17" showLabel="1"/>
        <attributeEditorField name="def_width" index="18" showLabel="1"/>
        <attributeEditorField name="def_height" index="19" showLabel="1"/>
        <attributeEditorField name="def_code" index="20" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" name="Connection nodes" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="orf_connection_node_start_id" index="14" showLabel="1"/>
        <attributeEditorField name="orf_connection_node_end_id" index="15" showLabel="1"/>
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
