<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.4.5-Madeira" labelsEnabled="0" styleCategories="AllStyleCategories" simplifyLocal="1" simplifyMaxScale="1" simplifyDrawingHints="1" simplifyDrawingTol="1" simplifyAlgorithm="0" hasScaleBasedVisibilityFlag="0" maxScale="0" readOnly="0" minScale="1e+08">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 type="singleSymbol" forceraster="0" symbollevels="0" enableorderby="0">
    <symbols>
      <symbol type="line" name="0" force_rhr="0" alpha="1" clip_to_extent="1">
        <layer enabled="1" locked="0" pass="0" class="SimpleLine">
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer enabled="1" locked="0" pass="0" class="MarkerLine">
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol type="marker" name="@0@1" force_rhr="0" alpha="1" clip_to_extent="1">
            <layer enabled="1" locked="0" pass="0" class="SimpleMarker">
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
                  <Option type="QString" name="name" value=""/>
                  <Option name="properties"/>
                  <Option type="QString" name="type" value="collection"/>
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
  <SingleCategoryDiagramRenderer diagramType="Pie" attributeLegend="1">
    <DiagramCategory scaleBasedVisibility="0" sizeType="MM" lineSizeType="MM" diagramOrientation="Up" barWidth="5" maxScaleDenominator="1e+08" labelPlacementMethod="XHeight" width="15" penAlpha="255" backgroundAlpha="255" penColor="#000000" penWidth="0" sizeScale="3x:0,0,0,0,0,0" scaleDependency="Area" minimumSize="0" rotationOffset="270" minScaleDenominator="0" opacity="1" backgroundColor="#ffffff" lineSizeScale="3x:0,0,0,0,0,0" enabled="0" height="15">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute label="" color="#000000" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings zIndex="0" obstacle="0" showAll="1" priority="0" placement="2" dist="0" linePlacementFlags="2">
    <properties>
      <Option type="Map">
        <Option type="QString" name="name" value=""/>
        <Option name="properties"/>
        <Option type="QString" name="type" value="collection"/>
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
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_crest_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
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
                <Option type="QString" name="3: broad crested" value="3"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="4: short crested" value="4"/>
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
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_sewerage">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option type="QString" name="CheckedState" value="1"/>
            <Option type="QString" name="UncheckedState" value="0"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_discharge_coefficient_positive">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_discharge_coefficient_negative">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_external">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option type="QString" name="CheckedState" value="1"/>
            <Option type="QString" name="UncheckedState" value="0"/>
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
                <Option type="QString" name="-1" value="-1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="0" value="0"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="1" value="1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="2" value="2"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="3" value="3"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="4" value="4"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="5" value="5"/>
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
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
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
    <field name="weir_connection_node_start_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="weir_connection_node_end_id">
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
                <Option type="QString" name="1: Rectangle" value="1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="2: Circle" value="2"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="3: Egg" value="3"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="5: Tabulated rectangle" value="5"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="6: Tabulated trapezium" value="6"/>
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
    <default field="ROWID" applyOnUpdate="0" expression=""/>
    <default field="weir_id" applyOnUpdate="0" expression="if(maximum(weir_id) is null,1, maximum(weir_id)+1)"/>
    <default field="weir_display_name" applyOnUpdate="0" expression="'new'"/>
    <default field="weir_code" applyOnUpdate="0" expression="'new'"/>
    <default field="weir_crest_level" applyOnUpdate="0" expression=""/>
    <default field="weir_crest_type" applyOnUpdate="0" expression="4"/>
    <default field="weir_cross_section_definition_id" applyOnUpdate="0" expression=""/>
    <default field="weir_sewerage" applyOnUpdate="0" expression=""/>
    <default field="weir_discharge_coefficient_positive" applyOnUpdate="0" expression="0.8"/>
    <default field="weir_discharge_coefficient_negative" applyOnUpdate="0" expression="0.8"/>
    <default field="weir_external" applyOnUpdate="0" expression="1"/>
    <default field="weir_zoom_category" applyOnUpdate="0" expression="2"/>
    <default field="weir_friction_value" applyOnUpdate="0" expression="0.02"/>
    <default field="weir_friction_type" applyOnUpdate="0" expression="2"/>
    <default field="weir_connection_node_start_id" applyOnUpdate="0" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))) is null,'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))))"/>
    <default field="weir_connection_node_end_id" applyOnUpdate="0" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))) is null,'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))))"/>
    <default field="def_id" applyOnUpdate="0" expression=""/>
    <default field="def_shape" applyOnUpdate="0" expression=""/>
    <default field="def_width" applyOnUpdate="0" expression=""/>
    <default field="def_height" applyOnUpdate="0" expression=""/>
    <default field="def_code" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="ROWID" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="weir_id" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="weir_display_name" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="weir_code" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="weir_crest_level" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="weir_crest_type" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="weir_cross_section_definition_id" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="weir_sewerage" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="weir_discharge_coefficient_positive" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="weir_discharge_coefficient_negative" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="weir_external" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="weir_zoom_category" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="weir_friction_value" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="weir_friction_type" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="weir_connection_node_start_id" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="weir_connection_node_end_id" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="def_id" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="def_shape" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="def_width" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="def_height" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="def_code" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="ROWID" desc=""/>
    <constraint exp="" field="weir_id" desc=""/>
    <constraint exp="" field="weir_display_name" desc=""/>
    <constraint exp="" field="weir_code" desc=""/>
    <constraint exp="" field="weir_crest_level" desc=""/>
    <constraint exp="" field="weir_crest_type" desc=""/>
    <constraint exp="" field="weir_cross_section_definition_id" desc=""/>
    <constraint exp="" field="weir_sewerage" desc=""/>
    <constraint exp="" field="weir_discharge_coefficient_positive" desc=""/>
    <constraint exp="" field="weir_discharge_coefficient_negative" desc=""/>
    <constraint exp="" field="weir_external" desc=""/>
    <constraint exp="" field="weir_zoom_category" desc=""/>
    <constraint exp="" field="weir_friction_value" desc=""/>
    <constraint exp="" field="weir_friction_type" desc=""/>
    <constraint exp="" field="weir_connection_node_start_id" desc=""/>
    <constraint exp="" field="weir_connection_node_end_id" desc=""/>
    <constraint exp="" field="def_id" desc=""/>
    <constraint exp="" field="def_shape" desc=""/>
    <constraint exp="" field="def_width" desc=""/>
    <constraint exp="" field="def_height" desc=""/>
    <constraint exp="" field="def_code" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="" sortOrder="0">
    <columns>
      <column type="field" name="ROWID" width="-1" hidden="0"/>
      <column type="field" name="weir_id" width="-1" hidden="0"/>
      <column type="field" name="weir_display_name" width="-1" hidden="0"/>
      <column type="field" name="weir_code" width="-1" hidden="0"/>
      <column type="field" name="weir_crest_level" width="-1" hidden="0"/>
      <column type="field" name="weir_crest_type" width="-1" hidden="0"/>
      <column type="field" name="weir_cross_section_definition_id" width="185" hidden="0"/>
      <column type="field" name="weir_sewerage" width="-1" hidden="0"/>
      <column type="field" name="weir_discharge_coefficient_positive" width="-1" hidden="0"/>
      <column type="field" name="weir_discharge_coefficient_negative" width="-1" hidden="0"/>
      <column type="field" name="weir_external" width="-1" hidden="0"/>
      <column type="field" name="weir_zoom_category" width="-1" hidden="0"/>
      <column type="field" name="weir_friction_value" width="-1" hidden="0"/>
      <column type="field" name="weir_friction_type" width="-1" hidden="0"/>
      <column type="field" name="weir_connection_node_start_id" width="-1" hidden="0"/>
      <column type="field" name="weir_connection_node_end_id" width="-1" hidden="0"/>
      <column type="field" name="def_id" width="-1" hidden="0"/>
      <column type="field" name="def_shape" width="-1" hidden="0"/>
      <column type="field" name="def_width" width="-1" hidden="0"/>
      <column type="field" name="def_height" width="-1" hidden="0"/>
      <column type="field" name="def_code" width="-1" hidden="0"/>
      <column type="actions" width="-1" hidden="1"/>
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
    <attributeEditorContainer columnCount="1" visibilityExpression="" name="Weir view" groupBox="0" visibilityExpressionEnabled="0" showLabel="1">
      <attributeEditorContainer columnCount="1" visibilityExpression="" name="General" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="weir_id" index="1" showLabel="1"/>
        <attributeEditorField name="weir_display_name" index="2" showLabel="1"/>
        <attributeEditorField name="weir_code" index="3" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" visibilityExpression="" name="Characteristics" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="weir_crest_level" index="4" showLabel="1"/>
        <attributeEditorField name="weir_crest_type" index="5" showLabel="1"/>
        <attributeEditorField name="weir_discharge_coefficient_positive" index="8" showLabel="1"/>
        <attributeEditorField name="weir_discharge_coefficient_negative" index="9" showLabel="1"/>
        <attributeEditorField name="weir_friction_value" index="12" showLabel="1"/>
        <attributeEditorField name="weir_friction_type" index="13" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" visibilityExpression="" name="Cross section" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="weir_cross_section_definition_id" index="6" showLabel="1"/>
        <attributeEditorField name="def_code" index="20" showLabel="1"/>
        <attributeEditorField name="def_shape" index="17" showLabel="1"/>
        <attributeEditorField name="def_width" index="18" showLabel="1"/>
        <attributeEditorField name="def_height" index="19" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" visibilityExpression="" name="Visualization" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="weir_sewerage" index="7" showLabel="1"/>
        <attributeEditorField name="weir_external" index="10" showLabel="1"/>
        <attributeEditorField name="weir_zoom_category" index="11" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" visibilityExpression="" name="Connection nodes" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="weir_connection_node_start_id" index="14" showLabel="1"/>
        <attributeEditorField name="weir_connection_node_end_id" index="15" showLabel="1"/>
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
