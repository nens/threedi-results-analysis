<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" readOnly="0" version="3.4.11-Madeira" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="1e+8">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property key="dualview/previewExpressions">
      <value>id</value>
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
    <field name="interflow_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="0" name="0: No interflow" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="1" name="1: Porosity is rescaled per computational cell with respect to the deepest surface level in that cell. (Defining the porosity_layer_thickness is mandatory)" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2: Porosity is rescaled per computational cell with respect to the deepest surface level in the 2D surface domain. (Defining the porosity_layer_thickness is mandatory)" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="3" name="3: The impervious layer thickness is uniform in the 2D surface domain and is based on the impervious_layer_elevation and the deepest surface level in that cell." type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="4" name="4: The impervious layer thickness is non-uniform in the 2D surface domain and is based on the impervious_layer_elevation with respect to the deepest surface level in the 2D surface domain." type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="porosity">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="porosity_file">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="porosity_layer_thickness">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="impervious_layer_elevation">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="hydraulic_conductivity">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="hydraulic_conductivity_file">
      <editWidget type="TextEdit">
        <config>
          <Option/>
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
    <alias index="1" name="" field="interflow_type"/>
    <alias index="2" name="" field="porosity"/>
    <alias index="3" name="" field="porosity_file"/>
    <alias index="4" name="" field="porosity_layer_thickness"/>
    <alias index="5" name="" field="impervious_layer_elevation"/>
    <alias index="6" name="" field="hydraulic_conductivity"/>
    <alias index="7" name="" field="hydraulic_conductivity_file"/>
    <alias index="8" name="" field="display_name"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" expression="if(maximum(id) is null,1, maximum(id)+1)" field="id"/>
    <default applyOnUpdate="0" expression="" field="interflow_type"/>
    <default applyOnUpdate="0" expression="" field="porosity"/>
    <default applyOnUpdate="0" expression="" field="porosity_file"/>
    <default applyOnUpdate="0" expression="" field="porosity_layer_thickness"/>
    <default applyOnUpdate="0" expression="" field="impervious_layer_elevation"/>
    <default applyOnUpdate="0" expression="" field="hydraulic_conductivity"/>
    <default applyOnUpdate="0" expression="" field="hydraulic_conductivity_file"/>
    <default applyOnUpdate="0" expression="" field="display_name"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" notnull_strength="1" field="id" constraints="3" unique_strength="1"/>
    <constraint exp_strength="0" notnull_strength="2" field="interflow_type" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="porosity" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="porosity_file" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="porosity_layer_thickness" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="impervious_layer_elevation" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="hydraulic_conductivity" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="hydraulic_conductivity_file" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="display_name" constraints="1" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="interflow_type"/>
    <constraint exp="" desc="" field="porosity"/>
    <constraint exp="" desc="" field="porosity_file"/>
    <constraint exp="" desc="" field="porosity_layer_thickness"/>
    <constraint exp="" desc="" field="impervious_layer_elevation"/>
    <constraint exp="" desc="" field="hydraulic_conductivity"/>
    <constraint exp="" desc="" field="hydraulic_conductivity_file"/>
    <constraint exp="" desc="" field="display_name"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="" sortOrder="0">
    <columns>
      <column width="-1" hidden="0" name="id" type="field"/>
      <column width="-1" hidden="0" name="interflow_type" type="field"/>
      <column width="-1" hidden="0" name="porosity" type="field"/>
      <column width="-1" hidden="0" name="porosity_file" type="field"/>
      <column width="-1" hidden="0" name="porosity_layer_thickness" type="field"/>
      <column width="-1" hidden="0" name="impervious_layer_elevation" type="field"/>
      <column width="-1" hidden="0" name="hydraulic_conductivity" type="field"/>
      <column width="-1" hidden="0" name="hydraulic_conductivity_file" type="field"/>
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
      <attributeEditorField showLabel="1" index="8" name="display_name"/>
      <attributeEditorField showLabel="1" index="1" name="interflow_type"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="Porosity" groupBox="0" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="2" name="porosity"/>
      <attributeEditorField showLabel="1" index="3" name="porosity_file"/>
      <attributeEditorField showLabel="1" index="4" name="porosity_layer_thickness"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="Hydraulic conductivity" groupBox="0" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="7" name="hydraulic_conductivity_file"/>
      <attributeEditorField showLabel="1" index="6" name="hydraulic_conductivity"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="Impervious layer" groupBox="0" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="5" name="impervious_layer_elevation"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="display_name"/>
    <field editable="1" name="hydraulic_conductivity"/>
    <field editable="1" name="hydraulic_conductivity_file"/>
    <field editable="1" name="id"/>
    <field editable="1" name="impervious_layer_elevation"/>
    <field editable="1" name="interflow_type"/>
    <field editable="1" name="porosity"/>
    <field editable="1" name="porosity_file"/>
    <field editable="1" name="porosity_layer_thickness"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="display_name"/>
    <field labelOnTop="0" name="hydraulic_conductivity"/>
    <field labelOnTop="0" name="hydraulic_conductivity_file"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="impervious_layer_elevation"/>
    <field labelOnTop="0" name="interflow_type"/>
    <field labelOnTop="0" name="porosity"/>
    <field labelOnTop="0" name="porosity_file"/>
    <field labelOnTop="0" name="porosity_layer_thickness"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
