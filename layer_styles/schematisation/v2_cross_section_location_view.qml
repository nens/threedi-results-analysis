<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.4.5-Madeira" simplifyDrawingTol="1" minScale="1e+08" readOnly="0" styleCategories="AllStyleCategories" maxScale="0" simplifyDrawingHints="0" simplifyLocal="1" labelsEnabled="0" simplifyAlgorithm="0" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" forceraster="0" type="singleSymbol" enableorderby="0">
    <symbols>
      <symbol alpha="1" force_rhr="0" type="marker" clip_to_extent="1" name="0">
        <layer pass="0" class="SimpleMarker" enabled="1" locked="0">
          <prop v="0" k="angle"/>
          <prop v="19,61,142,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="diamond" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="area" k="scale_method"/>
          <prop v="2" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
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
    <property key="dualview/previewExpressions">
      <value>id</value>
    </property>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory opacity="1" height="15" enabled="0" sizeType="MM" width="15" diagramOrientation="Up" minimumSize="0" penAlpha="255" lineSizeScale="3x:0,0,0,0,0,0" lineSizeType="MM" penColor="#000000" labelPlacementMethod="XHeight" scaleDependency="Area" scaleBasedVisibility="0" rotationOffset="270" maxScaleDenominator="1e+08" minScaleDenominator="0" sizeScale="3x:0,0,0,0,0,0" penWidth="0" backgroundColor="#ffffff" backgroundAlpha="255" barWidth="5">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings obstacle="0" linePlacementFlags="18" showAll="1" dist="0" zIndex="0" placement="0" priority="0">
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
    <field name="location_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="location_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="location_reference_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="location_bank_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="location_friction_type">
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
    <field name="location_friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="location_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="location_channel_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_shape">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="1" type="QString" name="1: rectangle"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: round"/>
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3: egg"/>
              </Option>
              <Option type="Map">
                <Option value="5" type="QString" name="5: tabulated rectangle"/>
              </Option>
              <Option type="Map">
                <Option value="6" type="QString" name="6: tabulated trapezium"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_width">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_height">
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
    <alias index="0" field="location_id" name="id"/>
    <alias index="1" field="location_code" name="code"/>
    <alias index="2" field="location_reference_level" name=""/>
    <alias index="3" field="location_bank_level" name="bank_level"/>
    <alias index="4" field="location_friction_type" name="friction_type"/>
    <alias index="5" field="location_friction_value" name="friction_value"/>
    <alias index="6" field="location_definition_id" name="definition_id"/>
    <alias index="7" field="location_channel_id" name="channel_id"/>
    <alias index="8" field="def_id" name=""/>
    <alias index="9" field="def_shape" name=""/>
    <alias index="10" field="def_width" name=""/>
    <alias index="11" field="def_code" name=""/>
    <alias index="12" field="def_height" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="if(maximum(location_id) is null,1,maximum(location_id)+1)" applyOnUpdate="0" field="location_id"/>
    <default expression="'new'" applyOnUpdate="0" field="location_code"/>
    <default expression="" applyOnUpdate="0" field="location_reference_level"/>
    <default expression="" applyOnUpdate="0" field="location_bank_level"/>
    <default expression="2" applyOnUpdate="0" field="location_friction_type"/>
    <default expression="" applyOnUpdate="0" field="location_friction_value"/>
    <default expression="" applyOnUpdate="0" field="location_definition_id"/>
    <default expression="'filled automatically'" applyOnUpdate="0" field="location_channel_id"/>
    <default expression="" applyOnUpdate="0" field="def_id"/>
    <default expression="" applyOnUpdate="0" field="def_shape"/>
    <default expression="" applyOnUpdate="0" field="def_width"/>
    <default expression="" applyOnUpdate="0" field="def_code"/>
    <default expression="" applyOnUpdate="0" field="def_height"/>
  </defaults>
  <constraints>
    <constraint constraints="3" notnull_strength="2" unique_strength="1" exp_strength="0" field="location_id"/>
    <constraint constraints="1" notnull_strength="2" unique_strength="0" exp_strength="0" field="location_code"/>
    <constraint constraints="1" notnull_strength="2" unique_strength="0" exp_strength="0" field="location_reference_level"/>
    <constraint constraints="4" notnull_strength="0" unique_strength="0" exp_strength="2" field="location_bank_level"/>
    <constraint constraints="1" notnull_strength="2" unique_strength="0" exp_strength="0" field="location_friction_type"/>
    <constraint constraints="1" notnull_strength="2" unique_strength="0" exp_strength="0" field="location_friction_value"/>
    <constraint constraints="1" notnull_strength="2" unique_strength="0" exp_strength="0" field="location_definition_id"/>
    <constraint constraints="1" notnull_strength="2" unique_strength="0" exp_strength="0" field="location_channel_id"/>
    <constraint constraints="0" notnull_strength="0" unique_strength="0" exp_strength="0" field="def_id"/>
    <constraint constraints="0" notnull_strength="0" unique_strength="0" exp_strength="0" field="def_shape"/>
    <constraint constraints="0" notnull_strength="0" unique_strength="0" exp_strength="0" field="def_width"/>
    <constraint constraints="0" notnull_strength="0" unique_strength="0" exp_strength="0" field="def_code"/>
    <constraint constraints="0" notnull_strength="0" unique_strength="0" exp_strength="0" field="def_height"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="location_id" desc=""/>
    <constraint exp="" field="location_code" desc=""/>
    <constraint exp="" field="location_reference_level" desc=""/>
    <constraint exp="&quot;bank_level&quot;>&quot;reference_level&quot; or &quot;bank_level&quot;  is null or &quot;reference_level&quot; is null" field="location_bank_level" desc="exceeds reference"/>
    <constraint exp="" field="location_friction_type" desc=""/>
    <constraint exp="" field="location_friction_value" desc=""/>
    <constraint exp="" field="location_definition_id" desc=""/>
    <constraint exp="" field="location_channel_id" desc=""/>
    <constraint exp="" field="def_id" desc=""/>
    <constraint exp="" field="def_shape" desc=""/>
    <constraint exp="" field="def_width" desc=""/>
    <constraint exp="" field="def_code" desc=""/>
    <constraint exp="" field="def_height" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column hidden="1" type="actions" width="-1"/>
      <column hidden="0" type="field" width="-1" name="location_id"/>
      <column hidden="0" type="field" width="-1" name="location_code"/>
      <column hidden="0" type="field" width="-1" name="location_reference_level"/>
      <column hidden="0" type="field" width="-1" name="location_bank_level"/>
      <column hidden="0" type="field" width="-1" name="location_friction_type"/>
      <column hidden="0" type="field" width="-1" name="location_friction_value"/>
      <column hidden="0" type="field" width="-1" name="location_definition_id"/>
      <column hidden="0" type="field" width="-1" name="location_channel_id"/>
      <column hidden="0" type="field" width="-1" name="def_id"/>
      <column hidden="0" type="field" width="-1" name="def_shape"/>
      <column hidden="0" type="field" width="-1" name="def_width"/>
      <column hidden="0" type="field" width="-1" name="def_code"/>
      <column hidden="0" type="field" width="-1" name="def_height"/>
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
    <attributeEditorContainer columnCount="1" visibilityExpression="" groupBox="0" showLabel="1" name="Cross section location view" visibilityExpressionEnabled="0">
      <attributeEditorContainer columnCount="1" visibilityExpression="" groupBox="1" showLabel="1" name="General" visibilityExpressionEnabled="0">
        <attributeEditorField index="0" showLabel="1" name="location_id"/>
        <attributeEditorField index="1" showLabel="1" name="location_code"/>
        <attributeEditorField index="2" showLabel="1" name="location_reference_level"/>
        <attributeEditorField index="3" showLabel="1" name="location_bank_level"/>
        <attributeEditorField index="4" showLabel="1" name="location_friction_type"/>
        <attributeEditorField index="5" showLabel="1" name="location_friction_value"/>
        <attributeEditorField index="7" showLabel="1" name="location_channel_id"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" visibilityExpression="" groupBox="1" showLabel="1" name="Cross section" visibilityExpressionEnabled="0">
        <attributeEditorField index="6" showLabel="1" name="definition_id"/>
        <attributeEditorField index="11" showLabel="1" name="def_code"/>
        <attributeEditorField index="9" showLabel="1" name="def_shape"/>
        <attributeEditorField index="10" showLabel="1" name="def_width"/>
        <attributeEditorField index="12" showLabel="1" name="def_height"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="bank_level"/>
    <field editable="1" name="channel_id"/>
    <field editable="1" name="code"/>
    <field editable="0" name="def_code"/>
    <field editable="0" name="def_height"/>
    <field editable="1" name="def_id"/>
    <field editable="0" name="def_shape"/>
    <field editable="0" name="def_width"/>
    <field editable="1" name="definition_id"/>
    <field editable="1" name="friction_type"/>
    <field editable="1" name="friction_value"/>
    <field editable="1" name="id"/>
    <field editable="1" name="location_bank_level"/>
    <field editable="1" name="location_channel_id"/>
    <field editable="1" name="location_code"/>
    <field editable="1" name="location_definition_id"/>
    <field editable="1" name="location_friction_type"/>
    <field editable="1" name="location_friction_value"/>
    <field editable="1" name="location_id"/>
    <field editable="1" name="location_reference_level"/>
    <field editable="1" name="reference_level"/>
    <field editable="0" name="v2_cross_section_definition_code"/>
    <field editable="0" name="v2_cross_section_definition_height"/>
    <field editable="0" name="v2_cross_section_definition_shape"/>
    <field editable="0" name="v2_cross_section_definition_width"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="bank_level"/>
    <field labelOnTop="0" name="channel_id"/>
    <field labelOnTop="0" name="code"/>
    <field labelOnTop="0" name="def_code"/>
    <field labelOnTop="0" name="def_height"/>
    <field labelOnTop="0" name="def_id"/>
    <field labelOnTop="0" name="def_shape"/>
    <field labelOnTop="0" name="def_width"/>
    <field labelOnTop="0" name="definition_id"/>
    <field labelOnTop="0" name="friction_type"/>
    <field labelOnTop="0" name="friction_value"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="location_bank_level"/>
    <field labelOnTop="0" name="location_channel_id"/>
    <field labelOnTop="0" name="location_code"/>
    <field labelOnTop="0" name="location_definition_id"/>
    <field labelOnTop="0" name="location_friction_type"/>
    <field labelOnTop="0" name="location_friction_value"/>
    <field labelOnTop="0" name="location_id"/>
    <field labelOnTop="0" name="location_reference_level"/>
    <field labelOnTop="0" name="reference_level"/>
    <field labelOnTop="0" name="v2_cross_section_definition_code"/>
    <field labelOnTop="0" name="v2_cross_section_definition_height"/>
    <field labelOnTop="0" name="v2_cross_section_definition_shape"/>
    <field labelOnTop="0" name="v2_cross_section_definition_width"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>location_id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
