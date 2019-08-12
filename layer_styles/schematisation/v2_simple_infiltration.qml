<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" version="3.4.5-Madeira" maxScale="0" styleCategories="AllStyleCategories" minScale="1e+08" hasScaleBasedVisibilityFlag="0">
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
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_rate">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_rate_file">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_surface_option">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="max_infiltration_capacity_file">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="id" index="0"/>
    <alias name="" field="infiltration_rate" index="1"/>
    <alias name="" field="infiltration_rate_file" index="2"/>
    <alias name="" field="infiltration_surface_option" index="3"/>
    <alias name="" field="max_infiltration_capacity_file" index="4"/>
    <alias name="" field="display_name" index="5"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="if(maximum(id) is null,1,maximum(id)+1)" applyOnUpdate="0" field="id"/>
    <default expression="0" applyOnUpdate="0" field="infiltration_rate"/>
    <default expression="" applyOnUpdate="0" field="infiltration_rate_file"/>
    <default expression="" applyOnUpdate="0" field="infiltration_surface_option"/>
    <default expression="" applyOnUpdate="0" field="max_infiltration_capacity_file"/>
    <default expression="'new'" applyOnUpdate="0" field="display_name"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" unique_strength="1" notnull_strength="1" constraints="3" field="id"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="infiltration_rate"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="infiltration_rate_file"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="infiltration_surface_option"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="max_infiltration_capacity_file"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="display_name"/>
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
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column width="-1" type="field" hidden="0" name="id"/>
      <column width="-1" type="field" hidden="0" name="infiltration_rate"/>
      <column width="-1" type="field" hidden="0" name="infiltration_rate_file"/>
      <column width="-1" type="field" hidden="0" name="infiltration_surface_option"/>
      <column width="-1" type="field" hidden="0" name="max_infiltration_capacity_file"/>
      <column width="-1" type="field" hidden="0" name="display_name"/>
      <column width="-1" type="actions" hidden="1"/>
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
    <attributeEditorContainer groupBox="0" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" name="General" columnCount="1">
      <attributeEditorField showLabel="1" name="id" index="0"/>
      <attributeEditorField showLabel="1" name="display_name" index="5"/>
      <attributeEditorField showLabel="1" name="infiltration_rate" index="1"/>
      <attributeEditorField showLabel="1" name="infiltration_rate_file" index="2"/>
      <attributeEditorField showLabel="1" name="max_infiltration_capacity_file" index="4"/>
      <attributeEditorField showLabel="1" name="infiltration_surface_option" index="3"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="display_name" editable="1"/>
    <field name="id" editable="1"/>
    <field name="infiltration_rate" editable="1"/>
    <field name="infiltration_rate_file" editable="1"/>
    <field name="infiltration_surface_option" editable="1"/>
    <field name="max_infiltration_capacity_file" editable="1"/>
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
