<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.4.5-Madeira" styleCategories="AllStyleCategories" simplifyDrawingTol="1" minScale="1e+08" labelsEnabled="0" simplifyLocal="1" hasScaleBasedVisibilityFlag="0" simplifyDrawingHints="0" readOnly="0" simplifyMaxScale="1" simplifyAlgorithm="0" maxScale="-4.65661e-10">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" forceraster="0" type="singleSymbol" symbollevels="0">
    <symbols>
      <symbol alpha="1" name="0" force_rhr="0" type="marker" clip_to_extent="1">
        <layer class="SimpleMarker" enabled="1" locked="0" pass="0">
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
  <customproperties>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Pie" attributeLegend="1">
    <DiagramCategory sizeScale="3x:0,0,0,0,0,0" penAlpha="255" width="15" penColor="#000000" lineSizeScale="3x:0,0,0,0,0,0" penWidth="0" rotationOffset="270" barWidth="5" sizeType="MM" backgroundColor="#ffffff" diagramOrientation="Up" maxScaleDenominator="1e+08" enabled="0" lineSizeType="MM" backgroundAlpha="255" labelPlacementMethod="XHeight" scaleDependency="Area" scaleBasedVisibility="0" minScaleDenominator="-4.65661e-10" opacity="1" height="15" minimumSize="0">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute color="#000000" field="" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings placement="0" linePlacementFlags="2" obstacle="0" dist="0" showAll="1" priority="0" zIndex="0">
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
    <default field="timeseries" expression="'0,1&#xd;&#xa;9999,1'" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" exp_strength="0" field="ROWID" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="id" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" exp_strength="0" field="connection_node_id" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="boundary_type" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" exp_strength="0" field="timeseries" notnull_strength="2" constraints="1"/>
  </constraints>
  <constraintExpressions>
    <constraint field="ROWID" desc="" exp=""/>
    <constraint field="id" desc="" exp=""/>
    <constraint field="connection_node_id" desc="" exp=""/>
    <constraint field="boundary_type" desc="" exp=""/>
    <constraint field="timeseries" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column hidden="0" name="ROWID" type="field" width="-1"/>
      <column hidden="0" name="id" type="field" width="-1"/>
      <column hidden="0" name="connection_node_id" type="field" width="-1"/>
      <column hidden="0" name="boundary_type" type="field" width="-1"/>
      <column hidden="0" name="timeseries" type="field" width="-1"/>
      <column hidden="1" type="actions" width="-1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
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
    <attributeEditorContainer showLabel="1" name="General" visibilityExpression="" groupBox="0" visibilityExpressionEnabled="0" columnCount="1">
      <attributeEditorField showLabel="1" name="id" index="1"/>
      <attributeEditorField showLabel="1" name="connection_node_id" index="2"/>
      <attributeEditorField showLabel="1" name="boundary_type" index="3"/>
      <attributeEditorField showLabel="1" name="timeseries" index="4"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="ROWID" editable="1"/>
    <field name="boundary_type" editable="1"/>
    <field name="connection_node_id" editable="0"/>
    <field name="id" editable="1"/>
    <field name="timeseries" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="ROWID" labelOnTop="0"/>
    <field name="boundary_type" labelOnTop="0"/>
    <field name="connection_node_id" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="timeseries" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>ROWID</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
