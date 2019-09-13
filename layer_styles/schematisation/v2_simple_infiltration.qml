<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" readOnly="0" version="3.4.11-Madeira" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="1e+8">
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
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
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
    <field name="infiltration_rate">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_rate_file">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_surface_option">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="max_infiltration_capacity_file">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="display_name">
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
    <alias index="0" name="" field="id"/>
    <alias index="1" name="" field="infiltration_rate"/>
    <alias index="2" name="" field="infiltration_rate_file"/>
    <alias index="3" name="" field="infiltration_surface_option"/>
    <alias index="4" name="" field="max_infiltration_capacity_file"/>
    <alias index="5" name="" field="display_name"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" expression="if(maximum(id) is null,1,maximum(id)+1)" field="id"/>
    <default applyOnUpdate="0" expression="" field="infiltration_rate"/>
    <default applyOnUpdate="0" expression="" field="infiltration_rate_file"/>
    <default applyOnUpdate="0" expression="0" field="infiltration_surface_option"/>
    <default applyOnUpdate="0" expression="" field="max_infiltration_capacity_file"/>
    <default applyOnUpdate="0" expression="'new'" field="display_name"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" notnull_strength="1" field="id" constraints="3" unique_strength="1"/>
    <constraint exp_strength="0" notnull_strength="2" field="infiltration_rate" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="infiltration_rate_file" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="infiltration_surface_option" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="max_infiltration_capacity_file" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="display_name" constraints="1" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="infiltration_rate"/>
    <constraint exp="" desc="" field="infiltration_rate_file"/>
    <constraint exp="" desc="" field="infiltration_surface_option"/>
    <constraint exp="" desc="" field="max_infiltration_capacity_file"/>
    <constraint exp="" desc="" field="display_name"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="" sortOrder="0">
    <columns>
      <column width="-1" hidden="0" name="id" type="field"/>
      <column width="-1" hidden="0" name="infiltration_rate" type="field"/>
      <column width="-1" hidden="0" name="infiltration_rate_file" type="field"/>
      <column width="-1" hidden="0" name="infiltration_surface_option" type="field"/>
      <column width="-1" hidden="0" name="max_infiltration_capacity_file" type="field"/>
      <column width="-1" hidden="0" name="display_name" type="field"/>
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
    <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="General" groupBox="0" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="0" name="id"/>
      <attributeEditorField showLabel="1" index="5" name="display_name"/>
      <attributeEditorField showLabel="1" index="1" name="infiltration_rate"/>
      <attributeEditorField showLabel="1" index="2" name="infiltration_rate_file"/>
      <attributeEditorField showLabel="1" index="4" name="max_infiltration_capacity_file"/>
      <attributeEditorField showLabel="1" index="3" name="infiltration_surface_option"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="display_name"/>
    <field editable="1" name="id"/>
    <field editable="1" name="infiltration_rate"/>
    <field editable="1" name="infiltration_rate_file"/>
    <field editable="1" name="infiltration_surface_option"/>
    <field editable="1" name="max_infiltration_capacity_file"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="display_name"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="infiltration_rate"/>
    <field labelOnTop="0" name="infiltration_rate_file"/>
    <field labelOnTop="0" name="infiltration_surface_option"/>
    <field labelOnTop="0" name="max_infiltration_capacity_file"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
