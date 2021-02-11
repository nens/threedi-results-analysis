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
    <field name="shape">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="00" name="00: square" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="01" name="01: round" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="02" name="02: rectangle" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="width">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="length">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manhole_indicator">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="0" name="0: inspection" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="1" name="1: outlet" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2: pumpstation" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="calculation_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="0" name="0: embedded" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="1" name="1: isolated" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2: connected" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="bottom_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="surface_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="drain_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="sediment_level">
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
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="" field="id"/>
    <alias index="1" name="" field="display_name"/>
    <alias index="2" name="" field="code"/>
    <alias index="3" name="" field="connection_node_id"/>
    <alias index="4" name="" field="shape"/>
    <alias index="5" name="" field="width"/>
    <alias index="6" name="" field="length"/>
    <alias index="7" name="" field="manhole_indicator"/>
    <alias index="8" name="" field="calculation_type"/>
    <alias index="9" name="" field="bottom_level"/>
    <alias index="10" name="" field="surface_level"/>
    <alias index="11" name="" field="drain_level"/>
    <alias index="12" name="" field="sediment_level"/>
    <alias index="13" name="" field="zoom_category"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" expression="if(maximum(id) is null,1, maximum(id)+1)" field="id"/>
    <default applyOnUpdate="0" expression="'new'" field="display_name"/>
    <default applyOnUpdate="0" expression="'new'" field="code"/>
    <default applyOnUpdate="0" expression="" field="connection_node_id"/>
    <default applyOnUpdate="0" expression="" field="shape"/>
    <default applyOnUpdate="0" expression="" field="width"/>
    <default applyOnUpdate="0" expression="" field="length"/>
    <default applyOnUpdate="0" expression="0" field="manhole_indicator"/>
    <default applyOnUpdate="0" expression="" field="calculation_type"/>
    <default applyOnUpdate="0" expression="" field="bottom_level"/>
    <default applyOnUpdate="0" expression="" field="surface_level"/>
    <default applyOnUpdate="0" expression="" field="drain_level"/>
    <default applyOnUpdate="0" expression="" field="sediment_level"/>
    <default applyOnUpdate="0" expression="1" field="zoom_category"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" notnull_strength="1" field="id" constraints="3" unique_strength="1"/>
    <constraint exp_strength="0" notnull_strength="0" field="display_name" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="code" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="connection_node_id" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="shape" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="width" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="length" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="manhole_indicator" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="calculation_type" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="bottom_level" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="surface_level" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="drain_level" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="sediment_level" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="zoom_category" constraints="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="display_name"/>
    <constraint exp="" desc="" field="code"/>
    <constraint exp="" desc="" field="connection_node_id"/>
    <constraint exp="" desc="" field="shape"/>
    <constraint exp="" desc="" field="width"/>
    <constraint exp="" desc="" field="length"/>
    <constraint exp="" desc="" field="manhole_indicator"/>
    <constraint exp="" desc="" field="calculation_type"/>
    <constraint exp="" desc="" field="bottom_level"/>
    <constraint exp="" desc="" field="surface_level"/>
    <constraint exp="" desc="" field="drain_level"/>
    <constraint exp="" desc="" field="sediment_level"/>
    <constraint exp="" desc="" field="zoom_category"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="" sortOrder="0">
    <columns>
      <column width="-1" hidden="0" name="id" type="field"/>
      <column width="-1" hidden="0" name="display_name" type="field"/>
      <column width="-1" hidden="0" name="code" type="field"/>
      <column width="-1" hidden="0" name="connection_node_id" type="field"/>
      <column width="-1" hidden="0" name="shape" type="field"/>
      <column width="-1" hidden="0" name="width" type="field"/>
      <column width="-1" hidden="0" name="length" type="field"/>
      <column width="-1" hidden="0" name="manhole_indicator" type="field"/>
      <column width="-1" hidden="0" name="calculation_type" type="field"/>
      <column width="-1" hidden="0" name="bottom_level" type="field"/>
      <column width="-1" hidden="0" name="surface_level" type="field"/>
      <column width="-1" hidden="0" name="drain_level" type="field"/>
      <column width="-1" hidden="0" name="sediment_level" type="field"/>
      <column width="-1" hidden="0" name="zoom_category" type="field"/>
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
    <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="Manhole" groupBox="0" visibilityExpressionEnabled="0">
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="General" groupBox="1" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="0" name="id"/>
        <attributeEditorField showLabel="1" index="1" name="display_name"/>
        <attributeEditorField showLabel="1" index="2" name="code"/>
        <attributeEditorField showLabel="1" index="3" name="connection_node_id"/>
        <attributeEditorField showLabel="1" index="8" name="calculation_type"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="Characteristics" groupBox="1" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="4" name="shape"/>
        <attributeEditorField showLabel="1" index="5" name="width"/>
        <attributeEditorField showLabel="1" index="6" name="length"/>
        <attributeEditorField showLabel="1" index="10" name="surface_level"/>
        <attributeEditorField showLabel="1" index="11" name="drain_level"/>
        <attributeEditorField showLabel="1" index="9" name="bottom_level"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="Visualization" groupBox="1" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="13" name="zoom_category"/>
        <attributeEditorField showLabel="1" index="7" name="manhole_indicator"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="bottom_level"/>
    <field editable="1" name="calculation_type"/>
    <field editable="1" name="code"/>
    <field editable="1" name="connection_node_id"/>
    <field editable="1" name="display_name"/>
    <field editable="1" name="drain_level"/>
    <field editable="1" name="id"/>
    <field editable="1" name="length"/>
    <field editable="1" name="manhole_indicator"/>
    <field editable="1" name="sediment_level"/>
    <field editable="1" name="shape"/>
    <field editable="1" name="surface_level"/>
    <field editable="1" name="width"/>
    <field editable="1" name="zoom_category"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="bottom_level"/>
    <field labelOnTop="0" name="calculation_type"/>
    <field labelOnTop="0" name="code"/>
    <field labelOnTop="0" name="connection_node_id"/>
    <field labelOnTop="0" name="display_name"/>
    <field labelOnTop="0" name="drain_level"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="length"/>
    <field labelOnTop="0" name="manhole_indicator"/>
    <field labelOnTop="0" name="sediment_level"/>
    <field labelOnTop="0" name="shape"/>
    <field labelOnTop="0" name="surface_level"/>
    <field labelOnTop="0" name="width"/>
    <field labelOnTop="0" name="zoom_category"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
