<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" version="3.4.5-Madeira" minScale="1e+08" maxScale="0" readOnly="0" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property key="dualview/previewExpressions" value="id"/>
    <property key="embeddedWidgets/count" value="0"/>
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
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="surface_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" value="v2_surface" name="v2_surface"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="v2_impervious_surface" name="v2_impervious_surface"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="surface_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="percentage">
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
    <alias field="id" index="0" name=""/>
    <alias field="surface_type" index="1" name=""/>
    <alias field="surface_id" index="2" name=""/>
    <alias field="connection_node_id" index="3" name=""/>
    <alias field="percentage" index="4" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
    <default expression="" applyOnUpdate="0" field="surface_type"/>
    <default expression="" applyOnUpdate="0" field="surface_id"/>
    <default expression="" applyOnUpdate="0" field="connection_node_id"/>
    <default expression="" applyOnUpdate="0" field="percentage"/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" constraints="3" notnull_strength="1" field="id" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="surface_type" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="surface_id" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="connection_node_id" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="percentage" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="id" exp=""/>
    <constraint desc="" field="surface_type" exp=""/>
    <constraint desc="" field="surface_id" exp=""/>
    <constraint desc="" field="connection_node_id" exp=""/>
    <constraint desc="" field="percentage" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column width="-1" hidden="0" type="field" name="id"/>
      <column width="-1" hidden="0" type="field" name="surface_type"/>
      <column width="-1" hidden="0" type="field" name="surface_id"/>
      <column width="-1" hidden="0" type="field" name="connection_node_id"/>
      <column width="-1" hidden="0" type="field" name="percentage"/>
      <column width="-1" hidden="1" type="actions"/>
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
    <attributeEditorContainer visibilityExpression="" visibilityExpressionEnabled="0" columnCount="1" name="General" showLabel="1" groupBox="0">
      <attributeEditorField index="0" name="id" showLabel="1"/>
      <attributeEditorField index="1" name="surface_type" showLabel="1"/>
      <attributeEditorField index="2" name="surface_id" showLabel="1"/>
      <attributeEditorField index="3" name="connection_node_id" showLabel="1"/>
      <attributeEditorField index="4" name="percentage" showLabel="1"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="connection_node_id"/>
    <field editable="1" name="id"/>
    <field editable="1" name="percentage"/>
    <field editable="1" name="surface_id"/>
    <field editable="1" name="surface_type"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="connection_node_id"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="percentage"/>
    <field labelOnTop="0" name="surface_id"/>
    <field labelOnTop="0" name="surface_type"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
