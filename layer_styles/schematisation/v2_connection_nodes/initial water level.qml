<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis minScale="1e+08" simplifyDrawingTol="1" maxScale="0" labelsEnabled="1" simplifyMaxScale="1" simplifyDrawingHints="0" readOnly="0" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" version="3.10.10-A Coruña" simplifyAlgorithm="0" simplifyLocal="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" type="RuleRenderer" symbollevels="0" forceraster="0">
    <rules key="{a1065705-9372-4a82-8b49-4a30152c1b2a}">
      <rule label="Initial water level" key="{fa832e1f-ba5c-47ef-b6e3-13f779a6ce11}" filter="initial_waterlevel IS NOT NULL" symbol="0"/>
      <rule label="No initial water level" key="{f1ef164a-7d60-4c16-91d6-96fd46517dad}" filter="initial_waterlevel IS NULL" symbol="1"/>
    </rules>
    <symbols>
      <symbol type="marker" name="0" force_rhr="0" alpha="1" clip_to_extent="1">
        <layer enabled="1" pass="0" locked="0" class="SimpleMarker">
          <prop k="angle" v="0"/>
          <prop k="color" v="0,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="marker" name="1" force_rhr="0" alpha="1" clip_to_extent="1">
        <layer enabled="1" pass="0" locked="0" class="SimpleMarker">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,255,255,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="1.2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontItalic="0" fontLetterSpacing="0" fontCapitals="0" textOrientation="horizontal" fontKerning="1" fontFamily="MS Gothic" textOpacity="1" fontSizeUnit="Point" fontWordSpacing="0" fontStrikeout="0" useSubstitutions="0" fontWeight="50" fieldName="format_number(initial_waterlevel, 2)" textColor="0,0,0,255" previewBkgrdColor="255,255,255,255" fontSize="8" blendMode="0" multilineHeight="1" isExpression="1" namedStyle="Regular" fontUnderline="0">
        <text-buffer bufferDraw="1" bufferSizeUnits="MM" bufferSize="0.7" bufferColor="255,255,255,255" bufferNoFill="1" bufferOpacity="1" bufferJoinStyle="128" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferBlendMode="0"/>
        <background shapeOpacity="1" shapeSizeUnit="MM" shapeJoinStyle="64" shapeDraw="0" shapeRotation="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetUnit="MM" shapeBorderWidth="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeSVGFile="" shapeRotationType="0" shapeSizeType="0" shapeRadiiY="0" shapeFillColor="255,255,255,255" shapeSizeX="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetY="0" shapeRadiiUnit="MM" shapeType="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeSizeY="0" shapeOffsetX="0" shapeBorderColor="128,128,128,255" shapeBorderWidthUnit="MM" shapeRadiiX="0" shapeBlendMode="0">
          <symbol type="marker" name="markerSymbol" force_rhr="0" alpha="1" clip_to_extent="1">
            <layer enabled="1" pass="0" locked="0" class="SimpleMarker">
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
                  <Option type="QString" name="name" value=""/>
                  <Option name="properties"/>
                  <Option type="QString" name="type" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </background>
        <shadow shadowUnder="0" shadowOffsetDist="1" shadowOffsetGlobal="1" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetAngle="135" shadowBlendMode="6" shadowDraw="0" shadowRadiusUnit="MM" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowScale="100" shadowOffsetUnit="MM" shadowRadius="1.5" shadowColor="0,0,0,255" shadowOpacity="0.7" shadowRadiusAlphaOnly="0"/>
        <dd_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format reverseDirectionSymbol="0" placeDirectionSymbol="0" decimals="3" plussign="0" multilineAlign="3" autoWrapLength="0" rightDirectionSymbol=">" useMaxLineLengthForAutoWrap="1" wrapChar="" formatNumbers="0" leftDirectionSymbol="&lt;" addDirectionSymbol="0"/>
      <placement overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" distMapUnitScale="3x:0,0,0,0,0,0" preserveRotation="1" overrunDistanceUnit="MM" geometryGeneratorEnabled="0" maxCurvedCharAngleOut="-25" dist="0" geometryGeneratorType="PointGeometry" centroidWhole="0" priority="5" xOffset="0" placement="0" quadOffset="4" layerType="PointGeometry" placementFlags="10" repeatDistance="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" yOffset="0" centroidInside="0" geometryGenerator="" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" maxCurvedCharAngleIn="25" overrunDistance="0" rotationAngle="0" repeatDistanceUnits="MM" offsetType="0" offsetUnits="MM" fitInPolygonOnly="0" distUnits="MM"/>
      <rendering zIndex="0" mergeLines="0" fontMinPixelSize="3" scaleMax="2500" limitNumLabels="0" labelPerPart="0" drawLabels="1" obstacleFactor="1" obstacleType="0" scaleVisibility="1" fontLimitPixelSize="0" displayAll="0" maxNumLabels="2000" scaleMin="0" minFeatureSize="0" upsidedownLabels="0" fontMaxPixelSize="10000" obstacle="1"/>
      <dd_properties>
        <Option type="Map">
          <Option type="QString" name="name" value=""/>
          <Option name="properties"/>
          <Option type="QString" name="type" value="collection"/>
        </Option>
      </dd_properties>
      <callout type="simple">
        <Option type="Map">
          <Option type="QString" name="anchorPoint" value="pole_of_inaccessibility"/>
          <Option type="Map" name="ddProperties">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
          <Option type="bool" name="drawToAllParts" value="false"/>
          <Option type="QString" name="enabled" value="0"/>
          <Option type="QString" name="lineSymbol" value="&lt;symbol type=&quot;line&quot; name=&quot;symbol&quot; force_rhr=&quot;0&quot; alpha=&quot;1&quot; clip_to_extent=&quot;1&quot;>&lt;layer enabled=&quot;1&quot; pass=&quot;0&quot; locked=&quot;0&quot; class=&quot;SimpleLine&quot;>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option type=&quot;QString&quot; name=&quot;name&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;type&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
          <Option type="double" name="minLength" value="0"/>
          <Option type="QString" name="minLengthMapUnitScale" value="3x:0,0,0,0,0,0"/>
          <Option type="QString" name="minLengthUnit" value="MM"/>
          <Option type="double" name="offsetFromAnchor" value="0"/>
          <Option type="QString" name="offsetFromAnchorMapUnitScale" value="3x:0,0,0,0,0,0"/>
          <Option type="QString" name="offsetFromAnchorUnit" value="MM"/>
          <Option type="double" name="offsetFromLabel" value="0"/>
          <Option type="QString" name="offsetFromLabelMapUnitScale" value="3x:0,0,0,0,0,0"/>
          <Option type="QString" name="offsetFromLabelUnit" value="MM"/>
        </Option>
      </callout>
    </settings>
  </labeling>
  <customproperties>
    <property key="dualview/previewExpressions" value="id"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Pie">
    <DiagramCategory diagramOrientation="Up" height="15" lineSizeScale="3x:0,0,0,0,0,0" barWidth="5" scaleBasedVisibility="0" minScaleDenominator="0" penWidth="0" penColor="#000000" sizeType="MM" labelPlacementMethod="XHeight" opacity="1" lineSizeType="MM" backgroundAlpha="255" sizeScale="3x:0,0,0,0,0,0" rotationOffset="270" penAlpha="255" width="15" enabled="0" maxScaleDenominator="1e+08" backgroundColor="#ffffff" minimumSize="0" scaleDependency="Area">
      <fontProperties description="MS Shell Dlg 2,7.5,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" field="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings linePlacementFlags="2" priority="0" zIndex="0" placement="0" dist="0" obstacle="0" showAll="1">
    <properties>
      <Option type="Map">
        <Option type="QString" name="name" value=""/>
        <Option type="Map" name="properties">
          <Option type="Map" name="show">
            <Option type="bool" name="active" value="true"/>
            <Option type="QString" name="field" value="the_geom_linestring"/>
            <Option type="int" name="type" value="2"/>
          </Option>
        </Option>
        <Option type="QString" name="type" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="the_geom_linestring">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="initial_waterlevel">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="storage_area">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="" field="the_geom_linestring"/>
    <alias index="1" name="" field="code"/>
    <alias index="2" name="" field="initial_waterlevel"/>
    <alias index="3" name="" field="storage_area"/>
    <alias index="4" name="" field="id"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="the_geom_linestring"/>
    <default expression="'new'" applyOnUpdate="0" field="code"/>
    <default expression="" applyOnUpdate="0" field="initial_waterlevel"/>
    <default expression="" applyOnUpdate="0" field="storage_area"/>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" notnull_strength="0" unique_strength="0" constraints="0" field="the_geom_linestring"/>
    <constraint exp_strength="0" notnull_strength="0" unique_strength="0" constraints="0" field="code"/>
    <constraint exp_strength="0" notnull_strength="0" unique_strength="0" constraints="0" field="initial_waterlevel"/>
    <constraint exp_strength="0" notnull_strength="0" unique_strength="0" constraints="0" field="storage_area"/>
    <constraint exp_strength="0" notnull_strength="1" unique_strength="1" constraints="3" field="id"/>
  </constraints>
  <constraintExpressions>
    <constraint field="the_geom_linestring" desc="" exp=""/>
    <constraint field="code" desc="" exp=""/>
    <constraint field="initial_waterlevel" desc="" exp=""/>
    <constraint field="storage_area" desc="" exp=""/>
    <constraint field="id" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortExpression="&quot;code&quot;" actionWidgetStyle="dropDown" sortOrder="1">
    <columns>
      <column type="field" name="the_geom_linestring" hidden="0" width="-1"/>
      <column type="field" name="code" hidden="0" width="-1"/>
      <column type="field" name="initial_waterlevel" hidden="0" width="-1"/>
      <column type="field" name="storage_area" hidden="0" width="-1"/>
      <column type="field" name="id" hidden="0" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1">../../../OSGEO4~1/bin</editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath>../../../OSGEO4~1/bin</editforminitfilepath>
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
    <attributeEditorContainer showLabel="1" visibilityExpressionEnabled="0" name="General" visibilityExpression="" columnCount="1" groupBox="0">
      <attributeEditorField showLabel="1" name="id" index="4"/>
      <attributeEditorField showLabel="1" name="code" index="1"/>
      <attributeEditorField showLabel="1" name="initial_waterlevel" index="2"/>
      <attributeEditorField showLabel="1" name="storage_area" index="3"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="code"/>
    <field editable="1" name="id"/>
    <field editable="1" name="initial_waterlevel"/>
    <field editable="1" name="storage_area"/>
    <field editable="1" name="the_geom_linestring"/>
  </editable>
  <labelOnTop>
    <field name="code" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="initial_waterlevel" labelOnTop="0"/>
    <field name="storage_area" labelOnTop="0"/>
    <field name="the_geom_linestring" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>"id"</previewExpression>
  <mapTip>Name</mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
