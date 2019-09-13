<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" version="3.4.5-Madeira" minScale="1e+08" maxScale="0" readOnly="0" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
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
    <field name="outflow_delay">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="surface_layer_thickness">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="max_infiltration_capacity">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="min_infiltration_capacity">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_decay_constant">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_recovery_constant">
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
    <alias field="outflow_delay" index="1" name=""/>
    <alias field="surface_layer_thickness" index="2" name=""/>
    <alias field="infiltration" index="3" name=""/>
    <alias field="max_infiltration_capacity" index="4" name=""/>
    <alias field="min_infiltration_capacity" index="5" name=""/>
    <alias field="infiltration_decay_constant" index="6" name=""/>
    <alias field="infiltration_recovery_constant" index="7" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
    <default expression="" applyOnUpdate="0" field="outflow_delay"/>
    <default expression="" applyOnUpdate="0" field="surface_layer_thickness"/>
    <default expression="" applyOnUpdate="0" field="infiltration"/>
    <default expression="" applyOnUpdate="0" field="max_infiltration_capacity"/>
    <default expression="" applyOnUpdate="0" field="min_infiltration_capacity"/>
    <default expression="" applyOnUpdate="0" field="infiltration_decay_constant"/>
    <default expression="" applyOnUpdate="0" field="infiltration_recovery_constant"/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" constraints="3" notnull_strength="1" field="id" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="outflow_delay" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="surface_layer_thickness" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="infiltration" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="max_infiltration_capacity" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="min_infiltration_capacity" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="infiltration_decay_constant" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="infiltration_recovery_constant" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="id" exp=""/>
    <constraint desc="" field="outflow_delay" exp=""/>
    <constraint desc="" field="surface_layer_thickness" exp=""/>
    <constraint desc="" field="infiltration" exp=""/>
    <constraint desc="" field="max_infiltration_capacity" exp=""/>
    <constraint desc="" field="min_infiltration_capacity" exp=""/>
    <constraint desc="" field="infiltration_decay_constant" exp=""/>
    <constraint desc="" field="infiltration_recovery_constant" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column width="-1" hidden="0" type="field" name="id"/>
      <column width="-1" hidden="0" type="field" name="outflow_delay"/>
      <column width="-1" hidden="0" type="field" name="surface_layer_thickness"/>
      <column width="-1" hidden="0" type="field" name="infiltration"/>
      <column width="-1" hidden="0" type="field" name="max_infiltration_capacity"/>
      <column width="-1" hidden="0" type="field" name="min_infiltration_capacity"/>
      <column width="-1" hidden="0" type="field" name="infiltration_decay_constant"/>
      <column width="-1" hidden="0" type="field" name="infiltration_recovery_constant"/>
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
      <attributeEditorField index="3" name="infiltration" showLabel="1"/>
      <attributeEditorField index="4" name="max_infiltration_capacity" showLabel="1"/>
      <attributeEditorField index="5" name="min_infiltration_capacity" showLabel="1"/>
      <attributeEditorField index="6" name="infiltration_decay_constant" showLabel="1"/>
      <attributeEditorField index="7" name="infiltration_recovery_constant" showLabel="1"/>
      <attributeEditorField index="2" name="surface_layer_thickness" showLabel="1"/>
      <attributeEditorField index="1" name="outflow_delay" showLabel="1"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="id"/>
    <field editable="1" name="infiltration"/>
    <field editable="1" name="infiltration_decay_constant"/>
    <field editable="1" name="infiltration_recovery_constant"/>
    <field editable="1" name="max_infiltration_capacity"/>
    <field editable="1" name="min_infiltration_capacity"/>
    <field editable="1" name="outflow_delay"/>
    <field editable="1" name="surface_layer_thickness"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="infiltration"/>
    <field labelOnTop="0" name="infiltration_decay_constant"/>
    <field labelOnTop="0" name="infiltration_recovery_constant"/>
    <field labelOnTop="0" name="max_infiltration_capacity"/>
    <field labelOnTop="0" name="min_infiltration_capacity"/>
    <field labelOnTop="0" name="outflow_delay"/>
    <field labelOnTop="0" name="surface_layer_thickness"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
