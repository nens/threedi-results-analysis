<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" version="3.4.5-Madeira" labelsEnabled="0" simplifyDrawingHints="1" simplifyDrawingTol="1" simplifyLocal="1" minScale="1e+08" maxScale="0" simplifyMaxScale="1" readOnly="0" hasScaleBasedVisibilityFlag="0" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" type="singleSymbol" symbollevels="0" forceraster="0">
    <symbols>
      <symbol clip_to_extent="1" force_rhr="0" type="fill" name="0" alpha="1">
        <layer enabled="1" pass="0" locked="0" class="SimpleFill">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="121,191,130,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="17,94,46,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.46"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="dense5"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>0.7</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory labelPlacementMethod="XHeight" scaleBasedVisibility="0" opacity="1" penColor="#000000" lineSizeScale="3x:0,0,0,0,0,0" minimumSize="0" backgroundColor="#ffffff" width="15" sizeType="MM" scaleDependency="Area" penAlpha="255" sizeScale="3x:0,0,0,0,0,0" diagramOrientation="Up" height="15" minScaleDenominator="0" penWidth="0" lineSizeType="MM" rotationOffset="270" enabled="0" barWidth="5" maxScaleDenominator="1e+08" backgroundAlpha="255">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute label="" color="#000000" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings placement="0" linePlacementFlags="2" showAll="1" dist="0" priority="0" obstacle="0" zIndex="0">
    <properties>
      <Option type="Map">
        <Option type="QString" value="" name="name"/>
        <Option name="properties"/>
        <Option type="QString" value="collection" name="type"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
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
    <field name="refinement_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
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
  </fieldConfiguration>
  <aliases>
    <alias field="id" index="0" name=""/>
    <alias field="display_name" index="1" name=""/>
    <alias field="refinement_level" index="2" name=""/>
    <alias field="code" index="3" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
    <default expression="'new'" applyOnUpdate="0" field="display_name"/>
    <default expression="1" applyOnUpdate="0" field="refinement_level"/>
    <default expression="'new'" applyOnUpdate="0" field="code"/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" constraints="3" notnull_strength="1" field="id" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="display_name" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="refinement_level" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="code" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="id" exp=""/>
    <constraint desc="" field="display_name" exp=""/>
    <constraint desc="" field="refinement_level" exp=""/>
    <constraint desc="" field="code" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column width="-1" hidden="0" type="field" name="id"/>
      <column width="-1" hidden="0" type="field" name="display_name"/>
      <column width="-1" hidden="0" type="field" name="refinement_level"/>
      <column width="-1" hidden="0" type="field" name="code"/>
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
      <attributeEditorField index="1" name="display_name" showLabel="1"/>
      <attributeEditorField index="3" name="code" showLabel="1"/>
      <attributeEditorField index="2" name="refinement_level" showLabel="1"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="code"/>
    <field editable="1" name="display_name"/>
    <field editable="1" name="id"/>
    <field editable="1" name="refinement_level"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="code"/>
    <field labelOnTop="0" name="display_name"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="refinement_level"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>display_name</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
