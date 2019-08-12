<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" version="3.4.5-Madeira" minScale="1e+08" maxScale="0" readOnly="0" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property key="dualview/previewExpressions" value="var_name"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="global_settings_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="timestep">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="var_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="aggregation_in_space">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option type="QString" value="1" name="CheckedState"/>
            <Option type="QString" value="0" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="aggregation_method">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" value="avg" name="average"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="min" name="minimum"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="max" name="maximum"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="cum" name="cumulative"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="med" name="median"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="cum_negative" name="cumulative negative"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="cum_positive" name="cumulative positive"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="current" name="current"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="flow_variable">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" value="discharge" name="discharge"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="flow_velocity" name="flow velocity"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="pump_discharge" name="pump discharge"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="rain" name="rain"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="waterlevel" name="waterlevel"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="wet_cross-section" name="wet cross section"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="wet_surface" name="wet surface"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="lateral_discharge" name="lateral discharge"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="volume" name="volume"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="simple_infiltration" name="infiltration"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="leakage" name="leakage"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="interception" name="interception"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
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
  </fieldConfiguration>
  <aliases>
    <alias field="global_settings_id" index="0" name=""/>
    <alias field="timestep" index="1" name=""/>
    <alias field="var_name" index="2" name=""/>
    <alias field="aggregation_in_space" index="3" name=""/>
    <alias field="aggregation_method" index="4" name=""/>
    <alias field="flow_variable" index="5" name=""/>
    <alias field="id" index="6" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="global_settings_id"/>
    <default expression="" applyOnUpdate="0" field="timestep"/>
    <default expression="" applyOnUpdate="0" field="var_name"/>
    <default expression="0" applyOnUpdate="0" field="aggregation_in_space"/>
    <default expression="" applyOnUpdate="0" field="aggregation_method"/>
    <default expression="" applyOnUpdate="0" field="flow_variable"/>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="global_settings_id" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="timestep" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="var_name" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="aggregation_in_space" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="aggregation_method" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="flow_variable" exp_strength="0"/>
    <constraint unique_strength="1" constraints="3" notnull_strength="1" field="id" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="global_settings_id" exp=""/>
    <constraint desc="" field="timestep" exp=""/>
    <constraint desc="" field="var_name" exp=""/>
    <constraint desc="" field="aggregation_in_space" exp=""/>
    <constraint desc="" field="aggregation_method" exp=""/>
    <constraint desc="" field="flow_variable" exp=""/>
    <constraint desc="" field="id" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column width="-1" hidden="0" type="field" name="timestep"/>
      <column width="-1" hidden="0" type="field" name="var_name"/>
      <column width="-1" hidden="0" type="field" name="global_settings_id"/>
      <column width="-1" hidden="0" type="field" name="aggregation_in_space"/>
      <column width="-1" hidden="0" type="field" name="aggregation_method"/>
      <column width="-1" hidden="0" type="field" name="flow_variable"/>
      <column width="-1" hidden="0" type="field" name="id"/>
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
      <attributeEditorField index="6" name="id" showLabel="1"/>
      <attributeEditorField index="5" name="flow_variable" showLabel="1"/>
      <attributeEditorField index="4" name="aggregation_method" showLabel="1"/>
      <attributeEditorField index="1" name="timestep" showLabel="1"/>
      <attributeEditorField index="2" name="var_name" showLabel="1"/>
      <attributeEditorField index="0" name="global_settings_id" showLabel="1"/>
      <attributeEditorField index="3" name="aggregation_in_space" showLabel="1"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="aggregation_in_space"/>
    <field editable="1" name="aggregation_method"/>
    <field editable="1" name="flow_variable"/>
    <field editable="1" name="global_settings_id"/>
    <field editable="1" name="id"/>
    <field editable="1" name="timestep"/>
    <field editable="1" name="var_name"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="aggregation_in_space"/>
    <field labelOnTop="0" name="aggregation_method"/>
    <field labelOnTop="0" name="flow_variable"/>
    <field labelOnTop="0" name="global_settings_id"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="timestep"/>
    <field labelOnTop="0" name="var_name"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>var_name</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
