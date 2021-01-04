<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" labelsEnabled="0" simplifyAlgorithm="0" simplifyMaxScale="1" version="3.10.10-A Coruña" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="1e+08" simplifyDrawingTol="1" simplifyDrawingHints="0" maxScale="-4.65661e-10" simplifyLocal="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" type="RuleRenderer" symbollevels="0" forceraster="0">
    <rules key="{4fbba513-a3b1-4a92-97bc-3d44735ac986}">
      <rule key="{a951db60-faa9-4c95-9eaa-a51d84ff90b1}" filter="manh_manhole_indicator = 0" symbol="0" scalemaxdenom="2500" label="Manhole (inspection)"/>
      <rule key="{c9e7ab73-45d5-45d6-970d-b4e28230c1e5}" filter="manh_manhole_indicator = 1" symbol="1" scalemaxdenom="15000" label="Outlet"/>
      <rule key="{a1d98efc-8098-4201-a75e-93dc7c47f076}" filter="manh_manhole_indicator = 2" symbol="2" label="Pumping station"/>
      <rule key="{1b6d21ed-8a83-4e3f-850e-ca64e766f7da}" filter="ELSE" symbol="3" scalemaxdenom="2500" label="Manhole (unspecified)"/>
    </rules>
    <symbols>
      <symbol force_rhr="0" type="marker" clip_to_extent="1" name="0" alpha="1">
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
          <prop v="0" k="angle"/>
          <prop v="85,255,127,0" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="square" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
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
      <symbol force_rhr="0" type="marker" clip_to_extent="1" name="1" alpha="1">
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
          <prop v="0" k="angle"/>
          <prop v="85,255,127,0" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="miter" k="joinstyle"/>
          <prop v="square" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="85,170,255,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.75" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="2.5" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <effect enabled="1" type="effectStack">
            <effect type="dropShadow">
              <prop v="13" k="blend_mode"/>
              <prop v="0.5" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="2" k="draw_mode"/>
              <prop v="1" k="enabled"/>
              <prop v="135" k="offset_angle"/>
              <prop v="0.2" k="offset_distance"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="outerGlow">
              <prop v="0" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,255,255" k="color1"/>
              <prop v="0,255,0,255" k="color2"/>
              <prop v="0" k="color_type"/>
              <prop v="0" k="discrete"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="0.5" k="opacity"/>
              <prop v="gradient" k="rampType"/>
              <prop v="255,255,255,255" k="single_color"/>
              <prop v="2" k="spread"/>
              <prop v="MM" k="spread_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="spread_unit_scale"/>
            </effect>
            <effect type="drawSource">
              <prop v="0" k="blend_mode"/>
              <prop v="2" k="draw_mode"/>
              <prop v="1" k="enabled"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="innerShadow">
              <prop v="13" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="135" k="offset_angle"/>
              <prop v="2" k="offset_distance"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="innerGlow">
              <prop v="0" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,255,255" k="color1"/>
              <prop v="0,255,0,255" k="color2"/>
              <prop v="0" k="color_type"/>
              <prop v="0" k="discrete"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="0.5" k="opacity"/>
              <prop v="gradient" k="rampType"/>
              <prop v="255,255,255,255" k="single_color"/>
              <prop v="2" k="spread"/>
              <prop v="MM" k="spread_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="spread_unit_scale"/>
            </effect>
          </effect>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="marker" clip_to_extent="1" name="2" alpha="1">
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
          <prop v="0" k="angle"/>
          <prop v="85,255,127,0" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="pentagon" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="255,127,0,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.7" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="4" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <effect enabled="1" type="effectStack">
            <effect type="dropShadow">
              <prop v="13" k="blend_mode"/>
              <prop v="0.5" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="2" k="draw_mode"/>
              <prop v="1" k="enabled"/>
              <prop v="135" k="offset_angle"/>
              <prop v="0.2" k="offset_distance"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="outerGlow">
              <prop v="0" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,255,255" k="color1"/>
              <prop v="0,255,0,255" k="color2"/>
              <prop v="0" k="color_type"/>
              <prop v="0" k="discrete"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="0.5" k="opacity"/>
              <prop v="gradient" k="rampType"/>
              <prop v="255,255,255,255" k="single_color"/>
              <prop v="2" k="spread"/>
              <prop v="MM" k="spread_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="spread_unit_scale"/>
            </effect>
            <effect type="drawSource">
              <prop v="0" k="blend_mode"/>
              <prop v="2" k="draw_mode"/>
              <prop v="1" k="enabled"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="innerShadow">
              <prop v="13" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="135" k="offset_angle"/>
              <prop v="2" k="offset_distance"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
              <prop v="1" k="opacity"/>
            </effect>
            <effect type="innerGlow">
              <prop v="0" k="blend_mode"/>
              <prop v="2.645" k="blur_level"/>
              <prop v="MM" k="blur_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="blur_unit_scale"/>
              <prop v="0,0,255,255" k="color1"/>
              <prop v="0,255,0,255" k="color2"/>
              <prop v="0" k="color_type"/>
              <prop v="0" k="discrete"/>
              <prop v="2" k="draw_mode"/>
              <prop v="0" k="enabled"/>
              <prop v="0.5" k="opacity"/>
              <prop v="gradient" k="rampType"/>
              <prop v="255,255,255,255" k="single_color"/>
              <prop v="2" k="spread"/>
              <prop v="MM" k="spread_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="spread_unit_scale"/>
            </effect>
          </effect>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="marker" clip_to_extent="1" name="3" alpha="1">
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
          <prop v="0" k="angle"/>
          <prop v="85,255,127,0" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="square" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="255,9,1,255" k="outline_color"/>
          <prop v="dot" k="outline_style"/>
          <prop v="0.25" k="outline_width"/>
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
    </symbols>
  </renderer-v2>
  <customproperties>
    <property key="dualview/previewExpressions" value="manh_display_name"/>
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
  <DiagramLayerSettings dist="0" linePlacementFlags="2" obstacle="0" zIndex="0" priority="0" placement="0" showAll="1">
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
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_connection_node_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_shape">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="00" type="QString" name="00: square"/>
              </Option>
              <Option type="Map">
                <Option value="01" type="QString" name="01: round"/>
              </Option>
              <Option type="Map">
                <Option value="02" type="QString" name="02: rectangle"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_width">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_length">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_manhole_indicator">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="0: inspection"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1: outlet"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: pump"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_calculation_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="0: embedded"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1: isolated"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: connected"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_bottom_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_surface_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_drain_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_sediment_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_zoom_category">
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
    <field name="node_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_storage_area">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_initial_waterlevel">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_the_geom_linestring">
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
    <alias index="1" field="manh_id" name="id"/>
    <alias index="2" field="manh_display_name" name="display_name"/>
    <alias index="3" field="manh_code" name="code"/>
    <alias index="4" field="manh_connection_node_id" name="connection_node_id"/>
    <alias index="5" field="manh_shape" name="shape"/>
    <alias index="6" field="manh_width" name="width"/>
    <alias index="7" field="manh_length" name="length"/>
    <alias index="8" field="manh_manhole_indicator" name="manhole_indicator"/>
    <alias index="9" field="manh_calculation_type" name="calculation_type"/>
    <alias index="10" field="manh_bottom_level" name="bottom_level"/>
    <alias index="11" field="manh_surface_level" name="surface_level"/>
    <alias index="12" field="manh_drain_level" name="drain_level"/>
    <alias index="13" field="manh_sediment_level" name="sediment_level"/>
    <alias index="14" field="manh_zoom_category" name="zoom_category"/>
    <alias index="15" field="node_id" name=""/>
    <alias index="16" field="node_storage_area" name=""/>
    <alias index="17" field="node_initial_waterlevel" name=""/>
    <alias index="18" field="node_code" name=""/>
    <alias index="19" field="node_the_geom_linestring" name="the_geom_linestring"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="ROWID" applyOnUpdate="0" expression=""/>
    <default field="manh_id" applyOnUpdate="0" expression="if(maximum(manh_id) is null,1, maximum(manh_id)+1)"/>
    <default field="manh_display_name" applyOnUpdate="0" expression="'new'"/>
    <default field="manh_code" applyOnUpdate="0" expression="'new'"/>
    <default field="manh_connection_node_id" applyOnUpdate="0" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,geometry(@parent))) is null,'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,geometry(@parent))))"/>
    <default field="manh_shape" applyOnUpdate="0" expression=""/>
    <default field="manh_width" applyOnUpdate="0" expression=""/>
    <default field="manh_length" applyOnUpdate="0" expression=""/>
    <default field="manh_manhole_indicator" applyOnUpdate="0" expression="'0'"/>
    <default field="manh_calculation_type" applyOnUpdate="0" expression=""/>
    <default field="manh_bottom_level" applyOnUpdate="0" expression="&quot;manh_bottom_level&quot;&lt;&quot;manh_surface_level&quot;"/>
    <default field="manh_surface_level" applyOnUpdate="0" expression=""/>
    <default field="manh_drain_level" applyOnUpdate="0" expression=""/>
    <default field="manh_sediment_level" applyOnUpdate="0" expression=""/>
    <default field="manh_zoom_category" applyOnUpdate="0" expression="1"/>
    <default field="node_id" applyOnUpdate="0" expression="'filled automatically'"/>
    <default field="node_storage_area" applyOnUpdate="0" expression=""/>
    <default field="node_initial_waterlevel" applyOnUpdate="0" expression=""/>
    <default field="node_code" applyOnUpdate="0" expression="'new'"/>
    <default field="node_the_geom_linestring" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="ROWID" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="manh_id" notnull_strength="0"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="manh_display_name" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="manh_code" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="manh_connection_node_id" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="manh_shape" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="manh_width" notnull_strength="2"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="manh_length" notnull_strength="0"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="manh_manhole_indicator" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="manh_calculation_type" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="manh_bottom_level" notnull_strength="2"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="manh_surface_level" notnull_strength="2"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="manh_drain_level" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="manh_sediment_level" notnull_strength="0"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="manh_zoom_category" notnull_strength="2"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="node_id" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="node_storage_area" notnull_strength="0"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="node_initial_waterlevel" notnull_strength="0"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" field="node_code" notnull_strength="2"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" field="node_the_geom_linestring" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="ROWID" exp=""/>
    <constraint desc="" field="manh_id" exp=""/>
    <constraint desc="" field="manh_display_name" exp=""/>
    <constraint desc="" field="manh_code" exp=""/>
    <constraint desc="" field="manh_connection_node_id" exp=""/>
    <constraint desc="" field="manh_shape" exp=""/>
    <constraint desc="" field="manh_width" exp=""/>
    <constraint desc="" field="manh_length" exp=""/>
    <constraint desc="" field="manh_manhole_indicator" exp=""/>
    <constraint desc="" field="manh_calculation_type" exp=""/>
    <constraint desc="" field="manh_bottom_level" exp=""/>
    <constraint desc="" field="manh_surface_level" exp=""/>
    <constraint desc="" field="manh_drain_level" exp=""/>
    <constraint desc="" field="manh_sediment_level" exp=""/>
    <constraint desc="" field="manh_zoom_category" exp=""/>
    <constraint desc="" field="node_id" exp=""/>
    <constraint desc="" field="node_storage_area" exp=""/>
    <constraint desc="" field="node_initial_waterlevel" exp=""/>
    <constraint desc="" field="node_code" exp=""/>
    <constraint desc="" field="node_the_geom_linestring" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="&quot;manh_manhole_indicator&quot;">
    <columns>
      <column width="-1" type="field" hidden="0" name="ROWID"/>
      <column width="-1" type="field" hidden="0" name="manh_id"/>
      <column width="-1" type="field" hidden="0" name="manh_display_name"/>
      <column width="-1" type="field" hidden="0" name="manh_code"/>
      <column width="-1" type="field" hidden="0" name="manh_connection_node_id"/>
      <column width="-1" type="field" hidden="0" name="manh_shape"/>
      <column width="-1" type="field" hidden="0" name="manh_width"/>
      <column width="-1" type="field" hidden="0" name="manh_length"/>
      <column width="-1" type="field" hidden="0" name="manh_manhole_indicator"/>
      <column width="-1" type="field" hidden="0" name="manh_calculation_type"/>
      <column width="-1" type="field" hidden="0" name="manh_bottom_level"/>
      <column width="-1" type="field" hidden="0" name="manh_surface_level"/>
      <column width="-1" type="field" hidden="0" name="manh_drain_level"/>
      <column width="-1" type="field" hidden="0" name="manh_sediment_level"/>
      <column width="-1" type="field" hidden="0" name="manh_zoom_category"/>
      <column width="-1" type="field" hidden="0" name="node_id"/>
      <column width="-1" type="field" hidden="0" name="node_storage_area"/>
      <column width="-1" type="field" hidden="0" name="node_initial_waterlevel"/>
      <column width="-1" type="field" hidden="0" name="node_code"/>
      <column width="-1" type="field" hidden="0" name="node_the_geom_linestring"/>
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
    <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="0" name="Manhole_view">
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="General">
        <attributeEditorField showLabel="1" index="1" name="manh_id"/>
        <attributeEditorField showLabel="1" index="2" name="manh_display_name"/>
        <attributeEditorField showLabel="1" index="3" name="manh_code"/>
        <attributeEditorField showLabel="1" index="9" name="manh_calculation_type"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Characteristics">
        <attributeEditorField showLabel="1" index="5" name="manh_shape"/>
        <attributeEditorField showLabel="1" index="6" name="manh_width"/>
        <attributeEditorField showLabel="1" index="7" name="manh_length"/>
        <attributeEditorField showLabel="1" index="10" name="manh_bottom_level"/>
        <attributeEditorField showLabel="1" index="11" name="manh_surface_level"/>
        <attributeEditorField showLabel="1" index="12" name="manh_drain_level"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Visualisation">
        <attributeEditorField showLabel="1" index="8" name="manh_manhole_indicator"/>
        <attributeEditorField showLabel="1" index="14" name="manh_zoom_category"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Connection node">
        <attributeEditorField showLabel="1" index="4" name="manh_connection_node_id"/>
        <attributeEditorField showLabel="1" index="18" name="node_code"/>
        <attributeEditorField showLabel="1" index="17" name="node_initial_waterlevel"/>
        <attributeEditorField showLabel="1" index="16" name="node_storage_area"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="ROWID" editable="1"/>
    <field name="manh_bottom_level" editable="1"/>
    <field name="manh_calculation_type" editable="1"/>
    <field name="manh_code" editable="1"/>
    <field name="manh_connection_node_id" editable="0"/>
    <field name="manh_display_name" editable="1"/>
    <field name="manh_drain_level" editable="1"/>
    <field name="manh_id" editable="0"/>
    <field name="manh_length" editable="1"/>
    <field name="manh_manhole_indicator" editable="1"/>
    <field name="manh_sediment_level" editable="1"/>
    <field name="manh_shape" editable="1"/>
    <field name="manh_surface_level" editable="1"/>
    <field name="manh_width" editable="1"/>
    <field name="manh_zoom_category" editable="1"/>
    <field name="node_code" editable="1"/>
    <field name="node_id" editable="0"/>
    <field name="node_initial_waterlevel" editable="1"/>
    <field name="node_storage_area" editable="1"/>
    <field name="node_the_geom_linestring" editable="1"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="ROWID"/>
    <field labelOnTop="0" name="manh_bottom_level"/>
    <field labelOnTop="0" name="manh_calculation_type"/>
    <field labelOnTop="0" name="manh_code"/>
    <field labelOnTop="0" name="manh_connection_node_id"/>
    <field labelOnTop="0" name="manh_display_name"/>
    <field labelOnTop="0" name="manh_drain_level"/>
    <field labelOnTop="0" name="manh_id"/>
    <field labelOnTop="0" name="manh_length"/>
    <field labelOnTop="0" name="manh_manhole_indicator"/>
    <field labelOnTop="0" name="manh_sediment_level"/>
    <field labelOnTop="0" name="manh_shape"/>
    <field labelOnTop="0" name="manh_surface_level"/>
    <field labelOnTop="0" name="manh_width"/>
    <field labelOnTop="0" name="manh_zoom_category"/>
    <field labelOnTop="0" name="node_code"/>
    <field labelOnTop="0" name="node_id"/>
    <field labelOnTop="0" name="node_initial_waterlevel"/>
    <field labelOnTop="0" name="node_storage_area"/>
    <field labelOnTop="0" name="node_the_geom_linestring"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>"manh_display_name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
