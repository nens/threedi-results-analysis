<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="0" readOnly="0" simplifyLocal="1" simplifyDrawingTol="1" minScale="1e+08" simplifyDrawingHints="0" simplifyAlgorithm="0" styleCategories="AllStyleCategories" simplifyMaxScale="1" version="3.4.5-Madeira" maxScale="0" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" type="singleSymbol" symbollevels="0" enableorderby="0">
    <symbols>
      <symbol name="0" type="marker" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer locked="0" class="SimpleMarker" pass="0" enabled="1">
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
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
    <DiagramCategory minimumSize="0" opacity="1" penWidth="0" scaleDependency="Area" height="15" minScaleDenominator="0" scaleBasedVisibility="0" lineSizeType="MM" penColor="#000000" rotationOffset="270" width="15" maxScaleDenominator="1e+08" enabled="0" sizeScale="3x:0,0,0,0,0,0" labelPlacementMethod="XHeight" penAlpha="255" barWidth="5" backgroundAlpha="255" diagramOrientation="Up" lineSizeScale="3x:0,0,0,0,0,0" backgroundColor="#ffffff" sizeType="MM">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute field="" color="#000000" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings placement="0" priority="0" obstacle="0" zIndex="0" dist="0" showAll="1" linePlacementFlags="18">
    <properties>
      <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
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
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_reference_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_bank_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
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
                <Option value="1" name="1: Chèzy" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2: Manning" type="QString"/>
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
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_channel_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
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
                <Option value="1" name="1: rectangle" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2: round" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="3" name="3: egg" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="5" name="5: tabulated rectangle" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="6" name="6: tabulated trapezium" type="QString"/>
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
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_height">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="ROWID" index="0" name=""/>
    <alias field="loc_id" index="1" name="id"/>
    <alias field="loc_code" index="2" name="code"/>
    <alias field="loc_reference_level" index="3" name="reference_level"/>
    <alias field="loc_bank_level" index="4" name="bank_level"/>
    <alias field="loc_friction_type" index="5" name="friction_type"/>
    <alias field="loc_friction_value" index="6" name="friction_value"/>
    <alias field="loc_definition_id" index="7" name="definition_id"/>
    <alias field="loc_channel_id" index="8" name="channel_id"/>
    <alias field="def_id" index="9" name=""/>
    <alias field="def_shape" index="10" name=""/>
    <alias field="def_width" index="11" name=""/>
    <alias field="def_code" index="12" name=""/>
    <alias field="def_height" index="13" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="ROWID" expression="" applyOnUpdate="0"/>
    <default field="loc_id" expression="if(maximum(loc_id) is null,1,maximum(loc_id)+1)" applyOnUpdate="0"/>
    <default field="loc_code" expression="'new'" applyOnUpdate="0"/>
    <default field="loc_reference_level" expression="" applyOnUpdate="0"/>
    <default field="loc_bank_level" expression="" applyOnUpdate="0"/>
    <default field="loc_friction_type" expression="2" applyOnUpdate="0"/>
    <default field="loc_friction_value" expression="" applyOnUpdate="0"/>
    <default field="loc_definition_id" expression="" applyOnUpdate="0"/>
    <default field="loc_channel_id" expression="aggregate('v2_channel','min',&quot;id&quot;, intersects($geometry,geometry(@parent)))" applyOnUpdate="0"/>
    <default field="def_id" expression="" applyOnUpdate="0"/>
    <default field="def_shape" expression="" applyOnUpdate="0"/>
    <default field="def_width" expression="" applyOnUpdate="0"/>
    <default field="def_code" expression="" applyOnUpdate="0"/>
    <default field="def_height" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="ROWID" notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="loc_id" notnull_strength="2" exp_strength="0" constraints="1" unique_strength="0"/>
    <constraint field="loc_code" notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="loc_reference_level" notnull_strength="2" exp_strength="0" constraints="1" unique_strength="0"/>
    <constraint field="loc_bank_level" notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="loc_friction_type" notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="loc_friction_value" notnull_strength="2" exp_strength="0" constraints="1" unique_strength="0"/>
    <constraint field="loc_definition_id" notnull_strength="2" exp_strength="0" constraints="1" unique_strength="0"/>
    <constraint field="loc_channel_id" notnull_strength="2" exp_strength="0" constraints="1" unique_strength="0"/>
    <constraint field="def_id" notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="def_shape" notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="def_width" notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="def_code" notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint field="def_height" notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="ROWID" desc="" exp=""/>
    <constraint field="loc_id" desc="" exp=""/>
    <constraint field="loc_code" desc="" exp=""/>
    <constraint field="loc_reference_level" desc="" exp=""/>
    <constraint field="loc_bank_level" desc="" exp=""/>
    <constraint field="loc_friction_type" desc="" exp=""/>
    <constraint field="loc_friction_value" desc="" exp=""/>
    <constraint field="loc_definition_id" desc="" exp=""/>
    <constraint field="loc_channel_id" desc="" exp=""/>
    <constraint field="def_id" desc="" exp=""/>
    <constraint field="def_shape" desc="" exp=""/>
    <constraint field="def_width" desc="" exp=""/>
    <constraint field="def_code" desc="" exp=""/>
    <constraint field="def_height" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column hidden="1" width="-1" type="actions"/>
      <column hidden="0" width="-1" name="def_id" type="field"/>
      <column hidden="0" width="-1" name="def_shape" type="field"/>
      <column hidden="0" width="-1" name="def_width" type="field"/>
      <column hidden="0" width="-1" name="def_code" type="field"/>
      <column hidden="0" width="-1" name="def_height" type="field"/>
      <column hidden="0" width="-1" name="ROWID" type="field"/>
      <column hidden="0" width="-1" name="loc_id" type="field"/>
      <column hidden="0" width="-1" name="loc_code" type="field"/>
      <column hidden="0" width="-1" name="loc_reference_level" type="field"/>
      <column hidden="0" width="-1" name="loc_bank_level" type="field"/>
      <column hidden="0" width="-1" name="loc_friction_type" type="field"/>
      <column hidden="0" width="-1" name="loc_friction_value" type="field"/>
      <column hidden="0" width="-1" name="loc_definition_id" type="field"/>
      <column hidden="0" width="-1" name="loc_channel_id" type="field"/>
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
    <attributeEditorContainer visibilityExpression="" showLabel="1" groupBox="0" name="Cross section location view" columnCount="1" visibilityExpressionEnabled="0">
      <attributeEditorContainer visibilityExpression="" showLabel="1" groupBox="1" name="General" columnCount="1" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="1" name="loc_id"/>
        <attributeEditorField showLabel="1" index="2" name="loc_code"/>
        <attributeEditorField showLabel="1" index="3" name="loc_reference_level"/>
        <attributeEditorField showLabel="1" index="4" name="loc_bank_level"/>
        <attributeEditorField showLabel="1" index="5" name="loc_friction_type"/>
        <attributeEditorField showLabel="1" index="6" name="loc_friction_value"/>
        <attributeEditorField showLabel="1" index="8" name="loc_channel_id"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" showLabel="1" groupBox="1" name="Cross section" columnCount="1" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="7" name="loc_definition_id"/>
        <attributeEditorField showLabel="1" index="12" name="def_code"/>
        <attributeEditorField showLabel="1" index="10" name="def_shape"/>
        <attributeEditorField showLabel="1" index="11" name="def_width"/>
        <attributeEditorField showLabel="1" index="13" name="def_height"/>
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
