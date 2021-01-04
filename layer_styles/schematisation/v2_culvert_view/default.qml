<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" labelsEnabled="0" simplifyAlgorithm="0" simplifyMaxScale="1" version="3.10.10-A Coruña" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="1e+08" simplifyDrawingTol="1" simplifyDrawingHints="1" maxScale="-4.65661e-10" simplifyLocal="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" type="singleSymbol" symbollevels="0" forceraster="0">
    <symbols>
      <symbol force_rhr="0" type="line" clip_to_extent="1" name="0" alpha="1">
        <layer enabled="1" class="SimpleLine" locked="0" pass="0">
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
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer enabled="1" class="MarkerLine" locked="0" pass="0">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="3" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="0" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="RenderMetersInMapUnits" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="firstvertex" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="1" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="cul_discharge_coefficient_negative > 0&#xd;&#xa;AND cul_discharge_coefficient_positive = 0" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="offsetAlongLine">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="0.6667*$length" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" type="marker" clip_to_extent="1" name="@0@1" alpha="1">
            <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
              <prop v="180" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="line" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="101,101,101,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0.8" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
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
        </layer>
        <layer enabled="1" class="MarkerLine" locked="0" pass="0">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="3" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="0" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="RenderMetersInMapUnits" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="firstvertex" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="1" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="cul_discharge_coefficient_negative > 0&#xd;&#xa;AND cul_discharge_coefficient_positive = 0" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="offsetAlongLine">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="0.3333*$length" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" type="marker" clip_to_extent="1" name="@0@2" alpha="1">
            <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
              <prop v="180" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="arrowhead" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="101,101,101,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0.8" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
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
        </layer>
        <layer enabled="1" class="MarkerLine" locked="0" pass="0">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="3" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="0" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="RenderMetersInMapUnits" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="firstvertex" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="1" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="cul_discharge_coefficient_positive > 0&#xd;&#xa;AND cul_discharge_coefficient_negative = 0" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="offsetAlongLine">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="0.3333*$length" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" type="marker" clip_to_extent="1" name="@0@3" alpha="1">
            <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
              <prop v="0" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="line" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="101,101,101,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0.8" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
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
        </layer>
        <layer enabled="1" class="MarkerLine" locked="0" pass="0">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="3" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="0" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="RenderMetersInMapUnits" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="firstvertex" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="1" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="cul_discharge_coefficient_positive > 0&#xd;&#xa;AND cul_discharge_coefficient_negative = 0" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="offsetAlongLine">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="0.66667*$length" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" type="marker" clip_to_extent="1" name="@0@4" alpha="1">
            <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
              <prop v="0" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="arrowhead" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="101,101,101,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0.8" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
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
        </layer>
        <layer enabled="1" class="MarkerLine" locked="0" pass="0">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
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
          <prop v="1" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" type="marker" clip_to_extent="1" name="@0@5" alpha="1">
            <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
              <prop v="0" k="angle"/>
              <prop v="101,101,101,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="circle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
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
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Pie">
    <DiagramCategory labelPlacementMethod="XHeight" diagramOrientation="Up" penWidth="0" sizeScale="3x:0,0,0,0,0,0" scaleDependency="Area" lineSizeType="MM" lineSizeScale="3x:0,0,0,0,0,0" backgroundColor="#ffffff" minScaleDenominator="-4.65661e-10" backgroundAlpha="255" penColor="#000000" minimumSize="0" enabled="0" sizeType="MM" maxScaleDenominator="1e+08" scaleBasedVisibility="0" height="15" rotationOffset="270" barWidth="5" opacity="1" penAlpha="255" width="15">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute field="" color="#000000" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings dist="0" linePlacementFlags="2" obstacle="0" zIndex="0" priority="0" placement="2" showAll="1">
    <properties>
      <Option type="Map">
        <Option value="" type="QString" name="name"/>
        <Option name="properties"/>
        <Option value="collection" type="QString" name="type"/>
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
    <field name="cul_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_calculation_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="100" type="QString" name="100: embedded"/>
              </Option>
              <Option type="Map">
                <Option value="101" type="QString" name="101: isolated"/>
              </Option>
              <Option type="Map">
                <Option value="102" type="QString" name="102: connected"/>
              </Option>
              <Option type="Map">
                <Option value="105" type="QString" name="105: double connected"/>
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
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_friction_type">
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
    <field name="cul_dist_calc_points">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_zoom_category">
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
    <field name="cul_cross_section_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_discharge_coefficient_positive">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_discharge_coefficient_negative">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_invert_level_start_point">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_invert_level_end_point">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_connection_node_start_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_connection_node_end_id">
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
    <alias index="0" field="ROWID" name=""/>
    <alias index="1" field="cul_id" name="id"/>
    <alias index="2" field="cul_display_name" name="display_name"/>
    <alias index="3" field="cul_code" name="code"/>
    <alias index="4" field="cul_calculation_type" name="calculation_type"/>
    <alias index="5" field="cul_friction_value" name="friction_value"/>
    <alias index="6" field="cul_friction_type" name="friction_type"/>
    <alias index="7" field="cul_dist_calc_points" name="dist_calc_points"/>
    <alias index="8" field="cul_zoom_category" name="zoom_category"/>
    <alias index="9" field="cul_cross_section_definition_id" name="cross_section_definition_id"/>
    <alias index="10" field="cul_discharge_coefficient_positive" name="discharge_coefficient_positive"/>
    <alias index="11" field="cul_discharge_coefficient_negative" name="discharge_coefficient_negative"/>
    <alias index="12" field="cul_invert_level_start_point" name="invert_level_start_point"/>
    <alias index="13" field="cul_invert_level_end_point" name="invert_level_end_point"/>
    <alias index="14" field="cul_connection_node_start_id" name="connection_node_start_id"/>
    <alias index="15" field="cul_connection_node_end_id" name="connection_node_end_id"/>
    <alias index="16" field="def_id" name="id"/>
    <alias index="17" field="def_shape" name="shape"/>
    <alias index="18" field="def_width" name="width"/>
    <alias index="19" field="def_height" name="height"/>
    <alias index="20" field="def_code" name="code"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="ROWID" applyOnUpdate="0" expression=""/>
    <default field="cul_id" applyOnUpdate="0" expression="if(maximum(cul_id) is null,1, maximum(cul_id)+1)"/>
    <default field="cul_display_name" applyOnUpdate="0" expression="'new'"/>
    <default field="cul_code" applyOnUpdate="0" expression="'new'"/>
    <default field="cul_calculation_type" applyOnUpdate="0" expression="101"/>
    <default field="cul_friction_value" applyOnUpdate="0" expression=""/>
    <default field="cul_friction_type" applyOnUpdate="0" expression="2"/>
    <default field="cul_dist_calc_points" applyOnUpdate="0" expression="10000"/>
    <default field="cul_zoom_category" applyOnUpdate="0" expression="3"/>
    <default field="cul_cross_section_definition_id" applyOnUpdate="0" expression=""/>
    <default field="cul_discharge_coefficient_positive" applyOnUpdate="0" expression="0.8"/>
    <default field="cul_discharge_coefficient_negative" applyOnUpdate="0" expression="0.8"/>
    <default field="cul_invert_level_start_point" applyOnUpdate="0" expression="aggregate('v2_manhole_view','min',&quot;bottom_level&quot;, intersects($geometry,start_point(geometry(@parent)))) "/>
    <default field="cul_invert_level_end_point" applyOnUpdate="0" expression="aggregate('v2_manhole_view','min',&quot;bottom_level&quot;, intersects($geometry,end_point(geometry(@parent)))) "/>
    <default field="cul_connection_node_start_id" applyOnUpdate="0" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))) is null, 'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))))"/>
    <default field="cul_connection_node_end_id" applyOnUpdate="0" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))) is null, 'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))))"/>
    <default field="def_id" applyOnUpdate="0" expression=""/>
    <default field="def_shape" applyOnUpdate="0" expression=""/>
    <default field="def_width" applyOnUpdate="0" expression=""/>
    <default field="def_height" applyOnUpdate="0" expression=""/>
    <default field="def_code" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="ROWID" notnull_strength="0"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="cul_id" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="cul_display_name" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="cul_code" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="cul_calculation_type" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="cul_friction_value" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="cul_friction_type" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="cul_dist_calc_points" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="cul_zoom_category" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="cul_cross_section_definition_id" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="cul_discharge_coefficient_positive" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="cul_discharge_coefficient_negative" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="cul_invert_level_start_point" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="cul_invert_level_end_point" notnull_strength="2"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="cul_connection_node_start_id" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="cul_connection_node_end_id" notnull_strength="0"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="def_id" notnull_strength="2"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="def_shape" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="def_width" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="def_height" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="def_code" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="ROWID" exp=""/>
    <constraint desc="" field="cul_id" exp=""/>
    <constraint desc="" field="cul_display_name" exp=""/>
    <constraint desc="" field="cul_code" exp=""/>
    <constraint desc="" field="cul_calculation_type" exp=""/>
    <constraint desc="" field="cul_friction_value" exp=""/>
    <constraint desc="" field="cul_friction_type" exp=""/>
    <constraint desc="" field="cul_dist_calc_points" exp=""/>
    <constraint desc="" field="cul_zoom_category" exp=""/>
    <constraint desc="" field="cul_cross_section_definition_id" exp=""/>
    <constraint desc="" field="cul_discharge_coefficient_positive" exp=""/>
    <constraint desc="" field="cul_discharge_coefficient_negative" exp=""/>
    <constraint desc="" field="cul_invert_level_start_point" exp=""/>
    <constraint desc="" field="cul_invert_level_end_point" exp=""/>
    <constraint desc="" field="cul_connection_node_start_id" exp=""/>
    <constraint desc="" field="cul_connection_node_end_id" exp=""/>
    <constraint desc="" field="def_id" exp=""/>
    <constraint desc="" field="def_shape" exp=""/>
    <constraint desc="" field="def_width" exp=""/>
    <constraint desc="" field="def_height" exp=""/>
    <constraint desc="" field="def_code" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column width="-1" type="field" hidden="0" name="ROWID"/>
      <column width="-1" type="field" hidden="0" name="cul_id"/>
      <column width="-1" type="field" hidden="0" name="cul_display_name"/>
      <column width="-1" type="field" hidden="0" name="cul_code"/>
      <column width="-1" type="field" hidden="0" name="cul_calculation_type"/>
      <column width="-1" type="field" hidden="0" name="cul_friction_value"/>
      <column width="-1" type="field" hidden="0" name="cul_friction_type"/>
      <column width="-1" type="field" hidden="0" name="cul_dist_calc_points"/>
      <column width="-1" type="field" hidden="0" name="cul_zoom_category"/>
      <column width="-1" type="field" hidden="0" name="cul_cross_section_definition_id"/>
      <column width="-1" type="field" hidden="0" name="cul_discharge_coefficient_positive"/>
      <column width="-1" type="field" hidden="0" name="cul_discharge_coefficient_negative"/>
      <column width="-1" type="field" hidden="0" name="cul_invert_level_start_point"/>
      <column width="-1" type="field" hidden="0" name="cul_invert_level_end_point"/>
      <column width="-1" type="field" hidden="0" name="cul_connection_node_start_id"/>
      <column width="-1" type="field" hidden="0" name="cul_connection_node_end_id"/>
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
    <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="0" name="Culvert view">
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="General">
        <attributeEditorField showLabel="1" index="1" name="cul_id"/>
        <attributeEditorField showLabel="1" index="2" name="cul_display_name"/>
        <attributeEditorField showLabel="1" index="3" name="cul_code"/>
        <attributeEditorField showLabel="1" index="4" name="cul_calculation_type"/>
        <attributeEditorField showLabel="1" index="7" name="cul_dist_calc_points"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Characteristics">
        <attributeEditorField showLabel="1" index="12" name="cul_invert_level_start_point"/>
        <attributeEditorField showLabel="1" index="13" name="cul_invert_level_end_point"/>
        <attributeEditorField showLabel="1" index="6" name="cul_friction_type"/>
        <attributeEditorField showLabel="1" index="5" name="cul_friction_value"/>
        <attributeEditorField showLabel="1" index="10" name="cul_discharge_coefficient_positive"/>
        <attributeEditorField showLabel="1" index="11" name="cul_discharge_coefficient_negative"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Cross section definition">
        <attributeEditorField showLabel="1" index="9" name="cul_cross_section_definition_id"/>
        <attributeEditorField showLabel="1" index="20" name="def_code"/>
        <attributeEditorField showLabel="1" index="17" name="def_shape"/>
        <attributeEditorField showLabel="1" index="18" name="def_width"/>
        <attributeEditorField showLabel="1" index="19" name="def_height"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Visualization">
        <attributeEditorField showLabel="1" index="8" name="cul_zoom_category"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Connection nodes">
        <attributeEditorField showLabel="1" index="14" name="cul_connection_node_start_id"/>
        <attributeEditorField showLabel="1" index="15" name="cul_connection_node_end_id"/>
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
    <field labelOnTop="0" name="ROWID"/>
    <field labelOnTop="0" name="cul_calculation_type"/>
    <field labelOnTop="0" name="cul_code"/>
    <field labelOnTop="0" name="cul_connection_node_end_id"/>
    <field labelOnTop="0" name="cul_connection_node_start_id"/>
    <field labelOnTop="0" name="cul_cross_section_definition_id"/>
    <field labelOnTop="0" name="cul_discharge_coefficient_negative"/>
    <field labelOnTop="0" name="cul_discharge_coefficient_positive"/>
    <field labelOnTop="0" name="cul_display_name"/>
    <field labelOnTop="0" name="cul_dist_calc_points"/>
    <field labelOnTop="0" name="cul_friction_type"/>
    <field labelOnTop="0" name="cul_friction_value"/>
    <field labelOnTop="0" name="cul_id"/>
    <field labelOnTop="0" name="cul_invert_level_end_point"/>
    <field labelOnTop="0" name="cul_invert_level_start_point"/>
    <field labelOnTop="0" name="cul_zoom_category"/>
    <field labelOnTop="0" name="def_code"/>
    <field labelOnTop="0" name="def_height"/>
    <field labelOnTop="0" name="def_id"/>
    <field labelOnTop="0" name="def_shape"/>
    <field labelOnTop="0" name="def_width"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>"ROWID"</previewExpression>
  <mapTip>display_name</mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
