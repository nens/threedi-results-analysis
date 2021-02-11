<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" minScale="1e+08" simplifyDrawingHints="0" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" simplifyMaxScale="1" simplifyAlgorithm="0" simplifyDrawingTol="1" readOnly="0" maxScale="-4.65661e-10" version="3.10.10-A Coruña" labelsEnabled="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" type="RuleRenderer" forceraster="0" enableorderby="0">
    <rules key="{4fbba513-a3b1-4a92-97bc-3d44735ac986}">
      <rule label="Manhole (inspection)" key="{a951db60-faa9-4c95-9eaa-a51d84ff90b1}" filter="manh_manhole_indicator = 0" scalemaxdenom="5000" symbol="0"/>
      <rule label="Outlet" key="{c9e7ab73-45d5-45d6-970d-b4e28230c1e5}" filter="manh_manhole_indicator = 1" scalemaxdenom="15000" symbol="1"/>
      <rule label="Pumping station" key="{a1d98efc-8098-4201-a75e-93dc7c47f076}" filter="manh_manhole_indicator = 2" symbol="2"/>
      <rule label="Manhole (unspecified)" key="{1b6d21ed-8a83-4e3f-850e-ca64e766f7da}" filter="ELSE" scalemaxdenom="5000" symbol="3"/>
    </rules>
    <symbols>
      <symbol force_rhr="0" type="marker" alpha="1" name="0" clip_to_extent="1">
        <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,255,255,255"/>
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
      <symbol force_rhr="0" type="marker" alpha="1" name="1" clip_to_extent="1">
        <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="63,128,192,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="miter"/>
          <prop k="name" v="square"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="85,170,255,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.75"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="2.5"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <effect enabled="0" type="effectStack">
            <effect type="dropShadow">
              <prop k="blend_mode" v="13"/>
              <prop k="blur_level" v="0.5"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color" v="0,0,0,255"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="1"/>
              <prop k="offset_angle" v="135"/>
              <prop k="offset_distance" v="0.2"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="offset_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="opacity" v="1"/>
            </effect>
            <effect type="outerGlow">
              <prop k="blend_mode" v="0"/>
              <prop k="blur_level" v="2.645"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color1" v="0,0,255,255"/>
              <prop k="color2" v="0,255,0,255"/>
              <prop k="color_type" v="0"/>
              <prop k="discrete" v="0"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="0"/>
              <prop k="opacity" v="0.5"/>
              <prop k="rampType" v="gradient"/>
              <prop k="single_color" v="255,255,255,255"/>
              <prop k="spread" v="2"/>
              <prop k="spread_unit" v="MM"/>
              <prop k="spread_unit_scale" v="3x:0,0,0,0,0,0"/>
            </effect>
            <effect type="drawSource">
              <prop k="blend_mode" v="0"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="1"/>
              <prop k="opacity" v="1"/>
            </effect>
            <effect type="innerShadow">
              <prop k="blend_mode" v="13"/>
              <prop k="blur_level" v="2.645"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color" v="0,0,0,255"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="0"/>
              <prop k="offset_angle" v="135"/>
              <prop k="offset_distance" v="2"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="offset_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="opacity" v="1"/>
            </effect>
            <effect type="innerGlow">
              <prop k="blend_mode" v="0"/>
              <prop k="blur_level" v="2.645"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color1" v="0,0,255,255"/>
              <prop k="color2" v="0,255,0,255"/>
              <prop k="color_type" v="0"/>
              <prop k="discrete" v="0"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="0"/>
              <prop k="opacity" v="0.5"/>
              <prop k="rampType" v="gradient"/>
              <prop k="single_color" v="255,255,255,255"/>
              <prop k="spread" v="2"/>
              <prop k="spread_unit" v="MM"/>
              <prop k="spread_unit_scale" v="3x:0,0,0,0,0,0"/>
            </effect>
          </effect>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="if(@map_scale&lt;10000, 2.5,1.5)"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="marker" alpha="1" name="2" clip_to_extent="1">
        <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="85,255,127,0"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="pentagon"/>
          <prop k="offset" v="0.10000000000000001,0.10000000000000001"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,183"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.7"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="4.1"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <effect enabled="0" type="effectStack">
            <effect type="dropShadow">
              <prop k="blend_mode" v="13"/>
              <prop k="blur_level" v="0.5"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color" v="0,0,0,255"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="1"/>
              <prop k="offset_angle" v="135"/>
              <prop k="offset_distance" v="0.2"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="offset_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="opacity" v="1"/>
            </effect>
            <effect type="outerGlow">
              <prop k="blend_mode" v="0"/>
              <prop k="blur_level" v="2.645"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color1" v="0,0,255,255"/>
              <prop k="color2" v="0,255,0,255"/>
              <prop k="color_type" v="0"/>
              <prop k="discrete" v="0"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="0"/>
              <prop k="opacity" v="0.5"/>
              <prop k="rampType" v="gradient"/>
              <prop k="single_color" v="255,255,255,255"/>
              <prop k="spread" v="2"/>
              <prop k="spread_unit" v="MM"/>
              <prop k="spread_unit_scale" v="3x:0,0,0,0,0,0"/>
            </effect>
            <effect type="drawSource">
              <prop k="blend_mode" v="0"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="1"/>
              <prop k="opacity" v="1"/>
            </effect>
            <effect type="innerShadow">
              <prop k="blend_mode" v="13"/>
              <prop k="blur_level" v="2.645"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color" v="0,0,0,255"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="0"/>
              <prop k="offset_angle" v="135"/>
              <prop k="offset_distance" v="2"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="offset_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="opacity" v="1"/>
            </effect>
            <effect type="innerGlow">
              <prop k="blend_mode" v="0"/>
              <prop k="blur_level" v="2.645"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color1" v="0,0,255,255"/>
              <prop k="color2" v="0,255,0,255"/>
              <prop k="color_type" v="0"/>
              <prop k="discrete" v="0"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="0"/>
              <prop k="opacity" v="0.5"/>
              <prop k="rampType" v="gradient"/>
              <prop k="single_color" v="255,255,255,255"/>
              <prop k="spread" v="2"/>
              <prop k="spread_unit" v="MM"/>
              <prop k="spread_unit_scale" v="3x:0,0,0,0,0,0"/>
            </effect>
          </effect>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="if(@map_scale&lt;10000, 4.1,3.1)"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="85,255,127,0"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="pentagon"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,127,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.7"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="4"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <effect enabled="0" type="effectStack">
            <effect type="dropShadow">
              <prop k="blend_mode" v="13"/>
              <prop k="blur_level" v="0.5"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color" v="0,0,0,255"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="1"/>
              <prop k="offset_angle" v="135"/>
              <prop k="offset_distance" v="0.2"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="offset_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="opacity" v="1"/>
            </effect>
            <effect type="outerGlow">
              <prop k="blend_mode" v="0"/>
              <prop k="blur_level" v="2.645"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color1" v="0,0,255,255"/>
              <prop k="color2" v="0,255,0,255"/>
              <prop k="color_type" v="0"/>
              <prop k="discrete" v="0"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="0"/>
              <prop k="opacity" v="0.5"/>
              <prop k="rampType" v="gradient"/>
              <prop k="single_color" v="255,255,255,255"/>
              <prop k="spread" v="2"/>
              <prop k="spread_unit" v="MM"/>
              <prop k="spread_unit_scale" v="3x:0,0,0,0,0,0"/>
            </effect>
            <effect type="drawSource">
              <prop k="blend_mode" v="0"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="1"/>
              <prop k="opacity" v="1"/>
            </effect>
            <effect type="innerShadow">
              <prop k="blend_mode" v="13"/>
              <prop k="blur_level" v="2.645"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color" v="0,0,0,255"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="0"/>
              <prop k="offset_angle" v="135"/>
              <prop k="offset_distance" v="2"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="offset_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="opacity" v="1"/>
            </effect>
            <effect type="innerGlow">
              <prop k="blend_mode" v="0"/>
              <prop k="blur_level" v="2.645"/>
              <prop k="blur_unit" v="MM"/>
              <prop k="blur_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color1" v="0,0,255,255"/>
              <prop k="color2" v="0,255,0,255"/>
              <prop k="color_type" v="0"/>
              <prop k="discrete" v="0"/>
              <prop k="draw_mode" v="2"/>
              <prop k="enabled" v="0"/>
              <prop k="opacity" v="0.5"/>
              <prop k="rampType" v="gradient"/>
              <prop k="single_color" v="255,255,255,255"/>
              <prop k="spread" v="2"/>
              <prop k="spread_unit" v="MM"/>
              <prop k="spread_unit_scale" v="3x:0,0,0,0,0,0"/>
            </effect>
          </effect>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="if(@map_scale&lt;10000, 4,3)"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="marker" alpha="1" name="3" clip_to_extent="1">
        <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="85,255,127,0"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="square"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,9,1,255"/>
          <prop k="outline_style" v="dot"/>
          <prop k="outline_width" v="0.25"/>
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
  <SingleCategoryDiagramRenderer diagramType="Pie" attributeLegend="1">
    <DiagramCategory scaleBasedVisibility="0" backgroundAlpha="255" penWidth="0" sizeType="MM" penAlpha="255" scaleDependency="Area" rotationOffset="270" height="15" minScaleDenominator="-4.65661e-10" maxScaleDenominator="1e+08" barWidth="5" labelPlacementMethod="XHeight" sizeScale="3x:0,0,0,0,0,0" lineSizeType="MM" opacity="1" enabled="0" minimumSize="0" penColor="#000000" width="15" backgroundColor="#ffffff" lineSizeScale="3x:0,0,0,0,0,0" diagramOrientation="Up">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" color="#000000" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings dist="0" obstacle="0" zIndex="0" placement="0" showAll="1" linePlacementFlags="2" priority="0">
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
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="" field="ROWID"/>
    <alias index="1" name="id" field="manh_id"/>
    <alias index="2" name="display_name" field="manh_display_name"/>
    <alias index="3" name="code" field="manh_code"/>
    <alias index="4" name="connection_node_id" field="manh_connection_node_id"/>
    <alias index="5" name="shape" field="manh_shape"/>
    <alias index="6" name="width" field="manh_width"/>
    <alias index="7" name="length" field="manh_length"/>
    <alias index="8" name="manhole_indicator" field="manh_manhole_indicator"/>
    <alias index="9" name="calculation_type" field="manh_calculation_type"/>
    <alias index="10" name="bottom_level" field="manh_bottom_level"/>
    <alias index="11" name="surface_level" field="manh_surface_level"/>
    <alias index="12" name="drain_level" field="manh_drain_level"/>
    <alias index="13" name="sediment_level" field="manh_sediment_level"/>
    <alias index="14" name="zoom_category" field="manh_zoom_category"/>
    <alias index="15" name="" field="node_id"/>
    <alias index="16" name="" field="node_storage_area"/>
    <alias index="17" name="" field="node_initial_waterlevel"/>
    <alias index="18" name="" field="node_code"/>
    <alias index="19" name="the_geom_linestring" field="node_the_geom_linestring"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="ROWID"/>
    <default expression="if(maximum(manh_id) is null,1, maximum(manh_id)+1)" applyOnUpdate="0" field="manh_id"/>
    <default expression="'new'" applyOnUpdate="0" field="manh_display_name"/>
    <default expression="'new'" applyOnUpdate="0" field="manh_code"/>
    <default expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,geometry(@parent))) is null,'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,geometry(@parent))))" applyOnUpdate="0" field="manh_connection_node_id"/>
    <default expression="" applyOnUpdate="0" field="manh_shape"/>
    <default expression="" applyOnUpdate="0" field="manh_width"/>
    <default expression="" applyOnUpdate="0" field="manh_length"/>
    <default expression="'0'" applyOnUpdate="0" field="manh_manhole_indicator"/>
    <default expression="" applyOnUpdate="0" field="manh_calculation_type"/>
    <default expression="&quot;manh_bottom_level&quot;&lt;&quot;manh_surface_level&quot;" applyOnUpdate="0" field="manh_bottom_level"/>
    <default expression="" applyOnUpdate="0" field="manh_surface_level"/>
    <default expression="" applyOnUpdate="0" field="manh_drain_level"/>
    <default expression="" applyOnUpdate="0" field="manh_sediment_level"/>
    <default expression="1" applyOnUpdate="0" field="manh_zoom_category"/>
    <default expression="'filled automatically'" applyOnUpdate="0" field="node_id"/>
    <default expression="" applyOnUpdate="0" field="node_storage_area"/>
    <default expression="" applyOnUpdate="0" field="node_initial_waterlevel"/>
    <default expression="'new'" applyOnUpdate="0" field="node_code"/>
    <default expression="" applyOnUpdate="0" field="node_the_geom_linestring"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="ROWID"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="manh_id"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="manh_display_name"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="manh_code"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="manh_connection_node_id"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="manh_shape"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="manh_width"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="manh_length"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="manh_manhole_indicator"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="manh_calculation_type"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="manh_bottom_level"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="manh_surface_level"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="manh_drain_level"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="manh_sediment_level"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="manh_zoom_category"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="node_id"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="node_storage_area"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="node_initial_waterlevel"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="node_code"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="node_the_geom_linestring"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="ROWID"/>
    <constraint desc="" exp="" field="manh_id"/>
    <constraint desc="" exp="" field="manh_display_name"/>
    <constraint desc="" exp="" field="manh_code"/>
    <constraint desc="" exp="" field="manh_connection_node_id"/>
    <constraint desc="" exp="" field="manh_shape"/>
    <constraint desc="" exp="" field="manh_width"/>
    <constraint desc="" exp="" field="manh_length"/>
    <constraint desc="" exp="" field="manh_manhole_indicator"/>
    <constraint desc="" exp="" field="manh_calculation_type"/>
    <constraint desc="" exp="" field="manh_bottom_level"/>
    <constraint desc="" exp="" field="manh_surface_level"/>
    <constraint desc="" exp="" field="manh_drain_level"/>
    <constraint desc="" exp="" field="manh_sediment_level"/>
    <constraint desc="" exp="" field="manh_zoom_category"/>
    <constraint desc="" exp="" field="node_id"/>
    <constraint desc="" exp="" field="node_storage_area"/>
    <constraint desc="" exp="" field="node_initial_waterlevel"/>
    <constraint desc="" exp="" field="node_code"/>
    <constraint desc="" exp="" field="node_the_geom_linestring"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortExpression="&quot;manh_manhole_indicator&quot;" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column type="field" name="ROWID" hidden="0" width="-1"/>
      <column type="field" name="manh_id" hidden="0" width="-1"/>
      <column type="field" name="manh_display_name" hidden="0" width="-1"/>
      <column type="field" name="manh_code" hidden="0" width="-1"/>
      <column type="field" name="manh_connection_node_id" hidden="0" width="-1"/>
      <column type="field" name="manh_shape" hidden="0" width="-1"/>
      <column type="field" name="manh_width" hidden="0" width="-1"/>
      <column type="field" name="manh_length" hidden="0" width="-1"/>
      <column type="field" name="manh_manhole_indicator" hidden="0" width="-1"/>
      <column type="field" name="manh_calculation_type" hidden="0" width="-1"/>
      <column type="field" name="manh_bottom_level" hidden="0" width="-1"/>
      <column type="field" name="manh_surface_level" hidden="0" width="-1"/>
      <column type="field" name="manh_drain_level" hidden="0" width="-1"/>
      <column type="field" name="manh_sediment_level" hidden="0" width="-1"/>
      <column type="field" name="manh_zoom_category" hidden="0" width="-1"/>
      <column type="field" name="node_id" hidden="0" width="-1"/>
      <column type="field" name="node_storage_area" hidden="0" width="-1"/>
      <column type="field" name="node_initial_waterlevel" hidden="0" width="-1"/>
      <column type="field" name="node_code" hidden="0" width="-1"/>
      <column type="field" name="node_the_geom_linestring" hidden="0" width="-1"/>
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
    <attributeEditorContainer groupBox="0" visibilityExpression="" showLabel="1" visibilityExpressionEnabled="0" columnCount="1" name="Manhole_view">
      <attributeEditorContainer groupBox="1" visibilityExpression="" showLabel="1" visibilityExpressionEnabled="0" columnCount="1" name="General">
        <attributeEditorField showLabel="1" index="1" name="manh_id"/>
        <attributeEditorField showLabel="1" index="2" name="manh_display_name"/>
        <attributeEditorField showLabel="1" index="3" name="manh_code"/>
        <attributeEditorField showLabel="1" index="9" name="manh_calculation_type"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpression="" showLabel="1" visibilityExpressionEnabled="0" columnCount="1" name="Characteristics">
        <attributeEditorField showLabel="1" index="5" name="manh_shape"/>
        <attributeEditorField showLabel="1" index="6" name="manh_width"/>
        <attributeEditorField showLabel="1" index="7" name="manh_length"/>
        <attributeEditorField showLabel="1" index="10" name="manh_bottom_level"/>
        <attributeEditorField showLabel="1" index="11" name="manh_surface_level"/>
        <attributeEditorField showLabel="1" index="12" name="manh_drain_level"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpression="" showLabel="1" visibilityExpressionEnabled="0" columnCount="1" name="Visualisation">
        <attributeEditorField showLabel="1" index="8" name="manh_manhole_indicator"/>
        <attributeEditorField showLabel="1" index="14" name="manh_zoom_category"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpression="" showLabel="1" visibilityExpressionEnabled="0" columnCount="1" name="Connection node">
        <attributeEditorField showLabel="1" index="4" name="manh_connection_node_id"/>
        <attributeEditorField showLabel="1" index="18" name="node_code"/>
        <attributeEditorField showLabel="1" index="17" name="node_initial_waterlevel"/>
        <attributeEditorField showLabel="1" index="16" name="node_storage_area"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="ROWID"/>
    <field editable="1" name="manh_bottom_level"/>
    <field editable="1" name="manh_calculation_type"/>
    <field editable="1" name="manh_code"/>
    <field editable="0" name="manh_connection_node_id"/>
    <field editable="1" name="manh_display_name"/>
    <field editable="1" name="manh_drain_level"/>
    <field editable="0" name="manh_id"/>
    <field editable="1" name="manh_length"/>
    <field editable="1" name="manh_manhole_indicator"/>
    <field editable="1" name="manh_sediment_level"/>
    <field editable="1" name="manh_shape"/>
    <field editable="1" name="manh_surface_level"/>
    <field editable="1" name="manh_width"/>
    <field editable="1" name="manh_zoom_category"/>
    <field editable="1" name="node_code"/>
    <field editable="0" name="node_id"/>
    <field editable="1" name="node_initial_waterlevel"/>
    <field editable="1" name="node_storage_area"/>
    <field editable="1" name="node_the_geom_linestring"/>
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
