<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" minScale="1e+08" simplifyDrawingHints="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" simplifyMaxScale="1" simplifyAlgorithm="0" simplifyDrawingTol="1" readOnly="0" maxScale="-4.65661e-10" version="3.10.10-A Coruña" labelsEnabled="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" type="singleSymbol" forceraster="0" enableorderby="0">
    <symbols>
      <symbol force_rhr="0" type="line" alpha="1" name="0" clip_to_extent="1">
        <layer locked="0" enabled="1" class="SimpleLine" pass="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="101,101,101,255"/>
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
        <layer locked="0" enabled="1" class="MarkerLine" pass="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="interval" v="3"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="0"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="placement" v="firstvertex"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="coalesce(cul_discharge_coefficient_positive, 0) = 0"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
                <Option type="Map" name="offsetAlongLine">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="0.6667*$length"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" type="marker" alpha="1" name="@0@1" clip_to_extent="1">
            <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
              <prop k="angle" v="180"/>
              <prop k="color" v="255,0,0,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="line"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="101,101,101,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0.8"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="2"/>
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
        <layer locked="0" enabled="1" class="MarkerLine" pass="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="interval" v="3"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="0"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="placement" v="firstvertex"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="coalesce(cul_discharge_coefficient_negative,0) > 0&#xd;&#xa;AND coalesce(cul_discharge_coefficient_positive,0) = 0"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
                <Option type="Map" name="offsetAlongLine">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="0.3333*$length"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" type="marker" alpha="1" name="@0@2" clip_to_extent="1">
            <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
              <prop k="angle" v="180"/>
              <prop k="color" v="255,0,0,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="arrowhead"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="101,101,101,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0.8"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="2"/>
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
        <layer locked="0" enabled="1" class="MarkerLine" pass="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="interval" v="3"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="0"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="placement" v="firstvertex"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="COALESCE(cul_discharge_coefficient_negative, 0) = 0"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
                <Option type="Map" name="offsetAlongLine">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="0.3333*$length"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" type="marker" alpha="1" name="@0@3" clip_to_extent="1">
            <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="255,0,0,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="line"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="101,101,101,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0.8"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="2"/>
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
        <layer locked="0" enabled="1" class="MarkerLine" pass="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="interval" v="3"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="0"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="placement" v="firstvertex"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="enabled">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="COALESCE(cul_discharge_coefficient_positive, 0) > 0&#xd;&#xa;AND COALESCE(cul_discharge_coefficient_negative) = 0"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
                <Option type="Map" name="offsetAlongLine">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="0.66667*$length"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" type="marker" alpha="1" name="@0@4" clip_to_extent="1">
            <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="255,0,0,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="arrowhead"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="101,101,101,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0.8"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="2"/>
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
        <layer locked="0" enabled="1" class="MarkerLine" pass="0">
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
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" type="marker" alpha="1" name="@0@5" clip_to_extent="1">
            <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="101,101,101,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="circle"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="35,35,35,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="2"/>
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
    <property key="dualview/previewExpressions" value="&quot;ROWID&quot;"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Pie" attributeLegend="1">
    <DiagramCategory scaleBasedVisibility="0" backgroundAlpha="255" penWidth="0" sizeType="MM" penAlpha="255" scaleDependency="Area" rotationOffset="270" height="15" minScaleDenominator="-4.65661e-10" maxScaleDenominator="1e+08" barWidth="5" labelPlacementMethod="XHeight" sizeScale="3x:0,0,0,0,0,0" lineSizeType="MM" opacity="1" enabled="0" minimumSize="0" penColor="#000000" width="15" backgroundColor="#ffffff" lineSizeScale="3x:0,0,0,0,0,0" diagramOrientation="Up">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" color="#000000" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings dist="0" obstacle="0" zIndex="0" placement="2" showAll="1" linePlacementFlags="2" priority="0">
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
    <field name="cul_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
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
                <Option type="QString" name="100: embedded" value="100"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="101: isolated" value="101"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="102: connected" value="102"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="105: double connected" value="105"/>
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
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
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
    <field name="cul_dist_calc_points">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
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
    <field name="cul_cross_section_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_discharge_coefficient_positive">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_discharge_coefficient_negative">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_invert_level_start_point">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_invert_level_end_point">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_connection_node_start_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cul_connection_node_end_id">
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
    <alias index="0" name="" field="ROWID"/>
    <alias index="1" name="id" field="cul_id"/>
    <alias index="2" name="display_name" field="cul_display_name"/>
    <alias index="3" name="code" field="cul_code"/>
    <alias index="4" name="calculation_type" field="cul_calculation_type"/>
    <alias index="5" name="friction_value" field="cul_friction_value"/>
    <alias index="6" name="friction_type" field="cul_friction_type"/>
    <alias index="7" name="dist_calc_points" field="cul_dist_calc_points"/>
    <alias index="8" name="zoom_category" field="cul_zoom_category"/>
    <alias index="9" name="cross_section_definition_id" field="cul_cross_section_definition_id"/>
    <alias index="10" name="discharge_coefficient_positive" field="cul_discharge_coefficient_positive"/>
    <alias index="11" name="discharge_coefficient_negative" field="cul_discharge_coefficient_negative"/>
    <alias index="12" name="invert_level_start_point" field="cul_invert_level_start_point"/>
    <alias index="13" name="invert_level_end_point" field="cul_invert_level_end_point"/>
    <alias index="14" name="connection_node_start_id" field="cul_connection_node_start_id"/>
    <alias index="15" name="connection_node_end_id" field="cul_connection_node_end_id"/>
    <alias index="16" name="id" field="def_id"/>
    <alias index="17" name="shape" field="def_shape"/>
    <alias index="18" name="width" field="def_width"/>
    <alias index="19" name="height" field="def_height"/>
    <alias index="20" name="code" field="def_code"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="ROWID"/>
    <default expression="if(maximum(cul_id) is null,1, maximum(cul_id)+1)" applyOnUpdate="0" field="cul_id"/>
    <default expression="'new'" applyOnUpdate="0" field="cul_display_name"/>
    <default expression="'new'" applyOnUpdate="0" field="cul_code"/>
    <default expression="101" applyOnUpdate="0" field="cul_calculation_type"/>
    <default expression="" applyOnUpdate="0" field="cul_friction_value"/>
    <default expression="2" applyOnUpdate="0" field="cul_friction_type"/>
    <default expression="10000" applyOnUpdate="0" field="cul_dist_calc_points"/>
    <default expression="3" applyOnUpdate="0" field="cul_zoom_category"/>
    <default expression="" applyOnUpdate="0" field="cul_cross_section_definition_id"/>
    <default expression="0.8" applyOnUpdate="0" field="cul_discharge_coefficient_positive"/>
    <default expression="0.8" applyOnUpdate="0" field="cul_discharge_coefficient_negative"/>
    <default expression="aggregate('v2_manhole_view','min',&quot;bottom_level&quot;, intersects($geometry,start_point(geometry(@parent)))) " applyOnUpdate="0" field="cul_invert_level_start_point"/>
    <default expression="aggregate('v2_manhole_view','min',&quot;bottom_level&quot;, intersects($geometry,end_point(geometry(@parent)))) " applyOnUpdate="0" field="cul_invert_level_end_point"/>
    <default expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))) is null, 'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))))" applyOnUpdate="0" field="cul_connection_node_start_id"/>
    <default expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))) is null, 'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))))" applyOnUpdate="0" field="cul_connection_node_end_id"/>
    <default expression="" applyOnUpdate="0" field="def_id"/>
    <default expression="" applyOnUpdate="0" field="def_shape"/>
    <default expression="" applyOnUpdate="0" field="def_width"/>
    <default expression="" applyOnUpdate="0" field="def_height"/>
    <default expression="" applyOnUpdate="0" field="def_code"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="ROWID"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_id"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_display_name"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_code"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_calculation_type"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_friction_value"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_friction_type"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_dist_calc_points"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_zoom_category"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_cross_section_definition_id"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_discharge_coefficient_positive"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_discharge_coefficient_negative"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_invert_level_start_point"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="cul_invert_level_end_point"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="cul_connection_node_start_id"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="cul_connection_node_end_id"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="def_id"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="def_shape"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="def_width"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="def_height"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="def_code"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="ROWID"/>
    <constraint desc="" exp="" field="cul_id"/>
    <constraint desc="" exp="" field="cul_display_name"/>
    <constraint desc="" exp="" field="cul_code"/>
    <constraint desc="" exp="" field="cul_calculation_type"/>
    <constraint desc="" exp="" field="cul_friction_value"/>
    <constraint desc="" exp="" field="cul_friction_type"/>
    <constraint desc="" exp="" field="cul_dist_calc_points"/>
    <constraint desc="" exp="" field="cul_zoom_category"/>
    <constraint desc="" exp="" field="cul_cross_section_definition_id"/>
    <constraint desc="" exp="" field="cul_discharge_coefficient_positive"/>
    <constraint desc="" exp="" field="cul_discharge_coefficient_negative"/>
    <constraint desc="" exp="" field="cul_invert_level_start_point"/>
    <constraint desc="" exp="" field="cul_invert_level_end_point"/>
    <constraint desc="" exp="" field="cul_connection_node_start_id"/>
    <constraint desc="" exp="" field="cul_connection_node_end_id"/>
    <constraint desc="" exp="" field="def_id"/>
    <constraint desc="" exp="" field="def_shape"/>
    <constraint desc="" exp="" field="def_width"/>
    <constraint desc="" exp="" field="def_height"/>
    <constraint desc="" exp="" field="def_code"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortExpression="" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column type="field" name="ROWID" hidden="0" width="-1"/>
      <column type="field" name="cul_id" hidden="0" width="-1"/>
      <column type="field" name="cul_display_name" hidden="0" width="-1"/>
      <column type="field" name="cul_code" hidden="0" width="-1"/>
      <column type="field" name="cul_calculation_type" hidden="0" width="-1"/>
      <column type="field" name="cul_friction_value" hidden="0" width="-1"/>
      <column type="field" name="cul_friction_type" hidden="0" width="-1"/>
      <column type="field" name="cul_dist_calc_points" hidden="0" width="-1"/>
      <column type="field" name="cul_zoom_category" hidden="0" width="-1"/>
      <column type="field" name="cul_cross_section_definition_id" hidden="0" width="-1"/>
      <column type="field" name="cul_discharge_coefficient_positive" hidden="0" width="-1"/>
      <column type="field" name="cul_discharge_coefficient_negative" hidden="0" width="-1"/>
      <column type="field" name="cul_invert_level_start_point" hidden="0" width="-1"/>
      <column type="field" name="cul_invert_level_end_point" hidden="0" width="-1"/>
      <column type="field" name="cul_connection_node_start_id" hidden="0" width="-1"/>
      <column type="field" name="cul_connection_node_end_id" hidden="0" width="-1"/>
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
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer groupBox="0" visibilityExpression="" showLabel="1" visibilityExpressionEnabled="0" columnCount="1" name="Culvert view">
      <attributeEditorContainer groupBox="1" visibilityExpression="" showLabel="1" visibilityExpressionEnabled="0" columnCount="1" name="General">
        <attributeEditorField showLabel="1" index="1" name="cul_id"/>
        <attributeEditorField showLabel="1" index="2" name="cul_display_name"/>
        <attributeEditorField showLabel="1" index="3" name="cul_code"/>
        <attributeEditorField showLabel="1" index="4" name="cul_calculation_type"/>
        <attributeEditorField showLabel="1" index="7" name="cul_dist_calc_points"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpression="" showLabel="1" visibilityExpressionEnabled="0" columnCount="1" name="Characteristics">
        <attributeEditorField showLabel="1" index="12" name="cul_invert_level_start_point"/>
        <attributeEditorField showLabel="1" index="13" name="cul_invert_level_end_point"/>
        <attributeEditorField showLabel="1" index="6" name="cul_friction_type"/>
        <attributeEditorField showLabel="1" index="5" name="cul_friction_value"/>
        <attributeEditorField showLabel="1" index="10" name="cul_discharge_coefficient_positive"/>
        <attributeEditorField showLabel="1" index="11" name="cul_discharge_coefficient_negative"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpression="" showLabel="1" visibilityExpressionEnabled="0" columnCount="1" name="Cross section definition">
        <attributeEditorField showLabel="1" index="9" name="cul_cross_section_definition_id"/>
        <attributeEditorField showLabel="1" index="20" name="def_code"/>
        <attributeEditorField showLabel="1" index="17" name="def_shape"/>
        <attributeEditorField showLabel="1" index="18" name="def_width"/>
        <attributeEditorField showLabel="1" index="19" name="def_height"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpression="" showLabel="1" visibilityExpressionEnabled="0" columnCount="1" name="Visualization">
        <attributeEditorField showLabel="1" index="8" name="cul_zoom_category"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpression="" showLabel="1" visibilityExpressionEnabled="0" columnCount="1" name="Connection nodes">
        <attributeEditorField showLabel="1" index="14" name="cul_connection_node_start_id"/>
        <attributeEditorField showLabel="1" index="15" name="cul_connection_node_end_id"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="ROWID"/>
    <field editable="1" name="cul_calculation_type"/>
    <field editable="1" name="cul_code"/>
    <field editable="0" name="cul_connection_node_end_id"/>
    <field editable="0" name="cul_connection_node_start_id"/>
    <field editable="1" name="cul_cross_section_definition_id"/>
    <field editable="1" name="cul_discharge_coefficient_negative"/>
    <field editable="1" name="cul_discharge_coefficient_positive"/>
    <field editable="1" name="cul_display_name"/>
    <field editable="1" name="cul_dist_calc_points"/>
    <field editable="1" name="cul_friction_type"/>
    <field editable="1" name="cul_friction_value"/>
    <field editable="1" name="cul_id"/>
    <field editable="1" name="cul_invert_level_end_point"/>
    <field editable="1" name="cul_invert_level_start_point"/>
    <field editable="1" name="cul_zoom_category"/>
    <field editable="0" name="def_code"/>
    <field editable="0" name="def_height"/>
    <field editable="0" name="def_id"/>
    <field editable="0" name="def_shape"/>
    <field editable="0" name="def_width"/>
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
