<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyMaxScale="1" styleCategories="AllStyleCategories" simplifyAlgorithm="0" readOnly="0" labelsEnabled="1" hasScaleBasedVisibilityFlag="0" simplifyDrawingTol="1" maxScale="-4.65661e-10" version="3.10.10-A Coruña" minScale="1e+08" simplifyDrawingHints="1" simplifyLocal="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" type="singleSymbol" enableorderby="0" symbollevels="0">
    <symbols>
      <symbol name="0" type="line" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="101,101,101,255" k="line_color"/>
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" enabled="1" locked="0" class="MarkerLine">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="10" k="interval"/>
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
          <prop v="0" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;"/>
                  <Option name="type" type="int" value="3"/>
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
          <symbol name="@0@1" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
            <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="arrowhead" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="101,101,101,255" k="outline_color"/>
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
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="line_interpolate_angle($geometry, length($geometry) * 0.33) + if(cul_invert_level_start_point > cul_invert_level_end_point, -90, 90)"/>
                      <Option name="type" type="int" value="3"/>
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
          <prop v="1" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@0@2" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
            <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="101,101,101,255" k="color"/>
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
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="rule-based">
    <rules key="{f1cc3d98-67c9-46db-8c88-5d864daa8620}">
      <rule key="{d3e3a8d9-62b8-46c0-bb29-30d228edf624}" description="Start point label" scalemaxdenom="1000">
        <settings calloutType="simple">
          <text-style previewBkgrdColor="255,255,255,255" textOpacity="1" isExpression="1" blendMode="0" fontStrikeout="0" multilineHeight="1" namedStyle="Standaard" fontSize="7" fieldName="'s:' || coalesce(format_number(round(cul_invert_level_start_point,2),2), 'NULL')" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontWordSpacing="0" fontFamily="MS Shell Dlg 2" fontItalic="0" fontWeight="50" fontSizeUnit="Point" textOrientation="horizontal" fontCapitals="0" fontUnderline="0" fontLetterSpacing="0" textColor="101,101,101,255" useSubstitutions="0" fontKerning="1">
            <text-buffer bufferBlendMode="0" bufferSizeUnits="MM" bufferOpacity="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferDraw="1" bufferJoinStyle="128" bufferColor="255,255,255,255" bufferNoFill="0" bufferSize="0.7"/>
            <background shapeOffsetX="0" shapeRadiiX="0" shapeJoinStyle="64" shapeOpacity="1" shapeBorderColor="128,128,128,255" shapeRotation="0" shapeSizeUnit="MM" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetY="0" shapeBorderWidth="0" shapeBlendMode="0" shapeSizeY="0" shapeRotationType="0" shapeType="0" shapeRadiiUnit="MM" shapeRadiiY="0" shapeOffsetUnit="MM" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeSizeType="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSVGFile="" shapeFillColor="255,255,255,255" shapeBorderWidthUnit="MM" shapeSizeX="0" shapeDraw="0">
              <symbol name="markerSymbol" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
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
                      <Option name="name" type="QString" value=""/>
                      <Option name="properties"/>
                      <Option name="type" type="QString" value="collection"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </background>
            <shadow shadowScale="100" shadowColor="0,0,0,255" shadowRadiusUnit="MM" shadowDraw="0" shadowRadiusAlphaOnly="0" shadowRadius="1.5" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.7" shadowOffsetDist="1" shadowOffsetUnit="MM" shadowBlendMode="6" shadowOffsetGlobal="1" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowUnder="0" shadowOffsetAngle="135"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" type="QString" value=""/>
                <Option name="properties"/>
                <Option name="type" type="QString" value="collection"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format rightDirectionSymbol=">" multilineAlign="0" reverseDirectionSymbol="0" wrapChar="" autoWrapLength="0" formatNumbers="0" decimals="3" useMaxLineLengthForAutoWrap="1" addDirectionSymbol="0" placeDirectionSymbol="0" plussign="0" leftDirectionSymbol="&lt;"/>
          <placement maxCurvedCharAngleIn="25" geometryGenerator="start_point($geometry)" quadOffset="2" priority="5" yOffset="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" maxCurvedCharAngleOut="-25" repeatDistance="0" centroidWhole="0" rotationAngle="0" overrunDistance="0" overrunDistanceUnit="MM" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorType="PointGeometry" distUnits="MM" fitInPolygonOnly="0" preserveRotation="0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" centroidInside="0" dist="0" layerType="LineGeometry" xOffset="2" placement="1" distMapUnitScale="3x:0,0,0,0,0,0" repeatDistanceUnits="MM" placementFlags="2" offsetType="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorEnabled="1" offsetUnits="MM"/>
          <rendering upsidedownLabels="0" obstacleFactor="1" fontMinPixelSize="3" maxNumLabels="2000" fontMaxPixelSize="10000" scaleMin="1" zIndex="0" displayAll="1" obstacle="1" fontLimitPixelSize="0" obstacleType="0" mergeLines="0" drawLabels="1" limitNumLabels="0" minFeatureSize="0" scaleVisibility="0" labelPerPart="0" scaleMax="10000000"/>
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
                  <Option name="expression" type="QString" value="360 - &#xd;&#xa;(90 - degrees(&#xd;&#xa;&#x9;azimuth(&#xd;&#xa;&#x9;&#x9;start_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9; @project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;end_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;@project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;)&#xd;&#xa;&#x9;)&#xd;&#xa;)&#xd;&#xa;)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="PositionX" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="expression" type="QString" value="x(start_point($geometry))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="PositionY" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="expression" type="QString" value="y(start_point($geometry))"/>
                  <Option name="type" type="int" value="3"/>
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
              <Option name="lineSymbol" type="QString" value="&lt;symbol name=&quot;symbol&quot; type=&quot;line&quot; clip_to_extent=&quot;1&quot; alpha=&quot;1&quot; force_rhr=&quot;0&quot;>&lt;layer pass=&quot;0&quot; enabled=&quot;1&quot; locked=&quot;0&quot; class=&quot;SimpleLine&quot;>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; type=&quot;QString&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; type=&quot;QString&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
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
      </rule>
      <rule key="{c838a60a-dfce-4ddc-b736-58e50b0edb58}" description="End point label" scalemaxdenom="1000">
        <settings calloutType="simple">
          <text-style previewBkgrdColor="255,255,255,255" textOpacity="1" isExpression="1" blendMode="0" fontStrikeout="0" multilineHeight="1" namedStyle="Standaard" fontSize="7" fieldName="'e:'||coalesce(format_number(round(cul_invert_level_end_point,2),2), 'NULL')" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontWordSpacing="0" fontFamily="MS Shell Dlg 2" fontItalic="0" fontWeight="50" fontSizeUnit="Point" textOrientation="horizontal" fontCapitals="0" fontUnderline="0" fontLetterSpacing="0" textColor="101,101,101,255" useSubstitutions="0" fontKerning="1">
            <text-buffer bufferBlendMode="0" bufferSizeUnits="MM" bufferOpacity="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferDraw="1" bufferJoinStyle="128" bufferColor="255,255,255,255" bufferNoFill="0" bufferSize="0.7"/>
            <background shapeOffsetX="0" shapeRadiiX="0" shapeJoinStyle="64" shapeOpacity="1" shapeBorderColor="128,128,128,255" shapeRotation="0" shapeSizeUnit="MM" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetY="0" shapeBorderWidth="0" shapeBlendMode="0" shapeSizeY="0" shapeRotationType="0" shapeType="0" shapeRadiiUnit="MM" shapeRadiiY="0" shapeOffsetUnit="MM" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeSizeType="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSVGFile="" shapeFillColor="255,255,255,255" shapeBorderWidthUnit="MM" shapeSizeX="0" shapeDraw="0">
              <symbol name="markerSymbol" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
                <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
                  <prop v="0" k="angle"/>
                  <prop v="145,82,45,255" k="color"/>
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
            <shadow shadowScale="100" shadowColor="0,0,0,255" shadowRadiusUnit="MM" shadowDraw="0" shadowRadiusAlphaOnly="0" shadowRadius="1.5" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.7" shadowOffsetDist="1" shadowOffsetUnit="MM" shadowBlendMode="6" shadowOffsetGlobal="1" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowUnder="0" shadowOffsetAngle="135"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" type="QString" value=""/>
                <Option name="properties"/>
                <Option name="type" type="QString" value="collection"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format rightDirectionSymbol=">" multilineAlign="0" reverseDirectionSymbol="0" wrapChar="" autoWrapLength="0" formatNumbers="0" decimals="3" useMaxLineLengthForAutoWrap="1" addDirectionSymbol="0" placeDirectionSymbol="0" plussign="0" leftDirectionSymbol="&lt;"/>
          <placement maxCurvedCharAngleIn="25" geometryGenerator="end_point($geometry)" quadOffset="2" priority="5" yOffset="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" maxCurvedCharAngleOut="-25" repeatDistance="0" centroidWhole="0" rotationAngle="0" overrunDistance="0" overrunDistanceUnit="MM" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorType="PointGeometry" distUnits="MM" fitInPolygonOnly="0" preserveRotation="0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" centroidInside="0" dist="0" layerType="LineGeometry" xOffset="2" placement="1" distMapUnitScale="3x:0,0,0,0,0,0" repeatDistanceUnits="MM" placementFlags="10" offsetType="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorEnabled="1" offsetUnits="MM"/>
          <rendering upsidedownLabels="0" obstacleFactor="1" fontMinPixelSize="3" maxNumLabels="2000" fontMaxPixelSize="10000" scaleMin="1" zIndex="0" displayAll="1" obstacle="1" fontLimitPixelSize="0" obstacleType="0" mergeLines="0" drawLabels="1" limitNumLabels="0" minFeatureSize="0" scaleVisibility="0" labelPerPart="0" scaleMax="10000000"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="Hali" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="'Right'"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="LabelRotation" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="expression" type="QString" value="360 - &#xd;&#xa;(90 - degrees(&#xd;&#xa;&#x9;azimuth(&#xd;&#xa;&#x9;&#x9;start_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9; @project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;end_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;@project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;)&#xd;&#xa;&#x9;)&#xd;&#xa;)&#xd;&#xa;)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="PositionX" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="expression" type="QString" value="x(end_point($geometry))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="PositionY" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="expression" type="QString" value="y(end_point($geometry))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="Show" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="intersects(transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;end_point( $geometry),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;  @map_crs  &#xd;&#xa;&#x9;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;&#x9;@map_extent&#xd;&#xa;)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="Vali" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="'Bottom'"/>
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
              <Option name="lineSymbol" type="QString" value="&lt;symbol name=&quot;symbol&quot; type=&quot;line&quot; clip_to_extent=&quot;1&quot; alpha=&quot;1&quot; force_rhr=&quot;0&quot;>&lt;layer pass=&quot;0&quot; enabled=&quot;1&quot; locked=&quot;0&quot; class=&quot;SimpleLine&quot;>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; type=&quot;QString&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; type=&quot;QString&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
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
    <DiagramCategory lineSizeScale="3x:0,0,0,0,0,0" penAlpha="255" backgroundColor="#ffffff" sizeScale="3x:0,0,0,0,0,0" minimumSize="0" rotationOffset="270" penWidth="0" minScaleDenominator="-4.65661e-10" width="15" scaleBasedVisibility="0" scaleDependency="Area" penColor="#000000" enabled="0" maxScaleDenominator="1e+08" diagramOrientation="Up" opacity="1" sizeType="MM" lineSizeType="MM" labelPlacementMethod="XHeight" height="15" backgroundAlpha="255" barWidth="5">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute color="#000000" field="" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings showAll="1" priority="0" obstacle="0" placement="2" zIndex="0" linePlacementFlags="2" dist="0">
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
    <field name="cul_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_calculation_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="100: embedded" type="QString" value="100"/>
              </Option>
              <Option type="Map">
                <Option name="101: isolated" type="QString" value="101"/>
              </Option>
              <Option type="Map">
                <Option name="102: connected" type="QString" value="102"/>
              </Option>
              <Option type="Map">
                <Option name="105: double connected" type="QString" value="105"/>
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
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_friction_type">
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
    <field name="cul_dist_calc_points">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_zoom_category">
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
    <field name="cul_cross_section_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_discharge_coefficient_positive">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_discharge_coefficient_negative">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_invert_level_start_point">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_invert_level_end_point">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_connection_node_start_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_connection_node_end_id">
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
    <alias name="" index="0" field="ROWID"/>
    <alias name="id" index="1" field="cul_id"/>
    <alias name="display_name" index="2" field="cul_display_name"/>
    <alias name="code" index="3" field="cul_code"/>
    <alias name="calculation_type" index="4" field="cul_calculation_type"/>
    <alias name="friction_value" index="5" field="cul_friction_value"/>
    <alias name="friction_type" index="6" field="cul_friction_type"/>
    <alias name="dist_calc_points" index="7" field="cul_dist_calc_points"/>
    <alias name="zoom_category" index="8" field="cul_zoom_category"/>
    <alias name="cross_section_definition_id" index="9" field="cul_cross_section_definition_id"/>
    <alias name="discharge_coefficient_positive" index="10" field="cul_discharge_coefficient_positive"/>
    <alias name="discharge_coefficient_negative" index="11" field="cul_discharge_coefficient_negative"/>
    <alias name="invert_level_start_point" index="12" field="cul_invert_level_start_point"/>
    <alias name="invert_level_end_point" index="13" field="cul_invert_level_end_point"/>
    <alias name="connection_node_start_id" index="14" field="cul_connection_node_start_id"/>
    <alias name="connection_node_end_id" index="15" field="cul_connection_node_end_id"/>
    <alias name="id" index="16" field="def_id"/>
    <alias name="shape" index="17" field="def_shape"/>
    <alias name="width" index="18" field="def_width"/>
    <alias name="height" index="19" field="def_height"/>
    <alias name="code" index="20" field="def_code"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" expression="" field="ROWID"/>
    <default applyOnUpdate="0" expression="if(maximum(cul_id) is null,1, maximum(cul_id)+1)" field="cul_id"/>
    <default applyOnUpdate="0" expression="'new'" field="cul_display_name"/>
    <default applyOnUpdate="0" expression="'new'" field="cul_code"/>
    <default applyOnUpdate="0" expression="101" field="cul_calculation_type"/>
    <default applyOnUpdate="0" expression="" field="cul_friction_value"/>
    <default applyOnUpdate="0" expression="2" field="cul_friction_type"/>
    <default applyOnUpdate="0" expression="10000" field="cul_dist_calc_points"/>
    <default applyOnUpdate="0" expression="3" field="cul_zoom_category"/>
    <default applyOnUpdate="0" expression="" field="cul_cross_section_definition_id"/>
    <default applyOnUpdate="0" expression="0.8" field="cul_discharge_coefficient_positive"/>
    <default applyOnUpdate="0" expression="0.8" field="cul_discharge_coefficient_negative"/>
    <default applyOnUpdate="0" expression="aggregate('v2_manhole_view','min',&quot;bottom_level&quot;, intersects($geometry,start_point(geometry(@parent)))) " field="cul_invert_level_start_point"/>
    <default applyOnUpdate="0" expression="aggregate('v2_manhole_view','min',&quot;bottom_level&quot;, intersects($geometry,end_point(geometry(@parent)))) " field="cul_invert_level_end_point"/>
    <default applyOnUpdate="0" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))) is null, 'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))))" field="cul_connection_node_start_id"/>
    <default applyOnUpdate="0" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))) is null, 'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))))" field="cul_connection_node_end_id"/>
    <default applyOnUpdate="0" expression="" field="def_id"/>
    <default applyOnUpdate="0" expression="" field="def_shape"/>
    <default applyOnUpdate="0" expression="" field="def_width"/>
    <default applyOnUpdate="0" expression="" field="def_height"/>
    <default applyOnUpdate="0" expression="" field="def_code"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" field="ROWID" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="2" field="cul_id" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="cul_display_name" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="cul_code" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="cul_calculation_type" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="cul_friction_value" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="cul_friction_type" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="cul_dist_calc_points" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="cul_zoom_category" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="cul_cross_section_definition_id" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="cul_discharge_coefficient_positive" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="cul_discharge_coefficient_negative" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="cul_invert_level_start_point" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="cul_invert_level_end_point" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" field="cul_connection_node_start_id" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="cul_connection_node_end_id" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="2" field="def_id" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" field="def_shape" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="def_width" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="def_height" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="def_code" exp_strength="0" unique_strength="0" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="ROWID"/>
    <constraint exp="" desc="" field="cul_id"/>
    <constraint exp="" desc="" field="cul_display_name"/>
    <constraint exp="" desc="" field="cul_code"/>
    <constraint exp="" desc="" field="cul_calculation_type"/>
    <constraint exp="" desc="" field="cul_friction_value"/>
    <constraint exp="" desc="" field="cul_friction_type"/>
    <constraint exp="" desc="" field="cul_dist_calc_points"/>
    <constraint exp="" desc="" field="cul_zoom_category"/>
    <constraint exp="" desc="" field="cul_cross_section_definition_id"/>
    <constraint exp="" desc="" field="cul_discharge_coefficient_positive"/>
    <constraint exp="" desc="" field="cul_discharge_coefficient_negative"/>
    <constraint exp="" desc="" field="cul_invert_level_start_point"/>
    <constraint exp="" desc="" field="cul_invert_level_end_point"/>
    <constraint exp="" desc="" field="cul_connection_node_start_id"/>
    <constraint exp="" desc="" field="cul_connection_node_end_id"/>
    <constraint exp="" desc="" field="def_id"/>
    <constraint exp="" desc="" field="def_shape"/>
    <constraint exp="" desc="" field="def_width"/>
    <constraint exp="" desc="" field="def_height"/>
    <constraint exp="" desc="" field="def_code"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortExpression="" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column name="ROWID" hidden="0" type="field" width="-1"/>
      <column name="cul_id" hidden="0" type="field" width="-1"/>
      <column name="cul_display_name" hidden="0" type="field" width="-1"/>
      <column name="cul_code" hidden="0" type="field" width="-1"/>
      <column name="cul_calculation_type" hidden="0" type="field" width="-1"/>
      <column name="cul_friction_value" hidden="0" type="field" width="-1"/>
      <column name="cul_friction_type" hidden="0" type="field" width="-1"/>
      <column name="cul_dist_calc_points" hidden="0" type="field" width="-1"/>
      <column name="cul_zoom_category" hidden="0" type="field" width="-1"/>
      <column name="cul_cross_section_definition_id" hidden="0" type="field" width="-1"/>
      <column name="cul_discharge_coefficient_positive" hidden="0" type="field" width="-1"/>
      <column name="cul_discharge_coefficient_negative" hidden="0" type="field" width="-1"/>
      <column name="cul_invert_level_start_point" hidden="0" type="field" width="-1"/>
      <column name="cul_invert_level_end_point" hidden="0" type="field" width="-1"/>
      <column name="cul_connection_node_start_id" hidden="0" type="field" width="-1"/>
      <column name="cul_connection_node_end_id" hidden="0" type="field" width="-1"/>
      <column name="def_id" hidden="0" type="field" width="-1"/>
      <column name="def_shape" hidden="0" type="field" width="-1"/>
      <column name="def_width" hidden="0" type="field" width="-1"/>
      <column name="def_height" hidden="0" type="field" width="-1"/>
      <column name="def_code" hidden="0" type="field" width="-1"/>
      <column hidden="1" type="actions" width="-1"/>
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
    <attributeEditorContainer visibilityExpressionEnabled="0" name="Culvert view" showLabel="1" columnCount="1" groupBox="0" visibilityExpression="">
      <attributeEditorContainer visibilityExpressionEnabled="0" name="General" showLabel="1" columnCount="1" groupBox="1" visibilityExpression="">
        <attributeEditorField name="cul_id" showLabel="1" index="1"/>
        <attributeEditorField name="cul_display_name" showLabel="1" index="2"/>
        <attributeEditorField name="cul_code" showLabel="1" index="3"/>
        <attributeEditorField name="cul_calculation_type" showLabel="1" index="4"/>
        <attributeEditorField name="cul_dist_calc_points" showLabel="1" index="7"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpressionEnabled="0" name="Characteristics" showLabel="1" columnCount="1" groupBox="1" visibilityExpression="">
        <attributeEditorField name="cul_invert_level_start_point" showLabel="1" index="12"/>
        <attributeEditorField name="cul_invert_level_end_point" showLabel="1" index="13"/>
        <attributeEditorField name="cul_friction_type" showLabel="1" index="6"/>
        <attributeEditorField name="cul_friction_value" showLabel="1" index="5"/>
        <attributeEditorField name="cul_discharge_coefficient_positive" showLabel="1" index="10"/>
        <attributeEditorField name="cul_discharge_coefficient_negative" showLabel="1" index="11"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpressionEnabled="0" name="Cross section definition" showLabel="1" columnCount="1" groupBox="1" visibilityExpression="">
        <attributeEditorField name="cul_cross_section_definition_id" showLabel="1" index="9"/>
        <attributeEditorField name="def_code" showLabel="1" index="20"/>
        <attributeEditorField name="def_shape" showLabel="1" index="17"/>
        <attributeEditorField name="def_width" showLabel="1" index="18"/>
        <attributeEditorField name="def_height" showLabel="1" index="19"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpressionEnabled="0" name="Visualization" showLabel="1" columnCount="1" groupBox="1" visibilityExpression="">
        <attributeEditorField name="cul_zoom_category" showLabel="1" index="8"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpressionEnabled="0" name="Connection nodes" showLabel="1" columnCount="1" groupBox="1" visibilityExpression="">
        <attributeEditorField name="cul_connection_node_start_id" showLabel="1" index="14"/>
        <attributeEditorField name="cul_connection_node_end_id" showLabel="1" index="15"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="ROWID" editable="1"/>
    <field name="cul_calculation_type" editable="1"/>
    <field name="cul_code" editable="1"/>
    <field name="cul_connection_node_end_id" editable="0"/>
    <field name="cul_connection_node_start_id" editable="0"/>
    <field name="cul_cross_section_definition_id" editable="1"/>
    <field name="cul_discharge_coefficient_negative" editable="1"/>
    <field name="cul_discharge_coefficient_positive" editable="1"/>
    <field name="cul_display_name" editable="1"/>
    <field name="cul_dist_calc_points" editable="1"/>
    <field name="cul_friction_type" editable="1"/>
    <field name="cul_friction_value" editable="1"/>
    <field name="cul_id" editable="1"/>
    <field name="cul_invert_level_end_point" editable="1"/>
    <field name="cul_invert_level_start_point" editable="1"/>
    <field name="cul_zoom_category" editable="1"/>
    <field name="def_code" editable="0"/>
    <field name="def_height" editable="0"/>
    <field name="def_id" editable="0"/>
    <field name="def_shape" editable="0"/>
    <field name="def_width" editable="0"/>
  </editable>
  <labelOnTop>
    <field name="ROWID" labelOnTop="0"/>
    <field name="cul_calculation_type" labelOnTop="0"/>
    <field name="cul_code" labelOnTop="0"/>
    <field name="cul_connection_node_end_id" labelOnTop="0"/>
    <field name="cul_connection_node_start_id" labelOnTop="0"/>
    <field name="cul_cross_section_definition_id" labelOnTop="0"/>
    <field name="cul_discharge_coefficient_negative" labelOnTop="0"/>
    <field name="cul_discharge_coefficient_positive" labelOnTop="0"/>
    <field name="cul_display_name" labelOnTop="0"/>
    <field name="cul_dist_calc_points" labelOnTop="0"/>
    <field name="cul_friction_type" labelOnTop="0"/>
    <field name="cul_friction_value" labelOnTop="0"/>
    <field name="cul_id" labelOnTop="0"/>
    <field name="cul_invert_level_end_point" labelOnTop="0"/>
    <field name="cul_invert_level_start_point" labelOnTop="0"/>
    <field name="cul_zoom_category" labelOnTop="0"/>
    <field name="def_code" labelOnTop="0"/>
    <field name="def_height" labelOnTop="0"/>
    <field name="def_id" labelOnTop="0"/>
    <field name="def_shape" labelOnTop="0"/>
    <field name="def_width" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>"ROWID"</previewExpression>
  <mapTip>display_name</mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
