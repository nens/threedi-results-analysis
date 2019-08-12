<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" version="3.4.5-Madeira" maxScale="0" styleCategories="AllStyleCategories" minScale="1e+08" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property value="id" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="boundary_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="1" type="QString" name="1: waterlevel"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: velocity"/>
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3: discharge"/>
              </Option>
              <Option type="Map">
                <Option value="5" type="QString" name="5: sommerfeld"/>
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
            <Option value="true" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="id" index="0"/>
    <alias name="" field="connection_node_id" index="1"/>
    <alias name="" field="boundary_type" index="2"/>
    <alias name="" field="timeseries" index="3"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
    <default expression="" applyOnUpdate="0" field="connection_node_id"/>
    <default expression="" applyOnUpdate="0" field="boundary_type"/>
    <default expression="'0,1&#xd;&#xa;9999,1'" applyOnUpdate="0" field="timeseries"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" unique_strength="1" notnull_strength="1" constraints="3" field="id"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="connection_node_id"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="boundary_type"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="timeseries"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="connection_node_id"/>
    <constraint exp="" desc="" field="boundary_type"/>
    <constraint exp="" desc="" field="timeseries"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column width="-1" type="field" hidden="0" name="id"/>
      <column width="-1" type="field" hidden="0" name="connection_node_id"/>
      <column width="-1" type="field" hidden="0" name="boundary_type"/>
      <column width="-1" type="field" hidden="0" name="timeseries"/>
      <column width="-1" type="actions" hidden="1"/>
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
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer groupBox="0" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" name="General" columnCount="1">
      <attributeEditorField showLabel="1" name="id" index="0"/>
      <attributeEditorField showLabel="1" name="connection_node_id" index="1"/>
      <attributeEditorField showLabel="1" name="boundary_type" index="2"/>
      <attributeEditorField showLabel="1" name="timeseries" index="3"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="boundary_type" editable="1"/>
    <field name="connection_node_id" editable="1"/>
    <field name="id" editable="1"/>
    <field name="timeseries" editable="1"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="boundary_type"/>
    <field labelOnTop="0" name="connection_node_id"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="timeseries"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
