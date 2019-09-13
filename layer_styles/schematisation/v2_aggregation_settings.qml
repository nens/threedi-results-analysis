<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" readOnly="0" version="3.4.11-Madeira" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="1e+8">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property key="dualview/previewExpressions">
      <value>var_name</value>
    </property>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="timestep">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="var_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="global_settings_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="aggregation_in_space">
      <editWidget type="Hidden">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="aggregation_method">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="avg" name="average" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="min" name="minimum" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="max" name="maximum" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="cum" name="cumulative" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="med" name="median" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="cum_negative" name="cumulative negative" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="cum_positive" name="cumulative positive" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="current" name="current" type="QString"/>
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
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="discharge" name="discharge" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="flow_velocity" name="flow velocity" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="pump_discharge" name="pump discharge" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="rain" name="rain" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="waterlevel" name="waterlevel" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="wet_cross-section" name="wet cross section" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="wet_surface" name="wet surface" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="lateral_discharge" name="lateral discharge" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="volume" name="volume" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="simple_infiltration" name="infiltration" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="leakage" name="leakage" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="interception" name="interception" type="QString"/>
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
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="" field="timestep"/>
    <alias index="1" name="" field="var_name"/>
    <alias index="2" name="" field="global_settings_id"/>
    <alias index="3" name="" field="aggregation_in_space"/>
    <alias index="4" name="" field="aggregation_method"/>
    <alias index="5" name="" field="flow_variable"/>
    <alias index="6" name="" field="id"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" expression="" field="timestep"/>
    <default applyOnUpdate="0" expression="" field="var_name"/>
    <default applyOnUpdate="0" expression="" field="global_settings_id"/>
    <default applyOnUpdate="0" expression="0" field="aggregation_in_space"/>
    <default applyOnUpdate="0" expression="" field="aggregation_method"/>
    <default applyOnUpdate="0" expression="" field="flow_variable"/>
    <default applyOnUpdate="0" expression="if(maximum(id) is null,1, maximum(id)+1)" field="id"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" notnull_strength="2" field="timestep" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="var_name" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="global_settings_id" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="aggregation_in_space" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="aggregation_method" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="flow_variable" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="1" field="id" constraints="3" unique_strength="1"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="timestep"/>
    <constraint exp="" desc="" field="var_name"/>
    <constraint exp="" desc="" field="global_settings_id"/>
    <constraint exp="" desc="" field="aggregation_in_space"/>
    <constraint exp="" desc="" field="aggregation_method"/>
    <constraint exp="" desc="" field="flow_variable"/>
    <constraint exp="" desc="" field="id"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="" sortOrder="0">
    <columns>
      <column width="214" hidden="0" name="timestep" type="field"/>
      <column width="207" hidden="0" name="var_name" type="field"/>
      <column width="123" hidden="0" name="global_settings_id" type="field"/>
      <column width="168" hidden="0" name="aggregation_in_space" type="field"/>
      <column width="-1" hidden="0" name="aggregation_method" type="field"/>
      <column width="-1" hidden="0" name="flow_variable" type="field"/>
      <column width="-1" hidden="0" name="id" type="field"/>
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
      <attributeEditorField showLabel="1" index="6" name="id"/>
      <attributeEditorField showLabel="1" index="5" name="flow_variable"/>
      <attributeEditorField showLabel="1" index="4" name="aggregation_method"/>
      <attributeEditorField showLabel="1" index="0" name="timestep"/>
      <attributeEditorField showLabel="1" index="1" name="var_name"/>
      <attributeEditorField showLabel="1" index="2" name="global_settings_id"/>
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
