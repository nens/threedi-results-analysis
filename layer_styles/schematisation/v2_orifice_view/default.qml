<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" labelsEnabled="0" simplifyAlgorithm="0" simplifyMaxScale="1" version="3.10.10-A Coruña" simplifyDrawingTol="1" minScale="1e+08" simplifyLocal="1" maxScale="0" readOnly="0" simplifyDrawingHints="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" forceraster="0" symbollevels="0" type="singleSymbol">
    <symbols>
      <symbol clip_to_extent="1" alpha="1" name="0" type="line" force_rhr="0">
        <layer locked="0" pass="0" class="SimpleLine" enabled="1">
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" pass="0" class="MarkerLine" enabled="1">
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="coalesce(orf_discharge_coefficient_negative,0) = 0" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
                <Option name="offset" type="Map">
                  <Option value="false" name="active" type="bool"/>
                  <Option value="1" name="type" type="int"/>
                  <Option value="" name="val" type="QString"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="0.3333 * $length" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol clip_to_extent="1" alpha="1" name="@0@1" type="marker" force_rhr="0">
            <layer locked="0" pass="0" class="SimpleMarker" enabled="1">
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
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option value="false" name="active" type="bool"/>
                      <Option value="1" name="type" type="int"/>
                      <Option value="" name="val" type="QString"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option value="false" name="active" type="bool"/>
                      <Option value="1" name="type" type="int"/>
                      <Option value="" name="val" type="QString"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option value="false" name="active" type="bool"/>
                      <Option value="" name="expression" type="QString"/>
                      <Option value="3" name="type" type="int"/>
                    </Option>
                  </Option>
                  <Option value="collection" name="type" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer locked="0" pass="0" class="MarkerLine" enabled="1">
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="coalesce(orf_discharge_coefficient_positive,0) > 0&#xd;&#xa;AND coalesce(orf_discharge_coefficient_negative,0) = 0" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
                <Option name="offset" type="Map">
                  <Option value="false" name="active" type="bool"/>
                  <Option value="1" name="type" type="int"/>
                  <Option value="" name="val" type="QString"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="0.66 * $length" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol clip_to_extent="1" alpha="1" name="@0@2" type="marker" force_rhr="0">
            <layer locked="0" pass="0" class="SimpleMarker" enabled="1">
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
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option value="false" name="active" type="bool"/>
                      <Option value="1" name="type" type="int"/>
                      <Option value="" name="val" type="QString"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option value="false" name="active" type="bool"/>
                      <Option value="1" name="type" type="int"/>
                      <Option value="" name="val" type="QString"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option value="false" name="active" type="bool"/>
                      <Option value="" name="expression" type="QString"/>
                      <Option value="3" name="type" type="int"/>
                    </Option>
                  </Option>
                  <Option value="collection" name="type" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer locked="0" pass="0" class="MarkerLine" enabled="1">
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="coalesce(orf_discharge_coefficient_positive,0) = 0" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
                <Option name="offset" type="Map">
                  <Option value="false" name="active" type="bool"/>
                  <Option value="1" name="type" type="int"/>
                  <Option value="" name="val" type="QString"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="0.6667 * $length" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol clip_to_extent="1" alpha="1" name="@0@3" type="marker" force_rhr="0">
            <layer locked="0" pass="0" class="SimpleMarker" enabled="1">
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
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option value="false" name="active" type="bool"/>
                      <Option value="1" name="type" type="int"/>
                      <Option value="" name="val" type="QString"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option value="false" name="active" type="bool"/>
                      <Option value="1" name="type" type="int"/>
                      <Option value="" name="val" type="QString"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option value="false" name="active" type="bool"/>
                      <Option value="" name="expression" type="QString"/>
                      <Option value="3" name="type" type="int"/>
                    </Option>
                  </Option>
                  <Option value="collection" name="type" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer locked="0" pass="0" class="MarkerLine" enabled="1">
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="coalesce(orf_discharge_coefficient_negative, 0) > 0&#xd;&#xa;AND coalesce(orf_discharge_coefficient_positive,0) = 0" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
                <Option name="offset" type="Map">
                  <Option value="false" name="active" type="bool"/>
                  <Option value="1" name="type" type="int"/>
                  <Option value="" name="val" type="QString"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="0.33 * $length" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol clip_to_extent="1" alpha="1" name="@0@4" type="marker" force_rhr="0">
            <layer locked="0" pass="0" class="SimpleMarker" enabled="1">
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
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option value="false" name="active" type="bool"/>
                      <Option value="1" name="type" type="int"/>
                      <Option value="" name="val" type="QString"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option value="false" name="active" type="bool"/>
                      <Option value="1" name="type" type="int"/>
                      <Option value="" name="val" type="QString"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option value="false" name="active" type="bool"/>
                      <Option value="" name="expression" type="QString"/>
                      <Option value="3" name="type" type="int"/>
                    </Option>
                  </Option>
                  <Option value="collection" name="type" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer locked="0" pass="0" class="MarkerLine" enabled="1">
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol clip_to_extent="1" alpha="1" name="@0@5" type="marker" force_rhr="0">
            <layer locked="0" pass="0" class="SimpleMarker" enabled="1">
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
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="fillColor" type="Map">
                      <Option value="false" name="active" type="bool"/>
                      <Option value="1" name="type" type="int"/>
                      <Option value="" name="val" type="QString"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option value="true" name="active" type="bool"/>
                      <Option value="if(@map_scale&lt;10000, 3.4,2)" name="expression" type="QString"/>
                      <Option value="3" name="type" type="int"/>
                    </Option>
                  </Option>
                  <Option value="collection" name="type" type="QString"/>
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
      <text-style fontLetterSpacing="0" textColor="227,26,28,255" textOrientation="horizontal" blendMode="0" fieldName="coalesce(round(weir_crest_level, 2), 'NULL')" fontWordSpacing="0" fontUnderline="0" previewBkgrdColor="255,255,255,255" fontItalic="0" fontStrikeout="0" fontWeight="50" fontSizeUnit="Point" namedStyle="Standaard" fontSize="8" multilineHeight="1" textOpacity="1" useSubstitutions="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontKerning="1" isExpression="1" fontCapitals="0" fontFamily="MS Shell Dlg 2">
        <text-buffer bufferNoFill="0" bufferSizeUnits="MM" bufferBlendMode="0" bufferDraw="1" bufferOpacity="1" bufferColor="255,255,255,255" bufferJoinStyle="128" bufferSize="0.7" bufferSizeMapUnitScale="3x:0,0,0,0,0,0"/>
        <background shapeRotationType="0" shapeOffsetUnit="MM" shapeRadiiY="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeBlendMode="0" shapeDraw="0" shapeSizeY="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeFillColor="255,255,255,255" shapeBorderColor="128,128,128,255" shapeSizeType="0" shapeSVGFile="" shapeBorderWidth="0" shapeJoinStyle="64" shapeOffsetY="0" shapeBorderWidthUnit="MM" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiX="0" shapeRotation="0" shapeRadiiUnit="MM" shapeOpacity="1" shapeOffsetX="0" shapeSizeUnit="MM" shapeType="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeSizeX="0">
          <symbol clip_to_extent="1" alpha="1" name="markerSymbol" type="marker" force_rhr="0">
            <layer locked="0" pass="0" class="SimpleMarker" enabled="1">
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
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties"/>
                  <Option value="collection" name="type" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </background>
        <shadow shadowUnder="0" shadowOffsetGlobal="1" shadowScale="100" shadowOffsetAngle="135" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadius="1.5" shadowRadiusAlphaOnly="0" shadowColor="0,0,0,255" shadowBlendMode="6" shadowRadiusUnit="MM" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowDraw="0" shadowOffsetDist="1" shadowOpacity="0.7" shadowOffsetUnit="MM"/>
        <dd_properties>
          <Option type="Map">
            <Option value="" name="name" type="QString"/>
            <Option name="properties"/>
            <Option value="collection" name="type" type="QString"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format decimals="3" autoWrapLength="0" placeDirectionSymbol="0" leftDirectionSymbol="&lt;" plussign="0" formatNumbers="0" addDirectionSymbol="0" rightDirectionSymbol=">" reverseDirectionSymbol="0" wrapChar="" multilineAlign="0" useMaxLineLengthForAutoWrap="1"/>
      <placement layerType="LineGeometry" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" maxCurvedCharAngleIn="25" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorEnabled="1" offsetUnits="MM" repeatDistance="0" yOffset="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" rotationAngle="0" overrunDistance="0" offsetType="0" geometryGenerator="centroid($geometry)" overrunDistanceUnit="MM" placement="1" distUnits="MM" fitInPolygonOnly="0" preserveRotation="0" maxCurvedCharAngleOut="-25" xOffset="2" priority="5" repeatDistanceUnits="MM" dist="0" placementFlags="2" quadOffset="2" centroidInside="0" geometryGeneratorType="PointGeometry" centroidWhole="0" distMapUnitScale="3x:0,0,0,0,0,0"/>
      <rendering scaleVisibility="1" maxNumLabels="2000" mergeLines="0" obstacle="1" labelPerPart="0" fontMaxPixelSize="10000" fontMinPixelSize="3" obstacleType="0" limitNumLabels="0" zIndex="0" scaleMin="1" obstacleFactor="1" fontLimitPixelSize="0" drawLabels="1" minFeatureSize="0" upsidedownLabels="0" displayAll="1" scaleMax="2500"/>
      <dd_properties>
        <Option type="Map">
          <Option value="" name="name" type="QString"/>
          <Option name="properties" type="Map">
            <Option name="Hali" type="Map">
              <Option value="true" name="active" type="bool"/>
              <Option value="'Left'" name="expression" type="QString"/>
              <Option value="3" name="type" type="int"/>
            </Option>
            <Option name="LabelRotation" type="Map">
              <Option value="false" name="active" type="bool"/>
              <Option value="1" name="type" type="int"/>
              <Option value="" name="val" type="QString"/>
            </Option>
            <Option name="PositionX" type="Map">
              <Option value="false" name="active" type="bool"/>
              <Option value="1" name="type" type="int"/>
              <Option value="" name="val" type="QString"/>
            </Option>
            <Option name="PositionY" type="Map">
              <Option value="false" name="active" type="bool"/>
              <Option value="1" name="type" type="int"/>
              <Option value="" name="val" type="QString"/>
            </Option>
            <Option name="Show" type="Map">
              <Option value="true" name="active" type="bool"/>
              <Option value="intersects(transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;start_point( $geometry),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;  @map_crs  &#xd;&#xa;&#x9;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;&#x9;@map_extent&#xd;&#xa;)" name="expression" type="QString"/>
              <Option value="3" name="type" type="int"/>
            </Option>
            <Option name="Vali" type="Map">
              <Option value="true" name="active" type="bool"/>
              <Option value="'Top'" name="expression" type="QString"/>
              <Option value="3" name="type" type="int"/>
            </Option>
          </Option>
          <Option value="collection" name="type" type="QString"/>
        </Option>
      </dd_properties>
      <callout type="simple">
        <Option type="Map">
          <Option value="pole_of_inaccessibility" name="anchorPoint" type="QString"/>
          <Option name="ddProperties" type="Map">
            <Option value="" name="name" type="QString"/>
            <Option name="properties"/>
            <Option value="collection" name="type" type="QString"/>
          </Option>
          <Option value="false" name="drawToAllParts" type="bool"/>
          <Option value="0" name="enabled" type="QString"/>
          <Option value="&lt;symbol clip_to_extent=&quot;1&quot; alpha=&quot;1&quot; name=&quot;symbol&quot; type=&quot;line&quot; force_rhr=&quot;0&quot;>&lt;layer locked=&quot;0&quot; pass=&quot;0&quot; class=&quot;SimpleLine&quot; enabled=&quot;1&quot;>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; name=&quot;name&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; name=&quot;type&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" name="lineSymbol" type="QString"/>
          <Option value="0" name="minLength" type="double"/>
          <Option value="3x:0,0,0,0,0,0" name="minLengthMapUnitScale" type="QString"/>
          <Option value="MM" name="minLengthUnit" type="QString"/>
          <Option value="0" name="offsetFromAnchor" type="double"/>
          <Option value="3x:0,0,0,0,0,0" name="offsetFromAnchorMapUnitScale" type="QString"/>
          <Option value="MM" name="offsetFromAnchorUnit" type="QString"/>
          <Option value="0" name="offsetFromLabel" type="double"/>
          <Option value="3x:0,0,0,0,0,0" name="offsetFromLabelMapUnitScale" type="QString"/>
          <Option value="MM" name="offsetFromLabelUnit" type="QString"/>
        </Option>
      </callout>
    </settings>
  </labeling>
  <customproperties>
    <property value="&quot;ROWID&quot;" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Pie" attributeLegend="1">
    <DiagramCategory height="15" scaleDependency="Area" width="15" enabled="0" maxScaleDenominator="1e+08" penAlpha="255" sizeType="MM" backgroundColor="#ffffff" diagramOrientation="Up" labelPlacementMethod="XHeight" rotationOffset="270" penWidth="0" minScaleDenominator="0" backgroundAlpha="255" sizeScale="3x:0,0,0,0,0,0" barWidth="5" minimumSize="0" lineSizeScale="3x:0,0,0,0,0,0" penColor="#000000" lineSizeType="MM" opacity="1" scaleBasedVisibility="0">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute field="" label="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings showAll="1" placement="2" dist="0" zIndex="0" obstacle="0" priority="0" linePlacementFlags="2">
    <properties>
      <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
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
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_crest_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_sewerage">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" name="CheckedState" type="QString"/>
            <Option value="0" name="UncheckedState" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_cross_section_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
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
                <Option value="1" name="1: Chèzy" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2: Manning" type="QString"/>
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
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_discharge_coefficient_negative">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
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
                <Option value="-1" name="-1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="0" name="0" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="1" name="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="3" name="3" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="4" name="4" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="5" name="5" type="QString"/>
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
                <Option value="3" name="3: broad crested" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="4" name="4: short crested" type="QString"/>
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
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_connection_node_end_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
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
                <Option value="1" name="1: rectangle" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2: round" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="3" name="3: egg" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="5" name="5: tabulated rectangle" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="6" name="6: tabulated trapezium" type="QString"/>
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
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_height">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="ROWID" index="0" name=""/>
    <alias field="orf_id" index="1" name="id"/>
    <alias field="orf_display_name" index="2" name="display_name"/>
    <alias field="orf_code" index="3" name="code"/>
    <alias field="orf_crest_level" index="4" name="crest_level"/>
    <alias field="orf_sewerage" index="5" name="sewerage"/>
    <alias field="orf_cross_section_definition_id" index="6" name="cross_section_definition_id"/>
    <alias field="orf_friction_value" index="7" name="friction_value"/>
    <alias field="orf_friction_type" index="8" name="friction_type"/>
    <alias field="orf_discharge_coefficient_positive" index="9" name="discharge_coefficient_positive"/>
    <alias field="orf_discharge_coefficient_negative" index="10" name="discharge_coefficient_negative"/>
    <alias field="orf_zoom_category" index="11" name="zoom_category"/>
    <alias field="orf_crest_type" index="12" name="crest_type"/>
    <alias field="orf_connection_node_start_id" index="13" name="connection_node_start_id"/>
    <alias field="orf_connection_node_end_id" index="14" name="connection_node_end_id"/>
    <alias field="def_id" index="15" name="id"/>
    <alias field="def_shape" index="16" name="shape"/>
    <alias field="def_width" index="17" name="width"/>
    <alias field="def_height" index="18" name="height"/>
    <alias field="def_code" index="19" name="code"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="ROWID" applyOnUpdate="0" expression=""/>
    <default field="orf_id" applyOnUpdate="0" expression="if(maximum(orf_id) is null,1, maximum(orf_id)+1)"/>
    <default field="orf_display_name" applyOnUpdate="0" expression="'new'"/>
    <default field="orf_code" applyOnUpdate="0" expression="'new'"/>
    <default field="orf_crest_level" applyOnUpdate="0" expression=""/>
    <default field="orf_sewerage" applyOnUpdate="0" expression=""/>
    <default field="orf_cross_section_definition_id" applyOnUpdate="0" expression=""/>
    <default field="orf_friction_value" applyOnUpdate="0" expression="0.02"/>
    <default field="orf_friction_type" applyOnUpdate="0" expression="2"/>
    <default field="orf_discharge_coefficient_positive" applyOnUpdate="0" expression="0.8"/>
    <default field="orf_discharge_coefficient_negative" applyOnUpdate="0" expression="0.8"/>
    <default field="orf_zoom_category" applyOnUpdate="0" expression="3"/>
    <default field="orf_crest_type" applyOnUpdate="0" expression="4"/>
    <default field="orf_connection_node_start_id" applyOnUpdate="0" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))) is null, 'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))))"/>
    <default field="orf_connection_node_end_id" applyOnUpdate="0" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))) is null, 'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))))"/>
    <default field="def_id" applyOnUpdate="0" expression=""/>
    <default field="def_shape" applyOnUpdate="0" expression=""/>
    <default field="def_width" applyOnUpdate="0" expression=""/>
    <default field="def_height" applyOnUpdate="0" expression=""/>
    <default field="def_code" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint field="ROWID" exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="orf_id" exp_strength="0" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint field="orf_display_name" exp_strength="2" constraints="5" notnull_strength="2" unique_strength="0"/>
    <constraint field="orf_code" exp_strength="2" constraints="5" notnull_strength="2" unique_strength="0"/>
    <constraint field="orf_crest_level" exp_strength="0" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint field="orf_sewerage" exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="orf_cross_section_definition_id" exp_strength="0" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint field="orf_friction_value" exp_strength="2" constraints="5" notnull_strength="2" unique_strength="0"/>
    <constraint field="orf_friction_type" exp_strength="0" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint field="orf_discharge_coefficient_positive" exp_strength="0" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint field="orf_discharge_coefficient_negative" exp_strength="0" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint field="orf_zoom_category" exp_strength="0" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint field="orf_crest_type" exp_strength="0" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint field="orf_connection_node_start_id" exp_strength="0" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint field="orf_connection_node_end_id" exp_strength="0" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint field="def_id" exp_strength="0" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint field="def_shape" exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="def_width" exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="def_height" exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="def_code" exp_strength="0" constraints="0" notnull_strength="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="ROWID" exp="" desc=""/>
    <constraint field="orf_id" exp="" desc=""/>
    <constraint field="orf_display_name" exp="&quot;orf_display_name&quot; is not null" desc=""/>
    <constraint field="orf_code" exp="&quot;orf_code&quot; is not null&#xd;&#xa;" desc=""/>
    <constraint field="orf_crest_level" exp="" desc=""/>
    <constraint field="orf_sewerage" exp="" desc=""/>
    <constraint field="orf_cross_section_definition_id" exp="" desc=""/>
    <constraint field="orf_friction_value" exp="&quot;orf_friction_value&quot; is not null" desc=""/>
    <constraint field="orf_friction_type" exp="" desc=""/>
    <constraint field="orf_discharge_coefficient_positive" exp="" desc=""/>
    <constraint field="orf_discharge_coefficient_negative" exp="" desc=""/>
    <constraint field="orf_zoom_category" exp="" desc=""/>
    <constraint field="orf_crest_type" exp="" desc=""/>
    <constraint field="orf_connection_node_start_id" exp="" desc=""/>
    <constraint field="orf_connection_node_end_id" exp="" desc=""/>
    <constraint field="def_id" exp="" desc=""/>
    <constraint field="def_shape" exp="" desc=""/>
    <constraint field="def_width" exp="" desc=""/>
    <constraint field="def_height" exp="" desc=""/>
    <constraint field="def_code" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortExpression="&quot;orf_discharge_coefficient_negative&quot;" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column hidden="0" width="-1" name="ROWID" type="field"/>
      <column hidden="0" width="-1" name="orf_id" type="field"/>
      <column hidden="0" width="-1" name="orf_display_name" type="field"/>
      <column hidden="0" width="-1" name="orf_code" type="field"/>
      <column hidden="0" width="-1" name="orf_crest_level" type="field"/>
      <column hidden="0" width="-1" name="orf_sewerage" type="field"/>
      <column hidden="0" width="-1" name="orf_cross_section_definition_id" type="field"/>
      <column hidden="0" width="-1" name="orf_friction_value" type="field"/>
      <column hidden="0" width="-1" name="orf_friction_type" type="field"/>
      <column hidden="0" width="-1" name="orf_discharge_coefficient_positive" type="field"/>
      <column hidden="0" width="-1" name="orf_discharge_coefficient_negative" type="field"/>
      <column hidden="0" width="-1" name="orf_zoom_category" type="field"/>
      <column hidden="0" width="-1" name="orf_crest_type" type="field"/>
      <column hidden="0" width="-1" name="orf_connection_node_start_id" type="field"/>
      <column hidden="0" width="-1" name="orf_connection_node_end_id" type="field"/>
      <column hidden="0" width="-1" name="def_id" type="field"/>
      <column hidden="0" width="-1" name="def_shape" type="field"/>
      <column hidden="0" width="-1" name="def_width" type="field"/>
      <column hidden="0" width="-1" name="def_height" type="field"/>
      <column hidden="0" width="-1" name="def_code" type="field"/>
      <column hidden="1" width="-1" type="actions"/>
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
    <attributeEditorContainer visibilityExpressionEnabled="0" groupBox="0" columnCount="1" name="Orifice view" showLabel="1" visibilityExpression="">
      <attributeEditorContainer visibilityExpressionEnabled="0" groupBox="1" columnCount="1" name="General" showLabel="1" visibilityExpression="">
        <attributeEditorField index="1" name="orf_id" showLabel="1"/>
        <attributeEditorField index="2" name="orf_display_name" showLabel="1"/>
        <attributeEditorField index="3" name="orf_code" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpressionEnabled="0" groupBox="1" columnCount="1" name="Characteristics" showLabel="1" visibilityExpression="">
        <attributeEditorField index="4" name="orf_crest_level" showLabel="1"/>
        <attributeEditorField index="12" name="orf_crest_type" showLabel="1"/>
        <attributeEditorField index="7" name="orf_friction_value" showLabel="1"/>
        <attributeEditorField index="8" name="orf_friction_type" showLabel="1"/>
        <attributeEditorField index="9" name="orf_discharge_coefficient_positive" showLabel="1"/>
        <attributeEditorField index="10" name="orf_discharge_coefficient_negative" showLabel="1"/>
        <attributeEditorField index="-1" name="orf_max_capacity" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpressionEnabled="0" groupBox="1" columnCount="1" name="Visualization" showLabel="1" visibilityExpression="">
        <attributeEditorField index="5" name="orf_sewerage" showLabel="1"/>
        <attributeEditorField index="11" name="orf_zoom_category" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpressionEnabled="0" groupBox="1" columnCount="1" name="Cross section" showLabel="1" visibilityExpression="">
        <attributeEditorField index="6" name="orf_cross_section_definition_id" showLabel="1"/>
        <attributeEditorField index="16" name="def_shape" showLabel="1"/>
        <attributeEditorField index="17" name="def_width" showLabel="1"/>
        <attributeEditorField index="18" name="def_height" showLabel="1"/>
        <attributeEditorField index="19" name="def_code" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpressionEnabled="0" groupBox="1" columnCount="1" name="Connection nodes" showLabel="1" visibilityExpression="">
        <attributeEditorField index="13" name="orf_connection_node_start_id" showLabel="1"/>
        <attributeEditorField index="14" name="orf_connection_node_end_id" showLabel="1"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="ROWID"/>
    <field editable="0" name="def_code"/>
    <field editable="0" name="def_height"/>
    <field editable="1" name="def_id"/>
    <field editable="0" name="def_shape"/>
    <field editable="0" name="def_width"/>
    <field editable="1" name="orf_code"/>
    <field editable="0" name="orf_connection_node_end_id"/>
    <field editable="0" name="orf_connection_node_start_id"/>
    <field editable="1" name="orf_crest_level"/>
    <field editable="1" name="orf_crest_type"/>
    <field editable="1" name="orf_cross_section_definition_id"/>
    <field editable="1" name="orf_discharge_coefficient_negative"/>
    <field editable="1" name="orf_discharge_coefficient_positive"/>
    <field editable="1" name="orf_display_name"/>
    <field editable="1" name="orf_friction_type"/>
    <field editable="1" name="orf_friction_value"/>
    <field editable="1" name="orf_id"/>
    <field editable="1" name="orf_max_capacity"/>
    <field editable="1" name="orf_sewerage"/>
    <field editable="1" name="orf_zoom_category"/>
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
  </labelOnTop>
  <widgets/>
  <previewExpression>"ROWID"</previewExpression>
  <mapTip>weir_display_name</mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
