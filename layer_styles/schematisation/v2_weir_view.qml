<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" simplifyDrawingTol="1" version="3.4.5-Madeira" simplifyAlgorithm="0" simplifyMaxScale="1" maxScale="0" labelsEnabled="0" simplifyDrawingHints="1" simplifyLocal="1" styleCategories="AllStyleCategories" minScale="1e+08" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" type="singleSymbol" forceraster="0" symbollevels="0">
    <symbols>
      <symbol clip_to_extent="1" force_rhr="0" type="line" alpha="1" name="0">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="215,25,28,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.66"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer enabled="1" class="MarkerLine" locked="0" pass="0">
          <prop k="interval" v="3"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="0"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="MM"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="placement" v="centralpoint"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
          <symbol clip_to_extent="1" force_rhr="0" type="marker" alpha="1" name="@0@1">
            <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="255,0,0,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="triangle"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="0,0,0,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="area"/>
              <prop k="size" v="3"/>
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
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property value="weir_display_name" key="dualview/previewExpressions"/>
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
  <DiagramLayerSettings dist="0" priority="0" linePlacementFlags="2" obstacle="0" showAll="1" placement="2" zIndex="0">
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
    <field name="ROWID">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="weir_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_crest_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_crest_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="3" type="QString" name="3: broad crested"/>
              </Option>
              <Option type="Map">
                <Option value="4" type="QString" name="4: short crested"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_cross_section_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_sewerage">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_discharge_coefficient_positive">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_discharge_coefficient_negative">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_external">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_zoom_category">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="-1" type="QString" name="-1"/>
              </Option>
              <Option type="Map">
                <Option value="0" type="QString" name="0"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2"/>
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3"/>
              </Option>
              <Option type="Map">
                <Option value="4" type="QString" name="4"/>
              </Option>
              <Option type="Map">
                <Option value="5" type="QString" name="5"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_friction_type">
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
    <field name="weir_connection_node_start_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_connection_node_end_id">
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
                <Option value="1" type="QString" name="1: Rectangle"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: Circle"/>
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3: Egg"/>
              </Option>
              <Option type="Map">
                <Option value="5" type="QString" name="5: Tabulated rectangle"/>
              </Option>
              <Option type="Map">
                <Option value="6" type="QString" name="6: Tabulated trapezium"/>
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
  </fieldConfiguration>
  <aliases>
    <alias name="" field="ROWID" index="0"/>
    <alias name="id" field="weir_id" index="1"/>
    <alias name="display_name" field="weir_display_name" index="2"/>
    <alias name="code" field="weir_code" index="3"/>
    <alias name="crest_level" field="weir_crest_level" index="4"/>
    <alias name="crest_type" field="weir_crest_type" index="5"/>
    <alias name="Cross_section_definition_id" field="weir_cross_section_definition_id" index="6"/>
    <alias name="sewerage" field="weir_sewerage" index="7"/>
    <alias name="discharge_coefficient_positive" field="weir_discharge_coefficient_positive" index="8"/>
    <alias name="discharge_coefficient_negative" field="weir_discharge_coefficient_negative" index="9"/>
    <alias name="external" field="weir_external" index="10"/>
    <alias name="zoom_category" field="weir_zoom_category" index="11"/>
    <alias name="friction_value" field="weir_friction_value" index="12"/>
    <alias name="friction_type" field="weir_friction_type" index="13"/>
    <alias name="connection_node_start_id" field="weir_connection_node_start_id" index="14"/>
    <alias name="connection_node_end_id" field="weir_connection_node_end_id" index="15"/>
    <alias name="id" field="def_id" index="16"/>
    <alias name="shape" field="def_shape" index="17"/>
    <alias name="width" field="def_width" index="18"/>
    <alias name="height" field="def_height" index="19"/>
    <alias name="code" field="def_code" index="20"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="ROWID"/>
    <default expression="if(maximum(weir_id) is null,1, maximum(weir_id)+1)" applyOnUpdate="0" field="weir_id"/>
    <default expression="'new'" applyOnUpdate="0" field="weir_display_name"/>
    <default expression="'new'" applyOnUpdate="0" field="weir_code"/>
    <default expression="" applyOnUpdate="0" field="weir_crest_level"/>
    <default expression="4" applyOnUpdate="0" field="weir_crest_type"/>
    <default expression="" applyOnUpdate="0" field="weir_cross_section_definition_id"/>
    <default expression="" applyOnUpdate="0" field="weir_sewerage"/>
    <default expression="0.8" applyOnUpdate="0" field="weir_discharge_coefficient_positive"/>
    <default expression="0.8" applyOnUpdate="0" field="weir_discharge_coefficient_negative"/>
    <default expression="1" applyOnUpdate="0" field="weir_external"/>
    <default expression="2" applyOnUpdate="0" field="weir_zoom_category"/>
    <default expression="0.02" applyOnUpdate="0" field="weir_friction_value"/>
    <default expression="2" applyOnUpdate="0" field="weir_friction_type"/>
    <default expression="'filled automatically'" applyOnUpdate="0" field="weir_connection_node_start_id"/>
    <default expression="'filled automatically'" applyOnUpdate="0" field="weir_connection_node_end_id"/>
    <default expression="" applyOnUpdate="0" field="def_id"/>
    <default expression="" applyOnUpdate="0" field="def_shape"/>
    <default expression="" applyOnUpdate="0" field="def_width"/>
    <default expression="" applyOnUpdate="0" field="def_height"/>
    <default expression="" applyOnUpdate="0" field="def_code"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="ROWID"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="weir_id"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="weir_display_name"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="weir_code"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="weir_crest_level"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="weir_crest_type"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="weir_cross_section_definition_id"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="weir_sewerage"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="weir_discharge_coefficient_positive"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="weir_discharge_coefficient_negative"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="weir_external"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="weir_zoom_category"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="weir_friction_value"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="weir_friction_type"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="weir_connection_node_start_id"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="weir_connection_node_end_id"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="def_id"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="def_shape"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="def_width"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="def_height"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="def_code"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="ROWID"/>
    <constraint exp="" desc="" field="weir_id"/>
    <constraint exp="" desc="" field="weir_display_name"/>
    <constraint exp="" desc="" field="weir_code"/>
    <constraint exp="" desc="" field="weir_crest_level"/>
    <constraint exp="" desc="" field="weir_crest_type"/>
    <constraint exp="" desc="" field="weir_cross_section_definition_id"/>
    <constraint exp="" desc="" field="weir_sewerage"/>
    <constraint exp="" desc="" field="weir_discharge_coefficient_positive"/>
    <constraint exp="" desc="" field="weir_discharge_coefficient_negative"/>
    <constraint exp="" desc="" field="weir_external"/>
    <constraint exp="" desc="" field="weir_zoom_category"/>
    <constraint exp="" desc="" field="weir_friction_value"/>
    <constraint exp="" desc="" field="weir_friction_type"/>
    <constraint exp="" desc="" field="weir_connection_node_start_id"/>
    <constraint exp="" desc="" field="weir_connection_node_end_id"/>
    <constraint exp="" desc="" field="def_id"/>
    <constraint exp="" desc="" field="def_shape"/>
    <constraint exp="" desc="" field="def_width"/>
    <constraint exp="" desc="" field="def_height"/>
    <constraint exp="" desc="" field="def_code"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column width="-1" type="field" hidden="0" name="ROWID"/>
      <column width="-1" type="field" hidden="0" name="weir_id"/>
      <column width="-1" type="field" hidden="0" name="weir_display_name"/>
      <column width="-1" type="field" hidden="0" name="weir_code"/>
      <column width="-1" type="field" hidden="0" name="weir_crest_level"/>
      <column width="-1" type="field" hidden="0" name="weir_crest_type"/>
      <column width="185" type="field" hidden="0" name="weir_cross_section_definition_id"/>
      <column width="-1" type="field" hidden="0" name="weir_sewerage"/>
      <column width="-1" type="field" hidden="0" name="weir_discharge_coefficient_positive"/>
      <column width="-1" type="field" hidden="0" name="weir_discharge_coefficient_negative"/>
      <column width="-1" type="field" hidden="0" name="weir_external"/>
      <column width="-1" type="field" hidden="0" name="weir_zoom_category"/>
      <column width="-1" type="field" hidden="0" name="weir_friction_value"/>
      <column width="-1" type="field" hidden="0" name="weir_friction_type"/>
      <column width="-1" type="field" hidden="0" name="weir_connection_node_start_id"/>
      <column width="-1" type="field" hidden="0" name="weir_connection_node_end_id"/>
      <column width="-1" type="field" hidden="0" name="def_id"/>
      <column width="-1" type="field" hidden="0" name="def_shape"/>
      <column width="-1" type="field" hidden="0" name="def_width"/>
      <column width="-1" type="field" hidden="0" name="def_height"/>
      <column width="-1" type="field" hidden="0" name="def_code"/>
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
    <attributeEditorContainer groupBox="0" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" name="Weir view" columnCount="1">
      <attributeEditorContainer groupBox="1" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" name="General" columnCount="1">
        <attributeEditorField showLabel="1" name="weir_id" index="1"/>
        <attributeEditorField showLabel="1" name="weir_display_name" index="2"/>
        <attributeEditorField showLabel="1" name="weir_code" index="3"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" name="Characteristics" columnCount="1">
        <attributeEditorField showLabel="1" name="weir_crest_level" index="4"/>
        <attributeEditorField showLabel="1" name="weir_crest_type" index="5"/>
        <attributeEditorField showLabel="1" name="weir_discharge_coefficient_positive" index="8"/>
        <attributeEditorField showLabel="1" name="weir_discharge_coefficient_negative" index="9"/>
        <attributeEditorField showLabel="1" name="weir_friction_value" index="12"/>
        <attributeEditorField showLabel="1" name="weir_friction_type" index="13"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" name="Cross section" columnCount="1">
        <attributeEditorField showLabel="1" name="weir_cross_section_definition_id" index="6"/>
        <attributeEditorField showLabel="1" name="def_code" index="20"/>
        <attributeEditorField showLabel="1" name="def_shape" index="17"/>
        <attributeEditorField showLabel="1" name="def_width" index="18"/>
        <attributeEditorField showLabel="1" name="def_height" index="19"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" name="Visualization" columnCount="1">
        <attributeEditorField showLabel="1" name="weir_sewerage" index="7"/>
        <attributeEditorField showLabel="1" name="weir_external" index="10"/>
        <attributeEditorField showLabel="1" name="weir_zoom_category" index="11"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" name="Connection nodes" columnCount="1">
        <attributeEditorField showLabel="1" name="weir_connection_node_start_id" index="14"/>
        <attributeEditorField showLabel="1" name="weir_connection_node_end_id" index="15"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="ROWID" editable="1"/>
    <field name="def_code" editable="0"/>
    <field name="def_height" editable="0"/>
    <field name="def_id" editable="0"/>
    <field name="def_shape" editable="0"/>
    <field name="def_width" editable="0"/>
    <field name="weir_code" editable="1"/>
    <field name="weir_connection_node_end_id" editable="0"/>
    <field name="weir_connection_node_start_id" editable="0"/>
    <field name="weir_crest_level" editable="1"/>
    <field name="weir_crest_type" editable="1"/>
    <field name="weir_cross_section_definition_id" editable="1"/>
    <field name="weir_discharge_coefficient_negative" editable="1"/>
    <field name="weir_discharge_coefficient_positive" editable="1"/>
    <field name="weir_display_name" editable="1"/>
    <field name="weir_external" editable="1"/>
    <field name="weir_friction_type" editable="1"/>
    <field name="weir_friction_value" editable="1"/>
    <field name="weir_id" editable="1"/>
    <field name="weir_sewerage" editable="1"/>
    <field name="weir_zoom_category" editable="1"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="ROWID"/>
    <field labelOnTop="0" name="def_code"/>
    <field labelOnTop="0" name="def_height"/>
    <field labelOnTop="0" name="def_id"/>
    <field labelOnTop="0" name="def_shape"/>
    <field labelOnTop="0" name="def_width"/>
    <field labelOnTop="0" name="weir_code"/>
    <field labelOnTop="0" name="weir_connection_node_end_id"/>
    <field labelOnTop="0" name="weir_connection_node_start_id"/>
    <field labelOnTop="0" name="weir_crest_level"/>
    <field labelOnTop="0" name="weir_crest_type"/>
    <field labelOnTop="0" name="weir_cross_section_definition_id"/>
    <field labelOnTop="0" name="weir_discharge_coefficient_negative"/>
    <field labelOnTop="0" name="weir_discharge_coefficient_positive"/>
    <field labelOnTop="0" name="weir_display_name"/>
    <field labelOnTop="0" name="weir_external"/>
    <field labelOnTop="0" name="weir_friction_type"/>
    <field labelOnTop="0" name="weir_friction_value"/>
    <field labelOnTop="0" name="weir_id"/>
    <field labelOnTop="0" name="weir_sewerage"/>
    <field labelOnTop="0" name="weir_zoom_category"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>weir_display_name</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
