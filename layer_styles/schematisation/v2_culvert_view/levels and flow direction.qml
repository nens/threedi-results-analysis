<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyDrawingTol="1" maxScale="-4.65661e-10" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" simplifyMaxScale="1" version="3.10.10-A Coruña" labelsEnabled="1" simplifyAlgorithm="0" readOnly="0" minScale="1e+08" simplifyLocal="1" simplifyDrawingHints="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" enableorderby="0" symbollevels="0" type="singleSymbol">
    <symbols>
      <symbol alpha="1" clip_to_extent="1" force_rhr="0" name="0" type="line">
        <layer locked="0" class="SimpleLine" pass="0" enabled="1">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="101,101,101,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.66"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" class="MarkerLine" pass="0" enabled="1">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="interval" v="10"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="0"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="placement" v="firstvertex"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
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
          <symbol alpha="1" clip_to_extent="1" force_rhr="0" name="@0@1" type="marker">
            <layer locked="0" class="SimpleMarker" pass="0" enabled="1">
              <prop k="angle" v="0"/>
              <prop k="color" v="255,0,0,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="arrowhead"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="101,101,101,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0.6"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="2"/>
              <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option value="true" name="active" type="bool"/>
                      <Option value="line_interpolate_angle($geometry, length($geometry) * 0.33) + if(cul_invert_level_start_point > cul_invert_level_end_point, -90, 90)" name="expression" type="QString"/>
                      <Option value="3" name="type" type="int"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option value="true" name="active" type="bool"/>
                      <Option value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;" name="expression" type="QString"/>
                      <Option value="3" name="type" type="int"/>
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
        <layer locked="0" class="MarkerLine" pass="0" enabled="1">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="interval" v="3"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="0"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="MM"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="placement" v="centralpoint"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol alpha="1" clip_to_extent="1" force_rhr="0" name="@0@2" type="marker">
            <layer locked="0" class="SimpleMarker" pass="0" enabled="1">
              <prop k="angle" v="0"/>
              <prop k="color" v="101,101,101,255"/>
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
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties"/>
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
  <labeling type="rule-based">
    <rules key="{adf68133-d959-46aa-b8ff-ee00678c1613}">
      <rule scalemaxdenom="1000" key="{f5e2a3fb-37fd-4aaa-96e2-cbdf08378df2}" description="Start point label">
        <settings calloutType="simple">
          <text-style fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontStrikeout="0" fontKerning="1" fontItalic="0" fontLetterSpacing="0" blendMode="0" multilineHeight="1" namedStyle="Standaard" previewBkgrdColor="255,255,255,255" useSubstitutions="0" textColor="101,101,101,255" fontWeight="50" fontFamily="MS Gothic" fontUnderline="0" fontSize="7" fieldName="'s:' || coalesce(format_number(round(cul_invert_level_start_point,2),2), 'NULL')" fontWordSpacing="0" textOpacity="1" isExpression="1" fontCapitals="0" textOrientation="horizontal" fontSizeUnit="Point">
            <text-buffer bufferSize="0.7" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferBlendMode="0" bufferColor="255,255,255,255" bufferSizeUnits="MM" bufferNoFill="0" bufferOpacity="1" bufferDraw="1" bufferJoinStyle="128"/>
            <background shapeBlendMode="0" shapeRadiiY="0" shapeFillColor="255,255,255,255" shapeSizeX="0" shapeOpacity="1" shapeType="0" shapeBorderColor="128,128,128,255" shapeJoinStyle="64" shapeSVGFile="" shapeSizeY="0" shapeRotationType="0" shapeRadiiUnit="MM" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeSizeType="0" shapeOffsetX="0" shapeRadiiX="0" shapeRotation="0" shapeOffsetUnit="MM" shapeSizeUnit="MM" shapeBorderWidth="0" shapeDraw="0" shapeBorderWidthUnit="MM" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetY="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0">
              <symbol alpha="1" clip_to_extent="1" force_rhr="0" name="markerSymbol" type="marker">
                <layer locked="0" class="SimpleMarker" pass="0" enabled="1">
                  <prop k="angle" v="0"/>
                  <prop k="color" v="190,178,151,255"/>
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
                      <Option value="" name="name" type="QString"/>
                      <Option name="properties"/>
                      <Option value="collection" name="type" type="QString"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </background>
            <shadow shadowOffsetUnit="MM" shadowColor="0,0,0,255" shadowRadiusAlphaOnly="0" shadowUnder="0" shadowOffsetGlobal="1" shadowRadiusUnit="MM" shadowScale="100" shadowDraw="0" shadowBlendMode="6" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetDist="1" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.7" shadowOffsetAngle="135" shadowRadius="1.5"/>
            <dd_properties>
              <Option type="Map">
                <Option value="" name="name" type="QString"/>
                <Option name="properties"/>
                <Option value="collection" name="type" type="QString"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format leftDirectionSymbol="&lt;" formatNumbers="0" multilineAlign="0" wrapChar="" decimals="3" useMaxLineLengthForAutoWrap="1" placeDirectionSymbol="0" autoWrapLength="0" reverseDirectionSymbol="0" rightDirectionSymbol=">" plussign="0" addDirectionSymbol="0"/>
          <placement placement="1" layerType="LineGeometry" priority="5" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" distMapUnitScale="3x:0,0,0,0,0,0" xOffset="2" centroidInside="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" maxCurvedCharAngleOut="-25" fitInPolygonOnly="0" offsetType="0" yOffset="0" preserveRotation="0" placementFlags="2" maxCurvedCharAngleIn="25" overrunDistance="0" dist="0" distUnits="MM" centroidWhole="0" offsetUnits="MM" geometryGenerator="start_point($geometry)" repeatDistanceUnits="MM" overrunDistanceUnit="MM" rotationAngle="0" quadOffset="2" repeatDistance="0" geometryGeneratorEnabled="1" geometryGeneratorType="PointGeometry"/>
          <rendering displayAll="1" fontMinPixelSize="3" fontLimitPixelSize="0" labelPerPart="0" limitNumLabels="0" obstacleFactor="1" minFeatureSize="0" scaleMin="1" drawLabels="1" zIndex="0" maxNumLabels="2000" mergeLines="0" obstacleType="0" upsidedownLabels="0" obstacle="1" fontMaxPixelSize="10000" scaleVisibility="0" scaleMax="10000000"/>
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
                  <Option value="360 - &#xd;&#xa;(90 - degrees(&#xd;&#xa;&#x9;azimuth(&#xd;&#xa;&#x9;&#x9;start_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9; @project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;end_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;@project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;)&#xd;&#xa;&#x9;)&#xd;&#xa;)&#xd;&#xa;)" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
                <Option name="PositionX" type="Map">
                  <Option value="false" name="active" type="bool"/>
                  <Option value="x(start_point($geometry))" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
                <Option name="PositionY" type="Map">
                  <Option value="false" name="active" type="bool"/>
                  <Option value="y(start_point($geometry))" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
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
              <Option value="&lt;symbol alpha=&quot;1&quot; clip_to_extent=&quot;1&quot; force_rhr=&quot;0&quot; name=&quot;symbol&quot; type=&quot;line&quot;>&lt;layer locked=&quot;0&quot; class=&quot;SimpleLine&quot; pass=&quot;0&quot; enabled=&quot;1&quot;>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; name=&quot;name&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; name=&quot;type&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" name="lineSymbol" type="QString"/>
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
      </rule>
      <rule scalemaxdenom="1000" key="{0f8a6095-f29f-485a-896e-f3f5ad8c91f8}" description="End point label">
        <settings calloutType="simple">
          <text-style fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontStrikeout="0" fontKerning="1" fontItalic="0" fontLetterSpacing="0" blendMode="0" multilineHeight="1" namedStyle="Standaard" previewBkgrdColor="255,255,255,255" useSubstitutions="0" textColor="101,101,101,255" fontWeight="50" fontFamily="MS Gothic" fontUnderline="0" fontSize="7" fieldName="'e:'||coalesce(format_number(round(cul_invert_level_end_point,2),2), 'NULL')" fontWordSpacing="0" textOpacity="1" isExpression="1" fontCapitals="0" textOrientation="horizontal" fontSizeUnit="Point">
            <text-buffer bufferSize="0.7" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferBlendMode="0" bufferColor="255,255,255,255" bufferSizeUnits="MM" bufferNoFill="0" bufferOpacity="1" bufferDraw="1" bufferJoinStyle="128"/>
            <background shapeBlendMode="0" shapeRadiiY="0" shapeFillColor="255,255,255,255" shapeSizeX="0" shapeOpacity="1" shapeType="0" shapeBorderColor="128,128,128,255" shapeJoinStyle="64" shapeSVGFile="" shapeSizeY="0" shapeRotationType="0" shapeRadiiUnit="MM" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeSizeType="0" shapeOffsetX="0" shapeRadiiX="0" shapeRotation="0" shapeOffsetUnit="MM" shapeSizeUnit="MM" shapeBorderWidth="0" shapeDraw="0" shapeBorderWidthUnit="MM" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetY="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0">
              <symbol alpha="1" clip_to_extent="1" force_rhr="0" name="markerSymbol" type="marker">
                <layer locked="0" class="SimpleMarker" pass="0" enabled="1">
                  <prop k="angle" v="0"/>
                  <prop k="color" v="145,82,45,255"/>
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
                      <Option value="" name="name" type="QString"/>
                      <Option name="properties"/>
                      <Option value="collection" name="type" type="QString"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </background>
            <shadow shadowOffsetUnit="MM" shadowColor="0,0,0,255" shadowRadiusAlphaOnly="0" shadowUnder="0" shadowOffsetGlobal="1" shadowRadiusUnit="MM" shadowScale="100" shadowDraw="0" shadowBlendMode="6" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetDist="1" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.7" shadowOffsetAngle="135" shadowRadius="1.5"/>
            <dd_properties>
              <Option type="Map">
                <Option value="" name="name" type="QString"/>
                <Option name="properties"/>
                <Option value="collection" name="type" type="QString"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format leftDirectionSymbol="&lt;" formatNumbers="0" multilineAlign="0" wrapChar="" decimals="3" useMaxLineLengthForAutoWrap="1" placeDirectionSymbol="0" autoWrapLength="0" reverseDirectionSymbol="0" rightDirectionSymbol=">" plussign="0" addDirectionSymbol="0"/>
          <placement placement="1" layerType="LineGeometry" priority="5" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" distMapUnitScale="3x:0,0,0,0,0,0" xOffset="2" centroidInside="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" maxCurvedCharAngleOut="-25" fitInPolygonOnly="0" offsetType="0" yOffset="0" preserveRotation="0" placementFlags="10" maxCurvedCharAngleIn="25" overrunDistance="0" dist="0" distUnits="MM" centroidWhole="0" offsetUnits="MM" geometryGenerator="end_point($geometry)" repeatDistanceUnits="MM" overrunDistanceUnit="MM" rotationAngle="0" quadOffset="2" repeatDistance="0" geometryGeneratorEnabled="1" geometryGeneratorType="PointGeometry"/>
          <rendering displayAll="1" fontMinPixelSize="3" fontLimitPixelSize="0" labelPerPart="0" limitNumLabels="0" obstacleFactor="1" minFeatureSize="0" scaleMin="1" drawLabels="1" zIndex="0" maxNumLabels="2000" mergeLines="0" obstacleType="0" upsidedownLabels="0" obstacle="1" fontMaxPixelSize="10000" scaleVisibility="0" scaleMax="10000000"/>
          <dd_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="Hali" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="'Right'" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
                <Option name="LabelRotation" type="Map">
                  <Option value="false" name="active" type="bool"/>
                  <Option value="360 - &#xd;&#xa;(90 - degrees(&#xd;&#xa;&#x9;azimuth(&#xd;&#xa;&#x9;&#x9;start_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9; @project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;end_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;@project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;)&#xd;&#xa;&#x9;)&#xd;&#xa;)&#xd;&#xa;)" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
                <Option name="PositionX" type="Map">
                  <Option value="false" name="active" type="bool"/>
                  <Option value="x(end_point($geometry))" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
                <Option name="PositionY" type="Map">
                  <Option value="false" name="active" type="bool"/>
                  <Option value="y(end_point($geometry))" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
                <Option name="Show" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="intersects(transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;end_point( $geometry),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;  @map_crs  &#xd;&#xa;&#x9;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;&#x9;@map_extent&#xd;&#xa;)" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
                <Option name="Vali" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="'Bottom'" name="expression" type="QString"/>
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
              <Option value="&lt;symbol alpha=&quot;1&quot; clip_to_extent=&quot;1&quot; force_rhr=&quot;0&quot; name=&quot;symbol&quot; type=&quot;line&quot;>&lt;layer locked=&quot;0&quot; class=&quot;SimpleLine&quot; pass=&quot;0&quot; enabled=&quot;1&quot;>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; name=&quot;name&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; name=&quot;type&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" name="lineSymbol" type="QString"/>
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
    <DiagramCategory backgroundAlpha="255" opacity="1" sizeScale="3x:0,0,0,0,0,0" penAlpha="255" minScaleDenominator="-4.65661e-10" barWidth="5" penWidth="0" scaleDependency="Area" lineSizeScale="3x:0,0,0,0,0,0" scaleBasedVisibility="0" width="15" rotationOffset="270" backgroundColor="#ffffff" height="15" lineSizeType="MM" diagramOrientation="Up" penColor="#000000" sizeType="MM" labelPlacementMethod="XHeight" maxScaleDenominator="1e+08" minimumSize="0" enabled="0">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute label="" color="#000000" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings priority="0" obstacle="0" dist="0" linePlacementFlags="2" placement="2" zIndex="0" showAll="1">
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
    <field name="cul_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
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
                <Option value="100" name="100: embedded" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="101" name="101: isolated" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="102" name="102: connected" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="105" name="105: double connected" type="QString"/>
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
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
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
    <field name="cul_dist_calc_points">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
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
    <field name="cul_cross_section_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_discharge_coefficient_positive">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_discharge_coefficient_negative">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_invert_level_start_point">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_invert_level_end_point">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_connection_node_start_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_connection_node_end_id">
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
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" field="ROWID" constraints="0"/>
    <constraint notnull_strength="2" exp_strength="0" unique_strength="0" field="cul_id" constraints="1"/>
    <constraint notnull_strength="2" exp_strength="0" unique_strength="0" field="cul_display_name" constraints="1"/>
    <constraint notnull_strength="2" exp_strength="0" unique_strength="0" field="cul_code" constraints="1"/>
    <constraint notnull_strength="2" exp_strength="0" unique_strength="0" field="cul_calculation_type" constraints="1"/>
    <constraint notnull_strength="2" exp_strength="0" unique_strength="0" field="cul_friction_value" constraints="1"/>
    <constraint notnull_strength="2" exp_strength="0" unique_strength="0" field="cul_friction_type" constraints="1"/>
    <constraint notnull_strength="2" exp_strength="0" unique_strength="0" field="cul_dist_calc_points" constraints="1"/>
    <constraint notnull_strength="2" exp_strength="0" unique_strength="0" field="cul_zoom_category" constraints="1"/>
    <constraint notnull_strength="2" exp_strength="0" unique_strength="0" field="cul_cross_section_definition_id" constraints="1"/>
    <constraint notnull_strength="2" exp_strength="0" unique_strength="0" field="cul_discharge_coefficient_positive" constraints="1"/>
    <constraint notnull_strength="2" exp_strength="0" unique_strength="0" field="cul_discharge_coefficient_negative" constraints="1"/>
    <constraint notnull_strength="2" exp_strength="0" unique_strength="0" field="cul_invert_level_start_point" constraints="1"/>
    <constraint notnull_strength="2" exp_strength="0" unique_strength="0" field="cul_invert_level_end_point" constraints="1"/>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" field="cul_connection_node_start_id" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" field="cul_connection_node_end_id" constraints="0"/>
    <constraint notnull_strength="2" exp_strength="0" unique_strength="0" field="def_id" constraints="1"/>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" field="def_shape" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" field="def_width" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" field="def_height" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" field="def_code" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="ROWID" exp=""/>
    <constraint desc="" field="cul_id" exp=""/>
    <constraint desc="" field="cul_display_name" exp=""/>
    <constraint desc="" field="cul_code" exp=""/>
    <constraint desc="" field="cul_calculation_type" exp=""/>
    <constraint desc="" field="cul_friction_value" exp=""/>
    <constraint desc="" field="cul_friction_type" exp=""/>
    <constraint desc="" field="cul_dist_calc_points" exp=""/>
    <constraint desc="" field="cul_zoom_category" exp=""/>
    <constraint desc="" field="cul_cross_section_definition_id" exp=""/>
    <constraint desc="" field="cul_discharge_coefficient_positive" exp=""/>
    <constraint desc="" field="cul_discharge_coefficient_negative" exp=""/>
    <constraint desc="" field="cul_invert_level_start_point" exp=""/>
    <constraint desc="" field="cul_invert_level_end_point" exp=""/>
    <constraint desc="" field="cul_connection_node_start_id" exp=""/>
    <constraint desc="" field="cul_connection_node_end_id" exp=""/>
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
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="" sortOrder="0">
    <columns>
      <column hidden="0" width="-1" name="ROWID" type="field"/>
      <column hidden="0" width="-1" name="cul_id" type="field"/>
      <column hidden="0" width="-1" name="cul_display_name" type="field"/>
      <column hidden="0" width="-1" name="cul_code" type="field"/>
      <column hidden="0" width="-1" name="cul_calculation_type" type="field"/>
      <column hidden="0" width="-1" name="cul_friction_value" type="field"/>
      <column hidden="0" width="-1" name="cul_friction_type" type="field"/>
      <column hidden="0" width="-1" name="cul_dist_calc_points" type="field"/>
      <column hidden="0" width="-1" name="cul_zoom_category" type="field"/>
      <column hidden="0" width="-1" name="cul_cross_section_definition_id" type="field"/>
      <column hidden="0" width="-1" name="cul_discharge_coefficient_positive" type="field"/>
      <column hidden="0" width="-1" name="cul_discharge_coefficient_negative" type="field"/>
      <column hidden="0" width="-1" name="cul_invert_level_start_point" type="field"/>
      <column hidden="0" width="-1" name="cul_invert_level_end_point" type="field"/>
      <column hidden="0" width="-1" name="cul_connection_node_start_id" type="field"/>
      <column hidden="0" width="-1" name="cul_connection_node_end_id" type="field"/>
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
    <attributeEditorContainer showLabel="1" columnCount="1" groupBox="0" visibilityExpression="" name="Culvert view" visibilityExpressionEnabled="0">
      <attributeEditorContainer showLabel="1" columnCount="1" groupBox="1" visibilityExpression="" name="General" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="1" name="cul_id"/>
        <attributeEditorField showLabel="1" index="2" name="cul_display_name"/>
        <attributeEditorField showLabel="1" index="3" name="cul_code"/>
        <attributeEditorField showLabel="1" index="4" name="cul_calculation_type"/>
        <attributeEditorField showLabel="1" index="7" name="cul_dist_calc_points"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" groupBox="1" visibilityExpression="" name="Characteristics" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="12" name="cul_invert_level_start_point"/>
        <attributeEditorField showLabel="1" index="13" name="cul_invert_level_end_point"/>
        <attributeEditorField showLabel="1" index="6" name="cul_friction_type"/>
        <attributeEditorField showLabel="1" index="5" name="cul_friction_value"/>
        <attributeEditorField showLabel="1" index="10" name="cul_discharge_coefficient_positive"/>
        <attributeEditorField showLabel="1" index="11" name="cul_discharge_coefficient_negative"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" groupBox="1" visibilityExpression="" name="Cross section definition" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="9" name="cul_cross_section_definition_id"/>
        <attributeEditorField showLabel="1" index="20" name="def_code"/>
        <attributeEditorField showLabel="1" index="17" name="def_shape"/>
        <attributeEditorField showLabel="1" index="18" name="def_width"/>
        <attributeEditorField showLabel="1" index="19" name="def_height"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" groupBox="1" visibilityExpression="" name="Visualization" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="8" name="cul_zoom_category"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" groupBox="1" visibilityExpression="" name="Connection nodes" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="14" name="cul_connection_node_start_id"/>
        <attributeEditorField showLabel="1" index="15" name="cul_connection_node_end_id"/>
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
