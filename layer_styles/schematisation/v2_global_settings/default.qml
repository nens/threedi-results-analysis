<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" minScale="1e+08" version="3.22.10-Białowieża" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" maxScale="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal endExpression="" endField="" fixedDuration="0" durationField="" enabled="0" durationUnit="min" startField="" startExpression="" mode="0" limitMode="0" accumulate="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <Option type="Map">
      <Option type="List" name="dualview/previewExpressions">
        <Option value="&quot;id&quot;" type="QString"/>
      </Option>
      <Option value="0" type="QString" name="embeddedWidgets/count"/>
      <Option name="variableNames"/>
      <Option name="variableValues"/>
    </Option>
  </customproperties>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <legend showLabelLegend="0" type="default-vector"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field configurationFlags="None" name="id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="use_2d_flow">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="use_1d_flow">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="manhole_storage_area">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="sim_time_step">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="output_time_step">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="nr_timesteps">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="start_time">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="allow_null"/>
            <Option value="true" type="bool" name="calendar_popup"/>
            <Option value="yyyy-MM-dd HH:mm:ss" type="QString" name="display_format"/>
            <Option value="yyyy-MM-dd HH:mm:ss" type="QString" name="field_format"/>
            <Option value="false" type="bool" name="field_iso_format"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="start_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="allow_null"/>
            <Option value="true" type="bool" name="calendar_popup"/>
            <Option value="yyyy-MM-dd" type="QString" name="display_format"/>
            <Option value="yyyy-MM-dd" type="QString" name="field_format"/>
            <Option value="false" type="bool" name="field_iso_format"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="grid_space">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="dist_calc_points">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="kmax">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="guess_dams">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="0" type="int" name="TextDisplayMethod"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="table_step_size">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="flooding_threshold">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="advection_1d">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="0: Do not use advection 1d"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1: Use advection 1d"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: Experimental advection 1d"/>
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3: Experimental advection 1d"/>
              </Option>
              <Option type="Map">
                <Option value="4" type="QString" name="4: Experimental advection 1d"/>
              </Option>
              <Option type="Map">
                <Option value="5" type="QString" name="5: Experimental advection 1d"/>
              </Option>
              <Option type="Map">
                <Option value="6" type="QString" name="6: Experimental advection 1d"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="advection_2d">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="0: Do not use advection 2d"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1: Use advection 2d"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="dem_file">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="frict_type">
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
    <field configurationFlags="None" name="frict_coef">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="frict_coef_file">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="water_level_ini_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="max"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="min"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="average"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="initial_waterlevel">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="initial_waterlevel_file">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="interception_global">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="interception_file">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="dem_obstacle_detection">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="0" type="int" name="TextDisplayMethod"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="dem_obstacle_height">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="embedded_cutoff_threshold">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="epsg_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="timestep_plus">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="0" type="int" name="TextDisplayMethod"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="max_angle_1d_advection">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="minimum_sim_time_step">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="maximum_sim_time_step">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="frict_avg">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="0" type="int" name="TextDisplayMethod"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="wind_shielding_file">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="use_0d_inflow">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="0: do not use 0d inflow"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1: use v2_impervious_surface"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: use v2_surface"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="table_step_size_1d">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="use_2d_rain">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="0" type="int" name="TextDisplayMethod"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="initial_groundwater_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="initial_groundwater_level_file">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="initial_groundwater_level_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="max"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="min"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="average"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="numerical_settings_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="interflow_settings_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="control_group_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="simple_infiltration_settings_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="groundwater_settings_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="maximum_table_step_size">
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
    <alias index="0" field="id" name=""/>
    <alias index="1" field="use_2d_flow" name=""/>
    <alias index="2" field="use_1d_flow" name=""/>
    <alias index="3" field="manhole_storage_area" name=""/>
    <alias index="4" field="name" name=""/>
    <alias index="5" field="sim_time_step" name=""/>
    <alias index="6" field="output_time_step" name=""/>
    <alias index="7" field="nr_timesteps" name=""/>
    <alias index="8" field="start_time" name=""/>
    <alias index="9" field="start_date" name=""/>
    <alias index="10" field="grid_space" name=""/>
    <alias index="11" field="dist_calc_points" name=""/>
    <alias index="12" field="kmax" name=""/>
    <alias index="13" field="guess_dams" name=""/>
    <alias index="14" field="table_step_size" name=""/>
    <alias index="15" field="flooding_threshold" name=""/>
    <alias index="16" field="advection_1d" name=""/>
    <alias index="17" field="advection_2d" name=""/>
    <alias index="18" field="dem_file" name=""/>
    <alias index="19" field="frict_type" name=""/>
    <alias index="20" field="frict_coef" name=""/>
    <alias index="21" field="frict_coef_file" name=""/>
    <alias index="22" field="water_level_ini_type" name=""/>
    <alias index="23" field="initial_waterlevel" name=""/>
    <alias index="24" field="initial_waterlevel_file" name=""/>
    <alias index="25" field="interception_global" name=""/>
    <alias index="26" field="interception_file" name=""/>
    <alias index="27" field="dem_obstacle_detection" name=""/>
    <alias index="28" field="dem_obstacle_height" name=""/>
    <alias index="29" field="embedded_cutoff_threshold" name=""/>
    <alias index="30" field="epsg_code" name=""/>
    <alias index="31" field="timestep_plus" name=""/>
    <alias index="32" field="max_angle_1d_advection" name=""/>
    <alias index="33" field="minimum_sim_time_step" name=""/>
    <alias index="34" field="maximum_sim_time_step" name=""/>
    <alias index="35" field="frict_avg" name=""/>
    <alias index="36" field="wind_shielding_file" name=""/>
    <alias index="37" field="use_0d_inflow" name=""/>
    <alias index="38" field="table_step_size_1d" name=""/>
    <alias index="39" field="use_2d_rain" name=""/>
    <alias index="40" field="initial_groundwater_level" name=""/>
    <alias index="41" field="initial_groundwater_level_file" name=""/>
    <alias index="42" field="initial_groundwater_level_type" name=""/>
    <alias index="43" field="numerical_settings_id" name=""/>
    <alias index="44" field="interflow_settings_id" name=""/>
    <alias index="45" field="control_group_id" name=""/>
    <alias index="46" field="simple_infiltration_settings_id" name=""/>
    <alias index="47" field="groundwater_settings_id" name=""/>
    <alias index="48" field="maximum_table_step_size" name=""/>
  </aliases>
  <defaults>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" field="id" applyOnUpdate="0"/>
    <default expression="" field="use_2d_flow" applyOnUpdate="0"/>
    <default expression="" field="use_1d_flow" applyOnUpdate="0"/>
    <default expression="" field="manhole_storage_area" applyOnUpdate="0"/>
    <default expression="" field="name" applyOnUpdate="0"/>
    <default expression="" field="sim_time_step" applyOnUpdate="0"/>
    <default expression="" field="output_time_step" applyOnUpdate="0"/>
    <default expression="" field="nr_timesteps" applyOnUpdate="0"/>
    <default expression=" to_date( now() ) ||  ' 00:00:00'" field="start_time" applyOnUpdate="0"/>
    <default expression=" to_date(now() )" field="start_date" applyOnUpdate="0"/>
    <default expression="" field="grid_space" applyOnUpdate="0"/>
    <default expression="10000" field="dist_calc_points" applyOnUpdate="0"/>
    <default expression="" field="kmax" applyOnUpdate="0"/>
    <default expression="0" field="guess_dams" applyOnUpdate="0"/>
    <default expression="0.01" field="table_step_size" applyOnUpdate="0"/>
    <default expression="0.001" field="flooding_threshold" applyOnUpdate="0"/>
    <default expression="" field="advection_1d" applyOnUpdate="0"/>
    <default expression="" field="advection_2d" applyOnUpdate="0"/>
    <default expression="" field="dem_file" applyOnUpdate="0"/>
    <default expression="2" field="frict_type" applyOnUpdate="0"/>
    <default expression="" field="frict_coef" applyOnUpdate="0"/>
    <default expression="" field="frict_coef_file" applyOnUpdate="0"/>
    <default expression="" field="water_level_ini_type" applyOnUpdate="0"/>
    <default expression="" field="initial_waterlevel" applyOnUpdate="0"/>
    <default expression="" field="initial_waterlevel_file" applyOnUpdate="0"/>
    <default expression="" field="interception_global" applyOnUpdate="0"/>
    <default expression="" field="interception_file" applyOnUpdate="0"/>
    <default expression="0" field="dem_obstacle_detection" applyOnUpdate="0"/>
    <default expression="" field="dem_obstacle_height" applyOnUpdate="0"/>
    <default expression="" field="embedded_cutoff_threshold" applyOnUpdate="0"/>
    <default expression="" field="epsg_code" applyOnUpdate="0"/>
    <default expression="0" field="timestep_plus" applyOnUpdate="0"/>
    <default expression="" field="max_angle_1d_advection" applyOnUpdate="0"/>
    <default expression="" field="minimum_sim_time_step" applyOnUpdate="0"/>
    <default expression="" field="maximum_sim_time_step" applyOnUpdate="0"/>
    <default expression="0" field="frict_avg" applyOnUpdate="0"/>
    <default expression="" field="wind_shielding_file" applyOnUpdate="0"/>
    <default expression="" field="use_0d_inflow" applyOnUpdate="0"/>
    <default expression="" field="table_step_size_1d" applyOnUpdate="0"/>
    <default expression="" field="use_2d_rain" applyOnUpdate="0"/>
    <default expression="" field="initial_groundwater_level" applyOnUpdate="0"/>
    <default expression="" field="initial_groundwater_level_file" applyOnUpdate="0"/>
    <default expression="" field="initial_groundwater_level_type" applyOnUpdate="0"/>
    <default expression="1" field="numerical_settings_id" applyOnUpdate="0"/>
    <default expression="" field="interflow_settings_id" applyOnUpdate="0"/>
    <default expression="" field="control_group_id" applyOnUpdate="0"/>
    <default expression="" field="simple_infiltration_settings_id" applyOnUpdate="0"/>
    <default expression="" field="groundwater_settings_id" applyOnUpdate="0"/>
    <default expression="" field="maximum_table_step_size" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" constraints="3" unique_strength="1" exp_strength="0" field="id"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="use_2d_flow"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="use_1d_flow"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="manhole_storage_area"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="name"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="sim_time_step"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="output_time_step"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="nr_timesteps"/>
    <constraint notnull_strength="2" constraints="5" unique_strength="0" exp_strength="2" field="start_time"/>
    <constraint notnull_strength="2" constraints="5" unique_strength="0" exp_strength="2" field="start_date"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="grid_space"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="dist_calc_points"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="kmax"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="guess_dams"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="table_step_size"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="flooding_threshold"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="advection_1d"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="advection_2d"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="dem_file"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="frict_type"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="frict_coef"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="frict_coef_file"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="water_level_ini_type"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="initial_waterlevel"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="initial_waterlevel_file"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="interception_global"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="interception_file"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="dem_obstacle_detection"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="dem_obstacle_height"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="embedded_cutoff_threshold"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="epsg_code"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="timestep_plus"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="max_angle_1d_advection"/>
    <constraint notnull_strength="0" constraints="4" unique_strength="0" exp_strength="2" field="minimum_sim_time_step"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="maximum_sim_time_step"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="frict_avg"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="wind_shielding_file"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="use_0d_inflow"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="table_step_size_1d"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="use_2d_rain"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="initial_groundwater_level"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="initial_groundwater_level_file"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="initial_groundwater_level_type"/>
    <constraint notnull_strength="2" constraints="1" unique_strength="0" exp_strength="0" field="numerical_settings_id"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="interflow_settings_id"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="control_group_id"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="simple_infiltration_settings_id"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="groundwater_settings_id"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0" field="maximum_table_step_size"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="id"/>
    <constraint desc="" exp="" field="use_2d_flow"/>
    <constraint desc="" exp="" field="use_1d_flow"/>
    <constraint desc="" exp="" field="manhole_storage_area"/>
    <constraint desc="" exp="" field="name"/>
    <constraint desc="" exp="" field="sim_time_step"/>
    <constraint desc="" exp="" field="output_time_step"/>
    <constraint desc="" exp="" field="nr_timesteps"/>
    <constraint desc="" exp="&quot;start_time&quot;" field="start_time"/>
    <constraint desc="" exp="&quot;start_date&quot; is not null" field="start_date"/>
    <constraint desc="" exp="" field="grid_space"/>
    <constraint desc="" exp="" field="dist_calc_points"/>
    <constraint desc="" exp="" field="kmax"/>
    <constraint desc="" exp="" field="guess_dams"/>
    <constraint desc="" exp="" field="table_step_size"/>
    <constraint desc="" exp="" field="flooding_threshold"/>
    <constraint desc="" exp="" field="advection_1d"/>
    <constraint desc="" exp="" field="advection_2d"/>
    <constraint desc="" exp="" field="dem_file"/>
    <constraint desc="" exp="" field="frict_type"/>
    <constraint desc="" exp="" field="frict_coef"/>
    <constraint desc="" exp="" field="frict_coef_file"/>
    <constraint desc="" exp="" field="water_level_ini_type"/>
    <constraint desc="" exp="" field="initial_waterlevel"/>
    <constraint desc="" exp="" field="initial_waterlevel_file"/>
    <constraint desc="" exp="" field="interception_global"/>
    <constraint desc="" exp="" field="interception_file"/>
    <constraint desc="" exp="" field="dem_obstacle_detection"/>
    <constraint desc="" exp="" field="dem_obstacle_height"/>
    <constraint desc="" exp="" field="embedded_cutoff_threshold"/>
    <constraint desc="" exp="" field="epsg_code"/>
    <constraint desc="" exp="" field="timestep_plus"/>
    <constraint desc="" exp="" field="max_angle_1d_advection"/>
    <constraint desc="" exp=" &quot;minimum_sim_time_step&quot; &lt; &quot;sim_time_step&quot; " field="minimum_sim_time_step"/>
    <constraint desc="" exp="" field="maximum_sim_time_step"/>
    <constraint desc="" exp="" field="frict_avg"/>
    <constraint desc="" exp="" field="wind_shielding_file"/>
    <constraint desc="" exp="" field="use_0d_inflow"/>
    <constraint desc="" exp="" field="table_step_size_1d"/>
    <constraint desc="" exp="" field="use_2d_rain"/>
    <constraint desc="" exp="" field="initial_groundwater_level"/>
    <constraint desc="" exp="" field="initial_groundwater_level_file"/>
    <constraint desc="" exp="" field="initial_groundwater_level_type"/>
    <constraint desc="" exp="" field="numerical_settings_id"/>
    <constraint desc="" exp="" field="interflow_settings_id"/>
    <constraint desc="" exp="" field="control_group_id"/>
    <constraint desc="" exp="" field="simple_infiltration_settings_id"/>
    <constraint desc="" exp="" field="groundwater_settings_id"/>
    <constraint desc="" exp="" field="maximum_table_step_size"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortExpression="&quot;maximum_sim_time_step&quot;" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column hidden="0" width="116" type="field" name="maximum_sim_time_step"/>
      <column hidden="0" width="-1" type="field" name="nr_timesteps"/>
      <column hidden="0" width="-1" type="field" name="dem_file"/>
      <column hidden="0" width="-1" type="field" name="minimum_sim_time_step"/>
      <column hidden="0" width="-1" type="field" name="id"/>
      <column hidden="0" width="-1" type="field" name="frict_coef_file"/>
      <column hidden="0" width="-1" type="field" name="initial_groundwater_level_file"/>
      <column hidden="0" width="-1" type="field" name="initial_waterlevel"/>
      <column hidden="0" width="-1" type="field" name="epsg_code"/>
      <column hidden="0" width="-1" type="field" name="numerical_settings_id"/>
      <column hidden="0" width="-1" type="field" name="dem_obstacle_detection"/>
      <column hidden="0" width="-1" type="field" name="frict_avg"/>
      <column hidden="0" width="-1" type="field" name="initial_groundwater_level_type"/>
      <column hidden="0" width="-1" type="field" name="water_level_ini_type"/>
      <column hidden="0" width="-1" type="field" name="grid_space"/>
      <column hidden="0" width="-1" type="field" name="advection_2d"/>
      <column hidden="0" width="-1" type="field" name="embedded_cutoff_threshold"/>
      <column hidden="0" width="-1" type="field" name="dist_calc_points"/>
      <column hidden="0" width="-1" type="field" name="start_date"/>
      <column hidden="0" width="-1" type="field" name="initial_groundwater_level"/>
      <column hidden="0" width="-1" type="field" name="output_time_step"/>
      <column hidden="0" width="-1" type="field" name="interflow_settings_id"/>
      <column hidden="0" width="-1" type="field" name="table_step_size"/>
      <column hidden="0" width="-1" type="field" name="use_1d_flow"/>
      <column hidden="0" width="-1" type="field" name="start_time"/>
      <column hidden="0" width="-1" type="field" name="use_2d_rain"/>
      <column hidden="0" width="-1" type="field" name="kmax"/>
      <column hidden="0" width="-1" type="field" name="initial_waterlevel_file"/>
      <column hidden="0" width="-1" type="field" name="sim_time_step"/>
      <column hidden="0" width="-1" type="field" name="frict_coef"/>
      <column hidden="0" width="-1" type="field" name="guess_dams"/>
      <column hidden="0" width="-1" type="field" name="control_group_id"/>
      <column hidden="0" width="-1" type="field" name="dem_obstacle_height"/>
      <column hidden="0" width="-1" type="field" name="timestep_plus"/>
      <column hidden="0" width="-1" type="field" name="name"/>
      <column hidden="0" width="-1" type="field" name="flooding_threshold"/>
      <column hidden="0" width="-1" type="field" name="frict_type"/>
      <column hidden="0" width="-1" type="field" name="use_2d_flow"/>
      <column hidden="0" width="-1" type="field" name="max_angle_1d_advection"/>
      <column hidden="0" width="-1" type="field" name="advection_1d"/>
      <column hidden="0" width="-1" type="field" name="wind_shielding_file"/>
      <column hidden="0" width="-1" type="field" name="simple_infiltration_settings_id"/>
      <column hidden="0" width="-1" type="field" name="groundwater_settings_id"/>
      <column hidden="0" width="-1" type="field" name="manhole_storage_area"/>
      <column hidden="0" width="-1" type="field" name="use_0d_inflow"/>
      <column hidden="0" width="-1" type="field" name="table_step_size_1d"/>
      <column hidden="1" width="-1" type="actions"/>
      <column hidden="0" width="-1" type="field" name="interception_global"/>
      <column hidden="0" width="-1" type="field" name="maximum_table_step_size"/>
      <column hidden="0" width="-1" type="field" name="interception_file"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer visibilityExpression="" visibilityExpressionEnabled="0" groupBox="0" name="General" columnCount="1" showLabel="1">
      <attributeEditorField index="0" name="id" showLabel="1"/>
      <attributeEditorField index="4" name="name" showLabel="1"/>
      <attributeEditorField index="37" name="use_0d_inflow" showLabel="1"/>
      <attributeEditorField index="2" name="use_1d_flow" showLabel="1"/>
      <attributeEditorField index="39" name="use_2d_rain" showLabel="1"/>
      <attributeEditorField index="1" name="use_2d_flow" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer visibilityExpression="" visibilityExpressionEnabled="0" groupBox="0" name="Grid" columnCount="1" showLabel="1">
      <attributeEditorField index="10" name="grid_space" showLabel="1"/>
      <attributeEditorField index="12" name="kmax" showLabel="1"/>
      <attributeEditorField index="14" name="table_step_size" showLabel="1"/>
      <attributeEditorField index="48" name="maximum_table_step_size" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer visibilityExpression="&quot;advection_1d&quot;" visibilityExpressionEnabled="0" groupBox="0" name="Terrain information" columnCount="1" showLabel="1">
      <attributeEditorContainer visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="DEM" columnCount="1" showLabel="1">
        <attributeEditorField index="18" name="dem_file" showLabel="1"/>
        <attributeEditorField index="30" name="epsg_code" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Friction" columnCount="1" showLabel="1">
        <attributeEditorField index="21" name="frict_coef_file" showLabel="1"/>
        <attributeEditorField index="20" name="frict_coef" showLabel="1"/>
        <attributeEditorField index="19" name="frict_type" showLabel="1"/>
        <attributeEditorField index="35" name="frict_avg" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Groundwater" columnCount="1" showLabel="1">
        <attributeEditorField index="41" name="initial_groundwater_level_file" showLabel="1"/>
        <attributeEditorField index="40" name="initial_groundwater_level" showLabel="1"/>
        <attributeEditorField index="42" name="initial_groundwater_level_type" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Initial waterlevel" columnCount="1" showLabel="1">
        <attributeEditorField index="24" name="initial_waterlevel_file" showLabel="1"/>
        <attributeEditorField index="23" name="initial_waterlevel" showLabel="1"/>
        <attributeEditorField index="22" name="water_level_ini_type" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Interception" columnCount="1" showLabel="1">
        <attributeEditorField index="26" name="interception_file" showLabel="1"/>
        <attributeEditorField index="25" name="interception_global" showLabel="1"/>
        <attributeEditorField index="-1" name="max_interception" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1" name="Wind" columnCount="1" showLabel="1">
        <attributeEditorField index="36" name="wind_shielding_file" showLabel="1"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
    <attributeEditorContainer visibilityExpression="" visibilityExpressionEnabled="0" groupBox="0" name="Time" columnCount="1" showLabel="1">
      <attributeEditorField index="9" name="start_date" showLabel="1"/>
      <attributeEditorField index="8" name="start_time" showLabel="1"/>
      <attributeEditorField index="5" name="sim_time_step" showLabel="1"/>
      <attributeEditorField index="31" name="timestep_plus" showLabel="1"/>
      <attributeEditorField index="33" name="minimum_sim_time_step" showLabel="1"/>
      <attributeEditorField index="34" name="maximum_sim_time_step" showLabel="1"/>
      <attributeEditorField index="7" name="nr_timesteps" showLabel="1"/>
      <attributeEditorField index="6" name="output_time_step" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer visibilityExpression="" visibilityExpressionEnabled="0" groupBox="0" name="Settings id's" columnCount="1" showLabel="1">
      <attributeEditorField index="44" name="interflow_settings_id" showLabel="1"/>
      <attributeEditorField index="47" name="groundwater_settings_id" showLabel="1"/>
      <attributeEditorField index="43" name="numerical_settings_id" showLabel="1"/>
      <attributeEditorField index="46" name="simple_infiltration_settings_id" showLabel="1"/>
      <attributeEditorField index="45" name="control_group_id" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer visibilityExpression="" visibilityExpressionEnabled="0" groupBox="0" name="Extra options 1D" columnCount="1" showLabel="1">
      <attributeEditorField index="16" name="advection_1d" showLabel="1"/>
      <attributeEditorField index="11" name="dist_calc_points" showLabel="1"/>
      <attributeEditorField index="3" name="manhole_storage_area" showLabel="1"/>
      <attributeEditorField index="32" name="max_angle_1d_advection" showLabel="1"/>
      <attributeEditorField index="38" name="table_step_size_1d" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer visibilityExpression="" visibilityExpressionEnabled="0" groupBox="0" name="Extra options 2D" columnCount="1" showLabel="1">
      <attributeEditorField index="17" name="advection_2d" showLabel="1"/>
      <attributeEditorField index="27" name="dem_obstacle_detection" showLabel="1"/>
      <attributeEditorField index="13" name="guess_dams" showLabel="1"/>
      <attributeEditorField index="28" name="dem_obstacle_height" showLabel="1"/>
      <attributeEditorField index="29" name="embedded_cutoff_threshold" showLabel="1"/>
      <attributeEditorField index="15" name="flooding_threshold" showLabel="1"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="advection_1d" editable="1"/>
    <field name="advection_2d" editable="1"/>
    <field name="control_group_id" editable="1"/>
    <field name="dem_file" editable="1"/>
    <field name="dem_obstacle_detection" editable="1"/>
    <field name="dem_obstacle_height" editable="1"/>
    <field name="dist_calc_points" editable="1"/>
    <field name="embedded_cutoff_threshold" editable="1"/>
    <field name="epsg_code" editable="1"/>
    <field name="flooding_threshold" editable="1"/>
    <field name="frict_avg" editable="1"/>
    <field name="frict_coef" editable="1"/>
    <field name="frict_coef_file" editable="1"/>
    <field name="frict_type" editable="1"/>
    <field name="grid_space" editable="1"/>
    <field name="groundwater_settings_id" editable="1"/>
    <field name="guess_dams" editable="1"/>
    <field name="id" editable="1"/>
    <field name="initial_groundwater_level" editable="1"/>
    <field name="initial_groundwater_level_file" editable="1"/>
    <field name="initial_groundwater_level_type" editable="1"/>
    <field name="initial_waterlevel" editable="1"/>
    <field name="initial_waterlevel_file" editable="1"/>
    <field name="interception_file" editable="1"/>
    <field name="interception_global" editable="1"/>
    <field name="interflow_settings_id" editable="1"/>
    <field name="kmax" editable="1"/>
    <field name="manhole_storage_area" editable="1"/>
    <field name="max_angle_1d_advection" editable="1"/>
    <field name="max_interception" editable="1"/>
    <field name="max_interception_file" editable="1"/>
    <field name="maximum_sim_time_step" editable="1"/>
    <field name="maximum_table_step_size" editable="1"/>
    <field name="minimum_sim_time_step" editable="1"/>
    <field name="name" editable="1"/>
    <field name="nr_timesteps" editable="1"/>
    <field name="numerical_settings_id" editable="1"/>
    <field name="output_time_step" editable="1"/>
    <field name="sim_time_step" editable="1"/>
    <field name="simple_infiltration_settings_id" editable="1"/>
    <field name="start_date" editable="1"/>
    <field name="start_time" editable="1"/>
    <field name="table_step_size" editable="1"/>
    <field name="table_step_size_1d" editable="1"/>
    <field name="table_step_size_volume_2d" editable="1"/>
    <field name="timestep_plus" editable="1"/>
    <field name="use_0d_inflow" editable="1"/>
    <field name="use_1d_flow" editable="1"/>
    <field name="use_2d_flow" editable="1"/>
    <field name="use_2d_rain" editable="1"/>
    <field name="water_level_ini_type" editable="1"/>
    <field name="wind_shielding_file" editable="1"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="advection_1d"/>
    <field labelOnTop="0" name="advection_2d"/>
    <field labelOnTop="0" name="control_group_id"/>
    <field labelOnTop="0" name="dem_file"/>
    <field labelOnTop="0" name="dem_obstacle_detection"/>
    <field labelOnTop="0" name="dem_obstacle_height"/>
    <field labelOnTop="0" name="dist_calc_points"/>
    <field labelOnTop="0" name="embedded_cutoff_threshold"/>
    <field labelOnTop="0" name="epsg_code"/>
    <field labelOnTop="0" name="flooding_threshold"/>
    <field labelOnTop="0" name="frict_avg"/>
    <field labelOnTop="0" name="frict_coef"/>
    <field labelOnTop="0" name="frict_coef_file"/>
    <field labelOnTop="0" name="frict_type"/>
    <field labelOnTop="0" name="grid_space"/>
    <field labelOnTop="0" name="groundwater_settings_id"/>
    <field labelOnTop="0" name="guess_dams"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="initial_groundwater_level"/>
    <field labelOnTop="0" name="initial_groundwater_level_file"/>
    <field labelOnTop="0" name="initial_groundwater_level_type"/>
    <field labelOnTop="0" name="initial_waterlevel"/>
    <field labelOnTop="0" name="initial_waterlevel_file"/>
    <field labelOnTop="0" name="interception_file"/>
    <field labelOnTop="0" name="interception_global"/>
    <field labelOnTop="0" name="interflow_settings_id"/>
    <field labelOnTop="0" name="kmax"/>
    <field labelOnTop="0" name="manhole_storage_area"/>
    <field labelOnTop="0" name="max_angle_1d_advection"/>
    <field labelOnTop="0" name="max_interception"/>
    <field labelOnTop="0" name="max_interception_file"/>
    <field labelOnTop="0" name="maximum_sim_time_step"/>
    <field labelOnTop="0" name="maximum_table_step_size"/>
    <field labelOnTop="0" name="minimum_sim_time_step"/>
    <field labelOnTop="0" name="name"/>
    <field labelOnTop="0" name="nr_timesteps"/>
    <field labelOnTop="0" name="numerical_settings_id"/>
    <field labelOnTop="0" name="output_time_step"/>
    <field labelOnTop="0" name="sim_time_step"/>
    <field labelOnTop="0" name="simple_infiltration_settings_id"/>
    <field labelOnTop="0" name="start_date"/>
    <field labelOnTop="0" name="start_time"/>
    <field labelOnTop="0" name="table_step_size"/>
    <field labelOnTop="0" name="table_step_size_1d"/>
    <field labelOnTop="0" name="table_step_size_volume_2d"/>
    <field labelOnTop="0" name="timestep_plus"/>
    <field labelOnTop="0" name="use_0d_inflow"/>
    <field labelOnTop="0" name="use_1d_flow"/>
    <field labelOnTop="0" name="use_2d_flow"/>
    <field labelOnTop="0" name="use_2d_rain"/>
    <field labelOnTop="0" name="water_level_ini_type"/>
    <field labelOnTop="0" name="wind_shielding_file"/>
  </labelOnTop>
  <reuseLastValue>
    <field reuseLastValue="0" name="advection_1d"/>
    <field reuseLastValue="0" name="advection_2d"/>
    <field reuseLastValue="0" name="control_group_id"/>
    <field reuseLastValue="0" name="dem_file"/>
    <field reuseLastValue="0" name="dem_obstacle_detection"/>
    <field reuseLastValue="0" name="dem_obstacle_height"/>
    <field reuseLastValue="0" name="dist_calc_points"/>
    <field reuseLastValue="0" name="embedded_cutoff_threshold"/>
    <field reuseLastValue="0" name="epsg_code"/>
    <field reuseLastValue="0" name="flooding_threshold"/>
    <field reuseLastValue="0" name="frict_avg"/>
    <field reuseLastValue="0" name="frict_coef"/>
    <field reuseLastValue="0" name="frict_coef_file"/>
    <field reuseLastValue="0" name="frict_type"/>
    <field reuseLastValue="0" name="grid_space"/>
    <field reuseLastValue="0" name="groundwater_settings_id"/>
    <field reuseLastValue="0" name="guess_dams"/>
    <field reuseLastValue="0" name="id"/>
    <field reuseLastValue="0" name="initial_groundwater_level"/>
    <field reuseLastValue="0" name="initial_groundwater_level_file"/>
    <field reuseLastValue="0" name="initial_groundwater_level_type"/>
    <field reuseLastValue="0" name="initial_waterlevel"/>
    <field reuseLastValue="0" name="initial_waterlevel_file"/>
    <field reuseLastValue="0" name="interception_file"/>
    <field reuseLastValue="0" name="interception_global"/>
    <field reuseLastValue="0" name="interflow_settings_id"/>
    <field reuseLastValue="0" name="kmax"/>
    <field reuseLastValue="0" name="manhole_storage_area"/>
    <field reuseLastValue="0" name="max_angle_1d_advection"/>
    <field reuseLastValue="0" name="maximum_sim_time_step"/>
    <field reuseLastValue="0" name="maximum_table_step_size"/>
    <field reuseLastValue="0" name="minimum_sim_time_step"/>
    <field reuseLastValue="0" name="name"/>
    <field reuseLastValue="0" name="nr_timesteps"/>
    <field reuseLastValue="0" name="numerical_settings_id"/>
    <field reuseLastValue="0" name="output_time_step"/>
    <field reuseLastValue="0" name="sim_time_step"/>
    <field reuseLastValue="0" name="simple_infiltration_settings_id"/>
    <field reuseLastValue="0" name="start_date"/>
    <field reuseLastValue="0" name="start_time"/>
    <field reuseLastValue="0" name="table_step_size"/>
    <field reuseLastValue="0" name="table_step_size_1d"/>
    <field reuseLastValue="0" name="timestep_plus"/>
    <field reuseLastValue="0" name="use_0d_inflow"/>
    <field reuseLastValue="0" name="use_1d_flow"/>
    <field reuseLastValue="0" name="use_2d_flow"/>
    <field reuseLastValue="0" name="use_2d_rain"/>
    <field reuseLastValue="0" name="water_level_ini_type"/>
    <field reuseLastValue="0" name="wind_shielding_file"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"id"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
