<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyMaxScale="1" simplifyAlgorithm="0" hasScaleBasedVisibilityFlag="0" version="3.10.10-A Coruña" maxScale="-4.65661e-10" simplifyDrawingHints="0" readOnly="0" labelsEnabled="1" simplifyDrawingTol="1" styleCategories="AllStyleCategories" minScale="1e+08" simplifyLocal="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" type="RuleRenderer" enableorderby="0" symbollevels="0">
    <rules key="{4fbba513-a3b1-4a92-97bc-3d44735ac986}">
      <rule filter="manh_manhole_indicator = 0" scalemaxdenom="2500" key="{a951db60-faa9-4c95-9eaa-a51d84ff90b1}" symbol="0" label="Manhole (inspection)"/>
      <rule filter="manh_manhole_indicator = 1" scalemaxdenom="15000" key="{c9e7ab73-45d5-45d6-970d-b4e28230c1e5}" symbol="1" label="Outlet"/>
      <rule filter="manh_manhole_indicator = 2" key="{a1d98efc-8098-4201-a75e-93dc7c47f076}" symbol="2" label="Pumping station"/>
      <rule filter="ELSE" scalemaxdenom="2500" key="{1b6d21ed-8a83-4e3f-850e-ca64e766f7da}" symbol="3" label="Manhole (unspecified)"/>
    </rules>
    <symbols>
      <symbol name="0" force_rhr="0" type="marker" alpha="1" clip_to_extent="1">
        <layer class="SimpleMarker" enabled="1" pass="0" locked="0">
          <prop v="0" k="angle"/>
          <prop v="85,255,127,0" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="square" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
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
      <symbol name="1" force_rhr="0" type="marker" alpha="1" clip_to_extent="1">
        <layer class="SimpleMarker" enabled="1" pass="0" locked="0">
          <prop v="0" k="angle"/>
          <prop v="85,255,127,0" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="miter" k="joinstyle"/>
          <prop v="square" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="85,170,255,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.75" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="2.5" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <effect enabled="1" type="effectStack">
            <effect type="dropShadow">
              <prop v="13" k="blend_mode"/>
              <prop v="0.5" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="2" k="draw_mode"/>
              <prop v="1" k="enabled"/>
              <prop v="135" k="offset_angle"/>
              <prop v="0.2" k="offset_distance"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="outerGlow">
              <prop v="0" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,255,255" k="color1"/>
              <prop v="0,255,0,255" k="color2"/>
              <prop v="0" k="color_type"/>
              <prop v="0" k="discrete"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="0.5" k="opacity"/>
              <prop v="gradient" k="rampType"/>
              <prop v="255,255,255,255" k="single_color"/>
              <prop v="2" k="spread"/>
              <prop v="MM" k="spread_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="spread_unit_scale"/>
            </effect>
            <effect type="drawSource">
              <prop v="0" k="blend_mode"/>
              <prop v="2" k="draw_mode"/>
              <prop v="1" k="enabled"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="innerShadow">
              <prop v="13" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="135" k="offset_angle"/>
              <prop v="2" k="offset_distance"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="innerGlow">
              <prop v="0" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,255,255" k="color1"/>
              <prop v="0,255,0,255" k="color2"/>
              <prop v="0" k="color_type"/>
              <prop v="0" k="discrete"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="0.5" k="opacity"/>
              <prop v="gradient" k="rampType"/>
              <prop v="255,255,255,255" k="single_color"/>
              <prop v="2" k="spread"/>
              <prop v="MM" k="spread_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="spread_unit_scale"/>
            </effect>
          </effect>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="2" force_rhr="0" type="marker" alpha="1" clip_to_extent="1">
        <layer class="SimpleMarker" enabled="1" pass="0" locked="0">
          <prop v="0" k="angle"/>
          <prop v="85,255,127,0" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="pentagon" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="255,127,0,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.7" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="4" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <effect enabled="1" type="effectStack">
            <effect type="dropShadow">
              <prop v="13" k="blend_mode"/>
              <prop v="0.5" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="2" k="draw_mode"/>
              <prop v="1" k="enabled"/>
              <prop v="135" k="offset_angle"/>
              <prop v="0.2" k="offset_distance"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="outerGlow">
              <prop v="0" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,255,255" k="color1"/>
              <prop v="0,255,0,255" k="color2"/>
              <prop v="0" k="color_type"/>
              <prop v="0" k="discrete"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="0.5" k="opacity"/>
              <prop v="gradient" k="rampType"/>
              <prop v="255,255,255,255" k="single_color"/>
              <prop v="2" k="spread"/>
              <prop v="MM" k="spread_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="spread_unit_scale"/>
            </effect>
            <effect type="drawSource">
              <prop v="0" k="blend_mode"/>
              <prop v="2" k="draw_mode"/>
              <prop v="1" k="enabled"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="innerShadow">
              <prop v="13" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="135" k="offset_angle"/>
              <prop v="2" k="offset_distance"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="innerGlow">
              <prop v="0" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,255,255" k="color1"/>
              <prop v="0,255,0,255" k="color2"/>
              <prop v="0" k="color_type"/>
              <prop v="0" k="discrete"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="0.5" k="opacity"/>
              <prop v="gradient" k="rampType"/>
              <prop v="255,255,255,255" k="single_color"/>
              <prop v="2" k="spread"/>
              <prop v="MM" k="spread_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="spread_unit_scale"/>
            </effect>
          </effect>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="3" force_rhr="0" type="marker" alpha="1" clip_to_extent="1">
        <layer class="SimpleMarker" enabled="1" pass="0" locked="0">
          <prop v="0" k="angle"/>
          <prop v="85,255,127,0" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="square" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="255,9,1,255" k="outline_color"/>
          <prop v="dot" k="outline_style"/>
          <prop v="0.25" k="outline_width"/>
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
    </symbols>
  </renderer-v2>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style textColor="0,0,0,255" fontWeight="50" blendMode="0" fontSize="8" fontStrikeout="0" fontCapitals="0" fontFamily="MS Gothic" multilineHeight="1" textOrientation="horizontal" fontUnderline="0" fieldName="'s:' || coalesce(manh_surface_level, 'NULL') || '\n' ||&#xd;&#xa;'d:' || coalesce(manh_drain_level, 'NULL') ||  '\n' || &#xd;&#xa;'b:' || coalesce(manh_bottom_level, 'NULL') " textOpacity="1" isExpression="1" useSubstitutions="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontSizeUnit="Point" namedStyle="Regular" fontItalic="0" previewBkgrdColor="255,255,255,255" fontWordSpacing="0" fontKerning="1" fontLetterSpacing="0">
        <text-buffer bufferSizeUnits="MM" bufferSize="0.7" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferOpacity="1" bufferBlendMode="0" bufferJoinStyle="128" bufferColor="255,255,255,255" bufferNoFill="1" bufferDraw="1"/>
        <background shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthUnit="MM" shapeRadiiY="0" shapeSizeType="0" shapeSizeX="0" shapeOpacity="1" shapeRotationType="0" shapeBorderColor="128,128,128,255" shapeRadiiUnit="MM" shapeBlendMode="0" shapeType="0" shapeOffsetX="0" shapeSizeY="0" shapeSizeUnit="MM" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetUnit="MM" shapeRadiiX="0" shapeBorderWidth="0" shapeOffsetY="0" shapeFillColor="255,255,255,255" shapeSVGFile="" shapeDraw="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRotation="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeJoinStyle="64">
          <symbol name="markerSymbol" force_rhr="0" type="marker" alpha="1" clip_to_extent="1">
            <layer class="SimpleMarker" enabled="1" pass="0" locked="0">
              <prop v="0" k="angle"/>
              <prop v="125,139,143,255" k="color"/>
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
        <shadow shadowDraw="0" shadowOffsetDist="1" shadowColor="0,0,0,255" shadowScale="100" shadowOffsetUnit="MM" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.7" shadowOffsetGlobal="1" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowBlendMode="6" shadowUnder="0" shadowOffsetAngle="135" shadowRadius="1.5" shadowRadiusAlphaOnly="0" shadowRadiusUnit="MM"/>
        <dd_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format multilineAlign="3" leftDirectionSymbol="&lt;" rightDirectionSymbol=">" wrapChar="" decimals="3" placeDirectionSymbol="0" autoWrapLength="0" addDirectionSymbol="0" reverseDirectionSymbol="0" useMaxLineLengthForAutoWrap="1" formatNumbers="0" plussign="0"/>
      <placement layerType="PointGeometry" placement="1" rotationAngle="0" xOffset="1" yOffset="-1" geometryGeneratorType="PointGeometry" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" distUnits="MM" overrunDistance="0" quadOffset="2" placementFlags="10" dist="0" offsetType="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" maxCurvedCharAngleIn="25" centroidInside="0" repeatDistance="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" fitInPolygonOnly="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGenerator="" maxCurvedCharAngleOut="-25" overrunDistanceUnit="MM" preserveRotation="1" centroidWhole="0" geometryGeneratorEnabled="0" distMapUnitScale="3x:0,0,0,0,0,0" offsetUnits="MM" priority="5" repeatDistanceUnits="MM"/>
      <rendering fontMinPixelSize="3" zIndex="0" displayAll="0" scaleMin="0" minFeatureSize="0" scaleMax="1000" mergeLines="0" scaleVisibility="1" obstacleType="0" limitNumLabels="0" drawLabels="1" obstacleFactor="1" maxNumLabels="2000" labelPerPart="0" fontMaxPixelSize="10000" upsidedownLabels="0" fontLimitPixelSize="0" obstacle="1"/>
      <dd_properties>
        <Option type="Map">
          <Option name="name" value="" type="QString"/>
          <Option name="properties"/>
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
          <Option name="lineSymbol" value="&lt;symbol name=&quot;symbol&quot; force_rhr=&quot;0&quot; type=&quot;line&quot; alpha=&quot;1&quot; clip_to_extent=&quot;1&quot;>&lt;layer class=&quot;SimpleLine&quot; enabled=&quot;1&quot; pass=&quot;0&quot; locked=&quot;0&quot;>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString"/>
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
    <property value="manh_display_name" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Pie" attributeLegend="1">
    <DiagramCategory scaleDependency="Area" minimumSize="0" backgroundColor="#ffffff" penWidth="0" opacity="1" enabled="0" backgroundAlpha="255" labelPlacementMethod="XHeight" diagramOrientation="Up" width="15" penColor="#000000" lineSizeType="MM" sizeType="MM" sizeScale="3x:0,0,0,0,0,0" minScaleDenominator="-4.65661e-10" rotationOffset="270" penAlpha="255" height="15" barWidth="5" maxScaleDenominator="1e+08" scaleBasedVisibility="0" lineSizeScale="3x:0,0,0,0,0,0">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute field="" color="#000000" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings linePlacementFlags="2" priority="0" zIndex="0" dist="0" placement="0" obstacle="0" showAll="1">
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
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_connection_node_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_shape">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="00: square" value="00" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="01: round" value="01" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="02: rectangle" value="02" type="QString"/>
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
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_length">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_manhole_indicator">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="0: inspection" value="0" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="1: outlet" value="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="2: pump" value="2" type="QString"/>
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
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="0: embedded" value="0" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="1: isolated" value="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="2: connected" value="2" type="QString"/>
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
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_surface_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_drain_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_sediment_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_zoom_category">
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
    <field name="node_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_storage_area">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_initial_waterlevel">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_the_geom_linestring">
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
    <alias name="" field="ROWID" index="0"/>
    <alias name="id" field="manh_id" index="1"/>
    <alias name="display_name" field="manh_display_name" index="2"/>
    <alias name="code" field="manh_code" index="3"/>
    <alias name="connection_node_id" field="manh_connection_node_id" index="4"/>
    <alias name="shape" field="manh_shape" index="5"/>
    <alias name="width" field="manh_width" index="6"/>
    <alias name="length" field="manh_length" index="7"/>
    <alias name="manhole_indicator" field="manh_manhole_indicator" index="8"/>
    <alias name="calculation_type" field="manh_calculation_type" index="9"/>
    <alias name="bottom_level" field="manh_bottom_level" index="10"/>
    <alias name="surface_level" field="manh_surface_level" index="11"/>
    <alias name="drain_level" field="manh_drain_level" index="12"/>
    <alias name="sediment_level" field="manh_sediment_level" index="13"/>
    <alias name="zoom_category" field="manh_zoom_category" index="14"/>
    <alias name="" field="node_id" index="15"/>
    <alias name="" field="node_storage_area" index="16"/>
    <alias name="" field="node_initial_waterlevel" index="17"/>
    <alias name="" field="node_code" index="18"/>
    <alias name="the_geom_linestring" field="node_the_geom_linestring" index="19"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="ROWID" expression=""/>
    <default applyOnUpdate="0" field="manh_id" expression="if(maximum(manh_id) is null,1, maximum(manh_id)+1)"/>
    <default applyOnUpdate="0" field="manh_display_name" expression="'new'"/>
    <default applyOnUpdate="0" field="manh_code" expression="'new'"/>
    <default applyOnUpdate="0" field="manh_connection_node_id" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,geometry(@parent))) is null,'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,geometry(@parent))))"/>
    <default applyOnUpdate="0" field="manh_shape" expression=""/>
    <default applyOnUpdate="0" field="manh_width" expression=""/>
    <default applyOnUpdate="0" field="manh_length" expression=""/>
    <default applyOnUpdate="0" field="manh_manhole_indicator" expression="'0'"/>
    <default applyOnUpdate="0" field="manh_calculation_type" expression=""/>
    <default applyOnUpdate="0" field="manh_bottom_level" expression="&quot;manh_bottom_level&quot;&lt;&quot;manh_surface_level&quot;"/>
    <default applyOnUpdate="0" field="manh_surface_level" expression=""/>
    <default applyOnUpdate="0" field="manh_drain_level" expression=""/>
    <default applyOnUpdate="0" field="manh_sediment_level" expression=""/>
    <default applyOnUpdate="0" field="manh_zoom_category" expression="1"/>
    <default applyOnUpdate="0" field="node_id" expression="'filled automatically'"/>
    <default applyOnUpdate="0" field="node_storage_area" expression=""/>
    <default applyOnUpdate="0" field="node_initial_waterlevel" expression=""/>
    <default applyOnUpdate="0" field="node_code" expression="'new'"/>
    <default applyOnUpdate="0" field="node_the_geom_linestring" expression=""/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" field="ROWID" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="manh_id" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="2" field="manh_display_name" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="manh_code" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="manh_connection_node_id" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="manh_shape" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="manh_width" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" field="manh_length" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="2" field="manh_manhole_indicator" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="manh_calculation_type" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="manh_bottom_level" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="manh_surface_level" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" field="manh_drain_level" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="manh_sediment_level" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="2" field="manh_zoom_category" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" field="node_id" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="node_storage_area" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="node_initial_waterlevel" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="2" field="node_code" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" field="node_the_geom_linestring" exp_strength="0" unique_strength="0" constraints="0"/>
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
  <attributetableconfig sortExpression="&quot;manh_manhole_indicator&quot;" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column name="ROWID" type="field" width="-1" hidden="0"/>
      <column name="manh_id" type="field" width="-1" hidden="0"/>
      <column name="manh_display_name" type="field" width="-1" hidden="0"/>
      <column name="manh_code" type="field" width="-1" hidden="0"/>
      <column name="manh_connection_node_id" type="field" width="-1" hidden="0"/>
      <column name="manh_shape" type="field" width="-1" hidden="0"/>
      <column name="manh_width" type="field" width="-1" hidden="0"/>
      <column name="manh_length" type="field" width="-1" hidden="0"/>
      <column name="manh_manhole_indicator" type="field" width="-1" hidden="0"/>
      <column name="manh_calculation_type" type="field" width="-1" hidden="0"/>
      <column name="manh_bottom_level" type="field" width="-1" hidden="0"/>
      <column name="manh_surface_level" type="field" width="-1" hidden="0"/>
      <column name="manh_drain_level" type="field" width="-1" hidden="0"/>
      <column name="manh_sediment_level" type="field" width="-1" hidden="0"/>
      <column name="manh_zoom_category" type="field" width="-1" hidden="0"/>
      <column name="node_id" type="field" width="-1" hidden="0"/>
      <column name="node_storage_area" type="field" width="-1" hidden="0"/>
      <column name="node_initial_waterlevel" type="field" width="-1" hidden="0"/>
      <column name="node_code" type="field" width="-1" hidden="0"/>
      <column name="node_the_geom_linestring" type="field" width="-1" hidden="0"/>
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
    <attributeEditorContainer columnCount="1" name="Manhole_view" visibilityExpressionEnabled="0" showLabel="1" visibilityExpression="" groupBox="0">
      <attributeEditorContainer columnCount="1" name="General" visibilityExpressionEnabled="0" showLabel="1" visibilityExpression="" groupBox="1">
        <attributeEditorField name="manh_id" showLabel="1" index="1"/>
        <attributeEditorField name="manh_display_name" showLabel="1" index="2"/>
        <attributeEditorField name="manh_code" showLabel="1" index="3"/>
        <attributeEditorField name="manh_calculation_type" showLabel="1" index="9"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" name="Characteristics" visibilityExpressionEnabled="0" showLabel="1" visibilityExpression="" groupBox="1">
        <attributeEditorField name="manh_shape" showLabel="1" index="5"/>
        <attributeEditorField name="manh_width" showLabel="1" index="6"/>
        <attributeEditorField name="manh_length" showLabel="1" index="7"/>
        <attributeEditorField name="manh_bottom_level" showLabel="1" index="10"/>
        <attributeEditorField name="manh_surface_level" showLabel="1" index="11"/>
        <attributeEditorField name="manh_drain_level" showLabel="1" index="12"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" name="Visualisation" visibilityExpressionEnabled="0" showLabel="1" visibilityExpression="" groupBox="1">
        <attributeEditorField name="manh_manhole_indicator" showLabel="1" index="8"/>
        <attributeEditorField name="manh_zoom_category" showLabel="1" index="14"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" name="Connection node" visibilityExpressionEnabled="0" showLabel="1" visibilityExpression="" groupBox="1">
        <attributeEditorField name="manh_connection_node_id" showLabel="1" index="4"/>
        <attributeEditorField name="node_code" showLabel="1" index="18"/>
        <attributeEditorField name="node_initial_waterlevel" showLabel="1" index="17"/>
        <attributeEditorField name="node_storage_area" showLabel="1" index="16"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="ROWID" editable="1"/>
    <field name="manh_bottom_level" editable="1"/>
    <field name="manh_calculation_type" editable="1"/>
    <field name="manh_code" editable="1"/>
    <field name="manh_connection_node_id" editable="0"/>
    <field name="manh_display_name" editable="1"/>
    <field name="manh_drain_level" editable="1"/>
    <field name="manh_id" editable="0"/>
    <field name="manh_length" editable="1"/>
    <field name="manh_manhole_indicator" editable="1"/>
    <field name="manh_sediment_level" editable="1"/>
    <field name="manh_shape" editable="1"/>
    <field name="manh_surface_level" editable="1"/>
    <field name="manh_width" editable="1"/>
    <field name="manh_zoom_category" editable="1"/>
    <field name="node_code" editable="1"/>
    <field name="node_id" editable="0"/>
    <field name="node_initial_waterlevel" editable="1"/>
    <field name="node_storage_area" editable="1"/>
    <field name="node_the_geom_linestring" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="ROWID" labelOnTop="0"/>
    <field name="manh_bottom_level" labelOnTop="0"/>
    <field name="manh_calculation_type" labelOnTop="0"/>
    <field name="manh_code" labelOnTop="0"/>
    <field name="manh_connection_node_id" labelOnTop="0"/>
    <field name="manh_display_name" labelOnTop="0"/>
    <field name="manh_drain_level" labelOnTop="0"/>
    <field name="manh_id" labelOnTop="0"/>
    <field name="manh_length" labelOnTop="0"/>
    <field name="manh_manhole_indicator" labelOnTop="0"/>
    <field name="manh_sediment_level" labelOnTop="0"/>
    <field name="manh_shape" labelOnTop="0"/>
    <field name="manh_surface_level" labelOnTop="0"/>
    <field name="manh_width" labelOnTop="0"/>
    <field name="manh_zoom_category" labelOnTop="0"/>
    <field name="node_code" labelOnTop="0"/>
    <field name="node_id" labelOnTop="0"/>
    <field name="node_initial_waterlevel" labelOnTop="0"/>
    <field name="node_storage_area" labelOnTop="0"/>
    <field name="node_the_geom_linestring" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>"manh_display_name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
