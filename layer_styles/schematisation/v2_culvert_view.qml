<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.4.5-Madeira" styleCategories="AllStyleCategories" simplifyDrawingTol="1" minScale="1e+08" labelsEnabled="0" simplifyLocal="1" hasScaleBasedVisibilityFlag="0" simplifyDrawingHints="1" readOnly="0" simplifyMaxScale="1" simplifyAlgorithm="0" maxScale="-4.65661e-10">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" forceraster="0" type="singleSymbol" symbollevels="0">
    <symbols>
      <symbol alpha="1" name="0" force_rhr="0" type="line" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" locked="0" pass="0">
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="101,101,101,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.66" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="MarkerLine" enabled="1" locked="0" pass="0">
          <prop v="3" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="0" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="MM" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="centralpoint" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol alpha="1" name="@0@1" force_rhr="0" type="marker" clip_to_extent="1">
            <layer class="SimpleMarker" enabled="1" locked="0" pass="0">
              <prop v="0" k="angle"/>
              <prop v="101,101,101,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="circle" k="name"/>
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
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties"/>
                  <Option value="collection" name="type" type="QString"/>
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
    <property key="dualview/previewExpressions" value="ROWID"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Pie" attributeLegend="1">
    <DiagramCategory sizeScale="3x:0,0,0,0,0,0" penAlpha="255" width="15" penColor="#000000" lineSizeScale="3x:0,0,0,0,0,0" penWidth="0" rotationOffset="270" barWidth="5" sizeType="MM" backgroundColor="#ffffff" diagramOrientation="Up" maxScaleDenominator="1e+08" enabled="0" lineSizeType="MM" backgroundAlpha="255" labelPlacementMethod="XHeight" scaleDependency="Area" scaleBasedVisibility="0" minScaleDenominator="-4.65661e-10" opacity="1" height="15" minimumSize="0">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute color="#000000" field="" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings placement="2" linePlacementFlags="2" obstacle="0" dist="0" showAll="1" priority="0" zIndex="0">
    <properties>
      <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
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
    <field name="cul_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_calculation_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="100" name="100: embedded" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="101" name="101: isolated" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="102" name="102: connected" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="105" name="105: double connected" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_friction_type">
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
    <field name="cul_dist_calc_points">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_zoom_category">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="-1" name="-1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="0" name="0" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="1" name="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="3" name="3" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="4" name="4" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="5" name="5" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_cross_section_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_discharge_coefficient_positive">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_discharge_coefficient_negative">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_invert_level_start_point">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_invert_level_end_point">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_connection_node_start_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_connection_node_end_id">
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
  </fieldConfiguration>
  <aliases>
    <alias field="ROWID" name="" index="0"/>
    <alias field="cul_id" name="id" index="1"/>
    <alias field="cul_display_name" name="display_name" index="2"/>
    <alias field="cul_code" name="code" index="3"/>
    <alias field="cul_calculation_type" name="calculation_type" index="4"/>
    <alias field="cul_friction_value" name="friction_value" index="5"/>
    <alias field="cul_friction_type" name="friction_type" index="6"/>
    <alias field="cul_dist_calc_points" name="dist_calc_points" index="7"/>
    <alias field="cul_zoom_category" name="zoom_category" index="8"/>
    <alias field="cul_cross_section_definition_id" name="cross_section_definition_id" index="9"/>
    <alias field="cul_discharge_coefficient_positive" name="discharge_coefficient_positive" index="10"/>
    <alias field="cul_discharge_coefficient_negative" name="discharge_coefficient_negative" index="11"/>
    <alias field="cul_invert_level_start_point" name="invert_level_start_point" index="12"/>
    <alias field="cul_invert_level_end_point" name="invert_level_end_point" index="13"/>
    <alias field="cul_connection_node_start_id" name="connection_node_start_id" index="14"/>
    <alias field="cul_connection_node_end_id" name="connection_node_end_id" index="15"/>
    <alias field="def_id" name="id" index="16"/>
    <alias field="def_shape" name="shape" index="17"/>
    <alias field="def_width" name="width" index="18"/>
    <alias field="def_height" name="height" index="19"/>
    <alias field="def_code" name="code" index="20"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="ROWID" expression="" applyOnUpdate="0"/>
    <default field="cul_id" expression="if(maximum(cul_id) is null,1, maximum(cul_id)+1)" applyOnUpdate="0"/>
    <default field="cul_display_name" expression="'new'" applyOnUpdate="0"/>
    <default field="cul_code" expression="'new'" applyOnUpdate="0"/>
    <default field="cul_calculation_type" expression="101" applyOnUpdate="0"/>
    <default field="cul_friction_value" expression="0.0145" applyOnUpdate="0"/>
    <default field="cul_friction_type" expression="2" applyOnUpdate="0"/>
    <default field="cul_dist_calc_points" expression="10000" applyOnUpdate="0"/>
    <default field="cul_zoom_category" expression="3" applyOnUpdate="0"/>
    <default field="cul_cross_section_definition_id" expression="" applyOnUpdate="0"/>
    <default field="cul_discharge_coefficient_positive" expression="0.8" applyOnUpdate="0"/>
    <default field="cul_discharge_coefficient_negative" expression="0.8" applyOnUpdate="0"/>
    <default field="cul_invert_level_start_point" expression="aggregate('v2_manhole_view','min',&quot;bottom_level&quot;, intersects($geometry,start_point(geometry(@parent)))) " applyOnUpdate="0"/>
    <default field="cul_invert_level_end_point" expression="aggregate('v2_manhole_view','min',&quot;bottom_level&quot;, intersects($geometry,end_point(geometry(@parent)))) " applyOnUpdate="0"/>
    <default field="cul_connection_node_start_id" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))) is null, 'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))))" applyOnUpdate="0"/>
    <default field="cul_connection_node_end_id" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))) is null, 'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))))" applyOnUpdate="0"/>
    <default field="def_id" expression="" applyOnUpdate="0"/>
    <default field="def_shape" expression="" applyOnUpdate="0"/>
    <default field="def_width" expression="" applyOnUpdate="0"/>
    <default field="def_height" expression="" applyOnUpdate="0"/>
    <default field="def_code" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" exp_strength="0" field="ROWID" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="cul_id" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" exp_strength="0" field="cul_display_name" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" exp_strength="0" field="cul_code" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" exp_strength="0" field="cul_calculation_type" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" exp_strength="0" field="cul_friction_value" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" exp_strength="0" field="cul_friction_type" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" exp_strength="0" field="cul_dist_calc_points" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" exp_strength="0" field="cul_zoom_category" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" exp_strength="0" field="cul_cross_section_definition_id" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" exp_strength="0" field="cul_discharge_coefficient_positive" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" exp_strength="0" field="cul_discharge_coefficient_negative" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" exp_strength="0" field="cul_invert_level_start_point" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" exp_strength="0" field="cul_invert_level_end_point" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" exp_strength="0" field="cul_connection_node_start_id" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="cul_connection_node_end_id" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="def_id" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" exp_strength="0" field="def_shape" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="def_width" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="def_height" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="def_code" notnull_strength="0" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="ROWID" desc="" exp=""/>
    <constraint field="cul_id" desc="" exp=""/>
    <constraint field="cul_display_name" desc="" exp=""/>
    <constraint field="cul_code" desc="" exp=""/>
    <constraint field="cul_calculation_type" desc="" exp=""/>
    <constraint field="cul_friction_value" desc="" exp=""/>
    <constraint field="cul_friction_type" desc="" exp=""/>
    <constraint field="cul_dist_calc_points" desc="" exp=""/>
    <constraint field="cul_zoom_category" desc="" exp=""/>
    <constraint field="cul_cross_section_definition_id" desc="" exp=""/>
    <constraint field="cul_discharge_coefficient_positive" desc="" exp=""/>
    <constraint field="cul_discharge_coefficient_negative" desc="" exp=""/>
    <constraint field="cul_invert_level_start_point" desc="" exp=""/>
    <constraint field="cul_invert_level_end_point" desc="" exp=""/>
    <constraint field="cul_connection_node_start_id" desc="" exp=""/>
    <constraint field="cul_connection_node_end_id" desc="" exp=""/>
    <constraint field="def_id" desc="" exp=""/>
    <constraint field="def_shape" desc="" exp=""/>
    <constraint field="def_width" desc="" exp=""/>
    <constraint field="def_height" desc="" exp=""/>
    <constraint field="def_code" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column hidden="0" name="ROWID" type="field" width="-1"/>
      <column hidden="0" name="cul_id" type="field" width="-1"/>
      <column hidden="0" name="cul_display_name" type="field" width="-1"/>
      <column hidden="0" name="cul_code" type="field" width="-1"/>
      <column hidden="0" name="cul_calculation_type" type="field" width="-1"/>
      <column hidden="0" name="cul_friction_value" type="field" width="-1"/>
      <column hidden="0" name="cul_friction_type" type="field" width="-1"/>
      <column hidden="0" name="cul_dist_calc_points" type="field" width="-1"/>
      <column hidden="0" name="cul_zoom_category" type="field" width="-1"/>
      <column hidden="0" name="cul_cross_section_definition_id" type="field" width="-1"/>
      <column hidden="0" name="cul_discharge_coefficient_positive" type="field" width="-1"/>
      <column hidden="0" name="cul_discharge_coefficient_negative" type="field" width="-1"/>
      <column hidden="0" name="cul_invert_level_start_point" type="field" width="-1"/>
      <column hidden="0" name="cul_invert_level_end_point" type="field" width="-1"/>
      <column hidden="0" name="cul_connection_node_start_id" type="field" width="-1"/>
      <column hidden="0" name="cul_connection_node_end_id" type="field" width="-1"/>
      <column hidden="0" name="def_id" type="field" width="-1"/>
      <column hidden="0" name="def_shape" type="field" width="-1"/>
      <column hidden="0" name="def_width" type="field" width="-1"/>
      <column hidden="0" name="def_height" type="field" width="-1"/>
      <column hidden="0" name="def_code" type="field" width="-1"/>
      <column hidden="1" type="actions" width="-1"/>
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
    <attributeEditorContainer showLabel="1" name="Culvert view" visibilityExpression="" groupBox="0" visibilityExpressionEnabled="0" columnCount="1">
      <attributeEditorContainer showLabel="1" name="General" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1">
        <attributeEditorField showLabel="1" name="cul_id" index="1"/>
        <attributeEditorField showLabel="1" name="cul_display_name" index="2"/>
        <attributeEditorField showLabel="1" name="cul_code" index="3"/>
        <attributeEditorField showLabel="1" name="cul_calculation_type" index="4"/>
        <attributeEditorField showLabel="1" name="cul_dist_calc_points" index="7"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" name="Characteristics" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1">
        <attributeEditorField showLabel="1" name="cul_invert_level_start_point" index="12"/>
        <attributeEditorField showLabel="1" name="cul_invert_level_end_point" index="13"/>
        <attributeEditorField showLabel="1" name="cul_friction_type" index="6"/>
        <attributeEditorField showLabel="1" name="cul_friction_value" index="5"/>
        <attributeEditorField showLabel="1" name="cul_discharge_coefficient_positive" index="10"/>
        <attributeEditorField showLabel="1" name="cul_discharge_coefficient_negative" index="11"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" name="Cross section definition" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1">
        <attributeEditorField showLabel="1" name="cul_cross_section_definition_id" index="9"/>
        <attributeEditorField showLabel="1" name="def_code" index="20"/>
        <attributeEditorField showLabel="1" name="def_shape" index="17"/>
        <attributeEditorField showLabel="1" name="def_width" index="18"/>
        <attributeEditorField showLabel="1" name="def_height" index="19"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" name="Visualization" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1">
        <attributeEditorField showLabel="1" name="cul_zoom_category" index="8"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" name="Connection nodes" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1">
        <attributeEditorField showLabel="1" name="cul_connection_node_start_id" index="14"/>
        <attributeEditorField showLabel="1" name="cul_connection_node_end_id" index="15"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="ROWID" editable="1"/>
    <field name="cul_calculation_type" editable="1"/>
    <field name="cul_code" editable="1"/>
    <field name="cul_connection_node_end_id" editable="0"/>
    <field name="cul_connection_node_start_id" editable="0"/>
    <field name="cul_cross_section_definition_id" editable="1"/>
    <field name="cul_discharge_coefficient_negative" editable="1"/>
    <field name="cul_discharge_coefficient_positive" editable="1"/>
    <field name="cul_display_name" editable="1"/>
    <field name="cul_dist_calc_points" editable="1"/>
    <field name="cul_friction_type" editable="1"/>
    <field name="cul_friction_value" editable="1"/>
    <field name="cul_id" editable="1"/>
    <field name="cul_invert_level_end_point" editable="1"/>
    <field name="cul_invert_level_start_point" editable="1"/>
    <field name="cul_zoom_category" editable="1"/>
    <field name="def_code" editable="0"/>
    <field name="def_height" editable="0"/>
    <field name="def_id" editable="0"/>
    <field name="def_shape" editable="0"/>
    <field name="def_width" editable="0"/>
  </editable>
  <labelOnTop>
    <field name="ROWID" labelOnTop="0"/>
    <field name="cul_calculation_type" labelOnTop="0"/>
    <field name="cul_code" labelOnTop="0"/>
    <field name="cul_connection_node_end_id" labelOnTop="0"/>
    <field name="cul_connection_node_start_id" labelOnTop="0"/>
    <field name="cul_cross_section_definition_id" labelOnTop="0"/>
    <field name="cul_discharge_coefficient_negative" labelOnTop="0"/>
    <field name="cul_discharge_coefficient_positive" labelOnTop="0"/>
    <field name="cul_display_name" labelOnTop="0"/>
    <field name="cul_dist_calc_points" labelOnTop="0"/>
    <field name="cul_friction_type" labelOnTop="0"/>
    <field name="cul_friction_value" labelOnTop="0"/>
    <field name="cul_id" labelOnTop="0"/>
    <field name="cul_invert_level_end_point" labelOnTop="0"/>
    <field name="cul_invert_level_start_point" labelOnTop="0"/>
    <field name="cul_zoom_category" labelOnTop="0"/>
    <field name="def_code" labelOnTop="0"/>
    <field name="def_height" labelOnTop="0"/>
    <field name="def_id" labelOnTop="0"/>
    <field name="def_shape" labelOnTop="0"/>
    <field name="def_width" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>ROWID</previewExpression>
  <mapTip>display_name</mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
