<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.4.5-Madeira" labelsEnabled="0" styleCategories="AllStyleCategories" simplifyLocal="1" simplifyMaxScale="1" simplifyDrawingHints="0" simplifyDrawingTol="1" simplifyAlgorithm="0" hasScaleBasedVisibilityFlag="0" maxScale="-4.65661e-10" readOnly="0" minScale="1e+08">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 type="RuleRenderer" forceraster="0" symbollevels="0" enableorderby="0">
    <rules key="{4fbba513-a3b1-4a92-97bc-3d44735ac986}">
      <rule scalemaxdenom="2500" label="Inspectieput" symbol="0" filter="manh_manhole_indicator = 0" key="{a951db60-faa9-4c95-9eaa-a51d84ff90b1}"/>
      <rule scalemaxdenom="15000" label="Uitlaat - boundary" symbol="1" filter="manh_manhole_indicator = 1" key="{c9e7ab73-45d5-45d6-970d-b4e28230c1e5}"/>
      <rule scalemaxdenom="15000" label="Uitlaat - connectie met 2d" symbol="2" filter="manh_calculation_type = 0" key="{bb971e07-f3e6-48c3-b84b-12496560a739}"/>
      <rule label="Gemaalkelder" symbol="3" filter="manh_manhole_indicator = 2" key="{a1d98efc-8098-4201-a75e-93dc7c47f076}"/>
      <rule label="Inprikpunt" symbol="4" filter="manh_manhole_indicator = 3" key="{b15fd57b-e6e4-43b6-8496-7ebf4f15ea68}"/>
      <rule label="RWZI" symbol="5" filter="manh_manhole_indicator = 4" key="{c3de3024-005b-42ac-9705-3bae1dc13053}"/>
    </rules>
    <symbols>
      <symbol type="marker" name="0" force_rhr="0" alpha="1" clip_to_extent="1">
        <layer enabled="1" locked="0" pass="0" class="SimpleMarker">
          <prop k="angle" v="0"/>
          <prop k="color" v="85,255,127,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="1.5"/>
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
      <symbol type="marker" name="1" force_rhr="0" alpha="1" clip_to_extent="1">
        <layer enabled="1" locked="0" pass="0" class="SimpleMarker">
          <prop k="angle" v="0"/>
          <prop k="color" v="170,0,255,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="square"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="1.8"/>
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
      <symbol type="marker" name="2" force_rhr="0" alpha="1" clip_to_extent="1">
        <layer enabled="1" locked="0" pass="0" class="SimpleMarker">
          <prop k="angle" v="0"/>
          <prop k="color" v="254,0,199,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="square"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="1.8"/>
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
      <symbol type="marker" name="3" force_rhr="0" alpha="1" clip_to_extent="1">
        <layer enabled="1" locked="0" pass="0" class="SimpleMarker">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,170,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="pentagon"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
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
      <symbol type="marker" name="4" force_rhr="0" alpha="1" clip_to_extent="1">
        <layer enabled="1" locked="0" pass="0" class="SimpleMarker">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,255,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="pentagon"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
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
      <symbol type="marker" name="5" force_rhr="0" alpha="1" clip_to_extent="1">
        <layer enabled="1" locked="0" pass="0" class="SimpleMarker">
          <prop k="angle" v="0"/>
          <prop k="color" v="85,170,255,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="5"/>
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
    </symbols>
  </renderer-v2>
  <customproperties>
    <property value="manh_display_name" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Pie" attributeLegend="1">
    <DiagramCategory scaleBasedVisibility="0" sizeType="MM" lineSizeType="MM" diagramOrientation="Up" barWidth="5" maxScaleDenominator="1e+08" labelPlacementMethod="XHeight" width="15" penAlpha="255" backgroundAlpha="255" penColor="#000000" penWidth="0" sizeScale="3x:0,0,0,0,0,0" scaleDependency="Area" minimumSize="0" rotationOffset="270" minScaleDenominator="-4.65661e-10" opacity="1" backgroundColor="#ffffff" lineSizeScale="3x:0,0,0,0,0,0" enabled="0" height="15">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute label="" color="#000000" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings zIndex="0" obstacle="0" showAll="1" priority="0" placement="0" dist="0" linePlacementFlags="2">
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
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_bottom_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_surface_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
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
                <Option type="QString" name="00: square" value="00"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="01: round" value="01"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="02: rectangle" value="02"/>
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
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_length">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
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
                <Option type="QString" name="0: inspection" value="0"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="1: outlet" value="1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="2: pump" value="2"/>
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
                <Option type="QString" name="0: embedded" value="0"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="1: isolated" value="1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="2: connected" value="2"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_drain_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
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
    <field name="node_initial_waterlevel">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_connection_node_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_storage_area">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_the_geom_linestring">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_sediment_level">
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
    <alias name="" field="node_id" index="1"/>
    <alias name="bottom_level" field="manh_bottom_level" index="2"/>
    <alias name="surface_level" field="manh_surface_level" index="3"/>
    <alias name="display_name" field="manh_display_name" index="4"/>
    <alias name="shape" field="manh_shape" index="5"/>
    <alias name="width" field="manh_width" index="6"/>
    <alias name="length" field="manh_length" index="7"/>
    <alias name="manhole_indicator" field="manh_manhole_indicator" index="8"/>
    <alias name="calculation_type" field="manh_calculation_type" index="9"/>
    <alias name="drain_level" field="manh_drain_level" index="10"/>
    <alias name="zoom_category" field="manh_zoom_category" index="11"/>
    <alias name="" field="node_initial_waterlevel" index="12"/>
    <alias name="id" field="manh_id" index="13"/>
    <alias name="connection_node_id" field="manh_connection_node_id" index="14"/>
    <alias name="" field="node_storage_area" index="15"/>
    <alias name="code" field="manh_code" index="16"/>
    <alias name="" field="node_code" index="17"/>
    <alias name="the_geom_linestring" field="node_the_geom_linestring" index="18"/>
    <alias name="sediment_level" field="manh_sediment_level" index="19"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="ROWID" applyOnUpdate="0" expression=""/>
    <default field="node_id" applyOnUpdate="0" expression="'filled automatically'"/>
    <default field="manh_bottom_level" applyOnUpdate="0" expression="&quot;manh_bottom_level&quot;&lt;&quot;manh_surface_level&quot;"/>
    <default field="manh_surface_level" applyOnUpdate="0" expression=""/>
    <default field="manh_display_name" applyOnUpdate="0" expression="'new'"/>
    <default field="manh_shape" applyOnUpdate="0" expression="'00'"/>
    <default field="manh_width" applyOnUpdate="0" expression="0.8"/>
    <default field="manh_length" applyOnUpdate="0" expression=""/>
    <default field="manh_manhole_indicator" applyOnUpdate="0" expression="'0'"/>
    <default field="manh_calculation_type" applyOnUpdate="0" expression=""/>
    <default field="manh_drain_level" applyOnUpdate="0" expression=""/>
    <default field="manh_zoom_category" applyOnUpdate="0" expression="1"/>
    <default field="node_initial_waterlevel" applyOnUpdate="0" expression=""/>
    <default field="manh_id" applyOnUpdate="0" expression="if(maximum(manh_id) is null,1, maximum(manh_id)+1)"/>
    <default field="manh_connection_node_id" applyOnUpdate="0" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,geometry(@parent))) is null,'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,geometry(@parent))))"/>
    <default field="node_storage_area" applyOnUpdate="0" expression=""/>
    <default field="manh_code" applyOnUpdate="0" expression="'new'"/>
    <default field="node_code" applyOnUpdate="0" expression="'new'"/>
    <default field="node_the_geom_linestring" applyOnUpdate="0" expression=""/>
    <default field="manh_sediment_level" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="ROWID" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="node_id" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="manh_bottom_level" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="manh_surface_level" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="manh_display_name" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="manh_shape" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="manh_width" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="manh_length" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="manh_manhole_indicator" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="manh_calculation_type" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="manh_drain_level" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="manh_zoom_category" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="node_initial_waterlevel" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="manh_id" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="manh_connection_node_id" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="node_storage_area" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="manh_code" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="node_code" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="node_the_geom_linestring" exp_strength="0"/>
    <constraint constraints="0" unique_strength="0" notnull_strength="0" field="manh_sediment_level" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="ROWID" desc=""/>
    <constraint exp="" field="node_id" desc=""/>
    <constraint exp="" field="manh_bottom_level" desc=""/>
    <constraint exp="" field="manh_surface_level" desc=""/>
    <constraint exp="" field="manh_display_name" desc=""/>
    <constraint exp="" field="manh_shape" desc=""/>
    <constraint exp="" field="manh_width" desc=""/>
    <constraint exp="" field="manh_length" desc=""/>
    <constraint exp="" field="manh_manhole_indicator" desc=""/>
    <constraint exp="" field="manh_calculation_type" desc=""/>
    <constraint exp="" field="manh_drain_level" desc=""/>
    <constraint exp="" field="manh_zoom_category" desc=""/>
    <constraint exp="" field="node_initial_waterlevel" desc=""/>
    <constraint exp="" field="manh_id" desc=""/>
    <constraint exp="" field="manh_connection_node_id" desc=""/>
    <constraint exp="" field="node_storage_area" desc=""/>
    <constraint exp="" field="manh_code" desc=""/>
    <constraint exp="" field="node_code" desc=""/>
    <constraint exp="" field="node_the_geom_linestring" desc=""/>
    <constraint exp="" field="manh_sediment_level" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="&quot;manh_id&quot;" sortOrder="0">
    <columns>
      <column type="field" name="ROWID" width="-1" hidden="0"/>
      <column type="field" name="manh_id" width="-1" hidden="0"/>
      <column type="field" name="manh_display_name" width="-1" hidden="0"/>
      <column type="field" name="manh_code" width="-1" hidden="0"/>
      <column type="field" name="manh_connection_node_id" width="-1" hidden="0"/>
      <column type="field" name="manh_shape" width="-1" hidden="0"/>
      <column type="field" name="manh_width" width="-1" hidden="0"/>
      <column type="field" name="manh_length" width="-1" hidden="0"/>
      <column type="field" name="manh_manhole_indicator" width="-1" hidden="0"/>
      <column type="field" name="manh_calculation_type" width="-1" hidden="0"/>
      <column type="field" name="manh_bottom_level" width="-1" hidden="0"/>
      <column type="field" name="manh_surface_level" width="-1" hidden="0"/>
      <column type="field" name="manh_drain_level" width="-1" hidden="0"/>
      <column type="field" name="manh_sediment_level" width="-1" hidden="0"/>
      <column type="field" name="manh_zoom_category" width="-1" hidden="0"/>
      <column type="field" name="node_id" width="-1" hidden="0"/>
      <column type="field" name="node_storage_area" width="-1" hidden="0"/>
      <column type="field" name="node_initial_waterlevel" width="-1" hidden="0"/>
      <column type="field" name="node_code" width="-1" hidden="0"/>
      <column type="field" name="node_the_geom_linestring" width="-1" hidden="0"/>
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
    <attributeEditorContainer columnCount="1" visibilityExpression="" name="Manhole_view" groupBox="0" visibilityExpressionEnabled="0" showLabel="1">
      <attributeEditorContainer columnCount="1" visibilityExpression="" name="General" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="manh_id" index="13" showLabel="1"/>
        <attributeEditorField name="manh_display_name" index="4" showLabel="1"/>
        <attributeEditorField name="manh_code" index="16" showLabel="1"/>
        <attributeEditorField name="manh_calculation_type" index="9" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" visibilityExpression="" name="Characteristics" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="manh_shape" index="5" showLabel="1"/>
        <attributeEditorField name="manh_width" index="6" showLabel="1"/>
        <attributeEditorField name="manh_length" index="7" showLabel="1"/>
        <attributeEditorField name="manh_bottom_level" index="2" showLabel="1"/>
        <attributeEditorField name="manh_surface_level" index="3" showLabel="1"/>
        <attributeEditorField name="manh_drain_level" index="10" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" visibilityExpression="" name="Visualisation" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="manh_manhole_indicator" index="8" showLabel="1"/>
        <attributeEditorField name="manh_zoom_category" index="11" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" visibilityExpression="" name="Connection node" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
        <attributeEditorField name="manh_connection_node_id" index="14" showLabel="1"/>
        <attributeEditorField name="node_code" index="17" showLabel="1"/>
        <attributeEditorField name="node_initial_waterlevel" index="12" showLabel="1"/>
        <attributeEditorField name="node_storage_area" index="15" showLabel="1"/>
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
  <previewExpression>manh_display_name</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
