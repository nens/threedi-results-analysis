<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="-4.65661e-10" simplifyDrawingTol="1" simplifyLocal="1" readOnly="0" simplifyDrawingHints="0" version="3.4.5-Madeira" styleCategories="AllStyleCategories" minScale="1e+08" labelsEnabled="0" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" symbollevels="0" forceraster="0" type="RuleRenderer">
    <rules key="{4fbba513-a3b1-4a92-97bc-3d44735ac986}">
      <rule key="{a951db60-faa9-4c95-9eaa-a51d84ff90b1}" label="Inspectieput" scalemaxdenom="2500" filter="manh_manhole_indicator = 0" symbol="0"/>
      <rule key="{c9e7ab73-45d5-45d6-970d-b4e28230c1e5}" label="Uitlaat - boundary" scalemaxdenom="15000" filter="manh_manhole_indicator = 1" symbol="1"/>
      <rule key="{bb971e07-f3e6-48c3-b84b-12496560a739}" label="Uitlaat - connectie met 2d" scalemaxdenom="15000" filter="manh_calculation_type = 0" symbol="2"/>
      <rule key="{a1d98efc-8098-4201-a75e-93dc7c47f076}" label="Gemaalkelder" filter="manh_manhole_indicator = 2" symbol="3"/>
      <rule key="{b15fd57b-e6e4-43b6-8496-7ebf4f15ea68}" label="Inprikpunt" filter="manh_manhole_indicator = 3" symbol="4"/>
      <rule key="{c3de3024-005b-42ac-9705-3bae1dc13053}" label="RWZI" filter="manh_manhole_indicator = 4" symbol="5"/>
    </rules>
    <symbols>
      <symbol alpha="1" clip_to_extent="1" name="0" force_rhr="0" type="marker">
        <layer enabled="1" class="SimpleMarker" pass="0" locked="0">
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" name="1" force_rhr="0" type="marker">
        <layer enabled="1" class="SimpleMarker" pass="0" locked="0">
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" name="2" force_rhr="0" type="marker">
        <layer enabled="1" class="SimpleMarker" pass="0" locked="0">
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" name="3" force_rhr="0" type="marker">
        <layer enabled="1" class="SimpleMarker" pass="0" locked="0">
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" name="4" force_rhr="0" type="marker">
        <layer enabled="1" class="SimpleMarker" pass="0" locked="0">
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" name="5" force_rhr="0" type="marker">
        <layer enabled="1" class="SimpleMarker" pass="0" locked="0">
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
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
    <DiagramCategory minimumSize="0" height="15" scaleDependency="Area" scaleBasedVisibility="0" minScaleDenominator="-4.65661e-10" penWidth="0" labelPlacementMethod="XHeight" opacity="1" width="15" sizeType="MM" enabled="0" lineSizeType="MM" penColor="#000000" maxScaleDenominator="1e+08" rotationOffset="270" sizeScale="3x:0,0,0,0,0,0" diagramOrientation="Up" backgroundAlpha="255" penAlpha="255" barWidth="5" backgroundColor="#ffffff" lineSizeScale="3x:0,0,0,0,0,0">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" color="#000000" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings dist="0" zIndex="0" placement="0" showAll="1" linePlacementFlags="2" priority="0" obstacle="0">
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
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_bottom_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_surface_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_shape">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="00" name="00: square" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="01" name="01: round" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="02" name="02: rectangle" type="QString"/>
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
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_length">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_manhole_indicator">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="0" name="0: Inspection" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="1" name="1: Outlet" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2: Pump" type="QString"/>
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
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="0" name="0: embedded" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="1" name="1: isolated" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2: connected" type="QString"/>
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
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_zoom_category">
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
    <field name="node_initial_waterlevel">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_connection_node_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_storage_area">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="node_the_geom_linestring">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manh_sediment_level">
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
    <alias index="0" name="" field="ROWID"/>
    <alias index="1" name="" field="node_id"/>
    <alias index="2" name="bottom_level" field="manh_bottom_level"/>
    <alias index="3" name="surface_level" field="manh_surface_level"/>
    <alias index="4" name="display_name" field="manh_display_name"/>
    <alias index="5" name="shape" field="manh_shape"/>
    <alias index="6" name="width" field="manh_width"/>
    <alias index="7" name="length" field="manh_length"/>
    <alias index="8" name="manhole_indicator" field="manh_manhole_indicator"/>
    <alias index="9" name="calculation_type" field="manh_calculation_type"/>
    <alias index="10" name="drain_level" field="manh_drain_level"/>
    <alias index="11" name="zoom_category" field="manh_zoom_category"/>
    <alias index="12" name="" field="node_initial_waterlevel"/>
    <alias index="13" name="id" field="manh_id"/>
    <alias index="14" name="connection_node_id" field="manh_connection_node_id"/>
    <alias index="15" name="" field="node_storage_area"/>
    <alias index="16" name="code" field="manh_code"/>
    <alias index="17" name="" field="node_code"/>
    <alias index="18" name="the_geom_linestring" field="node_the_geom_linestring"/>
    <alias index="19" name="sediment_level" field="manh_sediment_level"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" expression="" field="ROWID"/>
    <default applyOnUpdate="0" expression="" field="node_id"/>
    <default applyOnUpdate="0" expression="" field="manh_bottom_level"/>
    <default applyOnUpdate="0" expression="" field="manh_surface_level"/>
    <default applyOnUpdate="0" expression="'new'" field="manh_display_name"/>
    <default applyOnUpdate="0" expression="'00'" field="manh_shape"/>
    <default applyOnUpdate="0" expression="0.8" field="manh_width"/>
    <default applyOnUpdate="0" expression="" field="manh_length"/>
    <default applyOnUpdate="0" expression="'0'" field="manh_manhole_indicator"/>
    <default applyOnUpdate="0" expression="" field="manh_calculation_type"/>
    <default applyOnUpdate="0" expression="" field="manh_drain_level"/>
    <default applyOnUpdate="0" expression="1" field="manh_zoom_category"/>
    <default applyOnUpdate="0" expression="" field="node_initial_waterlevel"/>
    <default applyOnUpdate="0" expression="if(maximum(manh_id) is null,1, maximum(manh_id)+1)" field="manh_id"/>
    <default applyOnUpdate="0" expression="" field="manh_connection_node_id"/>
    <default applyOnUpdate="0" expression="" field="node_storage_area"/>
    <default applyOnUpdate="0" expression="'new'" field="manh_code"/>
    <default applyOnUpdate="0" expression="'new'" field="node_code"/>
    <default applyOnUpdate="0" expression="" field="node_the_geom_linestring"/>
    <default applyOnUpdate="0" expression="" field="manh_sediment_level"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="ROWID"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="node_id"/>
    <constraint exp_strength="0" constraints="1" unique_strength="0" notnull_strength="2" field="manh_bottom_level"/>
    <constraint exp_strength="0" constraints="1" unique_strength="0" notnull_strength="2" field="manh_surface_level"/>
    <constraint exp_strength="0" constraints="1" unique_strength="0" notnull_strength="2" field="manh_display_name"/>
    <constraint exp_strength="0" constraints="1" unique_strength="0" notnull_strength="2" field="manh_shape"/>
    <constraint exp_strength="0" constraints="1" unique_strength="0" notnull_strength="2" field="manh_width"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="manh_length"/>
    <constraint exp_strength="0" constraints="1" unique_strength="0" notnull_strength="2" field="manh_manhole_indicator"/>
    <constraint exp_strength="0" constraints="1" unique_strength="0" notnull_strength="2" field="manh_calculation_type"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="manh_drain_level"/>
    <constraint exp_strength="0" constraints="1" unique_strength="0" notnull_strength="2" field="manh_zoom_category"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="node_initial_waterlevel"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="manh_id"/>
    <constraint exp_strength="0" constraints="1" unique_strength="0" notnull_strength="2" field="manh_connection_node_id"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="node_storage_area"/>
    <constraint exp_strength="0" constraints="1" unique_strength="0" notnull_strength="2" field="manh_code"/>
    <constraint exp_strength="0" constraints="1" unique_strength="0" notnull_strength="2" field="node_code"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="node_the_geom_linestring"/>
    <constraint exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0" field="manh_sediment_level"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="ROWID"/>
    <constraint desc="" exp="" field="node_id"/>
    <constraint desc="" exp="" field="manh_bottom_level"/>
    <constraint desc="" exp="" field="manh_surface_level"/>
    <constraint desc="" exp="" field="manh_display_name"/>
    <constraint desc="" exp="" field="manh_shape"/>
    <constraint desc="" exp="" field="manh_width"/>
    <constraint desc="" exp="" field="manh_length"/>
    <constraint desc="" exp="" field="manh_manhole_indicator"/>
    <constraint desc="" exp="" field="manh_calculation_type"/>
    <constraint desc="" exp="" field="manh_drain_level"/>
    <constraint desc="" exp="" field="manh_zoom_category"/>
    <constraint desc="" exp="" field="node_initial_waterlevel"/>
    <constraint desc="" exp="" field="manh_id"/>
    <constraint desc="" exp="" field="manh_connection_node_id"/>
    <constraint desc="" exp="" field="node_storage_area"/>
    <constraint desc="" exp="" field="manh_code"/>
    <constraint desc="" exp="" field="node_code"/>
    <constraint desc="" exp="" field="node_the_geom_linestring"/>
    <constraint desc="" exp="" field="manh_sediment_level"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortExpression="&quot;manh_id&quot;" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column hidden="0" name="ROWID" width="-1" type="field"/>
      <column hidden="0" name="manh_id" width="-1" type="field"/>
      <column hidden="0" name="manh_display_name" width="-1" type="field"/>
      <column hidden="0" name="manh_code" width="-1" type="field"/>
      <column hidden="0" name="manh_connection_node_id" width="-1" type="field"/>
      <column hidden="0" name="manh_shape" width="-1" type="field"/>
      <column hidden="0" name="manh_width" width="-1" type="field"/>
      <column hidden="0" name="manh_length" width="-1" type="field"/>
      <column hidden="0" name="manh_manhole_indicator" width="-1" type="field"/>
      <column hidden="0" name="manh_calculation_type" width="-1" type="field"/>
      <column hidden="0" name="manh_bottom_level" width="-1" type="field"/>
      <column hidden="0" name="manh_surface_level" width="-1" type="field"/>
      <column hidden="0" name="manh_drain_level" width="-1" type="field"/>
      <column hidden="0" name="manh_sediment_level" width="-1" type="field"/>
      <column hidden="0" name="manh_zoom_category" width="-1" type="field"/>
      <column hidden="0" name="node_id" width="-1" type="field"/>
      <column hidden="0" name="node_storage_area" width="-1" type="field"/>
      <column hidden="0" name="node_initial_waterlevel" width="-1" type="field"/>
      <column hidden="0" name="node_code" width="-1" type="field"/>
      <column hidden="0" name="node_the_geom_linestring" width="-1" type="field"/>
      <column hidden="1" width="-1" type="actions"/>
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
    <attributeEditorContainer showLabel="1" name="Manhole_view" visibilityExpressionEnabled="0" columnCount="1" groupBox="0" visibilityExpression="">
      <attributeEditorContainer showLabel="1" name="General" visibilityExpressionEnabled="0" columnCount="1" groupBox="1" visibilityExpression="">
        <attributeEditorField showLabel="1" index="13" name="manh_id"/>
        <attributeEditorField showLabel="1" index="4" name="manh_display_name"/>
        <attributeEditorField showLabel="1" index="16" name="manh_code"/>
        <attributeEditorField showLabel="1" index="9" name="manh_calculation_type"/>
        <attributeEditorField showLabel="1" index="14" name="manh_connection_node_id"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" name="Characteristics" visibilityExpressionEnabled="0" columnCount="1" groupBox="1" visibilityExpression="">
        <attributeEditorField showLabel="1" index="5" name="manh_shape"/>
        <attributeEditorField showLabel="1" index="6" name="manh_width"/>
        <attributeEditorField showLabel="1" index="7" name="manh_length"/>
        <attributeEditorField showLabel="1" index="2" name="manh_bottom_level"/>
        <attributeEditorField showLabel="1" index="3" name="manh_surface_level"/>
        <attributeEditorField showLabel="1" index="10" name="manh_drain_level"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" name="Visualisation" visibilityExpressionEnabled="0" columnCount="1" groupBox="1" visibilityExpression="">
        <attributeEditorField showLabel="1" index="8" name="manh_manhole_indicator"/>
        <attributeEditorField showLabel="1" index="11" name="manh_zoom_category"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" name="Connection node" visibilityExpressionEnabled="0" columnCount="1" groupBox="1" visibilityExpression="">
        <attributeEditorField showLabel="1" index="1" name="node_id"/>
        <attributeEditorField showLabel="1" index="17" name="node_code"/>
        <attributeEditorField showLabel="1" index="12" name="node_initial_waterlevel"/>
        <attributeEditorField showLabel="1" index="15" name="node_storage_area"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="ROWID" editable="1"/>
    <field name="manh_bottom_level" editable="1"/>
    <field name="manh_calculation_type" editable="1"/>
    <field name="manh_code" editable="1"/>
    <field name="manh_connection_node_id" editable="1"/>
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
    <field name="node_id" editable="1"/>
    <field name="node_initial_waterlevel" editable="1"/>
    <field name="node_storage_area" editable="1"/>
    <field name="node_the_geom_linestring" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="ROWID" labelOnTop="0"/>
    <field name="manh_bottom_level" labelOnTop="0"/>
    <field name="manh_calculation_type" labelOnTop="0"/>
    <field name="manh_code" labelOnTop="0"/>
    <field name="manh_connection_node_id" labelOnTop="0"/>
    <field name="manh_display_name" labelOnTop="0"/>
    <field name="manh_drain_level" labelOnTop="0"/>
    <field name="manh_id" labelOnTop="0"/>
    <field name="manh_length" labelOnTop="0"/>
    <field name="manh_manhole_indicator" labelOnTop="0"/>
    <field name="manh_sediment_level" labelOnTop="0"/>
    <field name="manh_shape" labelOnTop="0"/>
    <field name="manh_surface_level" labelOnTop="0"/>
    <field name="manh_width" labelOnTop="0"/>
    <field name="manh_zoom_category" labelOnTop="0"/>
    <field name="node_code" labelOnTop="0"/>
    <field name="node_id" labelOnTop="0"/>
    <field name="node_initial_waterlevel" labelOnTop="0"/>
    <field name="node_storage_area" labelOnTop="0"/>
    <field name="node_the_geom_linestring" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>manh_display_name</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
