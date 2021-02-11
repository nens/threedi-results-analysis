<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" simplifyLocal="1" labelsEnabled="0" simplifyDrawingTol="1" version="3.10.10-A Coruña" simplifyAlgorithm="0" minScale="1e+08" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" maxScale="0" simplifyDrawingHints="0" simplifyMaxScale="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" type="singleSymbol" symbollevels="0" enableorderby="0">
    <symbols>
      <symbol type="marker" clip_to_extent="1" name="0" force_rhr="0" alpha="1">
        <layer class="SimpleMarker" pass="0" enabled="1" locked="0">
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
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="if(@map_scale&lt;10000, 2,0.5)"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
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
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory width="15" diagramOrientation="Up" rotationOffset="270" penAlpha="255" labelPlacementMethod="XHeight" minScaleDenominator="0" opacity="1" sizeScale="3x:0,0,0,0,0,0" penColor="#000000" lineSizeScale="3x:0,0,0,0,0,0" enabled="0" barWidth="5" penWidth="0" scaleBasedVisibility="0" backgroundColor="#ffffff" sizeType="MM" minimumSize="0" scaleDependency="Area" maxScaleDenominator="1e+08" lineSizeType="MM" height="15" backgroundAlpha="255">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute field="" label="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings obstacle="0" priority="0" showAll="1" placement="0" zIndex="0" linePlacementFlags="18" dist="0">
    <properties>
      <Option type="Map">
        <Option type="QString" name="name" value=""/>
        <Option name="properties"/>
        <Option type="QString" name="type" value="collection"/>
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
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_reference_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_bank_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_friction_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="1: Chèzy" value="1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="2: Manning" value="2"/>
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
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_channel_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
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
                <Option type="QString" name="1: rectangle" value="1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="2: round" value="2"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="3: egg" value="3"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="5: tabulated rectangle" value="5"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="6: tabulated trapezium" value="6"/>
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
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_height">
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
    <alias name="" field="ROWID" index="0"/>
    <alias name="id" field="loc_id" index="1"/>
    <alias name="code" field="loc_code" index="2"/>
    <alias name="reference_level" field="loc_reference_level" index="3"/>
    <alias name="bank_level" field="loc_bank_level" index="4"/>
    <alias name="friction_type" field="loc_friction_type" index="5"/>
    <alias name="friction_value" field="loc_friction_value" index="6"/>
    <alias name="definition_id" field="loc_definition_id" index="7"/>
    <alias name="channel_id" field="loc_channel_id" index="8"/>
    <alias name="" field="def_id" index="9"/>
    <alias name="" field="def_shape" index="10"/>
    <alias name="" field="def_width" index="11"/>
    <alias name="" field="def_code" index="12"/>
    <alias name="" field="def_height" index="13"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="ROWID" expression=""/>
    <default applyOnUpdate="0" field="loc_id" expression="if(maximum(loc_id) is null,1,maximum(loc_id)+1)"/>
    <default applyOnUpdate="0" field="loc_code" expression="'new'"/>
    <default applyOnUpdate="0" field="loc_reference_level" expression=""/>
    <default applyOnUpdate="0" field="loc_bank_level" expression=""/>
    <default applyOnUpdate="0" field="loc_friction_type" expression="2"/>
    <default applyOnUpdate="0" field="loc_friction_value" expression=""/>
    <default applyOnUpdate="0" field="loc_definition_id" expression=""/>
    <default applyOnUpdate="0" field="loc_channel_id" expression="aggregate('v2_channel','min',&quot;id&quot;, intersects($geometry,geometry(@parent)))"/>
    <default applyOnUpdate="0" field="def_id" expression=""/>
    <default applyOnUpdate="0" field="def_shape" expression=""/>
    <default applyOnUpdate="0" field="def_width" expression=""/>
    <default applyOnUpdate="0" field="def_code" expression=""/>
    <default applyOnUpdate="0" field="def_height" expression=""/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" constraints="0" field="ROWID" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" field="loc_id" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="loc_code" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" field="loc_reference_level" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="loc_bank_level" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="loc_friction_type" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" field="loc_friction_value" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" field="loc_definition_id" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" field="loc_channel_id" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="def_id" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="def_shape" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="def_width" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="def_code" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="def_height" notnull_strength="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="ROWID" exp=""/>
    <constraint desc="" field="loc_id" exp=""/>
    <constraint desc="" field="loc_code" exp=""/>
    <constraint desc="" field="loc_reference_level" exp=""/>
    <constraint desc="" field="loc_bank_level" exp=""/>
    <constraint desc="" field="loc_friction_type" exp=""/>
    <constraint desc="" field="loc_friction_value" exp=""/>
    <constraint desc="" field="loc_definition_id" exp=""/>
    <constraint desc="" field="loc_channel_id" exp=""/>
    <constraint desc="" field="def_id" exp=""/>
    <constraint desc="" field="def_shape" exp=""/>
    <constraint desc="" field="def_width" exp=""/>
    <constraint desc="" field="def_code" exp=""/>
    <constraint desc="" field="def_height" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column type="actions" hidden="1" width="-1"/>
      <column type="field" name="def_id" hidden="0" width="-1"/>
      <column type="field" name="def_shape" hidden="0" width="-1"/>
      <column type="field" name="def_width" hidden="0" width="-1"/>
      <column type="field" name="def_code" hidden="0" width="-1"/>
      <column type="field" name="def_height" hidden="0" width="-1"/>
      <column type="field" name="ROWID" hidden="0" width="-1"/>
      <column type="field" name="loc_id" hidden="0" width="-1"/>
      <column type="field" name="loc_code" hidden="0" width="-1"/>
      <column type="field" name="loc_reference_level" hidden="0" width="-1"/>
      <column type="field" name="loc_bank_level" hidden="0" width="-1"/>
      <column type="field" name="loc_friction_type" hidden="0" width="-1"/>
      <column type="field" name="loc_friction_value" hidden="0" width="-1"/>
      <column type="field" name="loc_definition_id" hidden="0" width="-1"/>
      <column type="field" name="loc_channel_id" hidden="0" width="-1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
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
    <attributeEditorContainer groupBox="0" visibilityExpressionEnabled="0" showLabel="1" name="Cross section location view" visibilityExpression="" columnCount="1">
      <attributeEditorContainer groupBox="1" visibilityExpressionEnabled="0" showLabel="1" name="General" visibilityExpression="" columnCount="1">
        <attributeEditorField showLabel="1" name="loc_id" index="1"/>
        <attributeEditorField showLabel="1" name="loc_code" index="2"/>
        <attributeEditorField showLabel="1" name="loc_reference_level" index="3"/>
        <attributeEditorField showLabel="1" name="loc_bank_level" index="4"/>
        <attributeEditorField showLabel="1" name="loc_friction_type" index="5"/>
        <attributeEditorField showLabel="1" name="loc_friction_value" index="6"/>
        <attributeEditorField showLabel="1" name="loc_channel_id" index="8"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpressionEnabled="0" showLabel="1" name="Cross section" visibilityExpression="" columnCount="1">
        <attributeEditorField showLabel="1" name="loc_definition_id" index="7"/>
        <attributeEditorField showLabel="1" name="def_code" index="12"/>
        <attributeEditorField showLabel="1" name="def_shape" index="10"/>
        <attributeEditorField showLabel="1" name="def_width" index="11"/>
        <attributeEditorField showLabel="1" name="def_height" index="13"/>
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
    <field name="ROWID" labelOnTop="0"/>
    <field name="bank_level" labelOnTop="0"/>
    <field name="channel_id" labelOnTop="0"/>
    <field name="code" labelOnTop="0"/>
    <field name="def_code" labelOnTop="0"/>
    <field name="def_height" labelOnTop="0"/>
    <field name="def_id" labelOnTop="0"/>
    <field name="def_shape" labelOnTop="0"/>
    <field name="def_width" labelOnTop="0"/>
    <field name="definition_id" labelOnTop="0"/>
    <field name="friction_type" labelOnTop="0"/>
    <field name="friction_value" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="loc_bank_level" labelOnTop="0"/>
    <field name="loc_channel_id" labelOnTop="0"/>
    <field name="loc_code" labelOnTop="0"/>
    <field name="loc_definition_id" labelOnTop="0"/>
    <field name="loc_friction_type" labelOnTop="0"/>
    <field name="loc_friction_value" labelOnTop="0"/>
    <field name="loc_id" labelOnTop="0"/>
    <field name="loc_reference_level" labelOnTop="0"/>
    <field name="location_bank_level" labelOnTop="0"/>
    <field name="location_channel_id" labelOnTop="0"/>
    <field name="location_code" labelOnTop="0"/>
    <field name="location_definition_id" labelOnTop="0"/>
    <field name="location_friction_type" labelOnTop="0"/>
    <field name="location_friction_value" labelOnTop="0"/>
    <field name="location_id" labelOnTop="0"/>
    <field name="location_reference_level" labelOnTop="0"/>
    <field name="reference_level" labelOnTop="0"/>
    <field name="v2_cross_section_definition_code" labelOnTop="0"/>
    <field name="v2_cross_section_definition_height" labelOnTop="0"/>
    <field name="v2_cross_section_definition_shape" labelOnTop="0"/>
    <field name="v2_cross_section_definition_width" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>location_id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
