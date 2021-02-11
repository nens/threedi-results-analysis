<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" version="3.4.5-Madeira" minScale="1e+08" maxScale="0" readOnly="0" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property key="dualview/previewExpressions" value="width"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="width">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="shape">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" value="1" name="1: rectangle"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="2" name="2: round"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="3" name="3: egg"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="5" name="5: tabulated rectangle"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="6" name="6: tabulated trapezium"/>
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
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
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
    <field name="height">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="width" index="0" name=""/>
    <alias field="shape" index="1" name=""/>
    <alias field="code" index="2" name=""/>
    <alias field="id" index="3" name=""/>
    <alias field="height" index="4" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="width"/>
    <default expression="" applyOnUpdate="0" field="shape"/>
    <default expression="'new'" applyOnUpdate="0" field="code"/>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
    <default expression="" applyOnUpdate="0" field="height"/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" constraints="5" notnull_strength="2" field="width" exp_strength="2"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="shape" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="code" exp_strength="0"/>
    <constraint unique_strength="1" constraints="3" notnull_strength="1" field="id" exp_strength="0"/>
    <constraint unique_strength="0" constraints="4" notnull_strength="0" field="height" exp_strength="2"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="width" exp="regexp_match(&quot;width&quot;,'^(-?\\d+(\\.\\d+)?)(\\s-?\\d+(\\.\\d+)?)*$')"/>
    <constraint desc="" field="shape" exp=""/>
    <constraint desc="" field="code" exp=""/>
    <constraint desc="" field="id" exp=""/>
    <constraint desc="" field="height" exp="regexp_match(&quot;height&quot;,'^(-?\\d+(\\.\\d+)?)(\\s-?\\d+(\\.\\d+)?)*$') or &quot;height&quot;is null"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column width="-1" hidden="0" type="field" name="width"/>
      <column width="-1" hidden="0" type="field" name="shape"/>
      <column width="-1" hidden="0" type="field" name="code"/>
      <column width="-1" hidden="0" type="field" name="id"/>
      <column width="-1" hidden="0" type="field" name="height"/>
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
      <attributeEditorField index="3" name="id" showLabel="1"/>
      <attributeEditorField index="2" name="code" showLabel="1"/>
      <attributeEditorField index="1" name="shape" showLabel="1"/>
      <attributeEditorField index="0" name="width" showLabel="1"/>
      <attributeEditorField index="4" name="height" showLabel="1"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="code"/>
    <field editable="1" name="height"/>
    <field editable="1" name="id"/>
    <field editable="1" name="shape"/>
    <field editable="1" name="width"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="code"/>
    <field labelOnTop="0" name="height"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="shape"/>
    <field labelOnTop="0" name="width"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>width</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
