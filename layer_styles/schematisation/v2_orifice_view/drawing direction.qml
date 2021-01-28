<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" simplifyLocal="1" labelsEnabled="0" simplifyDrawingTol="1" version="3.10.10-A Coruña" simplifyAlgorithm="0" minScale="0" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" maxScale="0" simplifyDrawingHints="1" simplifyMaxScale="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" type="singleSymbol" symbollevels="0" enableorderby="0">
    <symbols>
      <symbol type="line" clip_to_extent="1" name="0" force_rhr="0" alpha="1">
        <layer class="SimpleLine" pass="0" enabled="1" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="51,160,44,255"/>
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
        <layer class="MarkerLine" pass="0" enabled="1" locked="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="interval" v="5"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="0"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="MapUnit"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="placement" v="interval"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option type="bool" name="active" value="false"/>
                  <Option type="int" name="type" value="1"/>
                  <Option type="QString" name="val" value=""/>
                </Option>
                <Option type="Map" name="offsetAlongLine">
                  <Option type="bool" name="active" value="false"/>
                  <Option type="int" name="type" value="1"/>
                  <Option type="QString" name="val" value=""/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol type="marker" clip_to_extent="1" name="@0@1" force_rhr="0" alpha="1">
            <layer class="SimpleMarker" pass="0" enabled="1" locked="0">
              <prop k="angle" v="90"/>
              <prop k="color" v="51,160,44,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="triangle"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="51,160,44,255"/>
              <prop k="outline_style" v="no"/>
              <prop k="outline_width" v="0.6"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="2.4"/>
              <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option type="QString" name="name" value=""/>
                  <Option type="Map" name="properties">
                    <Option type="Map" name="angle">
                      <Option type="bool" name="active" value="false"/>
                      <Option type="int" name="type" value="1"/>
                      <Option type="QString" name="val" value=""/>
                    </Option>
                    <Option type="Map" name="enabled">
                      <Option type="bool" name="active" value="true"/>
                      <Option type="QString" name="expression" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;"/>
                      <Option type="int" name="type" value="3"/>
                    </Option>
                    <Option type="Map" name="size">
                      <Option type="bool" name="active" value="false"/>
                      <Option type="QString" name="expression" value=""/>
                      <Option type="int" name="type" value="3"/>
                    </Option>
                  </Option>
                  <Option type="QString" name="type" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer class="MarkerLine" pass="0" enabled="1" locked="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
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
          <symbol type="marker" clip_to_extent="1" name="@0@2" force_rhr="0" alpha="1">
            <layer class="SimpleMarker" pass="0" enabled="1" locked="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="51,160,44,255"/>
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
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="3.4"/>
              <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option type="QString" name="name" value=""/>
                  <Option type="Map" name="properties">
                    <Option type="Map" name="size">
                      <Option type="bool" name="active" value="true"/>
                      <Option type="QString" name="expression" value="if(@map_scale&lt;10000, 3.4,2)"/>
                      <Option type="int" name="type" value="3"/>
                    </Option>
                  </Option>
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
    <property value="&quot;weir_display_name&quot;" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory width="15" diagramOrientation="Up" rotationOffset="270" penAlpha="255" labelPlacementMethod="XHeight" minScaleDenominator="0" opacity="1" sizeScale="3x:0,0,0,0,0,0" penColor="#000000" lineSizeScale="3x:0,0,0,0,0,0" enabled="0" barWidth="5" penWidth="0" scaleBasedVisibility="0" backgroundColor="#ffffff" sizeType="MM" minimumSize="0" scaleDependency="Area" maxScaleDenominator="1e+08" lineSizeType="MM" height="15" backgroundAlpha="255">
      <fontProperties description="MS Shell Dlg 2,7.8,-1,5,50,0,0,0,0,0" style=""/>
      <attribute field="" label="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings obstacle="0" priority="0" showAll="1" placement="2" zIndex="0" linePlacementFlags="18" dist="0">
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
    <field name="orf_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_crest_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_sewerage">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option type="QString" name="CheckedState" value="1"/>
            <Option type="QString" name="UncheckedState" value="0"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_cross_section_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_friction_type">
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
    <field name="orf_discharge_coefficient_positive">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_discharge_coefficient_negative">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_zoom_category">
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
    <field name="orf_crest_type">
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
    <field name="orf_connection_node_start_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orf_connection_node_end_id">
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
    <alias name="" field="orf_id" index="1"/>
    <alias name="" field="orf_display_name" index="2"/>
    <alias name="" field="orf_code" index="3"/>
    <alias name="" field="orf_crest_level" index="4"/>
    <alias name="" field="orf_sewerage" index="5"/>
    <alias name="" field="orf_cross_section_definition_id" index="6"/>
    <alias name="" field="orf_friction_value" index="7"/>
    <alias name="" field="orf_friction_type" index="8"/>
    <alias name="" field="orf_discharge_coefficient_positive" index="9"/>
    <alias name="" field="orf_discharge_coefficient_negative" index="10"/>
    <alias name="" field="orf_zoom_category" index="11"/>
    <alias name="" field="orf_crest_type" index="12"/>
    <alias name="" field="orf_connection_node_start_id" index="13"/>
    <alias name="" field="orf_connection_node_end_id" index="14"/>
    <alias name="" field="def_id" index="15"/>
    <alias name="" field="def_shape" index="16"/>
    <alias name="" field="def_width" index="17"/>
    <alias name="" field="def_height" index="18"/>
    <alias name="" field="def_code" index="19"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="ROWID" expression=""/>
    <default applyOnUpdate="0" field="orf_id" expression=""/>
    <default applyOnUpdate="0" field="orf_display_name" expression=""/>
    <default applyOnUpdate="0" field="orf_code" expression=""/>
    <default applyOnUpdate="0" field="orf_crest_level" expression=""/>
    <default applyOnUpdate="0" field="orf_sewerage" expression=""/>
    <default applyOnUpdate="0" field="orf_cross_section_definition_id" expression=""/>
    <default applyOnUpdate="0" field="orf_friction_value" expression=""/>
    <default applyOnUpdate="0" field="orf_friction_type" expression=""/>
    <default applyOnUpdate="0" field="orf_discharge_coefficient_positive" expression=""/>
    <default applyOnUpdate="0" field="orf_discharge_coefficient_negative" expression=""/>
    <default applyOnUpdate="0" field="orf_zoom_category" expression=""/>
    <default applyOnUpdate="0" field="orf_crest_type" expression=""/>
    <default applyOnUpdate="0" field="orf_connection_node_start_id" expression=""/>
    <default applyOnUpdate="0" field="orf_connection_node_end_id" expression=""/>
    <default applyOnUpdate="0" field="def_id" expression=""/>
    <default applyOnUpdate="0" field="def_shape" expression=""/>
    <default applyOnUpdate="0" field="def_width" expression=""/>
    <default applyOnUpdate="0" field="def_height" expression=""/>
    <default applyOnUpdate="0" field="def_code" expression=""/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" constraints="0" field="ROWID" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="orf_id" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="orf_display_name" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="orf_code" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="orf_crest_level" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="orf_sewerage" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="orf_cross_section_definition_id" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="orf_friction_value" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="orf_friction_type" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="orf_discharge_coefficient_positive" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="orf_discharge_coefficient_negative" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="orf_zoom_category" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="orf_crest_type" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="orf_connection_node_start_id" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="orf_connection_node_end_id" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="def_id" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="def_shape" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="def_width" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="def_height" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="def_code" notnull_strength="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="ROWID" exp=""/>
    <constraint desc="" field="orf_id" exp=""/>
    <constraint desc="" field="orf_display_name" exp=""/>
    <constraint desc="" field="orf_code" exp=""/>
    <constraint desc="" field="orf_crest_level" exp=""/>
    <constraint desc="" field="orf_sewerage" exp=""/>
    <constraint desc="" field="orf_cross_section_definition_id" exp=""/>
    <constraint desc="" field="orf_friction_value" exp=""/>
    <constraint desc="" field="orf_friction_type" exp=""/>
    <constraint desc="" field="orf_discharge_coefficient_positive" exp=""/>
    <constraint desc="" field="orf_discharge_coefficient_negative" exp=""/>
    <constraint desc="" field="orf_zoom_category" exp=""/>
    <constraint desc="" field="orf_crest_type" exp=""/>
    <constraint desc="" field="orf_connection_node_start_id" exp=""/>
    <constraint desc="" field="orf_connection_node_end_id" exp=""/>
    <constraint desc="" field="def_id" exp=""/>
    <constraint desc="" field="def_shape" exp=""/>
    <constraint desc="" field="def_width" exp=""/>
    <constraint desc="" field="def_height" exp=""/>
    <constraint desc="" field="def_code" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column type="field" name="ROWID" hidden="0" width="-1"/>
      <column type="field" name="orf_id" hidden="0" width="-1"/>
      <column type="field" name="orf_display_name" hidden="0" width="-1"/>
      <column type="field" name="orf_code" hidden="0" width="-1"/>
      <column type="field" name="orf_crest_level" hidden="0" width="-1"/>
      <column type="field" name="orf_sewerage" hidden="0" width="-1"/>
      <column type="field" name="orf_cross_section_definition_id" hidden="0" width="-1"/>
      <column type="field" name="orf_friction_value" hidden="0" width="-1"/>
      <column type="field" name="orf_friction_type" hidden="0" width="-1"/>
      <column type="field" name="orf_discharge_coefficient_positive" hidden="0" width="-1"/>
      <column type="field" name="orf_discharge_coefficient_negative" hidden="0" width="-1"/>
      <column type="field" name="orf_zoom_category" hidden="0" width="-1"/>
      <column type="field" name="orf_crest_type" hidden="0" width="-1"/>
      <column type="field" name="orf_connection_node_start_id" hidden="0" width="-1"/>
      <column type="field" name="orf_connection_node_end_id" hidden="0" width="-1"/>
      <column type="field" name="def_id" hidden="0" width="-1"/>
      <column type="field" name="def_shape" hidden="0" width="-1"/>
      <column type="field" name="def_width" hidden="0" width="-1"/>
      <column type="field" name="def_height" hidden="0" width="-1"/>
      <column type="field" name="def_code" hidden="0" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
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
  <editorlayout>generatedlayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer groupBox="0" visibilityExpressionEnabled="0" showLabel="1" name="Orifice view" visibilityExpression="" columnCount="1">
      <attributeEditorContainer groupBox="1" visibilityExpressionEnabled="0" showLabel="1" name="General" visibilityExpression="" columnCount="1">
        <attributeEditorField showLabel="1" name="orf_id" index="1"/>
        <attributeEditorField showLabel="1" name="orf_display_name" index="2"/>
        <attributeEditorField showLabel="1" name="orf_code" index="3"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpressionEnabled="0" showLabel="1" name="Characteristics" visibilityExpression="" columnCount="1">
        <attributeEditorField showLabel="1" name="orf_crest_level" index="4"/>
        <attributeEditorField showLabel="1" name="orf_crest_type" index="12"/>
        <attributeEditorField showLabel="1" name="orf_friction_value" index="7"/>
        <attributeEditorField showLabel="1" name="orf_friction_type" index="8"/>
        <attributeEditorField showLabel="1" name="orf_discharge_coefficient_positive" index="9"/>
        <attributeEditorField showLabel="1" name="orf_discharge_coefficient_negative" index="10"/>
        <attributeEditorField showLabel="1" name="orf_max_capacity" index="-1"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpressionEnabled="0" showLabel="1" name="Visualization" visibilityExpression="" columnCount="1">
        <attributeEditorField showLabel="1" name="orf_sewerage" index="5"/>
        <attributeEditorField showLabel="1" name="orf_zoom_category" index="11"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpressionEnabled="0" showLabel="1" name="Cross section" visibilityExpression="" columnCount="1">
        <attributeEditorField showLabel="1" name="orf_cross_section_definition_id" index="6"/>
        <attributeEditorField showLabel="1" name="def_shape" index="16"/>
        <attributeEditorField showLabel="1" name="def_width" index="17"/>
        <attributeEditorField showLabel="1" name="def_height" index="18"/>
        <attributeEditorField showLabel="1" name="def_code" index="19"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpressionEnabled="0" showLabel="1" name="Connection nodes" visibilityExpression="" columnCount="1">
        <attributeEditorField showLabel="1" name="orf_connection_node_start_id" index="13"/>
        <attributeEditorField showLabel="1" name="orf_connection_node_end_id" index="14"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="ROWID"/>
    <field editable="1" name="def_code"/>
    <field editable="1" name="def_height"/>
    <field editable="1" name="def_id"/>
    <field editable="1" name="def_shape"/>
    <field editable="1" name="def_width"/>
    <field editable="1" name="orf_code"/>
    <field editable="1" name="orf_connection_node_end_id"/>
    <field editable="1" name="orf_connection_node_start_id"/>
    <field editable="1" name="orf_crest_level"/>
    <field editable="1" name="orf_crest_type"/>
    <field editable="1" name="orf_cross_section_definition_id"/>
    <field editable="1" name="orf_discharge_coefficient_negative"/>
    <field editable="1" name="orf_discharge_coefficient_positive"/>
    <field editable="1" name="orf_display_name"/>
    <field editable="1" name="orf_friction_type"/>
    <field editable="1" name="orf_friction_value"/>
    <field editable="1" name="orf_id"/>
    <field editable="1" name="orf_max_capacity"/>
    <field editable="1" name="orf_sewerage"/>
    <field editable="1" name="orf_zoom_category"/>
  </editable>
  <labelOnTop>
    <field name="ROWID" labelOnTop="0"/>
    <field name="def_code" labelOnTop="0"/>
    <field name="def_height" labelOnTop="0"/>
    <field name="def_id" labelOnTop="0"/>
    <field name="def_shape" labelOnTop="0"/>
    <field name="def_width" labelOnTop="0"/>
    <field name="orf_code" labelOnTop="0"/>
    <field name="orf_connection_node_end_id" labelOnTop="0"/>
    <field name="orf_connection_node_start_id" labelOnTop="0"/>
    <field name="orf_crest_level" labelOnTop="0"/>
    <field name="orf_crest_type" labelOnTop="0"/>
    <field name="orf_cross_section_definition_id" labelOnTop="0"/>
    <field name="orf_discharge_coefficient_negative" labelOnTop="0"/>
    <field name="orf_discharge_coefficient_positive" labelOnTop="0"/>
    <field name="orf_display_name" labelOnTop="0"/>
    <field name="orf_friction_type" labelOnTop="0"/>
    <field name="orf_friction_value" labelOnTop="0"/>
    <field name="orf_id" labelOnTop="0"/>
    <field name="orf_max_capacity" labelOnTop="0"/>
    <field name="orf_sewerage" labelOnTop="0"/>
    <field name="orf_zoom_category" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>"orf_display_name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
