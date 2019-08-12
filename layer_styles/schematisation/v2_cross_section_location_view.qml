<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyDrawingHints="0" simplifyMaxScale="1" styleCategories="AllStyleCategories" simplifyLocal="1" minScale="1e+08" simplifyAlgorithm="0" readOnly="0" maxScale="0" labelsEnabled="0" version="3.4.5-Madeira" hasScaleBasedVisibilityFlag="0" simplifyDrawingTol="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" symbollevels="0" type="singleSymbol" enableorderby="0">
    <symbols>
      <symbol name="0" force_rhr="0" alpha="1" type="marker" clip_to_extent="1">
        <layer class="SimpleMarker" enabled="1" locked="0" pass="0">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="dualview/previewExpressions" value="id"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory diagramOrientation="Up" barWidth="5" penAlpha="255" rotationOffset="270" penWidth="0" labelPlacementMethod="XHeight" lineSizeType="MM" height="15" opacity="1" minimumSize="0" backgroundColor="#ffffff" enabled="0" width="15" lineSizeScale="3x:0,0,0,0,0,0" minScaleDenominator="0" sizeScale="3x:0,0,0,0,0,0" sizeType="MM" scaleBasedVisibility="0" backgroundAlpha="255" penColor="#000000" scaleDependency="Area" maxScaleDenominator="1e+08">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" color="#000000" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings obstacle="0" showAll="1" placement="0" dist="0" linePlacementFlags="18" priority="0" zIndex="0">
    <properties>
      <Option type="Map">
        <Option name="name" type="QString" value=""/>
        <Option name="properties"/>
        <Option name="type" type="QString" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="ROWID">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="loc_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_reference_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_bank_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_friction_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="1: Chèzy" type="QString" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="2: Manning" type="QString" value="2"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_channel_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_shape">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="1: rectangle" type="QString" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="2: round" type="QString" value="2"/>
              </Option>
              <Option type="Map">
                <Option name="3: egg" type="QString" value="3"/>
              </Option>
              <Option type="Map">
                <Option name="5: tabulated rectangle" type="QString" value="5"/>
              </Option>
              <Option type="Map">
                <Option name="6: tabulated trapezium" type="QString" value="6"/>
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
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_height">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="ROWID" index="0"/>
    <alias name="id" field="loc_id" index="1"/>
    <alias name="code" field="loc_code" index="2"/>
    <alias name="" field="loc_reference_level" index="3"/>
    <alias name="" field="loc_bank_level" index="4"/>
    <alias name="" field="loc_friction_type" index="5"/>
    <alias name="" field="loc_friction_value" index="6"/>
    <alias name="" field="loc_definition_id" index="7"/>
    <alias name="" field="loc_channel_id" index="8"/>
    <alias name="" field="def_id" index="9"/>
    <alias name="" field="def_shape" index="10"/>
    <alias name="" field="def_width" index="11"/>
    <alias name="" field="def_code" index="12"/>
    <alias name="" field="def_height" index="13"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" field="ROWID" applyOnUpdate="0"/>
    <default expression="if(maximum(loc_id) is null,1,maximum(loc_id)+1)" field="loc_id" applyOnUpdate="0"/>
    <default expression="'new'" field="loc_code" applyOnUpdate="0"/>
    <default expression="" field="loc_reference_level" applyOnUpdate="0"/>
    <default expression="" field="loc_bank_level" applyOnUpdate="0"/>
    <default expression="2" field="loc_friction_type" applyOnUpdate="0"/>
    <default expression="" field="loc_friction_value" applyOnUpdate="0"/>
    <default expression="" field="loc_definition_id" applyOnUpdate="0"/>
    <default expression="'filled automatically'" field="loc_channel_id" applyOnUpdate="0"/>
    <default expression="" field="def_id" applyOnUpdate="0"/>
    <default expression="" field="def_shape" applyOnUpdate="0"/>
    <default expression="" field="def_width" applyOnUpdate="0"/>
    <default expression="" field="def_code" applyOnUpdate="0"/>
    <default expression="" field="def_height" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" field="ROWID" unique_strength="0"/>
    <constraint notnull_strength="2" exp_strength="0" constraints="1" field="loc_id" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" field="loc_code" unique_strength="0"/>
    <constraint notnull_strength="2" exp_strength="0" constraints="1" field="loc_reference_level" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" field="loc_bank_level" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" field="loc_friction_type" unique_strength="0"/>
    <constraint notnull_strength="2" exp_strength="0" constraints="1" field="loc_friction_value" unique_strength="0"/>
    <constraint notnull_strength="2" exp_strength="0" constraints="1" field="loc_definition_id" unique_strength="0"/>
    <constraint notnull_strength="2" exp_strength="0" constraints="1" field="loc_channel_id" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" field="def_id" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" field="def_shape" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" field="def_width" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" field="def_code" unique_strength="0"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" field="def_height" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="ROWID"/>
    <constraint exp="" desc="" field="loc_id"/>
    <constraint exp="" desc="" field="loc_code"/>
    <constraint exp="" desc="" field="loc_reference_level"/>
    <constraint exp="" desc="" field="loc_bank_level"/>
    <constraint exp="" desc="" field="loc_friction_type"/>
    <constraint exp="" desc="" field="loc_friction_value"/>
    <constraint exp="" desc="" field="loc_definition_id"/>
    <constraint exp="" desc="" field="loc_channel_id"/>
    <constraint exp="" desc="" field="def_id"/>
    <constraint exp="" desc="" field="def_shape"/>
    <constraint exp="" desc="" field="def_width"/>
    <constraint exp="" desc="" field="def_code"/>
    <constraint exp="" desc="" field="def_height"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column type="actions" hidden="1" width="-1"/>
      <column name="def_id" type="field" hidden="0" width="-1"/>
      <column name="def_shape" type="field" hidden="0" width="-1"/>
      <column name="def_width" type="field" hidden="0" width="-1"/>
      <column name="def_code" type="field" hidden="0" width="-1"/>
      <column name="def_height" type="field" hidden="0" width="-1"/>
      <column name="ROWID" type="field" hidden="0" width="-1"/>
      <column name="loc_id" type="field" hidden="0" width="-1"/>
      <column name="loc_code" type="field" hidden="0" width="-1"/>
      <column name="loc_reference_level" type="field" hidden="0" width="-1"/>
      <column name="loc_bank_level" type="field" hidden="0" width="-1"/>
      <column name="loc_friction_type" type="field" hidden="0" width="-1"/>
      <column name="loc_friction_value" type="field" hidden="0" width="-1"/>
      <column name="loc_definition_id" type="field" hidden="0" width="-1"/>
      <column name="loc_channel_id" type="field" hidden="0" width="-1"/>
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
    <attributeEditorContainer groupBox="0" name="Cross section location view" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" columnCount="1">
      <attributeEditorContainer groupBox="1" name="General" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" columnCount="1">
        <attributeEditorField name="loc_id" showLabel="1" index="1"/>
        <attributeEditorField name="loc_code" showLabel="1" index="2"/>
        <attributeEditorField name="loc_reference_level" showLabel="1" index="3"/>
        <attributeEditorField name="loc_bank_level" showLabel="1" index="4"/>
        <attributeEditorField name="loc_friction_type" showLabel="1" index="5"/>
        <attributeEditorField name="loc_friction_value" showLabel="1" index="6"/>
        <attributeEditorField name="loc_channel_id" showLabel="1" index="8"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" name="Cross section" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" columnCount="1">
        <attributeEditorField name="definition_id" showLabel="1" index="-1"/>
        <attributeEditorField name="def_code" showLabel="1" index="12"/>
        <attributeEditorField name="def_shape" showLabel="1" index="10"/>
        <attributeEditorField name="def_width" showLabel="1" index="11"/>
        <attributeEditorField name="def_height" showLabel="1" index="13"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="ROWID"/>
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
    <field editable="1" name="loc_bank_level"/>
    <field editable="1" name="loc_channel_id"/>
    <field editable="1" name="loc_code"/>
    <field editable="1" name="loc_definition_id"/>
    <field editable="1" name="loc_friction_type"/>
    <field editable="1" name="loc_friction_value"/>
    <field editable="1" name="loc_id"/>
    <field editable="1" name="loc_reference_level"/>
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
    <field labelOnTop="0" name="ROWID"/>
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
    <field labelOnTop="0" name="loc_bank_level"/>
    <field labelOnTop="0" name="loc_channel_id"/>
    <field labelOnTop="0" name="loc_code"/>
    <field labelOnTop="0" name="loc_definition_id"/>
    <field labelOnTop="0" name="loc_friction_type"/>
    <field labelOnTop="0" name="loc_friction_value"/>
    <field labelOnTop="0" name="loc_id"/>
    <field labelOnTop="0" name="loc_reference_level"/>
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
