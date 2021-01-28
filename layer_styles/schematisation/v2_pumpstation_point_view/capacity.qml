<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" simplifyDrawingTol="1" maxScale="-4.65661e-10" labelsEnabled="1" simplifyDrawingHints="0" readOnly="0" hasScaleBasedVisibilityFlag="0" version="3.10.10-A Coruña" simplifyMaxScale="1" minScale="1e+08" simplifyLocal="1" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" enableorderby="0" forceraster="0" type="RuleRenderer">
    <rules key="{a754b3b6-32f1-4905-987a-48076fc6f5b1}">
      <rule symbol="0" filter="&quot;capacity&quot; >= 0.000000 AND &quot;capacity&quot; &lt;= 1.000000" label="&lt; 1 L/s" key="{7d756727-4730-4b29-9193-399a6997bb08}"/>
      <rule symbol="1" filter="&quot;capacity&quot; > 1.000000 AND &quot;capacity&quot; &lt;= 10.000000" label="1 - 10 L/s" key="{4d53a218-ca07-42b3-b0af-98a3d3cdb434}"/>
      <rule symbol="2" filter="&quot;capacity&quot; > 10.000000 AND &quot;capacity&quot; &lt;= 20.000000" label="10 - 20 L/s" key="{73e00a94-1474-48a3-8466-26093d4ed33b}"/>
      <rule symbol="3" filter="&quot;capacity&quot; > 20.000000 AND &quot;capacity&quot; &lt;= 50.000000" label="20 - 50 L/s" key="{38274205-b52d-447c-ac86-9efbfb040ef4}"/>
      <rule symbol="4" filter="&quot;capacity&quot; > 50.000000 AND &quot;capacity&quot; &lt;= 100.000000" label="50 - 100 L/s" key="{be3eb17b-1327-4f75-be00-88b16cd5fbd2}"/>
      <rule symbol="5" filter="ELSE" label="NULL (invalid)" key="{e6eb5901-afe5-4042-9e53-093d97927320}"/>
      <rule symbol="6" filter="&quot;capacity&quot; > 100.000000 AND &quot;capacity&quot; &lt;= 200.000000" label="100 - 200 L/s" key="{c6526e69-9119-4950-b12c-9c197622c8d2}"/>
      <rule symbol="7" filter="&quot;capacity&quot; > 200.000000 AND &quot;capacity&quot; &lt;= 500.000000" label="200 - 500 L/s" key="{e587f070-4734-4646-ac47-e68febed9ffe}"/>
      <rule symbol="8" filter="&quot;capacity&quot; > 500.000000 AND &quot;capacity&quot; &lt;= 1000.000000" label="500 - 1000 L/s" key="{708fb390-7ac9-4c58-b4d0-030a1e648e55}"/>
      <rule symbol="9" filter="&quot;capacity&quot; > 1000.000000 AND &quot;capacity&quot; &lt;= 2000.000000" label="1000 - 2000 L/s" key="{db34dafa-0b03-4720-aa14-166bcae04b70}"/>
      <rule symbol="10" filter="&quot;capacity&quot; > 2000.000000 AND &quot;capacity&quot; &lt;= 999999999.000000" label="> 2000 L/s" key="{7c5ff552-6335-461a-8ad1-7167095c55f5}"/>
      <rule symbol="11" filter="ELSE" label="NULL (invalid)" key="{9220bb11-fdf2-451b-aed8-c6b86f2437e7}"/>
    </rules>
    <symbols>
      <symbol name="0" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
          <prop v="0" k="angle"/>
          <prop v="185,185,185,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="pentagon" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="77,77,77,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.6" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="0.5" k="size"/>
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
      <symbol name="1" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
          <prop v="0" k="angle"/>
          <prop v="185,185,185,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="pentagon" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="77,77,77,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.6" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="1.2" k="size"/>
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
      <symbol name="10" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
          <prop v="0" k="angle"/>
          <prop v="185,185,185,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="pentagon" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="77,77,77,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.6" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="6.8" k="size"/>
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
      <symbol name="11" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
          <prop v="0" k="angle"/>
          <prop v="255,213,181,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="pentagon" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="255,35,35,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.6" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="3.3" k="size"/>
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
      <symbol name="2" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
          <prop v="0" k="angle"/>
          <prop v="185,185,185,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="pentagon" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="77,77,77,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.6" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="1.9" k="size"/>
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
      <symbol name="3" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
          <prop v="0" k="angle"/>
          <prop v="185,185,185,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="pentagon" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="77,77,77,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.6" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="2.6" k="size"/>
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
      <symbol name="4" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
          <prop v="0" k="angle"/>
          <prop v="185,185,185,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="pentagon" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="77,77,77,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.6" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="3.3" k="size"/>
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
      <symbol name="5" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="6" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
          <prop v="0" k="angle"/>
          <prop v="185,185,185,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="pentagon" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="77,77,77,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.6" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="4" k="size"/>
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
      <symbol name="7" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
          <prop v="0" k="angle"/>
          <prop v="185,185,185,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="pentagon" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="77,77,77,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.6" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="4.7" k="size"/>
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
      <symbol name="8" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
          <prop v="0" k="angle"/>
          <prop v="185,185,185,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="pentagon" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="77,77,77,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.6" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="5.4" k="size"/>
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
      <symbol name="9" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
          <prop v="0" k="angle"/>
          <prop v="185,185,185,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="pentagon" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="77,77,77,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.6" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="6.1" k="size"/>
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
    </symbols>
  </renderer-v2>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style blendMode="0" fontSizeUnit="Point" textOrientation="horizontal" isExpression="1" fontUnderline="0" fontWeight="50" namedStyle="Regular" fontCapitals="0" textColor="0,0,0,255" fontFamily="MS Gothic" useSubstitutions="0" fontStrikeout="0" fontWordSpacing="0" fontKerning="1" multilineHeight="1" fontSize="8" previewBkgrdColor="255,255,255,255" fontSizeMapUnitScale="3x:0,0,0,0,0,0" textOpacity="1" fontLetterSpacing="0" fieldName="coalesce(round( &quot;capacity&quot; , 2), 'NULL')|| ' L/s'" fontItalic="0">
        <text-buffer bufferSizeUnits="MM" bufferNoFill="1" bufferSize="0.7" bufferColor="255,255,255,255" bufferOpacity="1" bufferJoinStyle="128" bufferDraw="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferBlendMode="0"/>
        <background shapeSVGFile="" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderColor="128,128,128,255" shapeBorderWidthUnit="MM" shapeOpacity="1" shapeRadiiY="0" shapeRotation="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetUnit="MM" shapeOffsetY="0" shapeSizeX="0" shapeFillColor="255,255,255,255" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidth="0" shapeSizeUnit="MM" shapeSizeY="0" shapeRadiiX="0" shapeDraw="0" shapeRadiiUnit="MM" shapeType="0" shapeRotationType="0" shapeOffsetX="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeJoinStyle="64" shapeBlendMode="0" shapeSizeType="0">
          <symbol name="markerSymbol" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
            <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
              <prop v="0" k="angle"/>
              <prop v="243,166,178,255" k="color"/>
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
        <shadow shadowDraw="0" shadowColor="0,0,0,255" shadowOffsetUnit="MM" shadowRadius="1.5" shadowBlendMode="6" shadowOffsetDist="1" shadowScale="100" shadowOffsetAngle="135" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.7" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetGlobal="1" shadowUnder="0" shadowRadiusUnit="MM" shadowRadiusAlphaOnly="0"/>
        <dd_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format decimals="3" leftDirectionSymbol="&lt;" placeDirectionSymbol="0" formatNumbers="0" autoWrapLength="0" wrapChar="" useMaxLineLengthForAutoWrap="1" reverseDirectionSymbol="0" addDirectionSymbol="0" rightDirectionSymbol=">" plussign="0" multilineAlign="0"/>
      <placement offsetType="0" maxCurvedCharAngleIn="25" rotationAngle="0" geometryGenerator="" geometryGeneratorEnabled="0" distUnits="MM" quadOffset="4" offsetUnits="MM" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" maxCurvedCharAngleOut="-25" overrunDistance="0" geometryGeneratorType="PointGeometry" dist="0" repeatDistance="0" priority="5" placementFlags="10" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" repeatDistanceUnits="MM" centroidWhole="0" centroidInside="0" layerType="PointGeometry" xOffset="0" preserveRotation="1" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" distMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0" placement="0" yOffset="0" overrunDistanceUnit="MM"/>
      <rendering scaleVisibility="1" obstacleType="0" limitNumLabels="0" drawLabels="1" upsidedownLabels="0" scaleMin="0" minFeatureSize="0" fontMaxPixelSize="10000" displayAll="0" obstacle="1" fontMinPixelSize="3" labelPerPart="0" fontLimitPixelSize="0" zIndex="0" obstacleFactor="1" scaleMax="20000" maxNumLabels="2000" mergeLines="0"/>
      <dd_properties>
        <Option type="Map">
          <Option name="name" type="QString" value=""/>
          <Option name="properties"/>
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
          <Option name="lineSymbol" type="QString" value="&lt;symbol name=&quot;symbol&quot; type=&quot;line&quot; clip_to_extent=&quot;1&quot; alpha=&quot;1&quot; force_rhr=&quot;0&quot;>&lt;layer locked=&quot;0&quot; enabled=&quot;1&quot; class=&quot;SimpleLine&quot; pass=&quot;0&quot;>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; type=&quot;QString&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; type=&quot;QString&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
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
    <property value="display_name" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Pie">
    <DiagramCategory maxScaleDenominator="1e+08" width="15" opacity="1" barWidth="5" minimumSize="0" rotationOffset="270" scaleBasedVisibility="0" height="15" lineSizeScale="3x:0,0,0,0,0,0" scaleDependency="Area" enabled="0" labelPlacementMethod="XHeight" penColor="#000000" diagramOrientation="Up" penWidth="0" sizeType="MM" minScaleDenominator="-4.65661e-10" sizeScale="3x:0,0,0,0,0,0" backgroundAlpha="255" lineSizeType="MM" penAlpha="255" backgroundColor="#ffffff">
      <fontProperties style="" description="MS Shell Dlg 2,7.5,-1,5,50,0,0,0,0,0"/>
      <attribute color="#000000" field="" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings dist="0" priority="0" zIndex="0" showAll="1" obstacle="0" placement="0" linePlacementFlags="2">
    <properties>
      <Option type="Map">
        <Option name="name" type="QString" value=""/>
        <Option name="properties"/>
        <Option name="type" type="QString" value="collection"/>
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
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pump_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="classification">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="sewerage">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option name="CheckedState" type="QString" value="1"/>
            <Option name="UncheckedState" type="QString" value="0"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="lower_stop_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="upper_stop_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="capacity">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="zoom_category">
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
    <field name="connection_node_start_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_end_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="1: pump reacts only on suction side" type="QString" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="2: pump reacts only on delivery side" type="QString" value="2"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="storage_area">
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
    <alias name="id" index="1" field="pump_id"/>
    <alias name="" index="2" field="display_name"/>
    <alias name="" index="3" field="code"/>
    <alias name="" index="4" field="classification"/>
    <alias name="" index="5" field="sewerage"/>
    <alias name="" index="6" field="start_level"/>
    <alias name="" index="7" field="lower_stop_level"/>
    <alias name="" index="8" field="upper_stop_level"/>
    <alias name="" index="9" field="capacity"/>
    <alias name="" index="10" field="zoom_category"/>
    <alias name="" index="11" field="connection_node_start_id"/>
    <alias name="" index="12" field="connection_node_end_id"/>
    <alias name="" index="13" field="type"/>
    <alias name="id" index="14" field="connection_node_id"/>
    <alias name="" index="15" field="storage_area"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="ROWID" applyOnUpdate="0" expression=""/>
    <default field="pump_id" applyOnUpdate="0" expression="if(maximum(pump_id) is null,1, maximum(pump_id)+1)"/>
    <default field="display_name" applyOnUpdate="0" expression="'new'"/>
    <default field="code" applyOnUpdate="0" expression="'new'"/>
    <default field="classification" applyOnUpdate="0" expression=""/>
    <default field="sewerage" applyOnUpdate="0" expression=""/>
    <default field="start_level" applyOnUpdate="0" expression=""/>
    <default field="lower_stop_level" applyOnUpdate="0" expression=""/>
    <default field="upper_stop_level" applyOnUpdate="0" expression=""/>
    <default field="capacity" applyOnUpdate="0" expression=""/>
    <default field="zoom_category" applyOnUpdate="0" expression="2"/>
    <default field="connection_node_start_id" applyOnUpdate="0" expression="'filled automatically'"/>
    <default field="connection_node_end_id" applyOnUpdate="0" expression="'if you want to use an endpoint use v2_pumpstation_view'"/>
    <default field="type" applyOnUpdate="0" expression="1"/>
    <default field="connection_node_id" applyOnUpdate="0" expression="'filled automatically'"/>
    <default field="storage_area" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint field="ROWID" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="pump_id" constraints="1" unique_strength="0" notnull_strength="2" exp_strength="0"/>
    <constraint field="display_name" constraints="1" unique_strength="0" notnull_strength="2" exp_strength="0"/>
    <constraint field="code" constraints="1" unique_strength="0" notnull_strength="2" exp_strength="0"/>
    <constraint field="classification" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="sewerage" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="start_level" constraints="1" unique_strength="0" notnull_strength="2" exp_strength="0"/>
    <constraint field="lower_stop_level" constraints="5" unique_strength="0" notnull_strength="2" exp_strength="2"/>
    <constraint field="upper_stop_level" constraints="4" unique_strength="0" notnull_strength="0" exp_strength="2"/>
    <constraint field="capacity" constraints="5" unique_strength="0" notnull_strength="2" exp_strength="2"/>
    <constraint field="zoom_category" constraints="1" unique_strength="0" notnull_strength="2" exp_strength="0"/>
    <constraint field="connection_node_start_id" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="connection_node_end_id" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="type" constraints="1" unique_strength="0" notnull_strength="2" exp_strength="0"/>
    <constraint field="connection_node_id" constraints="1" unique_strength="0" notnull_strength="2" exp_strength="0"/>
    <constraint field="storage_area" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="ROWID"/>
    <constraint desc="" exp="" field="pump_id"/>
    <constraint desc="" exp="" field="display_name"/>
    <constraint desc="" exp="" field="code"/>
    <constraint desc="" exp="" field="classification"/>
    <constraint desc="" exp="" field="sewerage"/>
    <constraint desc="" exp="" field="start_level"/>
    <constraint desc="" exp="&quot;lower_stop_level&quot;&lt;&quot;start_level&quot;" field="lower_stop_level"/>
    <constraint desc="" exp="&quot;upper_stop_level&quot;>&quot;start_level&quot; or &quot;upper_stop_level&quot; is null&#xd;&#xa;" field="upper_stop_level"/>
    <constraint desc="" exp="&quot;capacity&quot;>=0" field="capacity"/>
    <constraint desc="" exp="" field="zoom_category"/>
    <constraint desc="" exp="" field="connection_node_start_id"/>
    <constraint desc="" exp="" field="connection_node_end_id"/>
    <constraint desc="" exp="" field="type"/>
    <constraint desc="" exp="" field="connection_node_id"/>
    <constraint desc="" exp="" field="storage_area"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortExpression="" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column hidden="0" name="ROWID" type="field" width="-1"/>
      <column hidden="0" name="pump_id" type="field" width="-1"/>
      <column hidden="0" name="display_name" type="field" width="-1"/>
      <column hidden="0" name="code" type="field" width="-1"/>
      <column hidden="0" name="classification" type="field" width="-1"/>
      <column hidden="0" name="sewerage" type="field" width="-1"/>
      <column hidden="0" name="start_level" type="field" width="-1"/>
      <column hidden="0" name="lower_stop_level" type="field" width="-1"/>
      <column hidden="0" name="upper_stop_level" type="field" width="-1"/>
      <column hidden="0" name="capacity" type="field" width="-1"/>
      <column hidden="0" name="zoom_category" type="field" width="-1"/>
      <column hidden="0" name="connection_node_start_id" type="field" width="-1"/>
      <column hidden="0" name="connection_node_end_id" type="field" width="-1"/>
      <column hidden="0" name="type" type="field" width="-1"/>
      <column hidden="0" name="connection_node_id" type="field" width="-1"/>
      <column hidden="0" name="storage_area" type="field" width="-1"/>
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
    <attributeEditorContainer columnCount="1" name="Pumpstation point view" visibilityExpression="" groupBox="0" visibilityExpressionEnabled="0" showLabel="1">
      <attributeEditorContainer columnCount="1" name="General" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="pump_id" index="1" showLabel="1"/>
        <attributeEditorField name="display_name" index="2" showLabel="1"/>
        <attributeEditorField name="code" index="3" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" name="Characteristics" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="start_level" index="6" showLabel="1"/>
        <attributeEditorField name="lower_stop_level" index="7" showLabel="1"/>
        <attributeEditorField name="upper_stop_level" index="8" showLabel="1"/>
        <attributeEditorField name="capacity" index="9" showLabel="1"/>
        <attributeEditorField name="type" index="13" showLabel="1"/>
        <attributeEditorField name="storage_area" index="15" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" name="Visualization" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="sewerage" index="5" showLabel="1"/>
        <attributeEditorField name="zoom_category" index="10" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" name="Connection nodes" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="connection_node_id" index="14" showLabel="1"/>
        <attributeEditorField name="connection_node_start_id" index="11" showLabel="1"/>
        <attributeEditorField name="connection_node_end_id" index="12" showLabel="1"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="ROWID" editable="1"/>
    <field name="capacity" editable="1"/>
    <field name="classification" editable="1"/>
    <field name="code" editable="1"/>
    <field name="connection_node_end_id" editable="0"/>
    <field name="connection_node_id" editable="0"/>
    <field name="connection_node_start_id" editable="0"/>
    <field name="display_name" editable="1"/>
    <field name="lower_stop_level" editable="1"/>
    <field name="pump_id" editable="1"/>
    <field name="sewerage" editable="1"/>
    <field name="start_level" editable="1"/>
    <field name="storage_area" editable="1"/>
    <field name="type" editable="1"/>
    <field name="upper_stop_level" editable="1"/>
    <field name="zoom_category" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="ROWID" labelOnTop="0"/>
    <field name="capacity" labelOnTop="0"/>
    <field name="classification" labelOnTop="0"/>
    <field name="code" labelOnTop="0"/>
    <field name="connection_node_end_id" labelOnTop="0"/>
    <field name="connection_node_id" labelOnTop="0"/>
    <field name="connection_node_start_id" labelOnTop="0"/>
    <field name="display_name" labelOnTop="0"/>
    <field name="lower_stop_level" labelOnTop="0"/>
    <field name="pump_id" labelOnTop="0"/>
    <field name="sewerage" labelOnTop="0"/>
    <field name="start_level" labelOnTop="0"/>
    <field name="storage_area" labelOnTop="0"/>
    <field name="type" labelOnTop="0"/>
    <field name="upper_stop_level" labelOnTop="0"/>
    <field name="zoom_category" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>"display_name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
