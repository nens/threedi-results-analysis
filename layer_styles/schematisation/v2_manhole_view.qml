<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" simplifyDrawingTol="1" version="3.4.5-Madeira" simplifyAlgorithm="0" simplifyMaxScale="1" maxScale="-4.65661e-10" labelsEnabled="0" simplifyDrawingHints="0" simplifyLocal="1" styleCategories="AllStyleCategories" minScale="1e+08" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" type="RuleRenderer" forceraster="0" symbollevels="0">
    <rules key="{4fbba513-a3b1-4a92-97bc-3d44735ac986}">
      <rule key="{a951db60-faa9-4c95-9eaa-a51d84ff90b1}" symbol="0" scalemaxdenom="2500" label="Inspectieput" filter="manh_manhole_indicator = 0"/>
      <rule key="{c9e7ab73-45d5-45d6-970d-b4e28230c1e5}" symbol="1" scalemaxdenom="15000" label="Uitlaat - boundary" filter="manh_manhole_indicator = 1"/>
      <rule key="{bb971e07-f3e6-48c3-b84b-12496560a739}" symbol="2" scalemaxdenom="15000" label="Uitlaat - connectie met 2d" filter="manh_calculation_type = 0"/>
      <rule key="{a1d98efc-8098-4201-a75e-93dc7c47f076}" symbol="3" label="Gemaalkelder" filter="manh_manhole_indicator = 2"/>
      <rule key="{b15fd57b-e6e4-43b6-8496-7ebf4f15ea68}" symbol="4" label="Inprikpunt" filter="manh_manhole_indicator = 3"/>
      <rule key="{c3de3024-005b-42ac-9705-3bae1dc13053}" symbol="5" label="RWZI" filter="manh_manhole_indicator = 4"/>
    </rules>
    <symbols>
      <symbol clip_to_extent="1" force_rhr="0" type="marker" alpha="1" name="0">
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
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
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" force_rhr="0" type="marker" alpha="1" name="1">
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
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
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" force_rhr="0" type="marker" alpha="1" name="2">
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
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
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" force_rhr="0" type="marker" alpha="1" name="3">
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
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
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" force_rhr="0" type="marker" alpha="1" name="4">
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
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
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" force_rhr="0" type="marker" alpha="1" name="5">
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
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
    <property value="manh_display_name" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Pie">
    <DiagramCategory opacity="1" lineSizeType="MM" backgroundColor="#ffffff" penColor="#000000" barWidth="5" sizeType="MM" penAlpha="255" minScaleDenominator="-4.65661e-10" scaleBasedVisibility="0" diagramOrientation="Up" lineSizeScale="3x:0,0,0,0,0,0" labelPlacementMethod="XHeight" sizeScale="3x:0,0,0,0,0,0" minimumSize="0" height="15" maxScaleDenominator="1e+08" penWidth="0" backgroundAlpha="255" width="15" enabled="0" scaleDependency="Area" rotationOffset="270">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute color="#000000" label="" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings dist="0" priority="0" linePlacementFlags="2" obstacle="0" showAll="1" placement="0" zIndex="0">
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
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
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
    <default expression="" applyOnUpdate="0" field="ROWID"/>
    <default expression="'filled automatically'" applyOnUpdate="0" field="node_id"/>
    <default expression="&quot;manh_bottom_level&quot;&lt;&quot;manh_surface_level&quot;" applyOnUpdate="0" field="manh_bottom_level"/>
    <default expression="" applyOnUpdate="0" field="manh_surface_level"/>
    <default expression="'new'" applyOnUpdate="0" field="manh_display_name"/>
    <default expression="'00'" applyOnUpdate="0" field="manh_shape"/>
    <default expression="0.8" applyOnUpdate="0" field="manh_width"/>
    <default expression="" applyOnUpdate="0" field="manh_length"/>
    <default expression="'0'" applyOnUpdate="0" field="manh_manhole_indicator"/>
    <default expression="" applyOnUpdate="0" field="manh_calculation_type"/>
    <default expression="" applyOnUpdate="0" field="manh_drain_level"/>
    <default expression="1" applyOnUpdate="0" field="manh_zoom_category"/>
    <default expression="" applyOnUpdate="0" field="node_initial_waterlevel"/>
    <default expression="if(maximum(manh_id) is null,1, maximum(manh_id)+1)" applyOnUpdate="0" field="manh_id"/>
    <default expression="'filled automatically'" applyOnUpdate="0" field="manh_connection_node_id"/>
    <default expression="" applyOnUpdate="0" field="node_storage_area"/>
    <default expression="'new'" applyOnUpdate="0" field="manh_code"/>
    <default expression="'new'" applyOnUpdate="0" field="node_code"/>
    <default expression="" applyOnUpdate="0" field="node_the_geom_linestring"/>
    <default expression="" applyOnUpdate="0" field="manh_sediment_level"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="ROWID"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="node_id"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="manh_bottom_level"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="manh_surface_level"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="manh_display_name"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="manh_shape"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="manh_width"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="manh_length"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="manh_manhole_indicator"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="manh_calculation_type"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="manh_drain_level"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="manh_zoom_category"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="node_initial_waterlevel"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="manh_id"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="manh_connection_node_id"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="node_storage_area"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="manh_code"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="node_code"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="node_the_geom_linestring"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="manh_sediment_level"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="ROWID"/>
    <constraint exp="" desc="" field="node_id"/>
    <constraint exp="" desc="" field="manh_bottom_level"/>
    <constraint exp="" desc="" field="manh_surface_level"/>
    <constraint exp="" desc="" field="manh_display_name"/>
    <constraint exp="" desc="" field="manh_shape"/>
    <constraint exp="" desc="" field="manh_width"/>
    <constraint exp="" desc="" field="manh_length"/>
    <constraint exp="" desc="" field="manh_manhole_indicator"/>
    <constraint exp="" desc="" field="manh_calculation_type"/>
    <constraint exp="" desc="" field="manh_drain_level"/>
    <constraint exp="" desc="" field="manh_zoom_category"/>
    <constraint exp="" desc="" field="node_initial_waterlevel"/>
    <constraint exp="" desc="" field="manh_id"/>
    <constraint exp="" desc="" field="manh_connection_node_id"/>
    <constraint exp="" desc="" field="node_storage_area"/>
    <constraint exp="" desc="" field="manh_code"/>
    <constraint exp="" desc="" field="node_code"/>
    <constraint exp="" desc="" field="node_the_geom_linestring"/>
    <constraint exp="" desc="" field="manh_sediment_level"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="&quot;manh_id&quot;">
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
    <attributeEditorContainer groupBox="0" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" name="Manhole_view" columnCount="1">
      <attributeEditorContainer groupBox="1" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" name="General" columnCount="1">
        <attributeEditorField showLabel="1" name="manh_id" index="13"/>
        <attributeEditorField showLabel="1" name="manh_display_name" index="4"/>
        <attributeEditorField showLabel="1" name="manh_code" index="16"/>
        <attributeEditorField showLabel="1" name="manh_calculation_type" index="9"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" name="Characteristics" columnCount="1">
        <attributeEditorField showLabel="1" name="manh_shape" index="5"/>
        <attributeEditorField showLabel="1" name="manh_width" index="6"/>
        <attributeEditorField showLabel="1" name="manh_length" index="7"/>
        <attributeEditorField showLabel="1" name="manh_bottom_level" index="2"/>
        <attributeEditorField showLabel="1" name="manh_surface_level" index="3"/>
        <attributeEditorField showLabel="1" name="manh_drain_level" index="10"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" name="Visualisation" columnCount="1">
        <attributeEditorField showLabel="1" name="manh_manhole_indicator" index="8"/>
        <attributeEditorField showLabel="1" name="manh_zoom_category" index="11"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" name="Connection node" columnCount="1">
        <attributeEditorField showLabel="1" name="manh_connection_node_id" index="14"/>
        <attributeEditorField showLabel="1" name="node_code" index="17"/>
        <attributeEditorField showLabel="1" name="node_initial_waterlevel" index="12"/>
        <attributeEditorField showLabel="1" name="node_storage_area" index="15"/>
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
