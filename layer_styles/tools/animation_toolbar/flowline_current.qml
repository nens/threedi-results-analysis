<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.16.4-Hannover" styleCategories="Symbology|Rendering" simplifyLocal="1" hasScaleBasedVisibilityFlag="0" simplifyAlgorithm="0" simplifyMaxScale="1" maxScale="0" simplifyDrawingHints="1" simplifyDrawingTol="1" minScale="100000000">
  <renderer-v2 attr="abs(result)" graduatedMethod="GraduatedSize" forceraster="0" enableorderby="1" type="graduatedSymbol" symbollevels="0">
    <ranges>
      <range label="0 - 0" upper="0.000000000000000" render="true" lower="0.000000000000000" symbol="0"/>
      <range label="0 - 0" upper="0.000000000000000" render="true" lower="0.000000000000000" symbol="1"/>
      <range label="0 - 0" upper="0.000000000000000" render="true" lower="0.000000000000000" symbol="2"/>
      <range label="0 - 0.0005" upper="0.000495245854836" render="true" lower="0.000000000000000" symbol="3"/>
      <range label="0.0005 - 0.00118" upper="0.001178406353574" render="true" lower="0.000495245854836" symbol="4"/>
      <range label="0.00118 - 0.00196" upper="0.001962731126696" render="true" lower="0.001178406353574" symbol="5"/>
      <range label="0.00196 - 0.00324" upper="0.003240709309466" render="true" lower="0.001962731126696" symbol="6"/>
      <range label="0.00324 - 0.0059" upper="0.005895195528865" render="true" lower="0.003240709309466" symbol="7"/>
      <range label="0.0059 - 0.0126" upper="0.012603871989995" render="true" lower="0.005895195528865" symbol="8"/>
      <range label="0.0126 - 2.47251" upper="2.472512006759644" render="true" lower="0.012603871989995" symbol="9"/>
    </ranges>
    <symbols>
      <symbol name="0" force_rhr="0" alpha="1" type="line" clip_to_extent="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleLine">
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="abs(result) > 0"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="outlineColor" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="type" type="int" value="1"/>
                  <Option name="val" type="QString" value=""/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0, 1, 0.3), 0)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" pass="0" enabled="1" class="MarkerLine">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@0@1" force_rhr="0" alpha="1" type="marker" clip_to_extent="1">
            <layer locked="0" pass="0" enabled="1" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="triangle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="no" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="0" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="CASE WHEN result &lt; 0&#xd;&#xa;&#x9;THEN 90&#xd;&#xa;&#x9;ELSE -90&#xd;&#xa;END"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="($length /  @map_scale) > 0.0025 AND abs(result) > 0"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="fillColor" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="type" type="int" value="1"/>
                      <Option name="val" type="QString" value=""/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0.7, 3, 0.3), 0)"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                  </Option>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="1" force_rhr="0" alpha="1" type="line" clip_to_extent="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleLine">
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.0694445" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="abs(result) > 0"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="outlineColor" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="type" type="int" value="1"/>
                  <Option name="val" type="QString" value=""/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0, 1, 0.3), 0)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" pass="0" enabled="1" class="MarkerLine">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@1@1" force_rhr="0" alpha="1" type="marker" clip_to_extent="1">
            <layer locked="0" pass="0" enabled="1" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="triangle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="no" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="0.277778" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="CASE WHEN result &lt; 0&#xd;&#xa;&#x9;THEN 90&#xd;&#xa;&#x9;ELSE -90&#xd;&#xa;END"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="($length /  @map_scale) > 0.0025 AND abs(result) > 0"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="fillColor" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="type" type="int" value="1"/>
                      <Option name="val" type="QString" value=""/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0.7, 3, 0.3), 0)"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                  </Option>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="2" force_rhr="0" alpha="1" type="line" clip_to_extent="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleLine">
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.138889" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="abs(result) > 0"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="outlineColor" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="type" type="int" value="1"/>
                  <Option name="val" type="QString" value=""/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0, 1, 0.3), 0)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" pass="0" enabled="1" class="MarkerLine">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@2@1" force_rhr="0" alpha="1" type="marker" clip_to_extent="1">
            <layer locked="0" pass="0" enabled="1" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="triangle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="no" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="0.555556" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="CASE WHEN result &lt; 0&#xd;&#xa;&#x9;THEN 90&#xd;&#xa;&#x9;ELSE -90&#xd;&#xa;END"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="($length /  @map_scale) > 0.0025 AND abs(result) > 0"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="fillColor" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="type" type="int" value="1"/>
                      <Option name="val" type="QString" value=""/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0.7, 3, 0.3), 0)"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                  </Option>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="3" force_rhr="0" alpha="1" type="line" clip_to_extent="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleLine">
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.208333" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="abs(result) > 0"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="outlineColor" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="type" type="int" value="1"/>
                  <Option name="val" type="QString" value=""/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0, 1, 0.3), 0)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" pass="0" enabled="1" class="MarkerLine">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@3@1" force_rhr="0" alpha="1" type="marker" clip_to_extent="1">
            <layer locked="0" pass="0" enabled="1" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="triangle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="no" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="0.833333" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="CASE WHEN result &lt; 0&#xd;&#xa;&#x9;THEN 90&#xd;&#xa;&#x9;ELSE -90&#xd;&#xa;END"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="($length /  @map_scale) > 0.0025 AND abs(result) > 0"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="fillColor" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="type" type="int" value="1"/>
                      <Option name="val" type="QString" value=""/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0.7, 3, 0.3), 0)"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                  </Option>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="4" force_rhr="0" alpha="1" type="line" clip_to_extent="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleLine">
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.277778" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="abs(result) > 0"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="outlineColor" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="type" type="int" value="1"/>
                  <Option name="val" type="QString" value=""/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0, 1, 0.3), 0)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" pass="0" enabled="1" class="MarkerLine">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@4@1" force_rhr="0" alpha="1" type="marker" clip_to_extent="1">
            <layer locked="0" pass="0" enabled="1" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="triangle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="no" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="1.11111" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="CASE WHEN result &lt; 0&#xd;&#xa;&#x9;THEN 90&#xd;&#xa;&#x9;ELSE -90&#xd;&#xa;END"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="($length /  @map_scale) > 0.0025 AND abs(result) > 0"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="fillColor" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="type" type="int" value="1"/>
                      <Option name="val" type="QString" value=""/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0.7, 3, 0.3), 0)"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                  </Option>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="5" force_rhr="0" alpha="1" type="line" clip_to_extent="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleLine">
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.347222" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="abs(result) > 0"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="outlineColor" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="type" type="int" value="1"/>
                  <Option name="val" type="QString" value=""/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0, 1, 0.3), 0)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" pass="0" enabled="1" class="MarkerLine">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@5@1" force_rhr="0" alpha="1" type="marker" clip_to_extent="1">
            <layer locked="0" pass="0" enabled="1" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="triangle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="no" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="1.38889" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="CASE WHEN result &lt; 0&#xd;&#xa;&#x9;THEN 90&#xd;&#xa;&#x9;ELSE -90&#xd;&#xa;END"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="($length /  @map_scale) > 0.0025 AND abs(result) > 0"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="fillColor" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="type" type="int" value="1"/>
                      <Option name="val" type="QString" value=""/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0.7, 3, 0.3), 0)"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                  </Option>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="6" force_rhr="0" alpha="1" type="line" clip_to_extent="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleLine">
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.416668" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="abs(result) > 0"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="outlineColor" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="type" type="int" value="1"/>
                  <Option name="val" type="QString" value=""/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0, 1, 0.3), 0)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" pass="0" enabled="1" class="MarkerLine">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@6@1" force_rhr="0" alpha="1" type="marker" clip_to_extent="1">
            <layer locked="0" pass="0" enabled="1" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="triangle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="no" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="1.66667" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="CASE WHEN result &lt; 0&#xd;&#xa;&#x9;THEN 90&#xd;&#xa;&#x9;ELSE -90&#xd;&#xa;END"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="($length /  @map_scale) > 0.0025 AND abs(result) > 0"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="fillColor" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="type" type="int" value="1"/>
                      <Option name="val" type="QString" value=""/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0.7, 3, 0.3), 0)"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                  </Option>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="7" force_rhr="0" alpha="1" type="line" clip_to_extent="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleLine">
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.48611" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="abs(result) > 0"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="outlineColor" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="type" type="int" value="1"/>
                  <Option name="val" type="QString" value=""/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0, 1, 0.3), 0)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" pass="0" enabled="1" class="MarkerLine">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@7@1" force_rhr="0" alpha="1" type="marker" clip_to_extent="1">
            <layer locked="0" pass="0" enabled="1" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="triangle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="no" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="1.94444" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="CASE WHEN result &lt; 0&#xd;&#xa;&#x9;THEN 90&#xd;&#xa;&#x9;ELSE -90&#xd;&#xa;END"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="($length /  @map_scale) > 0.0025 AND abs(result) > 0"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="fillColor" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="type" type="int" value="1"/>
                      <Option name="val" type="QString" value=""/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0.7, 3, 0.3), 0)"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                  </Option>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="8" force_rhr="0" alpha="1" type="line" clip_to_extent="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleLine">
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.555555" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="abs(result) > 0"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="outlineColor" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="type" type="int" value="1"/>
                  <Option name="val" type="QString" value=""/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0, 1, 0.3), 0)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" pass="0" enabled="1" class="MarkerLine">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@8@1" force_rhr="0" alpha="1" type="marker" clip_to_extent="1">
            <layer locked="0" pass="0" enabled="1" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="triangle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="no" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="2.22222" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="CASE WHEN result &lt; 0&#xd;&#xa;&#x9;THEN 90&#xd;&#xa;&#x9;ELSE -90&#xd;&#xa;END"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="($length /  @map_scale) > 0.0025 AND abs(result) > 0"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="fillColor" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="type" type="int" value="1"/>
                      <Option name="val" type="QString" value=""/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0.7, 3, 0.3), 0)"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                  </Option>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="9" force_rhr="0" alpha="1" type="line" clip_to_extent="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleLine">
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.625" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="abs(result) > 0"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="outlineColor" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="type" type="int" value="1"/>
                  <Option name="val" type="QString" value=""/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0, 1, 0.3), 0)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" pass="0" enabled="1" class="MarkerLine">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@9@1" force_rhr="0" alpha="1" type="marker" clip_to_extent="1">
            <layer locked="0" pass="0" enabled="1" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="triangle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="no" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="2.5" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="CASE WHEN result &lt; 0&#xd;&#xa;&#x9;THEN 90&#xd;&#xa;&#x9;ELSE -90&#xd;&#xa;END"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="($length /  @map_scale) > 0.0025 AND abs(result) > 0"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="fillColor" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="type" type="int" value="1"/>
                      <Option name="val" type="QString" value=""/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0.7, 3, 0.3), 0)"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                  </Option>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol name="0" force_rhr="0" alpha="1" type="line" clip_to_extent="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleLine">
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.5" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="abs(result) > 0"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="outlineColor" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="type" type="int" value="1"/>
                  <Option name="val" type="QString" value=""/>
                </Option>
                <Option name="outlineWidth" type="Map">
                  <Option name="active" type="bool" value="false"/>
                  <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0, 1, 0.3), 0)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" pass="0" enabled="1" class="MarkerLine">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@0@1" force_rhr="0" alpha="1" type="marker" clip_to_extent="1">
            <layer locked="0" pass="0" enabled="1" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="0,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="triangle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="no" k="outline_style"/>
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
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="CASE WHEN result &lt; 0&#xd;&#xa;&#x9;THEN 90&#xd;&#xa;&#x9;ELSE -90&#xd;&#xa;END"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="($length /  @map_scale) > 0.0025 AND abs(result) > 0"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="fillColor" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="type" type="int" value="1"/>
                      <Option name="val" type="QString" value=""/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value="coalesce(scale_exp(abs(result), 0, @threedi_flowline_p90, 0.7, 3, 0.3), 0)"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                  </Option>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
    </source-symbol>
    <classificationMethod id="Quantile">
      <symmetricMode symmetrypoint="0" enabled="0" astride="0"/>
      <labelFormat trimtrailingzeroes="1" labelprecision="4" format="%1 - %2"/>
      <parameters>
        <Option/>
      </parameters>
      <extraInformation/>
    </classificationMethod>
    <rotation/>
    <sizescale/>
    <orderby>
      <orderByClause nullsFirst="0" asc="1">abs(result)</orderByClause>
    </orderby>
  </renderer-v2>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <layerGeometryType>1</layerGeometryType>
</qgis>
