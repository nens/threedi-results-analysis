<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" version="3.4.5-Madeira" readOnly="0" maxScale="0" minScale="1e+08" styleCategories="AllStyleCategories">
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
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_rate">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_rate_file">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_surface_option">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="max_infiltration_capacity_file">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
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
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="infiltration_rate" expression=""/>
    <default applyOnUpdate="0" field="infiltration_rate_file" expression=""/>
    <default applyOnUpdate="0" field="infiltration_surface_option" expression=""/>
    <default applyOnUpdate="0" field="max_infiltration_capacity_file" expression=""/>
    <default applyOnUpdate="0" field="display_name" expression=""/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" field="id" constraints="3" notnull_strength="1" exp_strength="0"/>
    <constraint unique_strength="0" field="infiltration_rate" constraints="1" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" field="infiltration_rate_file" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="infiltration_surface_option" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="max_infiltration_capacity_file" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="display_name" constraints="1" notnull_strength="2" exp_strength="0"/>
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
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column type="field" name="id" width="-1" hidden="0"/>
      <column type="field" name="infiltration_rate" width="-1" hidden="0"/>
      <column type="field" name="infiltration_rate_file" width="-1" hidden="0"/>
      <column type="field" name="infiltration_surface_option" width="-1" hidden="0"/>
      <column type="field" name="max_infiltration_capacity_file" width="-1" hidden="0"/>
      <column type="field" name="display_name" width="-1" hidden="0"/>
      <column type="actions" width="-1" hidden="1"/>
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
    <attributeEditorField name="id" index="0" showLabel="1"/>
    <attributeEditorField name="display_name" index="5" showLabel="1"/>
    <attributeEditorField name="infiltration_rate" index="1" showLabel="1"/>
    <attributeEditorField name="infiltration_rate_file" index="2" showLabel="1"/>
    <attributeEditorField name="infiltration_surface_option" index="3" showLabel="1"/>
    <attributeEditorField name="max_infiltration_capacity_file" index="4" showLabel="1"/>
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
    <field name="display_name" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="infiltration_rate" labelOnTop="0"/>
    <field name="infiltration_rate_file" labelOnTop="0"/>
    <field name="infiltration_surface_option" labelOnTop="0"/>
    <field name="max_infiltration_capacity_file" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
