<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" readOnly="0" version="3.4.11-Madeira" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="1e+8">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property value="display_name" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="upper_stop_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="zoom_category">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="-1" name="-1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="0" name="0" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="1" name="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="3" name="3" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="4" name="4" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="5" name="5" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="code">
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
    <field name="connection_node_end_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="classification">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="sewerage">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" name="CheckedState" type="QString"/>
            <Option value="0" name="UncheckedState" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="lower_stop_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_start_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="capacity">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="1" name="1: Pump behaviour is based on water levels on the suction-side of the pump" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2: Pump behaviour is based on water levels on the delivery-side of the pump" type="QString"/>
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
    <alias index="0" name="" field="upper_stop_level"/>
    <alias index="1" name="" field="zoom_category"/>
    <alias index="2" name="" field="code"/>
    <alias index="3" name="" field="display_name"/>
    <alias index="4" name="" field="connection_node_end_id"/>
    <alias index="5" name="" field="classification"/>
    <alias index="6" name="" field="sewerage"/>
    <alias index="7" name="" field="lower_stop_level"/>
    <alias index="8" name="" field="connection_node_start_id"/>
    <alias index="9" name="" field="start_level"/>
    <alias index="10" name="" field="capacity"/>
    <alias index="11" name="" field="type"/>
    <alias index="12" name="" field="id"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" expression="" field="upper_stop_level"/>
    <default applyOnUpdate="0" expression="3" field="zoom_category"/>
    <default applyOnUpdate="0" expression="'new'" field="code"/>
    <default applyOnUpdate="0" expression="'new'" field="display_name"/>
    <default applyOnUpdate="0" expression="" field="connection_node_end_id"/>
    <default applyOnUpdate="0" expression="" field="classification"/>
    <default applyOnUpdate="0" expression="" field="sewerage"/>
    <default applyOnUpdate="0" expression="" field="lower_stop_level"/>
    <default applyOnUpdate="0" expression="" field="connection_node_start_id"/>
    <default applyOnUpdate="0" expression="" field="start_level"/>
    <default applyOnUpdate="0" expression="" field="capacity"/>
    <default applyOnUpdate="0" expression="1" field="type"/>
    <default applyOnUpdate="0" expression="if(maximum(id) is null,1, maximum(id)+1)" field="id"/>
  </defaults>
  <constraints>
    <constraint exp_strength="2" notnull_strength="0" field="upper_stop_level" constraints="4" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="zoom_category" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="code" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="display_name" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="connection_node_end_id" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="classification" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="sewerage" constraints="0" unique_strength="0"/>
    <constraint exp_strength="2" notnull_strength="2" field="lower_stop_level" constraints="5" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="connection_node_start_id" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="start_level" constraints="1" unique_strength="0"/>
    <constraint exp_strength="2" notnull_strength="2" field="capacity" constraints="5" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="type" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="1" field="id" constraints="3" unique_strength="1"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="&quot;upper_stop_level&quot;>&quot;start_level&quot; or &quot;upper_stop_level&quot; is null" desc="" field="upper_stop_level"/>
    <constraint exp="" desc="" field="zoom_category"/>
    <constraint exp="" desc="" field="code"/>
    <constraint exp="" desc="" field="display_name"/>
    <constraint exp="" desc="" field="connection_node_end_id"/>
    <constraint exp="" desc="" field="classification"/>
    <constraint exp="" desc="" field="sewerage"/>
    <constraint exp="&quot;lower_stop_level&quot;&lt;&quot;start_level&quot;" desc="" field="lower_stop_level"/>
    <constraint exp="" desc="" field="connection_node_start_id"/>
    <constraint exp="" desc="" field="start_level"/>
    <constraint exp="&quot;capacity&quot;>=0" desc="" field="capacity"/>
    <constraint exp="" desc="" field="type"/>
    <constraint exp="" desc="" field="id"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="" sortOrder="0">
    <columns>
      <column width="-1" hidden="0" name="upper_stop_level" type="field"/>
      <column width="-1" hidden="0" name="zoom_category" type="field"/>
      <column width="-1" hidden="0" name="code" type="field"/>
      <column width="-1" hidden="0" name="display_name" type="field"/>
      <column width="-1" hidden="0" name="connection_node_end_id" type="field"/>
      <column width="-1" hidden="0" name="classification" type="field"/>
      <column width="-1" hidden="0" name="sewerage" type="field"/>
      <column width="-1" hidden="0" name="lower_stop_level" type="field"/>
      <column width="-1" hidden="0" name="connection_node_start_id" type="field"/>
      <column width="-1" hidden="0" name="start_level" type="field"/>
      <column width="-1" hidden="0" name="capacity" type="field"/>
      <column width="-1" hidden="0" name="type" type="field"/>
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
    <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="Pumpstation" groupBox="0" visibilityExpressionEnabled="0">
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="General" groupBox="1" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="12" name="id"/>
        <attributeEditorField showLabel="1" index="3" name="display_name"/>
        <attributeEditorField showLabel="1" index="2" name="code"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="Characteristics" groupBox="1" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="10" name="capacity"/>
        <attributeEditorField showLabel="1" index="9" name="start_level"/>
        <attributeEditorField showLabel="1" index="7" name="lower_stop_level"/>
        <attributeEditorField showLabel="1" index="0" name="upper_stop_level"/>
        <attributeEditorField showLabel="1" index="11" name="type"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="Visualization" groupBox="1" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="1" name="zoom_category"/>
        <attributeEditorField showLabel="1" index="6" name="sewerage"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="Connection nodes" groupBox="1" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="8" name="connection_node_start_id"/>
        <attributeEditorField showLabel="1" index="4" name="connection_node_end_id"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="capacity"/>
    <field editable="1" name="classification"/>
    <field editable="1" name="code"/>
    <field editable="1" name="connection_node_end_id"/>
    <field editable="1" name="connection_node_start_id"/>
    <field editable="1" name="display_name"/>
    <field editable="1" name="id"/>
    <field editable="1" name="lower_stop_level"/>
    <field editable="1" name="sewerage"/>
    <field editable="1" name="start_level"/>
    <field editable="1" name="type"/>
    <field editable="1" name="upper_stop_level"/>
    <field editable="1" name="zoom_category"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="capacity"/>
    <field labelOnTop="0" name="classification"/>
    <field labelOnTop="0" name="code"/>
    <field labelOnTop="0" name="connection_node_end_id"/>
    <field labelOnTop="0" name="connection_node_start_id"/>
    <field labelOnTop="0" name="display_name"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="lower_stop_level"/>
    <field labelOnTop="0" name="sewerage"/>
    <field labelOnTop="0" name="start_level"/>
    <field labelOnTop="0" name="type"/>
    <field labelOnTop="0" name="upper_stop_level"/>
    <field labelOnTop="0" name="zoom_category"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>display_name</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
