<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" simplifyDrawingTol="1" version="3.4.5-Madeira" simplifyAlgorithm="0" simplifyMaxScale="1" maxScale="0" labelsEnabled="0" simplifyDrawingHints="0" simplifyLocal="1" styleCategories="AllStyleCategories" minScale="1e+08" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" type="singleSymbol" forceraster="0" symbollevels="0">
    <symbols>
      <symbol clip_to_extent="1" force_rhr="0" type="marker" alpha="1" name="0">
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="19,61,142,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="diamond"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property value="id" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Pie">
    <DiagramCategory opacity="1" lineSizeType="MM" backgroundColor="#ffffff" penColor="#000000" barWidth="5" sizeType="MM" penAlpha="255" minScaleDenominator="0" scaleBasedVisibility="0" diagramOrientation="Up" lineSizeScale="3x:0,0,0,0,0,0" labelPlacementMethod="XHeight" sizeScale="3x:0,0,0,0,0,0" minimumSize="0" height="15" maxScaleDenominator="1e+08" penWidth="0" backgroundAlpha="255" width="15" enabled="0" scaleDependency="Area" rotationOffset="270">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute color="#000000" label="" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings dist="0" priority="0" linePlacementFlags="2" obstacle="0" showAll="1" placement="0" zIndex="0">
    <properties>
      <Option type="Map">
        <Option value="" type="QString" name="name"/>
        <Option name="properties"/>
        <Option value="collection" type="QString" name="type"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="reference_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="channel_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="friction_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="1" type="QString" name="1: Chèzy"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: Manning"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="bank_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
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
  </fieldConfiguration>
  <aliases>
    <alias name="" field="reference_level" index="0"/>
    <alias name="" field="definition_id" index="1"/>
    <alias name="" field="channel_id" index="2"/>
    <alias name="" field="code" index="3"/>
    <alias name="" field="friction_type" index="4"/>
    <alias name="" field="friction_value" index="5"/>
    <alias name="" field="bank_level" index="6"/>
    <alias name="" field="id" index="7"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="reference_level"/>
    <default expression="" applyOnUpdate="0" field="definition_id"/>
    <default expression="" applyOnUpdate="0" field="channel_id"/>
    <default expression="'new'" applyOnUpdate="0" field="code"/>
    <default expression="2" applyOnUpdate="0" field="friction_type"/>
    <default expression="" applyOnUpdate="0" field="friction_value"/>
    <default expression="" applyOnUpdate="0" field="bank_level"/>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="reference_level"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="definition_id"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="channel_id"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="code"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="friction_type"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="friction_value"/>
    <constraint exp_strength="2" unique_strength="0" notnull_strength="0" constraints="4" field="bank_level"/>
    <constraint exp_strength="0" unique_strength="1" notnull_strength="1" constraints="3" field="id"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="reference_level"/>
    <constraint exp="" desc="" field="definition_id"/>
    <constraint exp="" desc="" field="channel_id"/>
    <constraint exp="" desc="" field="code"/>
    <constraint exp="" desc="" field="friction_type"/>
    <constraint exp="" desc="" field="friction_value"/>
    <constraint exp="&quot;bank_level&quot;>&quot;reference_level&quot; or &quot;bank_level&quot;  is null or &quot;reference_level&quot; is null" desc="exceeds reference" field="bank_level"/>
    <constraint exp="" desc="" field="id"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column width="-1" type="field" hidden="0" name="reference_level"/>
      <column width="-1" type="field" hidden="0" name="definition_id"/>
      <column width="-1" type="field" hidden="0" name="channel_id"/>
      <column width="-1" type="field" hidden="0" name="code"/>
      <column width="-1" type="field" hidden="0" name="friction_type"/>
      <column width="-1" type="field" hidden="0" name="friction_value"/>
      <column width="-1" type="field" hidden="0" name="bank_level"/>
      <column width="-1" type="field" hidden="0" name="id"/>
      <column width="-1" type="actions" hidden="1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <editform tolerant="1">.</editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath>.</editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from PyQt4.QtGui import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer groupBox="1" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" name="General" columnCount="1">
      <attributeEditorField showLabel="1" name="id" index="7"/>
      <attributeEditorField showLabel="1" name="code" index="3"/>
      <attributeEditorField showLabel="1" name="reference_level" index="0"/>
      <attributeEditorField showLabel="1" name="bank_level" index="6"/>
      <attributeEditorField showLabel="1" name="friction_type" index="4"/>
      <attributeEditorField showLabel="1" name="friction_value" index="5"/>
      <attributeEditorField showLabel="1" name="definition_id" index="1"/>
      <attributeEditorField showLabel="1" name="channel_id" index="2"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="bank_level" editable="1"/>
    <field name="channel_id" editable="1"/>
    <field name="code" editable="1"/>
    <field name="definition_id" editable="1"/>
    <field name="friction_type" editable="1"/>
    <field name="friction_value" editable="1"/>
    <field name="id" editable="1"/>
    <field name="reference_level" editable="1"/>
    <field name="v2_cross_section_definition_code" editable="0"/>
    <field name="v2_cross_section_definition_height" editable="0"/>
    <field name="v2_cross_section_definition_shape" editable="0"/>
    <field name="v2_cross_section_definition_width" editable="0"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="bank_level"/>
    <field labelOnTop="0" name="channel_id"/>
    <field labelOnTop="0" name="code"/>
    <field labelOnTop="0" name="definition_id"/>
    <field labelOnTop="0" name="friction_type"/>
    <field labelOnTop="0" name="friction_value"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="reference_level"/>
    <field labelOnTop="0" name="v2_cross_section_definition_code"/>
    <field labelOnTop="0" name="v2_cross_section_definition_height"/>
    <field labelOnTop="0" name="v2_cross_section_definition_shape"/>
    <field labelOnTop="0" name="v2_cross_section_definition_width"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
