<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="1e+08" readOnly="0" version="3.4.5-Madeira" maxScale="0">
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
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="upper_stop_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
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
                <Option name="-1" value="-1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="0" value="0" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="1" value="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="2" value="2" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="3" value="3" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="4" value="4" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="5" value="5" type="QString"/>
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
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_end_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="classification">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="sewerage">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option name="CheckedState" value="1" type="QString"/>
            <Option name="UncheckedState" value="0" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="lower_stop_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_start_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="capacity">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
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
                <Option name="1: pump reacts only on suction side" value="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="2: pump reacts only on delivery side" value="2" type="QString"/>
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
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" index="0" field="upper_stop_level"/>
    <alias name="" index="1" field="zoom_category"/>
    <alias name="" index="2" field="code"/>
    <alias name="" index="3" field="display_name"/>
    <alias name="" index="4" field="connection_node_end_id"/>
    <alias name="" index="5" field="classification"/>
    <alias name="" index="6" field="sewerage"/>
    <alias name="" index="7" field="lower_stop_level"/>
    <alias name="" index="8" field="connection_node_start_id"/>
    <alias name="" index="9" field="start_level"/>
    <alias name="" index="10" field="capacity"/>
    <alias name="" index="11" field="type"/>
    <alias name="" index="12" field="id"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="upper_stop_level" expression=""/>
    <default applyOnUpdate="0" field="zoom_category" expression="3"/>
    <default applyOnUpdate="0" field="code" expression="'new'"/>
    <default applyOnUpdate="0" field="display_name" expression="'new'"/>
    <default applyOnUpdate="0" field="connection_node_end_id" expression=""/>
    <default applyOnUpdate="0" field="classification" expression=""/>
    <default applyOnUpdate="0" field="sewerage" expression=""/>
    <default applyOnUpdate="0" field="lower_stop_level" expression=""/>
    <default applyOnUpdate="0" field="connection_node_start_id" expression=""/>
    <default applyOnUpdate="0" field="start_level" expression=""/>
    <default applyOnUpdate="0" field="capacity" expression=""/>
    <default applyOnUpdate="0" field="type" expression="1"/>
    <default applyOnUpdate="0" field="id" expression="if(maximum(id) is null,1, maximum(id)+1)"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" constraints="4" exp_strength="2" field="upper_stop_level" unique_strength="0"/>
    <constraint notnull_strength="2" constraints="1" exp_strength="0" field="zoom_category" unique_strength="0"/>
    <constraint notnull_strength="2" constraints="1" exp_strength="0" field="code" unique_strength="0"/>
    <constraint notnull_strength="2" constraints="1" exp_strength="0" field="display_name" unique_strength="0"/>
    <constraint notnull_strength="2" constraints="1" exp_strength="0" field="connection_node_end_id" unique_strength="0"/>
    <constraint notnull_strength="0" constraints="0" exp_strength="0" field="classification" unique_strength="0"/>
    <constraint notnull_strength="0" constraints="0" exp_strength="0" field="sewerage" unique_strength="0"/>
    <constraint notnull_strength="2" constraints="5" exp_strength="2" field="lower_stop_level" unique_strength="0"/>
    <constraint notnull_strength="2" constraints="1" exp_strength="0" field="connection_node_start_id" unique_strength="0"/>
    <constraint notnull_strength="2" constraints="1" exp_strength="0" field="start_level" unique_strength="0"/>
    <constraint notnull_strength="2" constraints="5" exp_strength="2" field="capacity" unique_strength="0"/>
    <constraint notnull_strength="2" constraints="1" exp_strength="0" field="type" unique_strength="0"/>
    <constraint notnull_strength="1" constraints="3" exp_strength="0" field="id" unique_strength="1"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="&quot;upper_stop_level&quot;>&quot;start_level&quot; or &quot;upper_stop_level&quot; is null" field="upper_stop_level" desc=""/>
    <constraint exp="" field="zoom_category" desc=""/>
    <constraint exp="" field="code" desc=""/>
    <constraint exp="" field="display_name" desc=""/>
    <constraint exp="" field="connection_node_end_id" desc=""/>
    <constraint exp="" field="classification" desc=""/>
    <constraint exp="" field="sewerage" desc=""/>
    <constraint exp="&quot;lower_stop_level&quot;&lt;&quot;start_level&quot;" field="lower_stop_level" desc=""/>
    <constraint exp="" field="connection_node_start_id" desc=""/>
    <constraint exp="" field="start_level" desc=""/>
    <constraint exp="&quot;capacity&quot;>=0" field="capacity" desc=""/>
    <constraint exp="" field="type" desc=""/>
    <constraint exp="" field="id" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortExpression="" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column name="upper_stop_level" hidden="0" width="-1" type="field"/>
      <column name="zoom_category" hidden="0" width="-1" type="field"/>
      <column name="code" hidden="0" width="-1" type="field"/>
      <column name="display_name" hidden="0" width="-1" type="field"/>
      <column name="connection_node_end_id" hidden="0" width="-1" type="field"/>
      <column name="classification" hidden="0" width="-1" type="field"/>
      <column name="sewerage" hidden="0" width="-1" type="field"/>
      <column name="lower_stop_level" hidden="0" width="-1" type="field"/>
      <column name="connection_node_start_id" hidden="0" width="-1" type="field"/>
      <column name="start_level" hidden="0" width="-1" type="field"/>
      <column name="capacity" hidden="0" width="-1" type="field"/>
      <column name="type" hidden="0" width="-1" type="field"/>
      <column name="id" hidden="0" width="-1" type="field"/>
      <column hidden="1" width="-1" type="actions"/>
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
    <attributeEditorContainer name="Pumpstation" groupBox="0" columnCount="1" visibilityExpressionEnabled="0" visibilityExpression="" showLabel="1">
      <attributeEditorContainer name="General" groupBox="1" columnCount="1" visibilityExpressionEnabled="0" visibilityExpression="" showLabel="1">
        <attributeEditorField name="id" index="12" showLabel="1"/>
        <attributeEditorField name="display_name" index="3" showLabel="1"/>
        <attributeEditorField name="code" index="2" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Characteristics" groupBox="1" columnCount="1" visibilityExpressionEnabled="0" visibilityExpression="" showLabel="1">
        <attributeEditorField name="capacity" index="10" showLabel="1"/>
        <attributeEditorField name="start_level" index="9" showLabel="1"/>
        <attributeEditorField name="lower_stop_level" index="7" showLabel="1"/>
        <attributeEditorField name="upper_stop_level" index="0" showLabel="1"/>
        <attributeEditorField name="type" index="11" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Visualization" groupBox="1" columnCount="1" visibilityExpressionEnabled="0" visibilityExpression="" showLabel="1">
        <attributeEditorField name="zoom_category" index="1" showLabel="1"/>
        <attributeEditorField name="sewerage" index="6" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Connection nodes" groupBox="1" columnCount="1" visibilityExpressionEnabled="0" visibilityExpression="" showLabel="1">
        <attributeEditorField name="connection_node_start_id" index="8" showLabel="1"/>
        <attributeEditorField name="connection_node_end_id" index="4" showLabel="1"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="capacity" editable="1"/>
    <field name="classification" editable="1"/>
    <field name="code" editable="1"/>
    <field name="connection_node_end_id" editable="1"/>
    <field name="connection_node_start_id" editable="1"/>
    <field name="display_name" editable="1"/>
    <field name="id" editable="1"/>
    <field name="lower_stop_level" editable="1"/>
    <field name="sewerage" editable="1"/>
    <field name="start_level" editable="1"/>
    <field name="type" editable="1"/>
    <field name="upper_stop_level" editable="1"/>
    <field name="zoom_category" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="capacity" labelOnTop="0"/>
    <field name="classification" labelOnTop="0"/>
    <field name="code" labelOnTop="0"/>
    <field name="connection_node_end_id" labelOnTop="0"/>
    <field name="connection_node_start_id" labelOnTop="0"/>
    <field name="display_name" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="lower_stop_level" labelOnTop="0"/>
    <field name="sewerage" labelOnTop="0"/>
    <field name="start_level" labelOnTop="0"/>
    <field name="type" labelOnTop="0"/>
    <field name="upper_stop_level" labelOnTop="0"/>
    <field name="zoom_category" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>display_name</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
