<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyDrawingHints="0" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" minScale="1e+08" simplifyAlgorithm="0" maxScale="-4.65661e-10" version="3.10.10-A Coruña" labelsEnabled="1" simplifyMaxScale="1" simplifyDrawingTol="1" readOnly="0" simplifyLocal="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" forceraster="0" symbollevels="0" type="singleSymbol">
    <symbols>
      <symbol alpha="1" name="0" type="marker" clip_to_extent="1" force_rhr="0">
        <layer pass="0" locked="0" class="SimpleMarker" enabled="1">
          <prop v="0" k="angle"/>
          <prop v="170,0,255,255" k="color"/>
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
          <prop v="area" k="scale_method"/>
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
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style fontKerning="1" isExpression="1" fontLetterSpacing="0" namedStyle="Regular" blendMode="0" fontUnderline="0" fontCapitals="0" fieldName=" represent_value(&quot;boundary_type&quot;) || '\n' ||&#xd;&#xa;'min: '||&#xd;&#xa;format_number(&#xd;&#xa;&#x9;array_first(&#xd;&#xa;&#x9;&#x9;array_sort(&#xd;&#xa;&#x9;&#x9;&#x9;array_foreach(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;string_to_array(timeseries,  '\n' ),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;to_real(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;array_last(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;string_to_array(@element, ',')&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;)&#xd;&#xa;&#x9;),&#xd;&#xa;&#x9;2&#xd;&#xa;)&#xd;&#xa;|| '\nmax: ' ||&#xd;&#xa;format_number(&#xd;&#xa;&#x9;array_last(&#xd;&#xa;&#x9;&#x9;array_sort(&#xd;&#xa;&#x9;&#x9;&#x9;array_foreach(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;string_to_array(timeseries,  '\n' ),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;to_real(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;array_last(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;string_to_array(@element, ',')&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;)&#xd;&#xa;&#x9;),&#xd;&#xa;&#x9;2&#xd;&#xa;)&#xd;&#xa;" useSubstitutions="0" textColor="0,0,0,255" fontSizeUnit="Point" textOrientation="horizontal" fontItalic="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontWordSpacing="0" previewBkgrdColor="255,255,255,255" multilineHeight="1" fontWeight="50" fontSize="8" fontFamily="MS Gothic" fontStrikeout="0" textOpacity="1">
        <text-buffer bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferJoinStyle="128" bufferDraw="1" bufferSize="0.7" bufferSizeUnits="MM" bufferNoFill="1" bufferOpacity="1" bufferColor="255,255,255,255" bufferBlendMode="0"/>
        <background shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeSizeUnit="MM" shapeOffsetY="0" shapeRotationType="0" shapeSizeY="0" shapeRadiiY="0" shapeSizeX="0" shapeOffsetX="0" shapeOpacity="1" shapeRotation="0" shapeType="0" shapeSVGFile="" shapeOffsetUnit="MM" shapeBorderColor="128,128,128,255" shapeDraw="0" shapeFillColor="255,255,255,255" shapeRadiiX="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeBlendMode="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidth="0" shapeBorderWidthUnit="MM" shapeJoinStyle="64" shapeSizeType="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiUnit="MM">
          <symbol alpha="1" name="markerSymbol" type="marker" clip_to_extent="1" force_rhr="0">
            <layer pass="0" locked="0" class="SimpleMarker" enabled="1">
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
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties"/>
                  <Option value="collection" name="type" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </background>
        <shadow shadowOffsetDist="1" shadowOffsetGlobal="1" shadowRadiusAlphaOnly="0" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowScale="100" shadowColor="0,0,0,255" shadowDraw="0" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowBlendMode="6" shadowRadiusUnit="MM" shadowRadius="1.5" shadowOffsetAngle="135" shadowOffsetUnit="MM" shadowUnder="0" shadowOpacity="0.7"/>
        <dd_properties>
          <Option type="Map">
            <Option value="" name="name" type="QString"/>
            <Option name="properties"/>
            <Option value="collection" name="type" type="QString"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format multilineAlign="3" reverseDirectionSymbol="0" decimals="3" placeDirectionSymbol="0" plussign="0" useMaxLineLengthForAutoWrap="1" leftDirectionSymbol="&lt;" wrapChar="" autoWrapLength="0" rightDirectionSymbol=">" formatNumbers="0" addDirectionSymbol="0"/>
      <placement yOffset="0" geometryGeneratorEnabled="0" rotationAngle="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" placementFlags="10" overrunDistanceUnit="MM" quadOffset="4" offsetUnits="MM" maxCurvedCharAngleIn="25" placement="0" repeatDistanceUnits="MM" maxCurvedCharAngleOut="-25" offsetType="0" distUnits="MM" geometryGenerator="" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" geometryGeneratorType="PointGeometry" centroidWhole="0" centroidInside="0" priority="5" overrunDistance="0" xOffset="0" distMapUnitScale="3x:0,0,0,0,0,0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" repeatDistance="0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0" dist="0" layerType="PointGeometry" preserveRotation="1"/>
      <rendering scaleMax="2500" obstacle="1" upsidedownLabels="0" displayAll="0" minFeatureSize="0" obstacleType="0" limitNumLabels="0" maxNumLabels="2000" fontMaxPixelSize="10000" scaleVisibility="1" fontLimitPixelSize="0" zIndex="0" scaleMin="0" labelPerPart="0" mergeLines="0" obstacleFactor="1" drawLabels="1" fontMinPixelSize="3"/>
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
          <Option value="&lt;symbol alpha=&quot;1&quot; name=&quot;symbol&quot; type=&quot;line&quot; clip_to_extent=&quot;1&quot; force_rhr=&quot;0&quot;>&lt;layer pass=&quot;0&quot; locked=&quot;0&quot; class=&quot;SimpleLine&quot; enabled=&quot;1&quot;>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; name=&quot;name&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; name=&quot;type&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" name="lineSymbol" type="QString"/>
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
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Pie" attributeLegend="1">
    <DiagramCategory opacity="1" backgroundAlpha="255" diagramOrientation="Up" width="15" maxScaleDenominator="1e+08" penColor="#000000" height="15" scaleDependency="Area" scaleBasedVisibility="0" penWidth="0" lineSizeType="MM" backgroundColor="#ffffff" barWidth="5" penAlpha="255" minScaleDenominator="-4.65661e-10" labelPlacementMethod="XHeight" sizeType="MM" minimumSize="0" rotationOffset="270" sizeScale="3x:0,0,0,0,0,0" enabled="0" lineSizeScale="3x:0,0,0,0,0,0">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute field="" color="#000000" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings placement="0" priority="0" linePlacementFlags="2" dist="0" showAll="1" obstacle="0" zIndex="0">
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
  <fieldConfiguration>
    <field name="ROWID">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="boundary_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="1" name="1: waterlevel" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2: velocity" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="3" name="3: discharge" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="5" name="5: sommerfeld" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="timeseries">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="true" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="ROWID" name="" index="0"/>
    <alias field="id" name="" index="1"/>
    <alias field="connection_node_id" name="" index="2"/>
    <alias field="boundary_type" name="" index="3"/>
    <alias field="timeseries" name="" index="4"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="ROWID" expression="" applyOnUpdate="0"/>
    <default field="id" expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0"/>
    <default field="connection_node_id" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,geometry(@parent))) is null,'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,geometry(@parent))))" applyOnUpdate="0"/>
    <default field="boundary_type" expression="" applyOnUpdate="0"/>
    <default field="timeseries" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="ROWID" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="id" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="2"/>
    <constraint field="connection_node_id" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="boundary_type" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="2"/>
    <constraint field="timeseries" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="2"/>
  </constraints>
  <constraintExpressions>
    <constraint field="ROWID" exp="" desc=""/>
    <constraint field="id" exp="" desc=""/>
    <constraint field="connection_node_id" exp="" desc=""/>
    <constraint field="boundary_type" exp="" desc=""/>
    <constraint field="timeseries" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="" sortOrder="0">
    <columns>
      <column hidden="0" width="-1" name="ROWID" type="field"/>
      <column hidden="0" width="-1" name="id" type="field"/>
      <column hidden="0" width="-1" name="connection_node_id" type="field"/>
      <column hidden="0" width="-1" name="boundary_type" type="field"/>
      <column hidden="0" width="-1" name="timeseries" type="field"/>
      <column hidden="1" width="-1" type="actions"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
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
    <attributeEditorContainer showLabel="1" groupBox="0" visibilityExpressionEnabled="0" visibilityExpression="" name="General" columnCount="1">
      <attributeEditorField showLabel="1" name="id" index="1"/>
      <attributeEditorField showLabel="1" name="connection_node_id" index="2"/>
      <attributeEditorField showLabel="1" name="boundary_type" index="3"/>
      <attributeEditorField showLabel="1" name="timeseries" index="4"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="ROWID"/>
    <field editable="1" name="boundary_type"/>
    <field editable="0" name="connection_node_id"/>
    <field editable="1" name="id"/>
    <field editable="1" name="timeseries"/>
  </editable>
  <labelOnTop>
    <field name="ROWID" labelOnTop="0"/>
    <field name="boundary_type" labelOnTop="0"/>
    <field name="connection_node_id" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="timeseries" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>"ROWID"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
