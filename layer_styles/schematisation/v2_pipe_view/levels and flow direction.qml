<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyMaxScale="1" styleCategories="AllStyleCategories" simplifyAlgorithm="0" readOnly="0" labelsEnabled="1" hasScaleBasedVisibilityFlag="0" simplifyDrawingTol="1" maxScale="0" version="3.10.10-A Coruña" minScale="1e+08" simplifyDrawingHints="1" simplifyLocal="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" type="RuleRenderer" enableorderby="0" symbollevels="0">
    <rules key="{1c4a4e03-d442-4bb0-8ffc-82b9a703e08f}">
      <rule key="{844e5e28-ad8f-43dc-ae9b-2eedeecde873}" label="Combined sewer" filter="pipe_sewerage_type = 0" symbol="0"/>
      <rule key="{3b41f70d-2dfe-4438-8b1a-3722a52ff82b}" label="Storm drain" filter="pipe_sewerage_type = 1" symbol="1"/>
      <rule key="{c8833167-878e-49b2-bd37-5019aeea2451}" label="Sanitary sewer" filter="pipe_sewerage_type = 2" symbol="2"/>
      <rule key="{d62bccfa-4138-43ba-ab6d-51eae9f5b079}" label="Transport" filter="pipe_sewerage_type = 3" symbol="3"/>
      <rule key="{3d909156-553e-4d45-8a2f-02337ffb74d5}" label="Spillway" filter="pipe_sewerage_type = 4" symbol="4"/>
      <rule key="{a445abaf-878b-4b6b-8f1d-1314d1271d38}" label="Syphon" filter="pipe_sewerage_type =5" symbol="5"/>
      <rule key="{c6ba261b-8172-407e-bc72-8487b24a1cc4}" label="Storage" filter="pipe_sewerage_type = 6" symbol="6"/>
      <rule key="{8eb66a66-0335-4672-a78d-1aac6c4702ff}" label="Storage and settlement tank" filter="pipe_sewerage_type = 7" symbol="7"/>
      <rule key="{aa320dac-96a8-41e4-af30-3e9153ceaeae}" label="Other" filter="ELSE" symbol="8"/>
    </rules>
    <symbols>
      <symbol name="0" type="line" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="255,170,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.4" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" enabled="1" locked="0" class="MarkerLine">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="3" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="5" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="MapUnit" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="centralpoint" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="0.33 * $length"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@0@1" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
            <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
              <prop v="180" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="arrowhead" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="255,170,0,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0.6" k="outline_width"/>
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
                      <Option name="expression" type="QString" value="degrees(&#x9;azimuth(&#xd;&#xa;&#x9;&#x9;start_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9; @project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;end_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;@project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;)&#xd;&#xa;&#x9;)&#xd;&#xa;&#x9;+ &#xd;&#xa;if(&quot;pipe_invert_level_start_point&quot; >  &quot;pipe_invert_level_end_point&quot;, pi()/-2, pi()/2))"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value=""/>
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
      <symbol name="1" type="line" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="85,170,255,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.4" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" enabled="1" locked="0" class="MarkerLine">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="3" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="5" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="MapUnit" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="centralpoint" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="0.33 * $length"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@1@1" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
            <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
              <prop v="180" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="arrowhead" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="85,170,255,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0.6" k="outline_width"/>
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
                      <Option name="expression" type="QString" value="degrees(&#x9;azimuth(&#xd;&#xa;&#x9;&#x9;start_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9; @project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;end_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;@project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;)&#xd;&#xa;&#x9;)&#xd;&#xa;&#x9;+ &#xd;&#xa;if(&quot;pipe_invert_level_start_point&quot; >  &quot;pipe_invert_level_end_point&quot;, pi()/-2, pi()/2))"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value=""/>
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
      <symbol name="2" type="line" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="255,0,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.4" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" enabled="1" locked="0" class="MarkerLine">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="3" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="5" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="MapUnit" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="centralpoint" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="0.33 * $length"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@2@1" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
            <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
              <prop v="180" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="arrowhead" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="255,0,0,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0.6" k="outline_width"/>
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
                      <Option name="expression" type="QString" value="degrees(&#x9;azimuth(&#xd;&#xa;&#x9;&#x9;start_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9; @project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;end_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;@project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;)&#xd;&#xa;&#x9;)&#xd;&#xa;&#x9;+ &#xd;&#xa;if(&quot;pipe_invert_level_start_point&quot; >  &quot;pipe_invert_level_end_point&quot;, pi()/-2, pi()/2))"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value=""/>
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
      <symbol name="3" type="line" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="153,153,153,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.4" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" enabled="1" locked="0" class="MarkerLine">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="3" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="5" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="MapUnit" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="centralpoint" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="0.33 * $length"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@3@1" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
            <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
              <prop v="180" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="arrowhead" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="153,153,153,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0.6" k="outline_width"/>
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
                      <Option name="expression" type="QString" value="degrees(&#x9;azimuth(&#xd;&#xa;&#x9;&#x9;start_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9; @project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;end_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;@project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;)&#xd;&#xa;&#x9;)&#xd;&#xa;&#x9;+ &#xd;&#xa;if(&quot;pipe_invert_level_start_point&quot; >  &quot;pipe_invert_level_end_point&quot;, pi()/-2, pi()/2))"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value=""/>
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
      <symbol name="4" type="line" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="85,170,255,255" k="line_color"/>
          <prop v="dot" k="line_style"/>
          <prop v="0.4" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" enabled="1" locked="0" class="MarkerLine">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="3" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="5" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="MapUnit" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="centralpoint" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="0.33 * $length"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@4@1" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
            <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
              <prop v="180" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="arrowhead" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="85,170,255,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0.6" k="outline_width"/>
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
                      <Option name="expression" type="QString" value="degrees(&#x9;azimuth(&#xd;&#xa;&#x9;&#x9;start_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9; @project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;end_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;@project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;)&#xd;&#xa;&#x9;)&#xd;&#xa;&#x9;+ &#xd;&#xa;if(&quot;pipe_invert_level_start_point&quot; >  &quot;pipe_invert_level_end_point&quot;, pi()/-2, pi()/2))"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value=""/>
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
      <symbol name="5" type="line" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="85,170,255,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.4" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" enabled="1" locked="0" class="MarkerLine">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="3" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="5" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="MapUnit" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="centralpoint" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="0.33 * $length"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@5@1" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
            <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
              <prop v="180" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="arrowhead" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="85,170,255,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0.6" k="outline_width"/>
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
                      <Option name="expression" type="QString" value="degrees(&#x9;azimuth(&#xd;&#xa;&#x9;&#x9;start_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9; @project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;end_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;@project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;)&#xd;&#xa;&#x9;)&#xd;&#xa;&#x9;+ &#xd;&#xa;if(&quot;pipe_invert_level_start_point&quot; >  &quot;pipe_invert_level_end_point&quot;, pi()/-2, pi()/2))"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value=""/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                  </Option>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer pass="0" enabled="1" locked="0" class="MarkerLine">
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
          <prop v="interval" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="1" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@5@2" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
            <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="85,170,255,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="semi_circle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="no" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="1.4" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties"/>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="6" type="line" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="189,189,189,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="2" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="7" type="line" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="92,92,92,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="2" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="8" type="line" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0,0,255" k="line_color"/>
          <prop v="dot" k="line_style"/>
          <prop v="0.4" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer pass="0" enabled="1" locked="0" class="MarkerLine">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="3" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="MM" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="5" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="MapUnit" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="centralpoint" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="enabled" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="offsetAlongLine" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="0.33 * $length"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@8@1" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
            <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
              <prop v="180" k="angle"/>
              <prop v="255,0,0,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="arrowhead" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="0,0,0,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0.6" k="outline_width"/>
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
                      <Option name="expression" type="QString" value="degrees(&#x9;azimuth(&#xd;&#xa;&#x9;&#x9;start_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9; @project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;end_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;@project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;)&#xd;&#xa;&#x9;)&#xd;&#xa;&#x9;+ &#xd;&#xa;if(&quot;pipe_invert_level_start_point&quot; >  &quot;pipe_invert_level_end_point&quot;, pi()/-2, pi()/2))"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="enabled" type="Map">
                      <Option name="active" type="bool" value="true"/>
                      <Option name="expression" type="QString" value="&quot;pipe_invert_level_start_point&quot; !=  &quot;pipe_invert_level_end_point&quot;"/>
                      <Option name="type" type="int" value="3"/>
                    </Option>
                    <Option name="size" type="Map">
                      <Option name="active" type="bool" value="false"/>
                      <Option name="expression" type="QString" value=""/>
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
  </renderer-v2>
  <labeling type="rule-based">
    <rules key="{e01e074a-1882-476a-a99b-cba69c882878}">
      <rule key="{d1aa2acf-608e-47a6-a5cc-27bf63f45b65}" description="Start point label" scalemaxdenom="1000">
        <settings calloutType="simple">
          <text-style previewBkgrdColor="255,255,255,255" textOpacity="1" isExpression="1" blendMode="0" fontStrikeout="0" multilineHeight="1" namedStyle="Standaard" fontSize="7" fieldName="'    s:' || coalesce(format_number(round(pipe_invert_level_start_point,2),2), 'NULL')" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontWordSpacing="0" fontFamily="MS Shell Dlg 2" fontItalic="0" fontWeight="50" fontSizeUnit="Point" textOrientation="horizontal" fontCapitals="0" fontUnderline="0" fontLetterSpacing="0" textColor="0,0,223,255" useSubstitutions="0" fontKerning="1">
            <text-buffer bufferBlendMode="0" bufferSizeUnits="MM" bufferOpacity="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferDraw="1" bufferJoinStyle="128" bufferColor="255,255,255,255" bufferNoFill="0" bufferSize="0.7"/>
            <background shapeOffsetX="0" shapeRadiiX="0" shapeJoinStyle="64" shapeOpacity="1" shapeBorderColor="128,128,128,255" shapeRotation="0" shapeSizeUnit="MM" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetY="0" shapeBorderWidth="0" shapeBlendMode="0" shapeSizeY="0" shapeRotationType="0" shapeType="0" shapeRadiiUnit="MM" shapeRadiiY="0" shapeOffsetUnit="MM" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeSizeType="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSVGFile="" shapeFillColor="255,255,255,255" shapeBorderWidthUnit="MM" shapeSizeX="0" shapeDraw="0">
              <symbol name="markerSymbol" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
                <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
                  <prop v="0" k="angle"/>
                  <prop v="190,178,151,255" k="color"/>
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
                      <Option name="name" type="QString" value=""/>
                      <Option name="properties"/>
                      <Option name="type" type="QString" value="collection"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </background>
            <shadow shadowScale="100" shadowColor="0,0,0,255" shadowRadiusUnit="MM" shadowDraw="0" shadowRadiusAlphaOnly="0" shadowRadius="1.5" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.7" shadowOffsetDist="1" shadowOffsetUnit="MM" shadowBlendMode="6" shadowOffsetGlobal="1" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowUnder="0" shadowOffsetAngle="135"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" type="QString" value=""/>
                <Option name="properties"/>
                <Option name="type" type="QString" value="collection"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format rightDirectionSymbol=">" multilineAlign="0" reverseDirectionSymbol="0" wrapChar="" autoWrapLength="0" formatNumbers="0" decimals="3" useMaxLineLengthForAutoWrap="1" addDirectionSymbol="0" placeDirectionSymbol="0" plussign="0" leftDirectionSymbol="&lt;"/>
          <placement maxCurvedCharAngleIn="25" geometryGenerator="" quadOffset="4" priority="5" yOffset="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" maxCurvedCharAngleOut="-25" repeatDistance="0" centroidWhole="0" rotationAngle="0" overrunDistance="0" overrunDistanceUnit="MM" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorType="PointGeometry" distUnits="MM" fitInPolygonOnly="0" preserveRotation="0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" centroidInside="0" dist="0" layerType="LineGeometry" xOffset="0" placement="2" distMapUnitScale="3x:0,0,0,0,0,0" repeatDistanceUnits="MM" placementFlags="2" offsetType="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorEnabled="0" offsetUnits="MapUnit"/>
          <rendering upsidedownLabels="0" obstacleFactor="1" fontMinPixelSize="3" maxNumLabels="2000" fontMaxPixelSize="10000" scaleMin="1" zIndex="0" displayAll="1" obstacle="1" fontLimitPixelSize="0" obstacleType="0" mergeLines="0" drawLabels="1" limitNumLabels="0" minFeatureSize="0" scaleVisibility="0" labelPerPart="0" scaleMax="10000000"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="Color" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="case &#x9;when pipe_sewerage_type = 0 then '#ff7700'&#xd;&#xa;&#x9;&#x9;when pipe_sewerage_type in (1,4,5) then '#55aaff'&#xd;&#xa;&#x9;&#x9;when pipe_sewerage_type = 2 then '#ff0000'&#xd;&#xa;&#x9;&#x9;when pipe_sewerage_type in (3, 6) then '#999999'&#xd;&#xa;&#x9;&#x9;when pipe_sewerage_type = 7 then '#5c5c5c'&#xd;&#xa;else '#000000' &#xd;&#xa;end"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="Hali" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="'Left'"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="LabelRotation" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="360 - &#xd;&#xa;(90 - degrees(&#xd;&#xa;&#x9;azimuth(&#xd;&#xa;&#x9;&#x9;start_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9; @project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;end_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;@project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;)&#xd;&#xa;&#x9;)&#xd;&#xa;)&#xd;&#xa;)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="PositionX" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="x(start_point($geometry))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="PositionY" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="y(start_point($geometry))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="Show" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="intersects(transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;start_point( $geometry),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;  @map_crs  &#xd;&#xa;&#x9;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;&#x9;@map_extent&#xd;&#xa;)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="Vali" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="'Top'"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option name="anchorPoint" type="QString" value="pole_of_inaccessibility"/>
              <Option name="ddProperties" type="Map">
                <Option name="name" type="QString" value=""/>
                <Option name="properties"/>
                <Option name="type" type="QString" value="collection"/>
              </Option>
              <Option name="drawToAllParts" type="bool" value="false"/>
              <Option name="enabled" type="QString" value="0"/>
              <Option name="lineSymbol" type="QString" value="&lt;symbol name=&quot;symbol&quot; type=&quot;line&quot; clip_to_extent=&quot;1&quot; alpha=&quot;1&quot; force_rhr=&quot;0&quot;>&lt;layer pass=&quot;0&quot; enabled=&quot;1&quot; locked=&quot;0&quot; class=&quot;SimpleLine&quot;>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; type=&quot;QString&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; type=&quot;QString&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
              <Option name="minLength" type="double" value="0"/>
              <Option name="minLengthMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
              <Option name="minLengthUnit" type="QString" value="MM"/>
              <Option name="offsetFromAnchor" type="double" value="0"/>
              <Option name="offsetFromAnchorMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
              <Option name="offsetFromAnchorUnit" type="QString" value="MM"/>
              <Option name="offsetFromLabel" type="double" value="0"/>
              <Option name="offsetFromLabelMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
              <Option name="offsetFromLabelUnit" type="QString" value="MM"/>
            </Option>
          </callout>
        </settings>
      </rule>
      <rule key="{f250be74-c271-4a85-9045-201d51dbe4da}" description="End point label" scalemaxdenom="1000">
        <settings calloutType="simple">
          <text-style previewBkgrdColor="255,255,255,255" textOpacity="1" isExpression="1" blendMode="0" fontStrikeout="0" multilineHeight="1" namedStyle="Standaard" fontSize="7" fieldName="'e:'||coalesce(format_number(round(pipe_invert_level_end_point,2),2), 'NULL')|| '    '" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontWordSpacing="0" fontFamily="MS Shell Dlg 2" fontItalic="0" fontWeight="50" fontSizeUnit="Point" textOrientation="horizontal" fontCapitals="0" fontUnderline="0" fontLetterSpacing="0" textColor="255,119,0,255" useSubstitutions="0" fontKerning="1">
            <text-buffer bufferBlendMode="0" bufferSizeUnits="MM" bufferOpacity="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferDraw="1" bufferJoinStyle="128" bufferColor="255,255,255,255" bufferNoFill="0" bufferSize="0.7"/>
            <background shapeOffsetX="0" shapeRadiiX="0" shapeJoinStyle="64" shapeOpacity="1" shapeBorderColor="128,128,128,255" shapeRotation="0" shapeSizeUnit="MM" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetY="0" shapeBorderWidth="0" shapeBlendMode="0" shapeSizeY="0" shapeRotationType="0" shapeType="0" shapeRadiiUnit="MM" shapeRadiiY="0" shapeOffsetUnit="MM" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeSizeType="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSVGFile="" shapeFillColor="255,255,255,255" shapeBorderWidthUnit="MM" shapeSizeX="0" shapeDraw="0">
              <symbol name="markerSymbol" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
                <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
                  <prop v="0" k="angle"/>
                  <prop v="145,82,45,255" k="color"/>
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
                      <Option name="name" type="QString" value=""/>
                      <Option name="properties"/>
                      <Option name="type" type="QString" value="collection"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </background>
            <shadow shadowScale="100" shadowColor="0,0,0,255" shadowRadiusUnit="MM" shadowDraw="0" shadowRadiusAlphaOnly="0" shadowRadius="1.5" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.7" shadowOffsetDist="1" shadowOffsetUnit="MM" shadowBlendMode="6" shadowOffsetGlobal="1" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowUnder="0" shadowOffsetAngle="135"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" type="QString" value=""/>
                <Option name="properties"/>
                <Option name="type" type="QString" value="collection"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format rightDirectionSymbol=">" multilineAlign="0" reverseDirectionSymbol="0" wrapChar="" autoWrapLength="0" formatNumbers="0" decimals="3" useMaxLineLengthForAutoWrap="1" addDirectionSymbol="0" placeDirectionSymbol="0" plussign="0" leftDirectionSymbol="&lt;"/>
          <placement maxCurvedCharAngleIn="25" geometryGenerator="" quadOffset="4" priority="5" yOffset="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" maxCurvedCharAngleOut="-25" repeatDistance="0" centroidWhole="0" rotationAngle="0" overrunDistance="0" overrunDistanceUnit="MM" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorType="PointGeometry" distUnits="MM" fitInPolygonOnly="0" preserveRotation="0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" centroidInside="0" dist="0" layerType="LineGeometry" xOffset="0" placement="2" distMapUnitScale="3x:0,0,0,0,0,0" repeatDistanceUnits="MM" placementFlags="10" offsetType="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorEnabled="0" offsetUnits="MapUnit"/>
          <rendering upsidedownLabels="0" obstacleFactor="1" fontMinPixelSize="3" maxNumLabels="2000" fontMaxPixelSize="10000" scaleMin="1" zIndex="0" displayAll="1" obstacle="1" fontLimitPixelSize="0" obstacleType="0" mergeLines="0" drawLabels="1" limitNumLabels="0" minFeatureSize="0" scaleVisibility="0" labelPerPart="0" scaleMax="10000000"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="Color" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="case &#x9;when pipe_sewerage_type = 0 then '#ff7700'&#xd;&#xa;&#x9;&#x9;when pipe_sewerage_type in (1,4,5) then '#55aaff'&#xd;&#xa;&#x9;&#x9;when pipe_sewerage_type = 2 then '#ff0000'&#xd;&#xa;&#x9;&#x9;when pipe_sewerage_type in (3, 6) then '#999999'&#xd;&#xa;&#x9;&#x9;when pipe_sewerage_type = 7 then '#5c5c5c'&#xd;&#xa;else '#000000' &#xd;&#xa;end"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="Hali" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="'Right'"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="LabelRotation" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="360 - &#xd;&#xa;(90 - degrees(&#xd;&#xa;&#x9;azimuth(&#xd;&#xa;&#x9;&#x9;start_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9; @project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;end_point(&#xd;&#xa;&#x9;&#x9;&#x9;transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;$geometry,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;@project_crs &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;)&#xd;&#xa;&#x9;)&#xd;&#xa;)&#xd;&#xa;)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="PositionX" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="x(end_point($geometry))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="PositionY" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="y(end_point($geometry))"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="Show" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="intersects(transform(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;end_point( $geometry),&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;layer_property(  @layer , 'crs' ), &#xd;&#xa;&#x9;&#x9;&#x9;&#x9;  @map_crs  &#xd;&#xa;&#x9;&#x9;&#x9;), &#xd;&#xa;&#x9;&#x9;&#x9;@map_extent&#xd;&#xa;)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
                <Option name="Vali" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="'Bottom'"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option name="anchorPoint" type="QString" value="pole_of_inaccessibility"/>
              <Option name="ddProperties" type="Map">
                <Option name="name" type="QString" value=""/>
                <Option name="properties"/>
                <Option name="type" type="QString" value="collection"/>
              </Option>
              <Option name="drawToAllParts" type="bool" value="false"/>
              <Option name="enabled" type="QString" value="0"/>
              <Option name="lineSymbol" type="QString" value="&lt;symbol name=&quot;symbol&quot; type=&quot;line&quot; clip_to_extent=&quot;1&quot; alpha=&quot;1&quot; force_rhr=&quot;0&quot;>&lt;layer pass=&quot;0&quot; enabled=&quot;1&quot; locked=&quot;0&quot; class=&quot;SimpleLine&quot;>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; type=&quot;QString&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; type=&quot;QString&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
              <Option name="minLength" type="double" value="0"/>
              <Option name="minLengthMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
              <Option name="minLengthUnit" type="QString" value="MM"/>
              <Option name="offsetFromAnchor" type="double" value="0"/>
              <Option name="offsetFromAnchorMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
              <Option name="offsetFromAnchorUnit" type="QString" value="MM"/>
              <Option name="offsetFromLabel" type="double" value="0"/>
              <Option name="offsetFromLabelMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
              <Option name="offsetFromLabelUnit" type="QString" value="MM"/>
            </Option>
          </callout>
        </settings>
      </rule>
    </rules>
  </labeling>
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
    <DiagramCategory lineSizeScale="3x:0,0,0,0,0,0" penAlpha="255" backgroundColor="#ffffff" sizeScale="3x:0,0,0,0,0,0" minimumSize="0" rotationOffset="270" penWidth="0" minScaleDenominator="0" width="15" scaleBasedVisibility="0" scaleDependency="Area" penColor="#000000" enabled="0" maxScaleDenominator="1e+08" diagramOrientation="Up" opacity="1" sizeType="MM" lineSizeType="MM" labelPlacementMethod="XHeight" height="15" backgroundAlpha="255" barWidth="5">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute color="#000000" field="" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings showAll="1" priority="0" obstacle="0" placement="2" zIndex="0" linePlacementFlags="2" dist="0">
    <properties>
      <Option type="Map">
        <Option name="name" type="QString" value=""/>
        <Option name="properties"/>
        <Option name="type" type="QString" value="collection"/>
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
    <field name="pipe_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_profile_num">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_sewerage_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="0: mixed" type="QString" value="0"/>
              </Option>
              <Option type="Map">
                <Option name="1: rain water" type="QString" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="2: dry weather flow" type="QString" value="2"/>
              </Option>
              <Option type="Map">
                <Option name="3: transport" type="QString" value="3"/>
              </Option>
              <Option type="Map">
                <Option name="4: spillway" type="QString" value="4"/>
              </Option>
              <Option type="Map">
                <Option name="5: sinker" type="QString" value="5"/>
              </Option>
              <Option type="Map">
                <Option name="6: storage" type="QString" value="6"/>
              </Option>
              <Option type="Map">
                <Option name="7: storage tank" type="QString" value="7"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_calculation_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="0: embedded" type="QString" value="0"/>
              </Option>
              <Option type="Map">
                <Option name="1: isolated" type="QString" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="2: connected" type="QString" value="2"/>
              </Option>
              <Option type="Map">
                <Option name="3: broad crest" type="QString" value="3"/>
              </Option>
              <Option type="Map">
                <Option name="4: short crest" type="QString" value="4"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_invert_level_start_point">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_invert_level_end_point">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_cross_section_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_friction_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="1: Chèzy" type="QString" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="2: Manning" type="QString" value="2"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_dist_calc_points">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_material">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="0: concrete" type="QString" value="0"/>
              </Option>
              <Option type="Map">
                <Option name="1: pvc" type="QString" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="2: gres" type="QString" value="2"/>
              </Option>
              <Option type="Map">
                <Option name="3: cast iron" type="QString" value="3"/>
              </Option>
              <Option type="Map">
                <Option name="4: brickwork" type="QString" value="4"/>
              </Option>
              <Option type="Map">
                <Option name="5: HPE" type="QString" value="5"/>
              </Option>
              <Option type="Map">
                <Option name="6: HDPE" type="QString" value="6"/>
              </Option>
              <Option type="Map">
                <Option name="7: plate iron" type="QString" value="7"/>
              </Option>
              <Option type="Map">
                <Option name="8: steel" type="QString" value="8"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_pipe_quality">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="pipe_original_length">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_zoom_category">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="-1" type="QString" value="-1"/>
              </Option>
              <Option type="Map">
                <Option name="0" type="QString" value="0"/>
              </Option>
              <Option type="Map">
                <Option name="1" type="QString" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="2" type="QString" value="2"/>
              </Option>
              <Option type="Map">
                <Option name="3" type="QString" value="3"/>
              </Option>
              <Option type="Map">
                <Option name="4" type="QString" value="4"/>
              </Option>
              <Option type="Map">
                <Option name="5" type="QString" value="5"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_connection_node_start_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pipe_connection_node_end_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
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
                <Option name="1: rectangle" type="QString" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="2: round" type="QString" value="2"/>
              </Option>
              <Option type="Map">
                <Option name="3: egg" type="QString" value="3"/>
              </Option>
              <Option type="Map">
                <Option name="5: tabulated rectangle" type="QString" value="5"/>
              </Option>
              <Option type="Map">
                <Option name="6: tabulated trapezium" type="QString" value="6"/>
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
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_height">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" index="0" field="ROWID"/>
    <alias name="id" index="1" field="pipe_id"/>
    <alias name="display_name" index="2" field="pipe_display_name"/>
    <alias name="code" index="3" field="pipe_code"/>
    <alias name="profile_num" index="4" field="pipe_profile_num"/>
    <alias name="sewerage_type" index="5" field="pipe_sewerage_type"/>
    <alias name="calculation_type" index="6" field="pipe_calculation_type"/>
    <alias name="invert_level_start_point" index="7" field="pipe_invert_level_start_point"/>
    <alias name="invert_level_end_point" index="8" field="pipe_invert_level_end_point"/>
    <alias name="cross_section_definition_id" index="9" field="pipe_cross_section_definition_id"/>
    <alias name="friction_value" index="10" field="pipe_friction_value"/>
    <alias name="friction_type" index="11" field="pipe_friction_type"/>
    <alias name="dist_calc_points" index="12" field="pipe_dist_calc_points"/>
    <alias name="material" index="13" field="pipe_material"/>
    <alias name="" index="14" field="pipe_pipe_quality"/>
    <alias name="original_length" index="15" field="pipe_original_length"/>
    <alias name="zoom_category" index="16" field="pipe_zoom_category"/>
    <alias name="connection_node_start_id" index="17" field="pipe_connection_node_start_id"/>
    <alias name="connection_node_end_id" index="18" field="pipe_connection_node_end_id"/>
    <alias name="id" index="19" field="def_id"/>
    <alias name="shape" index="20" field="def_shape"/>
    <alias name="width" index="21" field="def_width"/>
    <alias name="height" index="22" field="def_height"/>
    <alias name="code" index="23" field="def_code"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" expression="" field="ROWID"/>
    <default applyOnUpdate="0" expression="if(maximum(pipe_id) is null,1, maximum(pipe_id)+1)" field="pipe_id"/>
    <default applyOnUpdate="0" expression="'new'" field="pipe_display_name"/>
    <default applyOnUpdate="0" expression="'new'" field="pipe_code"/>
    <default applyOnUpdate="0" expression="" field="pipe_profile_num"/>
    <default applyOnUpdate="0" expression="" field="pipe_sewerage_type"/>
    <default applyOnUpdate="0" expression="1" field="pipe_calculation_type"/>
    <default applyOnUpdate="0" expression="aggregate('v2_manhole_view','mean',&quot;bottom_level&quot;, intersects($geometry,start_point(geometry(@parent))))" field="pipe_invert_level_start_point"/>
    <default applyOnUpdate="0" expression="aggregate('v2_manhole_view','mean',&quot;bottom_level&quot;, intersects($geometry,end_point(geometry(@parent))))" field="pipe_invert_level_end_point"/>
    <default applyOnUpdate="0" expression="" field="pipe_cross_section_definition_id"/>
    <default applyOnUpdate="0" expression="" field="pipe_friction_value"/>
    <default applyOnUpdate="0" expression="2" field="pipe_friction_type"/>
    <default applyOnUpdate="0" expression="10000" field="pipe_dist_calc_points"/>
    <default applyOnUpdate="0" expression="" field="pipe_material"/>
    <default applyOnUpdate="0" expression="" field="pipe_pipe_quality"/>
    <default applyOnUpdate="0" expression="" field="pipe_original_length"/>
    <default applyOnUpdate="0" expression="2" field="pipe_zoom_category"/>
    <default applyOnUpdate="0" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))) is null, 'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent)))))" field="pipe_connection_node_start_id"/>
    <default applyOnUpdate="0" expression="if(aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))) is null, 'Created automatically',aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent)))))" field="pipe_connection_node_end_id"/>
    <default applyOnUpdate="0" expression="" field="def_id"/>
    <default applyOnUpdate="0" expression="" field="def_shape"/>
    <default applyOnUpdate="0" expression="" field="def_width"/>
    <default applyOnUpdate="0" expression="" field="def_height"/>
    <default applyOnUpdate="0" expression="" field="def_code"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" field="ROWID" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="2" field="pipe_id" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="pipe_display_name" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="pipe_code" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" field="pipe_profile_num" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="2" field="pipe_sewerage_type" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="pipe_calculation_type" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="pipe_invert_level_start_point" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="pipe_invert_level_end_point" exp_strength="2" unique_strength="0" constraints="5"/>
    <constraint notnull_strength="2" field="pipe_cross_section_definition_id" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="pipe_friction_value" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="2" field="pipe_friction_type" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" field="pipe_dist_calc_points" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="pipe_material" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="pipe_pipe_quality" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="pipe_original_length" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="2" field="pipe_zoom_category" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" field="pipe_connection_node_start_id" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="pipe_connection_node_end_id" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="2" field="def_id" exp_strength="0" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" field="def_shape" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="def_width" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="def_height" exp_strength="0" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="def_code" exp_strength="0" unique_strength="0" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="ROWID"/>
    <constraint exp="" desc="" field="pipe_id"/>
    <constraint exp="" desc="" field="pipe_display_name"/>
    <constraint exp="" desc="" field="pipe_code"/>
    <constraint exp="" desc="" field="pipe_profile_num"/>
    <constraint exp="" desc="" field="pipe_sewerage_type"/>
    <constraint exp="" desc="" field="pipe_calculation_type"/>
    <constraint exp="" desc="" field="pipe_invert_level_start_point"/>
    <constraint exp="&quot;invert_level_end_point&quot; is not null" desc="" field="pipe_invert_level_end_point"/>
    <constraint exp="" desc="" field="pipe_cross_section_definition_id"/>
    <constraint exp="" desc="" field="pipe_friction_value"/>
    <constraint exp="" desc="" field="pipe_friction_type"/>
    <constraint exp="" desc="" field="pipe_dist_calc_points"/>
    <constraint exp="" desc="" field="pipe_material"/>
    <constraint exp="" desc="" field="pipe_pipe_quality"/>
    <constraint exp="" desc="" field="pipe_original_length"/>
    <constraint exp="" desc="" field="pipe_zoom_category"/>
    <constraint exp="" desc="" field="pipe_connection_node_start_id"/>
    <constraint exp="" desc="" field="pipe_connection_node_end_id"/>
    <constraint exp="" desc="" field="def_id"/>
    <constraint exp="" desc="" field="def_shape"/>
    <constraint exp="" desc="" field="def_width"/>
    <constraint exp="" desc="" field="def_height"/>
    <constraint exp="" desc="" field="def_code"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortExpression="" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column name="ROWID" hidden="0" type="field" width="-1"/>
      <column name="pipe_id" hidden="0" type="field" width="-1"/>
      <column name="pipe_display_name" hidden="0" type="field" width="-1"/>
      <column name="pipe_code" hidden="0" type="field" width="-1"/>
      <column name="pipe_profile_num" hidden="0" type="field" width="-1"/>
      <column name="pipe_sewerage_type" hidden="0" type="field" width="-1"/>
      <column name="pipe_calculation_type" hidden="0" type="field" width="-1"/>
      <column name="pipe_invert_level_start_point" hidden="0" type="field" width="-1"/>
      <column name="pipe_invert_level_end_point" hidden="0" type="field" width="-1"/>
      <column name="pipe_cross_section_definition_id" hidden="0" type="field" width="-1"/>
      <column name="pipe_friction_value" hidden="0" type="field" width="-1"/>
      <column name="pipe_friction_type" hidden="0" type="field" width="-1"/>
      <column name="pipe_dist_calc_points" hidden="0" type="field" width="-1"/>
      <column name="pipe_material" hidden="0" type="field" width="-1"/>
      <column name="pipe_original_length" hidden="0" type="field" width="-1"/>
      <column name="pipe_zoom_category" hidden="0" type="field" width="-1"/>
      <column name="pipe_connection_node_start_id" hidden="0" type="field" width="-1"/>
      <column name="pipe_connection_node_end_id" hidden="0" type="field" width="-1"/>
      <column name="def_id" hidden="0" type="field" width="-1"/>
      <column name="def_shape" hidden="0" type="field" width="-1"/>
      <column name="def_width" hidden="0" type="field" width="-1"/>
      <column name="def_height" hidden="0" type="field" width="-1"/>
      <column name="def_code" hidden="0" type="field" width="-1"/>
      <column hidden="1" type="actions" width="-1"/>
      <column name="pipe_pipe_quality" hidden="0" type="field" width="-1"/>
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
Formulieren van QGIS mogen een functie van Python hebben die wordt aangeroepen wanneer het formulier wordt geopend.

Gebruik deze functie om extra logica aan uw formulieren toe te voegen.

Voer de naam van de functie in in het veld "Python Init functie".
Een voorbeeld volgt:
"""
from PyQt4.QtGui import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer visibilityExpressionEnabled="0" name="Pipe view" showLabel="1" columnCount="1" groupBox="0" visibilityExpression="">
      <attributeEditorContainer visibilityExpressionEnabled="0" name="General" showLabel="1" columnCount="1" groupBox="1" visibilityExpression="">
        <attributeEditorField name="pipe_id" showLabel="1" index="1"/>
        <attributeEditorField name="pipe_display_name" showLabel="1" index="2"/>
        <attributeEditorField name="pipe_code" showLabel="1" index="3"/>
        <attributeEditorField name="pipe_calculation_type" showLabel="1" index="6"/>
        <attributeEditorField name="pipe_dist_calc_points" showLabel="1" index="12"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpressionEnabled="0" name="Characteristics" showLabel="1" columnCount="1" groupBox="1" visibilityExpression="">
        <attributeEditorField name="pipe_invert_level_start_point" showLabel="1" index="7"/>
        <attributeEditorField name="pipe_invert_level_end_point" showLabel="1" index="8"/>
        <attributeEditorField name="pipe_friction_value" showLabel="1" index="10"/>
        <attributeEditorField name="pipe_friction_type" showLabel="1" index="11"/>
        <attributeEditorField name="pipe_material" showLabel="1" index="13"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpressionEnabled="0" name="Cross section definition" showLabel="1" columnCount="1" groupBox="1" visibilityExpression="">
        <attributeEditorField name="pipe_cross_section_definition_id" showLabel="1" index="9"/>
        <attributeEditorField name="def_shape" showLabel="1" index="20"/>
        <attributeEditorField name="def_width" showLabel="1" index="21"/>
        <attributeEditorField name="def_height" showLabel="1" index="22"/>
        <attributeEditorField name="def_code" showLabel="1" index="23"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpressionEnabled="0" name="Visualization" showLabel="1" columnCount="1" groupBox="1" visibilityExpression="">
        <attributeEditorField name="pipe_sewerage_type" showLabel="1" index="5"/>
        <attributeEditorField name="pipe_zoom_category" showLabel="1" index="16"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpressionEnabled="0" name="Connection nodes" showLabel="1" columnCount="1" groupBox="1" visibilityExpression="">
        <attributeEditorField name="pipe_connection_node_start_id" showLabel="1" index="17"/>
        <attributeEditorField name="pipe_connection_node_end_id" showLabel="1" index="18"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="ROWID" editable="1"/>
    <field name="def_code" editable="0"/>
    <field name="def_height" editable="0"/>
    <field name="def_id" editable="1"/>
    <field name="def_shape" editable="0"/>
    <field name="def_width" editable="0"/>
    <field name="pipe_calculation_type" editable="1"/>
    <field name="pipe_code" editable="1"/>
    <field name="pipe_connection_node_end_id" editable="0"/>
    <field name="pipe_connection_node_start_id" editable="0"/>
    <field name="pipe_cross_section_definition_id" editable="1"/>
    <field name="pipe_display_name" editable="1"/>
    <field name="pipe_dist_calc_points" editable="1"/>
    <field name="pipe_friction_type" editable="1"/>
    <field name="pipe_friction_value" editable="1"/>
    <field name="pipe_id" editable="1"/>
    <field name="pipe_invert_level_end_point" editable="1"/>
    <field name="pipe_invert_level_start_point" editable="1"/>
    <field name="pipe_material" editable="1"/>
    <field name="pipe_original_length" editable="1"/>
    <field name="pipe_pipe_quality" editable="1"/>
    <field name="pipe_profile_num" editable="1"/>
    <field name="pipe_sewerage_type" editable="1"/>
    <field name="pipe_zoom_category" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="ROWID" labelOnTop="0"/>
    <field name="def_code" labelOnTop="0"/>
    <field name="def_height" labelOnTop="0"/>
    <field name="def_id" labelOnTop="0"/>
    <field name="def_shape" labelOnTop="0"/>
    <field name="def_width" labelOnTop="0"/>
    <field name="pipe_calculation_type" labelOnTop="0"/>
    <field name="pipe_code" labelOnTop="0"/>
    <field name="pipe_connection_node_end_id" labelOnTop="0"/>
    <field name="pipe_connection_node_start_id" labelOnTop="0"/>
    <field name="pipe_cross_section_definition_id" labelOnTop="0"/>
    <field name="pipe_display_name" labelOnTop="0"/>
    <field name="pipe_dist_calc_points" labelOnTop="0"/>
    <field name="pipe_friction_type" labelOnTop="0"/>
    <field name="pipe_friction_value" labelOnTop="0"/>
    <field name="pipe_id" labelOnTop="0"/>
    <field name="pipe_invert_level_end_point" labelOnTop="0"/>
    <field name="pipe_invert_level_start_point" labelOnTop="0"/>
    <field name="pipe_material" labelOnTop="0"/>
    <field name="pipe_original_length" labelOnTop="0"/>
    <field name="pipe_pipe_quality" labelOnTop="0"/>
    <field name="pipe_profile_num" labelOnTop="0"/>
    <field name="pipe_sewerage_type" labelOnTop="0"/>
    <field name="pipe_zoom_category" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>"ROWID"</previewExpression>
  <mapTip>display_name</mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
