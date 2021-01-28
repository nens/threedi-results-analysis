<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="1" readOnly="0" simplifyAlgorithm="0" version="3.10.10-A Coruña" maxScale="-4.65661e-10" hasScaleBasedVisibilityFlag="0" simplifyMaxScale="1" minScale="1e+08" simplifyDrawingHints="0" simplifyLocal="1" styleCategories="AllStyleCategories" simplifyDrawingTol="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 type="RuleRenderer" symbollevels="0" enableorderby="0" forceraster="0">
    <rules key="{4fbba513-a3b1-4a92-97bc-3d44735ac986}">
      <rule symbol="0" filter="manh_manhole_indicator = 0" label="Manhole (inspection)" scalemaxdenom="5000" key="{a951db60-faa9-4c95-9eaa-a51d84ff90b1}"/>
      <rule symbol="1" filter="manh_manhole_indicator = 1" label="Outlet" scalemaxdenom="15000" key="{c9e7ab73-45d5-45d6-970d-b4e28230c1e5}"/>
      <rule symbol="2" filter="manh_manhole_indicator = 2" label="Pumping station" key="{a1d98efc-8098-4201-a75e-93dc7c47f076}"/>
      <rule symbol="3" filter="ELSE" label="Manhole (unspecified)" scalemaxdenom="5000" key="{1b6d21ed-8a83-4e3f-850e-ca64e766f7da}"/>
    </rules>
    <symbols>
      <symbol force_rhr="0" clip_to_extent="1" alpha="1" type="marker" name="0">
        <layer pass="0" locked="0" class="SimpleMarker" enabled="1">
          <prop k="angle" v="0"/>
          <prop k="color" v="85,255,127,0"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="square"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
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
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" clip_to_extent="1" alpha="1" type="marker" name="1">
        <layer pass="0" locked="0" class="SimpleMarker" enabled="1">
          <prop k="angle" v="0"/>
          <prop k="color" v="63,128,192,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="miter"/>
          <prop k="name" v="square"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="85,170,255,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.75"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="2.5"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <effect type="effectStack" enabled="0">
            <effect type="dropShadow">
              <prop k="blend_mode" v="13"/>
              <prop k="blur_level" v="0.5"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color" v="0,0,0,255"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="1"/>
              <prop k="offset_angle" v="135"/>
              <prop k="offset_distance" v="0.2"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="offset_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="opacity" v="1"/>
            </effect>
            <effect type="outerGlow">
              <prop k="blend_mode" v="0"/>
              <prop k="blur_level" v="2.645"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color1" v="0,0,255,255"/>
              <prop k="color2" v="0,255,0,255"/>
              <prop k="color_type" v="0"/>
              <prop k="discrete" v="0"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="0"/>
              <prop k="opacity" v="0.5"/>
              <prop k="rampType" v="gradient"/>
              <prop k="single_color" v="255,255,255,255"/>
              <prop k="spread" v="2"/>
              <prop k="spread_unit" v="MM"/>
              <prop k="spread_unit_scale" v="3x:0,0,0,0,0,0"/>
            </effect>
            <effect type="drawSource">
              <prop k="blend_mode" v="0"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="1"/>
              <prop k="opacity" v="1"/>
            </effect>
            <effect type="innerShadow">
              <prop k="blend_mode" v="13"/>
              <prop k="blur_level" v="2.645"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color" v="0,0,0,255"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="0"/>
              <prop k="offset_angle" v="135"/>
              <prop k="offset_distance" v="2"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="offset_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="opacity" v="1"/>
            </effect>
            <effect type="innerGlow">
              <prop k="blend_mode" v="0"/>
              <prop k="blur_level" v="2.645"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color1" v="0,0,255,255"/>
              <prop k="color2" v="0,255,0,255"/>
              <prop k="color_type" v="0"/>
              <prop k="discrete" v="0"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="0"/>
              <prop k="opacity" v="0.5"/>
              <prop k="rampType" v="gradient"/>
              <prop k="single_color" v="255,255,255,255"/>
              <prop k="spread" v="2"/>
              <prop k="spread_unit" v="MM"/>
              <prop k="spread_unit_scale" v="3x:0,0,0,0,0,0"/>
            </effect>
          </effect>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" value="" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option type="bool" value="true" name="active"/>
                  <Option type="QString" value="if(@map_scale&lt;10000, 2.5,1.5)" name="expression"/>
                  <Option type="int" value="3" name="type"/>
                </Option>
              </Option>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" clip_to_extent="1" alpha="1" type="marker" name="2">
        <layer pass="0" locked="0" class="SimpleMarker" enabled="1">
          <prop k="angle" v="0"/>
          <prop k="color" v="85,255,127,0"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="pentagon"/>
          <prop k="offset" v="0.10000000000000001,0.10000000000000001"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,183"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.7"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="4.1"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <effect type="effectStack" enabled="0">
            <effect type="dropShadow">
              <prop k="blend_mode" v="13"/>
              <prop k="blur_level" v="0.5"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color" v="0,0,0,255"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="1"/>
              <prop k="offset_angle" v="135"/>
              <prop k="offset_distance" v="0.2"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="offset_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="opacity" v="1"/>
            </effect>
            <effect type="outerGlow">
              <prop k="blend_mode" v="0"/>
              <prop k="blur_level" v="2.645"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color1" v="0,0,255,255"/>
              <prop k="color2" v="0,255,0,255"/>
              <prop k="color_type" v="0"/>
              <prop k="discrete" v="0"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="0"/>
              <prop k="opacity" v="0.5"/>
              <prop k="rampType" v="gradient"/>
              <prop k="single_color" v="255,255,255,255"/>
              <prop k="spread" v="2"/>
              <prop k="spread_unit" v="MM"/>
              <prop k="spread_unit_scale" v="3x:0,0,0,0,0,0"/>
            </effect>
            <effect type="drawSource">
              <prop k="blend_mode" v="0"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="1"/>
              <prop k="opacity" v="1"/>
            </effect>
            <effect type="innerShadow">
              <prop k="blend_mode" v="13"/>
              <prop k="blur_level" v="2.645"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color" v="0,0,0,255"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="0"/>
              <prop k="offset_angle" v="135"/>
              <prop k="offset_distance" v="2"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="offset_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="opacity" v="1"/>
            </effect>
            <effect type="innerGlow">
              <prop k="blend_mode" v="0"/>
              <prop k="blur_level" v="2.645"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color1" v="0,0,255,255"/>
              <prop k="color2" v="0,255,0,255"/>
              <prop k="color_type" v="0"/>
              <prop k="discrete" v="0"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="0"/>
              <prop k="opacity" v="0.5"/>
              <prop k="rampType" v="gradient"/>
              <prop k="single_color" v="255,255,255,255"/>
              <prop k="spread" v="2"/>
              <prop k="spread_unit" v="MM"/>
              <prop k="spread_unit_scale" v="3x:0,0,0,0,0,0"/>
            </effect>
          </effect>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" value="" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option type="bool" value="true" name="active"/>
                  <Option type="QString" value="if(@map_scale&lt;10000, 4.1,3.1)" name="expression"/>
                  <Option type="int" value="3" name="type"/>
                </Option>
              </Option>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" locked="0" class="SimpleMarker" enabled="1">
          <prop k="angle" v="0"/>
          <prop k="color" v="85,255,127,0"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="pentagon"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,127,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.7"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="4"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <effect type="effectStack" enabled="0">
            <effect type="dropShadow">
              <prop k="blend_mode" v="13"/>
              <prop k="blur_level" v="0.5"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color" v="0,0,0,255"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="1"/>
              <prop k="offset_angle" v="135"/>
              <prop k="offset_distance" v="0.2"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="offset_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="opacity" v="1"/>
            </effect>
            <effect type="outerGlow">
              <prop k="blend_mode" v="0"/>
              <prop k="blur_level" v="2.645"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color1" v="0,0,255,255"/>
              <prop k="color2" v="0,255,0,255"/>
              <prop k="color_type" v="0"/>
              <prop k="discrete" v="0"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="0"/>
              <prop k="opacity" v="0.5"/>
              <prop k="rampType" v="gradient"/>
              <prop k="single_color" v="255,255,255,255"/>
              <prop k="spread" v="2"/>
              <prop k="spread_unit" v="MM"/>
              <prop k="spread_unit_scale" v="3x:0,0,0,0,0,0"/>
            </effect>
            <effect type="drawSource">
              <prop k="blend_mode" v="0"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="1"/>
              <prop k="opacity" v="1"/>
            </effect>
            <effect type="innerShadow">
              <prop k="blend_mode" v="13"/>
              <prop k="blur_level" v="2.645"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color" v="0,0,0,255"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="0"/>
              <prop k="offset_angle" v="135"/>
              <prop k="offset_distance" v="2"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="offset_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="opacity" v="1"/>
            </effect>
            <effect type="innerGlow">
              <prop k="blend_mode" v="0"/>
              <prop k="blur_level" v="2.645"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color1" v="0,0,255,255"/>
              <prop k="color2" v="0,255,0,255"/>
              <prop k="color_type" v="0"/>
              <prop k="discrete" v="0"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="0"/>
              <prop k="opacity" v="0.5"/>
              <prop k="rampType" v="gradient"/>
              <prop k="single_color" v="255,255,255,255"/>
              <prop k="spread" v="2"/>
              <prop k="spread_unit" v="MM"/>
              <prop k="spread_unit_scale" v="3x:0,0,0,0,0,0"/>
            </effect>
          </effect>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" value="" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option type="bool" value="true" name="active"/>
                  <Option type="QString" value="if(@map_scale&lt;10000, 4,3)" name="expression"/>
                  <Option type="int" value="3" name="type"/>
                </Option>
              </Option>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" clip_to_extent="1" alpha="1" type="marker" name="3">
        <layer pass="0" locked="0" class="SimpleMarker" enabled="1">
          <prop k="angle" v="0"/>
          <prop k="color" v="85,255,127,0"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="square"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,9,1,255"/>
          <prop k="outline_style" v="dot"/>
          <prop k="outline_width" v="0.25"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style fontItalic="0" multilineHeight="1" blendMode="0" fontCapitals="0" fontWeight="50" useSubstitutions="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fieldName="'s:' || coalesce(manh_surface_level, 'NULL') || '\n' ||&#xd;&#xa;'d:' || coalesce(manh_drain_level, 'NULL') ||  '\n' || &#xd;&#xa;'b:' || coalesce(manh_bottom_level, 'NULL') " fontUnderline="0" fontWordSpacing="0" fontLetterSpacing="0" fontFamily="MS Gothic" fontStrikeout="0" fontKerning="1" fontSizeUnit="Point" textOrientation="horizontal" textOpacity="1" isExpression="1" fontSize="8" textColor="0,0,0,255" previewBkgrdColor="255,255,255,255" namedStyle="Regular">
        <text-buffer bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferJoinStyle="128" bufferNoFill="1" bufferSizeUnits="MM" bufferDraw="1" bufferColor="255,255,255,255" bufferBlendMode="0" bufferOpacity="1" bufferSize="0.7"/>
        <background shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeSizeUnit="MM" shapeType="0" shapeOffsetUnit="MM" shapeRadiiX="0" shapeJoinStyle="64" shapeOffsetX="0" shapeOffsetY="0" shapeBlendMode="0" shapeSVGFile="" shapeRotationType="0" shapeBorderColor="128,128,128,255" shapeOpacity="1" shapeRotation="0" shapeSizeY="0" shapeFillColor="255,255,255,255" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeDraw="0" shapeSizeX="0" shapeRadiiY="0" shapeSizeType="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiUnit="MM" shapeBorderWidthUnit="MM" shapeBorderWidth="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0">
          <symbol force_rhr="0" clip_to_extent="1" alpha="1" type="marker" name="markerSymbol">
            <layer pass="0" locked="0" class="SimpleMarker" enabled="1">
              <prop k="angle" v="0"/>
              <prop k="color" v="125,139,143,255"/>
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
                  <Option type="QString" value="" name="name"/>
                  <Option name="properties"/>
                  <Option type="QString" value="collection" name="type"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </background>
        <shadow shadowOffsetAngle="135" shadowRadius="1.5" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetGlobal="1" shadowScale="100" shadowRadiusUnit="MM" shadowDraw="0" shadowRadiusAlphaOnly="0" shadowOffsetDist="1" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowColor="0,0,0,255" shadowBlendMode="6" shadowOpacity="0.7" shadowOffsetUnit="MM" shadowUnder="0"/>
        <dd_properties>
          <Option type="Map">
            <Option type="QString" value="" name="name"/>
            <Option name="properties"/>
            <Option type="QString" value="collection" name="type"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format decimals="3" formatNumbers="0" autoWrapLength="0" addDirectionSymbol="0" reverseDirectionSymbol="0" multilineAlign="3" placeDirectionSymbol="0" plussign="0" useMaxLineLengthForAutoWrap="1" wrapChar="" leftDirectionSymbol="&lt;" rightDirectionSymbol=">"/>
      <placement repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" priority="5" repeatDistanceUnits="MM" xOffset="1" yOffset="-1" placementFlags="10" quadOffset="2" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" maxCurvedCharAngleIn="25" centroidInside="0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" overrunDistanceUnit="MM" layerType="PointGeometry" offsetUnits="MM" distUnits="MM" offsetType="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" distMapUnitScale="3x:0,0,0,0,0,0" preserveRotation="1" centroidWhole="0" rotationAngle="0" maxCurvedCharAngleOut="-25" geometryGeneratorType="PointGeometry" fitInPolygonOnly="0" geometryGeneratorEnabled="0" placement="1" dist="0" overrunDistance="0" repeatDistance="0" geometryGenerator=""/>
      <rendering displayAll="0" fontMinPixelSize="3" maxNumLabels="2000" fontLimitPixelSize="0" minFeatureSize="0" scaleMax="1000" fontMaxPixelSize="10000" mergeLines="0" drawLabels="1" obstacleType="0" scaleMin="0" obstacle="1" scaleVisibility="1" obstacleFactor="1" zIndex="0" upsidedownLabels="0" limitNumLabels="0" labelPerPart="0"/>
      <dd_properties>
        <Option type="Map">
          <Option type="QString" value="" name="name"/>
          <Option name="properties"/>
          <Option type="QString" value="collection" name="type"/>
        </Option>
      </dd_properties>
      <callout type="simple">
        <Option type="Map">
          <Option type="QString" value="pole_of_inaccessibility" name="anchorPoint"/>
          <Option type="Map" name="ddProperties">
            <Option type="QString" value="" name="name"/>
            <Option name="properties"/>
            <Option type="QString" value="collection" name="type"/>
          </Option>
          <Option type="bool" value="false" name="drawToAllParts"/>
          <Option type="QString" value="0" name="enabled"/>
          <Option type="QString" value="&lt;symbol force_rhr=&quot;0&quot; clip_to_extent=&quot;1&quot; alpha=&quot;1&quot; type=&quot;line&quot; name=&quot;symbol&quot;>&lt;layer pass=&quot;0&quot; locked=&quot;0&quot; class=&quot;SimpleLine&quot; enabled=&quot;1&quot;>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option type=&quot;QString&quot; value=&quot;&quot; name=&quot;name&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option type=&quot;QString&quot; value=&quot;collection&quot; name=&quot;type&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" name="lineSymbol"/>
          <Option type="double" value="0" name="minLength"/>
          <Option type="QString" value="3x:0,0,0,0,0,0" name="minLengthMapUnitScale"/>
          <Option type="QString" value="MM" name="minLengthUnit"/>
          <Option type="double" value="0" name="offsetFromAnchor"/>
          <Option type="QString" value="3x:0,0,0,0,0,0" name="offsetFromAnchorMapUnitScale"/>
          <Option type="QString" value="MM" name="offsetFromAnchorUnit"/>
          <Option type="double" value="0" name="offsetFromLabel"/>
          <Option type="QString" value="3x:0,0,0,0,0,0" name="offsetFromLabelMapUnitScale"/>
          <Option type="QString" value="MM" name="offsetFromLabelUnit"/>
        </Option>
      </callout>
    </settings>
  </labeling>
  <customproperties>
    <property value="manh_display_name" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Pie">
    <DiagramCategory penAlpha="255" opacity="1" lineSizeScale="3x:0,0,0,0,0,0" labelPlacementMethod="XHeight" backgroundAlpha="255" width="15" penWidth="0" lineSizeType="MM" maxScaleDenominator="1e+08" height="15" sizeScale="3x:0,0,0,0,0,0" scaleDependency="Area" diagramOrientation="Up" sizeType="MM" minScaleDenominator="-4.65661e-10" penColor="#000000" barWidth="5" scaleBasedVisibility="0" enabled="0" backgroundColor="#ffffff" rotationOffset="270" minimumSize="0">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute field="" color="#000000" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings dist="0" obstacle="0" linePlacementFlags="2" priority="0" showAll="1" placement="0" zIndex="0">
    <properties>
      <Option type="Map">
        <Option type="QString" value="" name="name"/>
        <Option name="properties"/>
        <Option type="QString" value="collection" name="type"/>
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
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_connection_node_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_shape">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" value="00" name="00: square"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="01" name="01: round"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="02" name="02: rectangle"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_width">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_length">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_manhole_indicator">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" value="0" name="0: inspection"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="1" name="1: outlet"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="2" name="2: pump"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_calculation_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" value="0" name="0: embedded"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="1" name="1: isolated"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="2" name="2: connected"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_bottom_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_surface_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_drain_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_sediment_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_zoom_category">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" value="-1" name="-1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="0" name="0"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="1" name="1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="2" name="2"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="3" name="3"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="4" name="4"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="5" name="5"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_storage_area">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_initial_waterlevel">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_the_geom_linestring">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="ROWID" name="" index="0"/>
    <alias field="manh_id" name="id" index="1"/>
    <alias field="manh_display_name" name="display_name" index="2"/>
    <alias field="manh_code" name="code" index="3"/>
    <alias field="manh_connection_node_id" name="connection_node_id" index="4"/>
    <alias field="manh_shape" name="shape" index="5"/>
    <alias field="manh_width" name="width" index="6"/>
    <alias field="manh_length" name="length" index="7"/>
    <alias field="manh_manhole_indicator" name="manhole_indicator" index="8"/>
    <alias field="manh_calculation_type" name="calculation_type" index="9"/>
    <alias field="manh_bottom_level" name="bottom_level" index="10"/>
    <alias field="manh_surface_level" name="surface_level" index="11"/>
    <alias field="manh_drain_level" name="drain_level" index="12"/>
    <alias field="manh_sediment_level" name="sediment_level" index="13"/>
    <alias field="manh_zoom_category" name="zoom_category" index="14"/>
    <alias field="node_id" name="" index="15"/>
    <alias field="node_storage_area" name="" index="16"/>
    <alias field="node_initial_waterlevel" name="" index="17"/>
    <alias field="node_code" name="" index="18"/>
    <alias field="node_the_geom_linestring" name="the_geom_linestring" index="19"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="ROWID" expression="" applyOnUpdate="0"/>
    <default field="manh_id" expression="if(maximum(manh_id) is null,1, maximum(manh_id)+1)" applyOnUpdate="0"/>
    <default field="manh_display_name" expression="'new'" applyOnUpdate="0"/>
    <default field="manh_code" expression="'new'" applyOnUpdate="0"/>
    <default field="manh_connection_node_id" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,geometry(@parent))) is null,'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,geometry(@parent))))" applyOnUpdate="0"/>
    <default field="manh_shape" expression="" applyOnUpdate="0"/>
    <default field="manh_width" expression="" applyOnUpdate="0"/>
    <default field="manh_length" expression="" applyOnUpdate="0"/>
    <default field="manh_manhole_indicator" expression="'0'" applyOnUpdate="0"/>
    <default field="manh_calculation_type" expression="" applyOnUpdate="0"/>
    <default field="manh_bottom_level" expression="&quot;manh_bottom_level&quot;&lt;&quot;manh_surface_level&quot;" applyOnUpdate="0"/>
    <default field="manh_surface_level" expression="" applyOnUpdate="0"/>
    <default field="manh_drain_level" expression="" applyOnUpdate="0"/>
    <default field="manh_sediment_level" expression="" applyOnUpdate="0"/>
    <default field="manh_zoom_category" expression="1" applyOnUpdate="0"/>
    <default field="node_id" expression="'filled automatically'" applyOnUpdate="0"/>
    <default field="node_storage_area" expression="" applyOnUpdate="0"/>
    <default field="node_initial_waterlevel" expression="" applyOnUpdate="0"/>
    <default field="node_code" expression="'new'" applyOnUpdate="0"/>
    <default field="node_the_geom_linestring" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="ROWID" notnull_strength="0" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint field="manh_id" notnull_strength="0" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint field="manh_display_name" notnull_strength="2" unique_strength="0" exp_strength="0" constraints="1"/>
    <constraint field="manh_code" notnull_strength="2" unique_strength="0" exp_strength="0" constraints="1"/>
    <constraint field="manh_connection_node_id" notnull_strength="2" unique_strength="0" exp_strength="0" constraints="1"/>
    <constraint field="manh_shape" notnull_strength="2" unique_strength="0" exp_strength="0" constraints="1"/>
    <constraint field="manh_width" notnull_strength="2" unique_strength="0" exp_strength="0" constraints="1"/>
    <constraint field="manh_length" notnull_strength="0" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint field="manh_manhole_indicator" notnull_strength="2" unique_strength="0" exp_strength="0" constraints="1"/>
    <constraint field="manh_calculation_type" notnull_strength="2" unique_strength="0" exp_strength="0" constraints="1"/>
    <constraint field="manh_bottom_level" notnull_strength="2" unique_strength="0" exp_strength="0" constraints="1"/>
    <constraint field="manh_surface_level" notnull_strength="2" unique_strength="0" exp_strength="0" constraints="1"/>
    <constraint field="manh_drain_level" notnull_strength="0" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint field="manh_sediment_level" notnull_strength="0" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint field="manh_zoom_category" notnull_strength="2" unique_strength="0" exp_strength="0" constraints="1"/>
    <constraint field="node_id" notnull_strength="0" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint field="node_storage_area" notnull_strength="0" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint field="node_initial_waterlevel" notnull_strength="0" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint field="node_code" notnull_strength="2" unique_strength="0" exp_strength="0" constraints="1"/>
    <constraint field="node_the_geom_linestring" notnull_strength="0" unique_strength="0" exp_strength="0" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="ROWID" exp="" desc=""/>
    <constraint field="manh_id" exp="" desc=""/>
    <constraint field="manh_display_name" exp="" desc=""/>
    <constraint field="manh_code" exp="" desc=""/>
    <constraint field="manh_connection_node_id" exp="" desc=""/>
    <constraint field="manh_shape" exp="" desc=""/>
    <constraint field="manh_width" exp="" desc=""/>
    <constraint field="manh_length" exp="" desc=""/>
    <constraint field="manh_manhole_indicator" exp="" desc=""/>
    <constraint field="manh_calculation_type" exp="" desc=""/>
    <constraint field="manh_bottom_level" exp="" desc=""/>
    <constraint field="manh_surface_level" exp="" desc=""/>
    <constraint field="manh_drain_level" exp="" desc=""/>
    <constraint field="manh_sediment_level" exp="" desc=""/>
    <constraint field="manh_zoom_category" exp="" desc=""/>
    <constraint field="node_id" exp="" desc=""/>
    <constraint field="node_storage_area" exp="" desc=""/>
    <constraint field="node_initial_waterlevel" exp="" desc=""/>
    <constraint field="node_code" exp="" desc=""/>
    <constraint field="node_the_geom_linestring" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="&quot;manh_manhole_indicator&quot;">
    <columns>
      <column width="-1" hidden="0" type="field" name="ROWID"/>
      <column width="-1" hidden="0" type="field" name="manh_id"/>
      <column width="-1" hidden="0" type="field" name="manh_display_name"/>
      <column width="-1" hidden="0" type="field" name="manh_code"/>
      <column width="-1" hidden="0" type="field" name="manh_connection_node_id"/>
      <column width="-1" hidden="0" type="field" name="manh_shape"/>
      <column width="-1" hidden="0" type="field" name="manh_width"/>
      <column width="-1" hidden="0" type="field" name="manh_length"/>
      <column width="-1" hidden="0" type="field" name="manh_manhole_indicator"/>
      <column width="-1" hidden="0" type="field" name="manh_calculation_type"/>
      <column width="-1" hidden="0" type="field" name="manh_bottom_level"/>
      <column width="-1" hidden="0" type="field" name="manh_surface_level"/>
      <column width="-1" hidden="0" type="field" name="manh_drain_level"/>
      <column width="-1" hidden="0" type="field" name="manh_sediment_level"/>
      <column width="-1" hidden="0" type="field" name="manh_zoom_category"/>
      <column width="-1" hidden="0" type="field" name="node_id"/>
      <column width="-1" hidden="0" type="field" name="node_storage_area"/>
      <column width="-1" hidden="0" type="field" name="node_initial_waterlevel"/>
      <column width="-1" hidden="0" type="field" name="node_code"/>
      <column width="-1" hidden="0" type="field" name="node_the_geom_linestring"/>
      <column width="-1" hidden="1" type="actions"/>
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
    <attributeEditorContainer visibilityExpressionEnabled="0" visibilityExpression="" groupBox="0" name="Manhole_view" columnCount="1" showLabel="1">
      <attributeEditorContainer visibilityExpressionEnabled="0" visibilityExpression="" groupBox="1" name="General" columnCount="1" showLabel="1">
        <attributeEditorField name="manh_id" showLabel="1" index="1"/>
        <attributeEditorField name="manh_display_name" showLabel="1" index="2"/>
        <attributeEditorField name="manh_code" showLabel="1" index="3"/>
        <attributeEditorField name="manh_calculation_type" showLabel="1" index="9"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpressionEnabled="0" visibilityExpression="" groupBox="1" name="Characteristics" columnCount="1" showLabel="1">
        <attributeEditorField name="manh_shape" showLabel="1" index="5"/>
        <attributeEditorField name="manh_width" showLabel="1" index="6"/>
        <attributeEditorField name="manh_length" showLabel="1" index="7"/>
        <attributeEditorField name="manh_bottom_level" showLabel="1" index="10"/>
        <attributeEditorField name="manh_surface_level" showLabel="1" index="11"/>
        <attributeEditorField name="manh_drain_level" showLabel="1" index="12"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpressionEnabled="0" visibilityExpression="" groupBox="1" name="Visualisation" columnCount="1" showLabel="1">
        <attributeEditorField name="manh_manhole_indicator" showLabel="1" index="8"/>
        <attributeEditorField name="manh_zoom_category" showLabel="1" index="14"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpressionEnabled="0" visibilityExpression="" groupBox="1" name="Connection node" columnCount="1" showLabel="1">
        <attributeEditorField name="manh_connection_node_id" showLabel="1" index="4"/>
        <attributeEditorField name="node_code" showLabel="1" index="18"/>
        <attributeEditorField name="node_initial_waterlevel" showLabel="1" index="17"/>
        <attributeEditorField name="node_storage_area" showLabel="1" index="16"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="ROWID"/>
    <field editable="1" name="manh_bottom_level"/>
    <field editable="1" name="manh_calculation_type"/>
    <field editable="1" name="manh_code"/>
    <field editable="0" name="manh_connection_node_id"/>
    <field editable="1" name="manh_display_name"/>
    <field editable="1" name="manh_drain_level"/>
    <field editable="0" name="manh_id"/>
    <field editable="1" name="manh_length"/>
    <field editable="1" name="manh_manhole_indicator"/>
    <field editable="1" name="manh_sediment_level"/>
    <field editable="1" name="manh_shape"/>
    <field editable="1" name="manh_surface_level"/>
    <field editable="1" name="manh_width"/>
    <field editable="1" name="manh_zoom_category"/>
    <field editable="1" name="node_code"/>
    <field editable="0" name="node_id"/>
    <field editable="1" name="node_initial_waterlevel"/>
    <field editable="1" name="node_storage_area"/>
    <field editable="1" name="node_the_geom_linestring"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="ROWID"/>
    <field labelOnTop="0" name="manh_bottom_level"/>
    <field labelOnTop="0" name="manh_calculation_type"/>
    <field labelOnTop="0" name="manh_code"/>
    <field labelOnTop="0" name="manh_connection_node_id"/>
    <field labelOnTop="0" name="manh_display_name"/>
    <field labelOnTop="0" name="manh_drain_level"/>
    <field labelOnTop="0" name="manh_id"/>
    <field labelOnTop="0" name="manh_length"/>
    <field labelOnTop="0" name="manh_manhole_indicator"/>
    <field labelOnTop="0" name="manh_sediment_level"/>
    <field labelOnTop="0" name="manh_shape"/>
    <field labelOnTop="0" name="manh_surface_level"/>
    <field labelOnTop="0" name="manh_width"/>
    <field labelOnTop="0" name="manh_zoom_category"/>
    <field labelOnTop="0" name="node_code"/>
    <field labelOnTop="0" name="node_id"/>
    <field labelOnTop="0" name="node_initial_waterlevel"/>
    <field labelOnTop="0" name="node_storage_area"/>
    <field labelOnTop="0" name="node_the_geom_linestring"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>"manh_display_name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
