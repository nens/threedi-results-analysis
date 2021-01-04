<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.14.0-Pi" simplifyAlgorithm="0" simplifyMaxScale="1" labelsEnabled="0" simplifyDrawingHints="1" styleCategories="AllStyleCategories" simplifyDrawingTol="1" maxScale="0" simplifyLocal="1" readOnly="0" hasScaleBasedVisibilityFlag="0" minScale="100000000">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal endField="" mode="0" startField="" startExpression="" endExpression="" enabled="0" fixedDuration="0" durationUnit="min" durationField="" accumulate="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 symbollevels="0" type="RuleRenderer" forceraster="0" enableorderby="0">
    <rules key="{1c4a4e03-d442-4bb0-8ffc-82b9a703e08f}">
      <rule label="Combined sewer" filter="pipe_sewerage_type = 0" symbol="0" key="{844e5e28-ad8f-43dc-ae9b-2eedeecde873}"/>
      <rule label="Storm drain" filter="pipe_sewerage_type = 1" symbol="1" key="{3b41f70d-2dfe-4438-8b1a-3722a52ff82b}"/>
      <rule label="Sanitary sewer" filter="pipe_sewerage_type = 2" symbol="2" key="{c8833167-878e-49b2-bd37-5019aeea2451}"/>
      <rule label="Transport" filter="pipe_sewerage_type = 3" symbol="3" key="{d62bccfa-4138-43ba-ab6d-51eae9f5b079}"/>
      <rule label="Spillway" filter="pipe_sewerage_type = 4" symbol="4" key="{3d909156-553e-4d45-8a2f-02337ffb74d5}"/>
      <rule label="Syphon" filter="pipe_sewerage_type =5" symbol="5" key="{a445abaf-878b-4b6b-8f1d-1314d1271d38}"/>
      <rule label="Storage" filter="pipe_sewerage_type = 6" symbol="6" key="{c6ba261b-8172-407e-bc72-8487b24a1cc4}"/>
      <rule label="Storage and settlement tank" filter="pipe_sewerage_type = 7" symbol="7" key="{8eb66a66-0335-4672-a78d-1aac6c4702ff}"/>
      <rule label="Other" filter="ELSE" symbol="8" key="{aa320dac-96a8-41e4-af30-3e9153ceaeae}"/>
    </rules>
    <symbols>
      <symbol name="0" type="line" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" pass="0" locked="0" class="SimpleLine">
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="1" type="line" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" pass="0" locked="0" class="SimpleLine">
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="2" type="line" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" pass="0" locked="0" class="SimpleLine">
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="3" type="line" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" pass="0" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="153,153,153,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.7" k="line_width"/>
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
      </symbol>
      <symbol name="4" type="line" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" pass="0" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="85,170,255,255" k="line_color"/>
          <prop v="dot" k="line_style"/>
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="5" type="line" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" pass="0" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer enabled="1" pass="0" locked="0" class="MarkerLine">
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
          <prop v="interval" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="1" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@5@1" type="marker" alpha="1" force_rhr="0" clip_to_extent="1">
            <layer enabled="1" pass="0" locked="0" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="85,170,255,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="semi_circle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="no" k="outline_style"/>
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
        </layer>
      </symbol>
      <symbol name="6" type="line" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" pass="0" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="189,189,189,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="2" k="line_width"/>
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
      </symbol>
      <symbol name="7" type="line" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" pass="0" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="92,92,92,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="2" k="line_width"/>
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
      </symbol>
      <symbol name="8" type="line" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" pass="0" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0,0,255" k="line_color"/>
          <prop v="dot" k="line_style"/>
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style allowHtml="0" fieldName="ROWID" previewBkgrdColor="255,255,255,255" fontKerning="1" fontUnderline="0" fontStrikeout="0" fontSize="8.25" textOrientation="horizontal" textColor="0,0,0,255" fontFamily="MS Shell Dlg 2" fontLetterSpacing="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontWeight="50" fontSizeUnit="Point" fontCapitals="0" fontItalic="0" isExpression="0" fontWordSpacing="0" namedStyle="Standaard" useSubstitutions="0" blendMode="0" textOpacity="1" multilineHeight="1">
        <text-buffer bufferSize="1" bufferNoFill="0" bufferBlendMode="0" bufferDraw="0" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferSizeUnits="MM" bufferJoinStyle="64" bufferOpacity="1" bufferColor="255,255,255,255"/>
        <text-mask maskEnabled="0" maskOpacity="1" maskType="0" maskSize="0" maskSizeUnits="MM" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskJoinStyle="128" maskedSymbolLayers=""/>
        <background shapeType="0" shapeRadiiX="0" shapeSizeY="0" shapeSizeUnit="MM" shapeBorderWidthUnit="MM" shapeBlendMode="0" shapeOffsetY="0" shapeRadiiY="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderColor="128,128,128,255" shapeDraw="0" shapeSVGFile="" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiUnit="MM" shapeJoinStyle="64" shapeRotation="0" shapeOffsetUnit="MM" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeSizeType="0" shapeFillColor="255,255,255,255" shapeSizeX="0" shapeRotationType="0" shapeOffsetX="0" shapeOpacity="1" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidth="0">
          <symbol name="markerSymbol" type="marker" alpha="1" force_rhr="0" clip_to_extent="1">
            <layer enabled="1" pass="0" locked="0" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="213,180,60,255" k="color"/>
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
        <shadow shadowOffsetGlobal="1" shadowOpacity="0.7" shadowOffsetAngle="135" shadowDraw="0" shadowRadiusUnit="MM" shadowColor="0,0,0,255" shadowRadius="1.5" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowUnder="0" shadowOffsetUnit="MM" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetDist="1" shadowRadiusAlphaOnly="0" shadowScale="100" shadowBlendMode="6"/>
        <dd_properties>
          <Option type="Map">
            <Option value="" name="name" type="QString"/>
            <Option name="properties"/>
            <Option value="collection" name="type" type="QString"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format leftDirectionSymbol="&lt;" multilineAlign="0" decimals="3" addDirectionSymbol="0" reverseDirectionSymbol="0" wrapChar="" rightDirectionSymbol=">" placeDirectionSymbol="0" formatNumbers="0" plussign="0" autoWrapLength="0" useMaxLineLengthForAutoWrap="1"/>
      <placement overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0" overrunDistanceUnit="MM" quadOffset="4" priority="5" geometryGeneratorEnabled="0" layerType="LineGeometry" placementFlags="10" centroidInside="0" repeatDistance="0" offsetType="0" maxCurvedCharAngleIn="20" geometryGenerator="" distMapUnitScale="3x:0,0,0,0,0,0" offsetUnits="MapUnit" repeatDistanceUnits="MM" placement="2" overrunDistance="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" maxCurvedCharAngleOut="-20" polygonPlacementFlags="2" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" yOffset="0" preserveRotation="1" geometryGeneratorType="PointGeometry" centroidWhole="0" rotationAngle="0" distUnits="MM" xOffset="0" dist="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0"/>
      <rendering mergeLines="0" drawLabels="1" fontMaxPixelSize="10000" upsidedownLabels="0" zIndex="0" scaleMin="1" displayAll="0" fontLimitPixelSize="0" obstacleFactor="1" limitNumLabels="0" scaleVisibility="0" obstacle="1" fontMinPixelSize="3" labelPerPart="0" obstacleType="0" scaleMax="10000000" maxNumLabels="2000" minFeatureSize="0"/>
      <dd_properties>
        <Option type="Map">
          <Option value="" name="name" type="QString"/>
          <Option name="properties"/>
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
          <Option value="point_on_exterior" name="labelAnchorPoint" type="QString"/>
          <Option value="&lt;symbol name=&quot;symbol&quot; type=&quot;line&quot; alpha=&quot;1&quot; force_rhr=&quot;0&quot; clip_to_extent=&quot;1&quot;>&lt;layer enabled=&quot;1&quot; pass=&quot;0&quot; locked=&quot;0&quot; class=&quot;SimpleLine&quot;>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; name=&quot;name&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; name=&quot;type&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" name="lineSymbol" type="QString"/>
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
    <property value="ROWID" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Pie" attributeLegend="1">
    <DiagramCategory spacing="0" rotationOffset="270" showAxis="0" barWidth="5" labelPlacementMethod="XHeight" penWidth="0" lineSizeType="MM" height="15" scaleDependency="Area" direction="1" penColor="#000000" lineSizeScale="3x:0,0,0,0,0,0" diagramOrientation="Up" scaleBasedVisibility="0" penAlpha="255" minimumSize="0" minScaleDenominator="0" backgroundAlpha="255" maxScaleDenominator="1e+08" sizeScale="3x:0,0,0,0,0,0" sizeType="MM" spacingUnitScale="3x:0,0,0,0,0,0" backgroundColor="#ffffff" spacingUnit="MM" enabled="0" width="15" opacity="1">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute field="" label="" color="#000000"/>
      <axisSymbol>
        <symbol name="" type="line" alpha="1" force_rhr="0" clip_to_extent="1">
          <layer enabled="1" pass="0" locked="0" class="SimpleLine">
            <prop v="square" k="capstyle"/>
            <prop v="5;2" k="customdash"/>
            <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
            <prop v="MM" k="customdash_unit"/>
            <prop v="0" k="draw_inside_polygon"/>
            <prop v="bevel" k="joinstyle"/>
            <prop v="35,35,35,255" k="line_color"/>
            <prop v="solid" k="line_style"/>
            <prop v="0.26" k="line_width"/>
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
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings priority="0" placement="2" zIndex="0" dist="0" showAll="1" linePlacementFlags="2" obstacle="0">
    <properties>
      <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <referencedLayers/>
  <referencingLayers/>
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
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_profile_num">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_sewerage_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="0" name="0: mixed" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="1" name="1: rain water" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2: dry weather flow" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="3" name="3: transport" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="4" name="4: spillway" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="5" name="5: sinker" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="6" name="6: storage" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="7" name="7: storage tank" type="QString"/>
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
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="0" name="0: embedded" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="1" name="1: isolated" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2: connected" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="3" name="3: broad crest" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="4" name="4: short crest" type="QString"/>
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
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_invert_level_end_point">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_cross_section_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_friction_type">
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
    <field name="pipe_dist_calc_points">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_material">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="0" name="0: concrete" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="1" name="1: pvc" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2: gres" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="3" name="3: cast iron" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="4" name="4: brickwork" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="5" name="5: HPE" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="6" name="6: HDPE" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="7" name="7: plate iron" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="8" name="8: steel" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_original_length">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_zoom_category">
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
    <field name="pipe_connection_node_start_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_connection_node_end_id">
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
    <alias field="ROWID" name="" index="0"/>
    <alias field="pipe_id" name="id" index="1"/>
    <alias field="pipe_display_name" name="display_name" index="2"/>
    <alias field="pipe_code" name="code" index="3"/>
    <alias field="pipe_profile_num" name="profile_num" index="4"/>
    <alias field="pipe_sewerage_type" name="sewerage_type" index="5"/>
    <alias field="pipe_calculation_type" name="calculation_type" index="6"/>
    <alias field="pipe_invert_level_start_point" name="invert_level_start_point" index="7"/>
    <alias field="pipe_invert_level_end_point" name="invert_level_end_point" index="8"/>
    <alias field="pipe_cross_section_definition_id" name="cross_section_definition_id" index="9"/>
    <alias field="pipe_friction_value" name="friction_value" index="10"/>
    <alias field="pipe_friction_type" name="friction_type" index="11"/>
    <alias field="pipe_dist_calc_points" name="dist_calc_points" index="12"/>
    <alias field="pipe_material" name="material" index="13"/>
    <alias field="pipe_original_length" name="original_length" index="14"/>
    <alias field="pipe_zoom_category" name="zoom_category" index="15"/>
    <alias field="pipe_connection_node_start_id" name="connection_node_start_id" index="16"/>
    <alias field="pipe_connection_node_end_id" name="connection_node_end_id" index="17"/>
    <alias field="def_id" name="id" index="18"/>
    <alias field="def_shape" name="shape" index="19"/>
    <alias field="def_width" name="width" index="20"/>
    <alias field="def_height" name="height" index="21"/>
    <alias field="def_code" name="code" index="22"/>
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
    <constraint exp_strength="0" field="ROWID" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="pipe_id" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint exp_strength="0" field="pipe_display_name" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint exp_strength="0" field="pipe_code" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint exp_strength="0" field="pipe_profile_num" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="pipe_sewerage_type" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint exp_strength="0" field="pipe_calculation_type" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint exp_strength="0" field="pipe_invert_level_start_point" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint exp_strength="2" field="pipe_invert_level_end_point" constraints="5" notnull_strength="2" unique_strength="0"/>
    <constraint exp_strength="0" field="pipe_cross_section_definition_id" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint exp_strength="0" field="pipe_friction_value" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint exp_strength="0" field="pipe_friction_type" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint exp_strength="0" field="pipe_dist_calc_points" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="pipe_material" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="pipe_original_length" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="pipe_zoom_category" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint exp_strength="0" field="pipe_connection_node_start_id" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="pipe_connection_node_end_id" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="def_id" constraints="1" notnull_strength="2" unique_strength="0"/>
    <constraint exp_strength="0" field="def_shape" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="def_width" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="def_height" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="def_code" constraints="0" notnull_strength="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="ROWID" exp="" desc=""/>
    <constraint field="pipe_id" exp="" desc=""/>
    <constraint field="pipe_display_name" exp="" desc=""/>
    <constraint field="pipe_code" exp="" desc=""/>
    <constraint field="pipe_profile_num" exp="" desc=""/>
    <constraint field="pipe_sewerage_type" exp="" desc=""/>
    <constraint field="pipe_calculation_type" exp="" desc=""/>
    <constraint field="pipe_invert_level_start_point" exp="" desc=""/>
    <constraint field="pipe_invert_level_end_point" exp="&quot;invert_level_end_point&quot; is not null" desc=""/>
    <constraint field="pipe_cross_section_definition_id" exp="" desc=""/>
    <constraint field="pipe_friction_value" exp="" desc=""/>
    <constraint field="pipe_friction_type" exp="" desc=""/>
    <constraint field="pipe_dist_calc_points" exp="" desc=""/>
    <constraint field="pipe_material" exp="" desc=""/>
    <constraint field="pipe_original_length" exp="" desc=""/>
    <constraint field="pipe_zoom_category" exp="" desc=""/>
    <constraint field="pipe_connection_node_start_id" exp="" desc=""/>
    <constraint field="pipe_connection_node_end_id" exp="" desc=""/>
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
  <attributetableconfig sortExpression="" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column hidden="0" name="ROWID" type="field" width="-1"/>
      <column hidden="0" name="pipe_id" type="field" width="-1"/>
      <column hidden="0" name="pipe_display_name" type="field" width="-1"/>
      <column hidden="0" name="pipe_code" type="field" width="-1"/>
      <column hidden="0" name="pipe_profile_num" type="field" width="-1"/>
      <column hidden="0" name="pipe_sewerage_type" type="field" width="-1"/>
      <column hidden="0" name="pipe_calculation_type" type="field" width="-1"/>
      <column hidden="0" name="pipe_invert_level_start_point" type="field" width="-1"/>
      <column hidden="0" name="pipe_invert_level_end_point" type="field" width="-1"/>
      <column hidden="0" name="pipe_cross_section_definition_id" type="field" width="-1"/>
      <column hidden="0" name="pipe_friction_value" type="field" width="-1"/>
      <column hidden="0" name="pipe_friction_type" type="field" width="-1"/>
      <column hidden="0" name="pipe_dist_calc_points" type="field" width="-1"/>
      <column hidden="0" name="pipe_material" type="field" width="-1"/>
      <column hidden="0" name="pipe_original_length" type="field" width="-1"/>
      <column hidden="0" name="pipe_zoom_category" type="field" width="-1"/>
      <column hidden="0" name="pipe_connection_node_start_id" type="field" width="-1"/>
      <column hidden="0" name="pipe_connection_node_end_id" type="field" width="-1"/>
      <column hidden="0" name="def_id" type="field" width="-1"/>
      <column hidden="0" name="def_shape" type="field" width="-1"/>
      <column hidden="0" name="def_width" type="field" width="-1"/>
      <column hidden="0" name="def_height" type="field" width="-1"/>
      <column hidden="0" name="def_code" type="field" width="-1"/>
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
    <attributeEditorContainer showLabel="1" groupBox="0" name="Pipe view" visibilityExpressionEnabled="0" columnCount="1" visibilityExpression="">
      <attributeEditorContainer showLabel="1" groupBox="1" name="General" visibilityExpressionEnabled="0" columnCount="1" visibilityExpression="">
        <attributeEditorField showLabel="1" name="pipe_id" index="1"/>
        <attributeEditorField showLabel="1" name="pipe_display_name" index="2"/>
        <attributeEditorField showLabel="1" name="pipe_code" index="3"/>
        <attributeEditorField showLabel="1" name="pipe_calculation_type" index="6"/>
        <attributeEditorField showLabel="1" name="pipe_dist_calc_points" index="12"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" groupBox="1" name="Characteristics" visibilityExpressionEnabled="0" columnCount="1" visibilityExpression="">
        <attributeEditorField showLabel="1" name="pipe_invert_level_start_point" index="7"/>
        <attributeEditorField showLabel="1" name="pipe_invert_level_end_point" index="8"/>
        <attributeEditorField showLabel="1" name="pipe_friction_value" index="10"/>
        <attributeEditorField showLabel="1" name="pipe_friction_type" index="11"/>
        <attributeEditorField showLabel="1" name="pipe_material" index="13"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" groupBox="1" name="Cross section definition" visibilityExpressionEnabled="0" columnCount="1" visibilityExpression="">
        <attributeEditorField showLabel="1" name="pipe_cross_section_definition_id" index="9"/>
        <attributeEditorField showLabel="1" name="def_shape" index="19"/>
        <attributeEditorField showLabel="1" name="def_width" index="20"/>
        <attributeEditorField showLabel="1" name="def_height" index="21"/>
        <attributeEditorField showLabel="1" name="def_code" index="22"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" groupBox="1" name="Visualization" visibilityExpressionEnabled="0" columnCount="1" visibilityExpression="">
        <attributeEditorField showLabel="1" name="pipe_sewerage_type" index="5"/>
        <attributeEditorField showLabel="1" name="pipe_zoom_category" index="15"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" groupBox="1" name="Connection nodes" visibilityExpressionEnabled="0" columnCount="1" visibilityExpression="">
        <attributeEditorField showLabel="1" name="pipe_connection_node_start_id" index="16"/>
        <attributeEditorField showLabel="1" name="pipe_connection_node_end_id" index="17"/>
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
    <field name="ROWID" labelOnTop="0"/>
    <field name="def_code" labelOnTop="0"/>
    <field name="def_height" labelOnTop="0"/>
    <field name="def_id" labelOnTop="0"/>
    <field name="def_shape" labelOnTop="0"/>
    <field name="def_width" labelOnTop="0"/>
    <field name="pipe_calculation_type" labelOnTop="0"/>
    <field name="pipe_code" labelOnTop="0"/>
    <field name="pipe_connection_node_end_id" labelOnTop="0"/>
    <field name="pipe_connection_node_start_id" labelOnTop="0"/>
    <field name="pipe_cross_section_definition_id" labelOnTop="0"/>
    <field name="pipe_display_name" labelOnTop="0"/>
    <field name="pipe_dist_calc_points" labelOnTop="0"/>
    <field name="pipe_friction_type" labelOnTop="0"/>
    <field name="pipe_friction_value" labelOnTop="0"/>
    <field name="pipe_id" labelOnTop="0"/>
    <field name="pipe_invert_level_end_point" labelOnTop="0"/>
    <field name="pipe_invert_level_start_point" labelOnTop="0"/>
    <field name="pipe_material" labelOnTop="0"/>
    <field name="pipe_original_length" labelOnTop="0"/>
    <field name="pipe_pipe_quality" labelOnTop="0"/>
    <field name="pipe_profile_num" labelOnTop="0"/>
    <field name="pipe_sewerage_type" labelOnTop="0"/>
    <field name="pipe_zoom_category" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"ROWID"</previewExpression>
  <mapTip>display_name</mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
