<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" simplifyLocal="1" labelsEnabled="1" simplifyDrawingTol="1" version="3.10.10-A Coruña" simplifyAlgorithm="0" minScale="1e+08" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" maxScale="0" simplifyDrawingHints="1" simplifyMaxScale="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" type="singleSymbol" symbollevels="0" enableorderby="0">
    <symbols>
      <symbol type="line" clip_to_extent="1" name="0" force_rhr="0" alpha="1">
        <layer class="SimpleLine" pass="0" enabled="1" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="5,77,209,255"/>
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
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="if(@map_scale&lt;10000, 0.66,0.3)"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
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
      <text-style textColor="0,0,0,255" fontFamily="MS Gothic" fontUnderline="0" isExpression="0" useSubstitutions="0" fontLetterSpacing="0" namedStyle="Regular" fontSizeMapUnitScale="3x:0,0,0,0,0,0" blendMode="0" multilineHeight="1" fontSizeUnit="Point" fontWordSpacing="0" fontSize="7" textOrientation="horizontal" previewBkgrdColor="255,255,255,255" fontStrikeout="0" textOpacity="1" fieldName="code" fontCapitals="0" fontItalic="0" fontKerning="1" fontWeight="50">
        <text-buffer bufferNoFill="0" bufferBlendMode="0" bufferSize="0.7" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferColor="255,255,255,255" bufferJoinStyle="128" bufferOpacity="1" bufferDraw="1" bufferSizeUnits="MM"/>
        <background shapeRadiiX="0" shapeOffsetUnit="MM" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiUnit="MM" shapeOpacity="1" shapeType="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeType="0" shapeSVGFile="" shapeJoinStyle="64" shapeRotationType="0" shapeSizeY="0" shapeSizeUnit="MM" shapeFillColor="255,255,255,255" shapeSizeX="0" shapeBorderWidth="0" shapeBlendMode="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeDraw="0" shapeRotation="0" shapeOffsetX="0" shapeRadiiY="0" shapeBorderWidthUnit="MM" shapeOffsetY="0" shapeBorderColor="128,128,128,255">
          <symbol type="marker" clip_to_extent="1" name="markerSymbol" force_rhr="0" alpha="1">
            <layer class="SimpleMarker" pass="0" enabled="1" locked="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="133,182,111,255"/>
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
        <shadow shadowBlendMode="6" shadowRadiusUnit="MM" shadowScale="100" shadowUnder="0" shadowOffsetUnit="MM" shadowDraw="0" shadowOffsetAngle="135" shadowOffsetDist="1" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.7" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadius="1.5" shadowColor="0,0,0,255" shadowOffsetGlobal="1" shadowRadiusAlphaOnly="0"/>
        <dd_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format autoWrapLength="0" multilineAlign="0" formatNumbers="0" leftDirectionSymbol="&lt;" rightDirectionSymbol=">" wrapChar="" placeDirectionSymbol="0" plussign="0" useMaxLineLengthForAutoWrap="1" addDirectionSymbol="0" reverseDirectionSymbol="0" decimals="3"/>
      <placement offsetUnits="MapUnit" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" distMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0" layerType="LineGeometry" centroidWhole="0" quadOffset="4" offsetType="0" dist="0" distUnits="MM" preserveRotation="1" geometryGeneratorType="PointGeometry" xOffset="0" overrunDistanceUnit="MM" geometryGenerator="" placementFlags="9" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" rotationAngle="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" centroidInside="0" placement="2" priority="5" repeatDistanceUnits="MM" overrunDistance="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" maxCurvedCharAngleOut="-25" repeatDistance="0" geometryGeneratorEnabled="0" yOffset="0" maxCurvedCharAngleIn="25"/>
      <rendering upsidedownLabels="0" limitNumLabels="0" obstacle="1" fontLimitPixelSize="0" scaleMax="10000000" maxNumLabels="2000" labelPerPart="0" obstacleFactor="1" drawLabels="1" mergeLines="0" fontMinPixelSize="3" minFeatureSize="0" fontMaxPixelSize="10000" displayAll="0" scaleMin="1" obstacleType="0" zIndex="0" scaleVisibility="0"/>
      <dd_properties>
        <Option type="Map">
          <Option type="QString" name="name" value=""/>
          <Option type="Map" name="properties">
            <Option type="Map" name="Color">
              <Option type="bool" name="active" value="false"/>
              <Option type="QString" name="expression" value="case &#xd;&#xa;when &quot;pipe_sewerage_type&quot; = 0 then '#ffaa00'&#xd;&#xa;when &quot;pipe_sewerage_type&quot; = 0 then '#55aaff'&#xd;&#xa;when &quot;pipe_sewerage_type&quot; = 0 then '#ff0000'&#xd;&#xa;when &quot;pipe_sewerage_type&quot; = 0 then '#999999'&#xd;&#xa;else '#000000'&#xd;&#xa;end"/>
              <Option type="int" name="type" value="3"/>
            </Option>
          </Option>
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
          <Option type="QString" name="lineSymbol" value="&lt;symbol type=&quot;line&quot; clip_to_extent=&quot;1&quot; name=&quot;symbol&quot; force_rhr=&quot;0&quot; alpha=&quot;1&quot;>&lt;layer class=&quot;SimpleLine&quot; pass=&quot;0&quot; enabled=&quot;1&quot; locked=&quot;0&quot;>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option type=&quot;QString&quot; name=&quot;name&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;type&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
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
    <property value="display_name" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Pie" attributeLegend="1">
    <DiagramCategory width="15" diagramOrientation="Up" rotationOffset="270" penAlpha="255" labelPlacementMethod="XHeight" minScaleDenominator="0" opacity="1" sizeScale="3x:0,0,0,0,0,0" penColor="#000000" lineSizeScale="3x:0,0,0,0,0,0" enabled="0" barWidth="5" penWidth="0" scaleBasedVisibility="0" backgroundColor="#ffffff" sizeType="MM" minimumSize="0" scaleDependency="Area" maxScaleDenominator="1e+08" lineSizeType="MM" height="15" backgroundAlpha="255">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute field="" label="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings obstacle="0" priority="0" showAll="1" placement="2" zIndex="0" linePlacementFlags="2" dist="0">
    <properties>
      <Option type="Map">
        <Option type="QString" name="name" value=""/>
        <Option type="Map" name="properties">
          <Option type="Map" name="show">
            <Option type="bool" name="active" value="true"/>
            <Option type="QString" name="field" value="id"/>
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
    <field name="display_name">
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
    <field name="calculation_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="100: embedded" value="100"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="101: isolated" value="101"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="102: connected" value="102"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="105: double connected" value="105"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dist_calc_points">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="zoom_category">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="-1" value="-1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="0" value="0"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="1" value="1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="2" value="2"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="3" value="3"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="4" value="4"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="5" value="5"/>
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
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_end_id">
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
    <alias name="" field="id" index="0"/>
    <alias name="" field="display_name" index="1"/>
    <alias name="" field="code" index="2"/>
    <alias name="" field="calculation_type" index="3"/>
    <alias name="" field="dist_calc_points" index="4"/>
    <alias name="" field="zoom_category" index="5"/>
    <alias name="" field="connection_node_start_id" index="6"/>
    <alias name="" field="connection_node_end_id" index="7"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression="if(maximum(id) is null,1, maximum(id)+1)"/>
    <default applyOnUpdate="0" field="display_name" expression="'new'"/>
    <default applyOnUpdate="0" field="code" expression="'new'"/>
    <default applyOnUpdate="0" field="calculation_type" expression=""/>
    <default applyOnUpdate="0" field="dist_calc_points" expression=""/>
    <default applyOnUpdate="0" field="zoom_category" expression="5"/>
    <default applyOnUpdate="0" field="connection_node_start_id" expression="aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent))))"/>
    <default applyOnUpdate="0" field="connection_node_end_id" expression="aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent))))"/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" constraints="3" field="id" notnull_strength="1" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" field="display_name" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" field="code" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" field="calculation_type" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" field="dist_calc_points" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="zoom_category" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" field="connection_node_start_id" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" field="connection_node_end_id" notnull_strength="2" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="id" exp=""/>
    <constraint desc="" field="display_name" exp=""/>
    <constraint desc="" field="code" exp=""/>
    <constraint desc="" field="calculation_type" exp=""/>
    <constraint desc="" field="dist_calc_points" exp=""/>
    <constraint desc="" field="zoom_category" exp=""/>
    <constraint desc="" field="connection_node_start_id" exp=""/>
    <constraint desc="" field="connection_node_end_id" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column type="field" name="id" hidden="0" width="-1"/>
      <column type="field" name="display_name" hidden="0" width="-1"/>
      <column type="field" name="code" hidden="0" width="-1"/>
      <column type="field" name="calculation_type" hidden="0" width="-1"/>
      <column type="field" name="dist_calc_points" hidden="0" width="-1"/>
      <column type="field" name="zoom_category" hidden="0" width="-1"/>
      <column type="field" name="connection_node_start_id" hidden="0" width="-1"/>
      <column type="field" name="connection_node_end_id" hidden="0" width="-1"/>
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
    <attributeEditorContainer groupBox="0" visibilityExpressionEnabled="0" showLabel="1" name="Channel" visibilityExpression="" columnCount="1">
      <attributeEditorContainer groupBox="1" visibilityExpressionEnabled="0" showLabel="1" name="General" visibilityExpression="" columnCount="1">
        <attributeEditorField showLabel="1" name="id" index="0"/>
        <attributeEditorField showLabel="1" name="display_name" index="1"/>
        <attributeEditorField showLabel="1" name="code" index="2"/>
        <attributeEditorField showLabel="1" name="calculation_type" index="3"/>
        <attributeEditorField showLabel="1" name="dist_calc_points" index="4"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpressionEnabled="0" showLabel="1" name="Visualization" visibilityExpression="" columnCount="1">
        <attributeEditorField showLabel="1" name="zoom_category" index="5"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpressionEnabled="0" showLabel="1" name="Connection nodes" visibilityExpression="" columnCount="1">
        <attributeEditorField showLabel="1" name="connection_node_start_id" index="6"/>
        <attributeEditorField showLabel="1" name="connection_node_end_id" index="7"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="calculation_type"/>
    <field editable="1" name="code"/>
    <field editable="1" name="connection_node_end_id"/>
    <field editable="1" name="connection_node_start_id"/>
    <field editable="1" name="display_name"/>
    <field editable="1" name="dist_calc_points"/>
    <field editable="1" name="id"/>
    <field editable="1" name="zoom_category"/>
  </editable>
  <labelOnTop>
    <field name="calculation_type" labelOnTop="0"/>
    <field name="code" labelOnTop="0"/>
    <field name="connection_node_end_id" labelOnTop="0"/>
    <field name="connection_node_start_id" labelOnTop="0"/>
    <field name="display_name" labelOnTop="0"/>
    <field name="dist_calc_points" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="zoom_category" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>"display_name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
