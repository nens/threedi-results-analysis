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
    <field name="interflow_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" value="0" name="No interflow"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="1" name="porosity rescaled to lowest pixel per cell"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="2" name="porosity rescaled to lowest pixel in whole model"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="3" name="porosity constant over entire model, interflow depends on impervious layer elevation below lowest pixel in cell"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="4" name="porosity constant over entire model, interflow depends on impervious layer elevation below lowest pixel in model"/>
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
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="id" index="0" name=""/>
    <alias field="interflow_type" index="1" name=""/>
    <alias field="porosity" index="2" name=""/>
    <alias field="porosity_file" index="3" name=""/>
    <alias field="porosity_layer_thickness" index="4" name=""/>
    <alias field="impervious_layer_elevation" index="5" name=""/>
    <alias field="hydraulic_conductivity" index="6" name=""/>
    <alias field="hydraulic_conductivity_file" index="7" name=""/>
    <alias field="display_name" index="8" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
    <default expression="" applyOnUpdate="0" field="interflow_type"/>
    <default expression="" applyOnUpdate="0" field="porosity"/>
    <default expression="" applyOnUpdate="0" field="porosity_file"/>
    <default expression="" applyOnUpdate="0" field="porosity_layer_thickness"/>
    <default expression="" applyOnUpdate="0" field="impervious_layer_elevation"/>
    <default expression="" applyOnUpdate="0" field="hydraulic_conductivity"/>
    <default expression="" applyOnUpdate="0" field="hydraulic_conductivity_file"/>
    <default expression="" applyOnUpdate="0" field="display_name"/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" constraints="3" notnull_strength="1" field="id" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="interflow_type" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="porosity" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="porosity_file" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="porosity_layer_thickness" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="impervious_layer_elevation" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="hydraulic_conductivity" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="hydraulic_conductivity_file" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="display_name" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="id" exp=""/>
    <constraint desc="" field="interflow_type" exp=""/>
    <constraint desc="" field="porosity" exp=""/>
    <constraint desc="" field="porosity_file" exp=""/>
    <constraint desc="" field="porosity_layer_thickness" exp=""/>
    <constraint desc="" field="impervious_layer_elevation" exp=""/>
    <constraint desc="" field="hydraulic_conductivity" exp=""/>
    <constraint desc="" field="hydraulic_conductivity_file" exp=""/>
    <constraint desc="" field="display_name" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column width="-1" hidden="0" type="field" name="id"/>
      <column width="-1" hidden="0" type="field" name="interflow_type"/>
      <column width="-1" hidden="0" type="field" name="porosity"/>
      <column width="-1" hidden="0" type="field" name="porosity_file"/>
      <column width="-1" hidden="0" type="field" name="porosity_layer_thickness"/>
      <column width="-1" hidden="0" type="field" name="impervious_layer_elevation"/>
      <column width="-1" hidden="0" type="field" name="hydraulic_conductivity"/>
      <column width="-1" hidden="0" type="field" name="hydraulic_conductivity_file"/>
      <column width="-1" hidden="0" type="field" name="display_name"/>
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
      <attributeEditorField index="8" name="display_name" showLabel="1"/>
      <attributeEditorField index="1" name="interflow_type" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer visibilityExpression="" visibilityExpressionEnabled="0" columnCount="1" name="Porosity" showLabel="1" groupBox="0">
      <attributeEditorField index="2" name="porosity" showLabel="1"/>
      <attributeEditorField index="3" name="porosity_file" showLabel="1"/>
      <attributeEditorField index="4" name="porosity_layer_thickness" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer visibilityExpression="" visibilityExpressionEnabled="0" columnCount="1" name="Hydraulic conductivity" showLabel="1" groupBox="0">
      <attributeEditorField index="7" name="hydraulic_conductivity_file" showLabel="1"/>
      <attributeEditorField index="6" name="hydraulic_conductivity" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer visibilityExpression="" visibilityExpressionEnabled="0" columnCount="1" name="Impervious layer" showLabel="1" groupBox="0">
      <attributeEditorField index="5" name="impervious_layer_elevation" showLabel="1"/>
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
