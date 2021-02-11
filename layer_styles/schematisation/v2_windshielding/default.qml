<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" version="3.4.5-Madeira" minScale="1e+08" maxScale="0" readOnly="0" hasScaleBasedVisibilityFlag="0">
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
    <field name="channel_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="north">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="northeast">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="east">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="southeast">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="south">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="southwest">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="west">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="northwest">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="the_geom">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="id" index="0" name=""/>
    <alias field="channel_id" index="1" name=""/>
    <alias field="north" index="2" name=""/>
    <alias field="northeast" index="3" name=""/>
    <alias field="east" index="4" name=""/>
    <alias field="southeast" index="5" name=""/>
    <alias field="south" index="6" name=""/>
    <alias field="southwest" index="7" name=""/>
    <alias field="west" index="8" name=""/>
    <alias field="northwest" index="9" name=""/>
    <alias field="the_geom" index="10" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
    <default expression="" applyOnUpdate="0" field="channel_id"/>
    <default expression="" applyOnUpdate="0" field="north"/>
    <default expression="" applyOnUpdate="0" field="northeast"/>
    <default expression="" applyOnUpdate="0" field="east"/>
    <default expression="" applyOnUpdate="0" field="southeast"/>
    <default expression="" applyOnUpdate="0" field="south"/>
    <default expression="" applyOnUpdate="0" field="southwest"/>
    <default expression="" applyOnUpdate="0" field="west"/>
    <default expression="" applyOnUpdate="0" field="northwest"/>
    <default expression="" applyOnUpdate="0" field="the_geom"/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" constraints="3" notnull_strength="1" field="id" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="channel_id" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="north" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="northeast" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="east" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="southeast" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="south" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="southwest" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="west" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="northwest" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" notnull_strength="0" field="the_geom" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="id" exp=""/>
    <constraint desc="" field="channel_id" exp=""/>
    <constraint desc="" field="north" exp=""/>
    <constraint desc="" field="northeast" exp=""/>
    <constraint desc="" field="east" exp=""/>
    <constraint desc="" field="southeast" exp=""/>
    <constraint desc="" field="south" exp=""/>
    <constraint desc="" field="southwest" exp=""/>
    <constraint desc="" field="west" exp=""/>
    <constraint desc="" field="northwest" exp=""/>
    <constraint desc="" field="the_geom" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column width="-1" hidden="0" type="field" name="id"/>
      <column width="-1" hidden="0" type="field" name="channel_id"/>
      <column width="-1" hidden="0" type="field" name="north"/>
      <column width="-1" hidden="0" type="field" name="northeast"/>
      <column width="-1" hidden="0" type="field" name="east"/>
      <column width="-1" hidden="0" type="field" name="southeast"/>
      <column width="-1" hidden="0" type="field" name="south"/>
      <column width="-1" hidden="0" type="field" name="southwest"/>
      <column width="-1" hidden="0" type="field" name="west"/>
      <column width="-1" hidden="0" type="field" name="northwest"/>
      <column width="-1" hidden="0" type="field" name="the_geom"/>
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
      <attributeEditorField index="1" name="channel_id" showLabel="1"/>
      <attributeEditorField index="2" name="north" showLabel="1"/>
      <attributeEditorField index="3" name="northeast" showLabel="1"/>
      <attributeEditorField index="4" name="east" showLabel="1"/>
      <attributeEditorField index="5" name="southeast" showLabel="1"/>
      <attributeEditorField index="6" name="south" showLabel="1"/>
      <attributeEditorField index="7" name="southwest" showLabel="1"/>
      <attributeEditorField index="8" name="west" showLabel="1"/>
      <attributeEditorField index="9" name="northwest" showLabel="1"/>
      <attributeEditorField index="10" name="the_geom" showLabel="1"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="channel_id"/>
    <field editable="1" name="east"/>
    <field editable="1" name="id"/>
    <field editable="1" name="north"/>
    <field editable="1" name="northeast"/>
    <field editable="1" name="northwest"/>
    <field editable="1" name="south"/>
    <field editable="1" name="southeast"/>
    <field editable="1" name="southwest"/>
    <field editable="1" name="the_geom"/>
    <field editable="1" name="west"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="channel_id"/>
    <field labelOnTop="0" name="east"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="north"/>
    <field labelOnTop="0" name="northeast"/>
    <field labelOnTop="0" name="northwest"/>
    <field labelOnTop="0" name="south"/>
    <field labelOnTop="0" name="southeast"/>
    <field labelOnTop="0" name="southwest"/>
    <field labelOnTop="0" name="the_geom"/>
    <field labelOnTop="0" name="west"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
