<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" readOnly="0" version="3.4.11-Madeira" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="1e+8">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property value="id" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="maximum_sim_time_step">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="nr_timesteps">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dem_file">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="minimum_sim_time_step">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="table_step_size_volume_2d">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="frict_coef_file">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="initial_groundwater_level_file">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="initial_waterlevel">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="epsg_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="numerical_settings_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dem_obstacle_detection">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" name="CheckedState" type="QString"/>
            <Option value="0" name="UncheckedState" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="frict_avg">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" name="CheckedState" type="QString"/>
            <Option value="0" name="UncheckedState" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="initial_groundwater_level_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="0" name="max" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="1" name="min" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="average" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="water_level_ini_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="0" name="max" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="1" name="min" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="average" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="grid_space">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="advection_2d">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="0" name="0: Do not use advection 2d" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="1" name="1: Use advection 2d" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="embedded_cutoff_threshold">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dist_calc_points">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_date">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" name="allow_null" type="bool"/>
            <Option value="true" name="calendar_popup" type="bool"/>
            <Option value="yyyy-MM-dd" name="display_format" type="QString"/>
            <Option value="yyyy-MM-dd" name="field_format" type="QString"/>
            <Option value="false" name="field_iso_format" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="initial_groundwater_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="output_time_step">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="interflow_settings_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="table_step_size">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="use_1d_flow">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" name="CheckedState" type="QString"/>
            <Option value="0" name="UncheckedState" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_time">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option value="true" name="allow_null" type="bool"/>
            <Option value="true" name="calendar_popup" type="bool"/>
            <Option value="yyyy-MM-dd HH:mm:ss" name="display_format" type="QString"/>
            <Option value="yyyy-MM-dd HH:mm:ss" name="field_format" type="QString"/>
            <Option value="false" name="field_iso_format" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="use_2d_rain">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" name="CheckedState" type="QString"/>
            <Option value="0" name="UncheckedState" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="interception_global">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="interception_file">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="kmax">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="initial_waterlevel_file">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="sim_time_step">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="frict_coef">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="guess_dams">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" name="CheckedState" type="QString"/>
            <Option value="0" name="UncheckedState" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="control_group_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dem_obstacle_height">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="timestep_plus">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" name="CheckedState" type="QString"/>
            <Option value="0" name="UncheckedState" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="flooding_threshold">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="frict_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="1" name="1: Chèzy" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2: Manning" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="use_2d_flow">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="1" name="CheckedState" type="QString"/>
            <Option value="0" name="UncheckedState" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="max_angle_1d_advection">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="advection_1d">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="0" name="0: Do not use advection 1d" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="1" name="1: Use advection 1d" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2: Experimental advection 1d" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="3" name="3: Experimental advection 1d" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="4" name="4: Experimental advection 1d" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="5" name="5: Experimental advection 1d" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="6" name="6: Experimental advection 1d" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="wind_shielding_file">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="simple_infiltration_settings_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="groundwater_settings_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="manhole_storage_area">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="use_0d_inflow">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="0" name="0: do not use 0d inflow" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="1" name="1: use v2_impervious_surface" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2: use v2_surface" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="table_step_size_1d">
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
    <alias index="0" name="" field="maximum_sim_time_step"/>
    <alias index="1" name="" field="nr_timesteps"/>
    <alias index="2" name="" field="dem_file"/>
    <alias index="3" name="" field="minimum_sim_time_step"/>
    <alias index="4" name="" field="id"/>
    <alias index="5" name="" field="table_step_size_volume_2d"/>
    <alias index="6" name="" field="frict_coef_file"/>
    <alias index="7" name="" field="initial_groundwater_level_file"/>
    <alias index="8" name="" field="initial_waterlevel"/>
    <alias index="9" name="" field="epsg_code"/>
    <alias index="10" name="" field="numerical_settings_id"/>
    <alias index="11" name="" field="dem_obstacle_detection"/>
    <alias index="12" name="" field="frict_avg"/>
    <alias index="13" name="" field="initial_groundwater_level_type"/>
    <alias index="14" name="" field="water_level_ini_type"/>
    <alias index="15" name="" field="grid_space"/>
    <alias index="16" name="" field="advection_2d"/>
    <alias index="17" name="" field="embedded_cutoff_threshold"/>
    <alias index="18" name="" field="dist_calc_points"/>
    <alias index="19" name="" field="start_date"/>
    <alias index="20" name="" field="initial_groundwater_level"/>
    <alias index="21" name="" field="output_time_step"/>
    <alias index="22" name="" field="interflow_settings_id"/>
    <alias index="23" name="" field="table_step_size"/>
    <alias index="24" name="" field="use_1d_flow"/>
    <alias index="25" name="" field="start_time"/>
    <alias index="26" name="" field="use_2d_rain"/>
    <alias index="27" name="" field="interception_global"/>
    <alias index="28" name="" field="interception_file"/>
    <alias index="29" name="" field="kmax"/>
    <alias index="30" name="" field="initial_waterlevel_file"/>
    <alias index="31" name="" field="sim_time_step"/>
    <alias index="32" name="" field="frict_coef"/>
    <alias index="33" name="" field="guess_dams"/>
    <alias index="34" name="" field="control_group_id"/>
    <alias index="35" name="" field="dem_obstacle_height"/>
    <alias index="36" name="" field="timestep_plus"/>
    <alias index="37" name="" field="name"/>
    <alias index="38" name="" field="flooding_threshold"/>
    <alias index="39" name="" field="frict_type"/>
    <alias index="40" name="" field="use_2d_flow"/>
    <alias index="41" name="" field="max_angle_1d_advection"/>
    <alias index="42" name="" field="advection_1d"/>
    <alias index="43" name="" field="wind_shielding_file"/>
    <alias index="44" name="" field="simple_infiltration_settings_id"/>
    <alias index="45" name="" field="groundwater_settings_id"/>
    <alias index="46" name="" field="manhole_storage_area"/>
    <alias index="47" name="" field="use_0d_inflow"/>
    <alias index="48" name="" field="table_step_size_1d"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" expression="" field="maximum_sim_time_step"/>
    <default applyOnUpdate="0" expression="" field="nr_timesteps"/>
    <default applyOnUpdate="0" expression="" field="dem_file"/>
    <default applyOnUpdate="0" expression="" field="minimum_sim_time_step"/>
    <default applyOnUpdate="0" expression="if(maximum(id) is null,1, maximum(id)+1)" field="id"/>
    <default applyOnUpdate="0" expression="" field="table_step_size_volume_2d"/>
    <default applyOnUpdate="0" expression="" field="frict_coef_file"/>
    <default applyOnUpdate="0" expression="" field="initial_groundwater_level_file"/>
    <default applyOnUpdate="0" expression="" field="initial_waterlevel"/>
    <default applyOnUpdate="0" expression="" field="epsg_code"/>
    <default applyOnUpdate="0" expression="1" field="numerical_settings_id"/>
    <default applyOnUpdate="0" expression="0" field="dem_obstacle_detection"/>
    <default applyOnUpdate="0" expression="0" field="frict_avg"/>
    <default applyOnUpdate="0" expression="" field="initial_groundwater_level_type"/>
    <default applyOnUpdate="0" expression="" field="water_level_ini_type"/>
    <default applyOnUpdate="0" expression="" field="grid_space"/>
    <default applyOnUpdate="0" expression="" field="advection_2d"/>
    <default applyOnUpdate="0" expression="" field="embedded_cutoff_threshold"/>
    <default applyOnUpdate="0" expression="10000" field="dist_calc_points"/>
    <default applyOnUpdate="0" expression=" to_date(now() )" field="start_date"/>
    <default applyOnUpdate="0" expression="" field="initial_groundwater_level"/>
    <default applyOnUpdate="0" expression="" field="output_time_step"/>
    <default applyOnUpdate="0" expression="" field="interflow_settings_id"/>
    <default applyOnUpdate="0" expression="0.01" field="table_step_size"/>
    <default applyOnUpdate="0" expression="" field="use_1d_flow"/>
    <default applyOnUpdate="0" expression=" to_date( now() ) ||  ' 00:00:00'" field="start_time"/>
    <default applyOnUpdate="0" expression="" field="use_2d_rain"/>
    <default applyOnUpdate="0" expression="" field="interception_global"/>
    <default applyOnUpdate="0" expression="" field="interception_file"/>
    <default applyOnUpdate="0" expression="" field="kmax"/>
    <default applyOnUpdate="0" expression="" field="initial_waterlevel_file"/>
    <default applyOnUpdate="0" expression="" field="sim_time_step"/>
    <default applyOnUpdate="0" expression="" field="frict_coef"/>
    <default applyOnUpdate="0" expression="0" field="guess_dams"/>
    <default applyOnUpdate="0" expression="" field="control_group_id"/>
    <default applyOnUpdate="0" expression="" field="dem_obstacle_height"/>
    <default applyOnUpdate="0" expression="0" field="timestep_plus"/>
    <default applyOnUpdate="0" expression="" field="name"/>
    <default applyOnUpdate="0" expression="0.001" field="flooding_threshold"/>
    <default applyOnUpdate="0" expression="2" field="frict_type"/>
    <default applyOnUpdate="0" expression="" field="use_2d_flow"/>
    <default applyOnUpdate="0" expression="" field="max_angle_1d_advection"/>
    <default applyOnUpdate="0" expression="" field="advection_1d"/>
    <default applyOnUpdate="0" expression="" field="wind_shielding_file"/>
    <default applyOnUpdate="0" expression="" field="simple_infiltration_settings_id"/>
    <default applyOnUpdate="0" expression="" field="groundwater_settings_id"/>
    <default applyOnUpdate="0" expression="" field="manhole_storage_area"/>
    <default applyOnUpdate="0" expression="" field="use_0d_inflow"/>
    <default applyOnUpdate="0" expression="" field="table_step_size_1d"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" notnull_strength="0" field="maximum_sim_time_step" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="nr_timesteps" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="dem_file" constraints="0" unique_strength="0"/>
    <constraint exp_strength="2" notnull_strength="0" field="minimum_sim_time_step" constraints="4" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="1" field="id" constraints="3" unique_strength="1"/>
    <constraint exp_strength="0" notnull_strength="0" field="table_step_size_volume_2d" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="frict_coef_file" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="initial_groundwater_level_file" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="initial_waterlevel" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="epsg_code" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="numerical_settings_id" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="dem_obstacle_detection" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="frict_avg" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="initial_groundwater_level_type" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="water_level_ini_type" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="grid_space" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="advection_2d" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="embedded_cutoff_threshold" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="dist_calc_points" constraints="1" unique_strength="0"/>
    <constraint exp_strength="2" notnull_strength="2" field="start_date" constraints="5" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="initial_groundwater_level" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="output_time_step" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="interflow_settings_id" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="table_step_size" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="use_1d_flow" constraints="1" unique_strength="0"/>
    <constraint exp_strength="2" notnull_strength="2" field="start_time" constraints="5" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="use_2d_rain" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="interception_global" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="interception_file" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="kmax" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="initial_waterlevel_file" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="sim_time_step" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="frict_coef" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="guess_dams" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="control_group_id" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="dem_obstacle_height" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="timestep_plus" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="name" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="flooding_threshold" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="frict_type" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="use_2d_flow" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="max_angle_1d_advection" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="advection_1d" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="wind_shielding_file" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="simple_infiltration_settings_id" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="groundwater_settings_id" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="manhole_storage_area" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="2" field="use_0d_inflow" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="0" field="table_step_size_1d" constraints="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="maximum_sim_time_step"/>
    <constraint exp="" desc="" field="nr_timesteps"/>
    <constraint exp="" desc="" field="dem_file"/>
    <constraint exp=" &quot;minimum_sim_time_step&quot; &lt; &quot;sim_time_step&quot; " desc="" field="minimum_sim_time_step"/>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="table_step_size_volume_2d"/>
    <constraint exp="" desc="" field="frict_coef_file"/>
    <constraint exp="" desc="" field="initial_groundwater_level_file"/>
    <constraint exp="" desc="" field="initial_waterlevel"/>
    <constraint exp="" desc="" field="epsg_code"/>
    <constraint exp="" desc="" field="numerical_settings_id"/>
    <constraint exp="" desc="" field="dem_obstacle_detection"/>
    <constraint exp="" desc="" field="frict_avg"/>
    <constraint exp="" desc="" field="initial_groundwater_level_type"/>
    <constraint exp="" desc="" field="water_level_ini_type"/>
    <constraint exp="" desc="" field="grid_space"/>
    <constraint exp="" desc="" field="advection_2d"/>
    <constraint exp="" desc="" field="embedded_cutoff_threshold"/>
    <constraint exp="" desc="" field="dist_calc_points"/>
    <constraint exp="&quot;start_date&quot; is not null" desc="" field="start_date"/>
    <constraint exp="" desc="" field="initial_groundwater_level"/>
    <constraint exp="" desc="" field="output_time_step"/>
    <constraint exp="" desc="" field="interflow_settings_id"/>
    <constraint exp="" desc="" field="table_step_size"/>
    <constraint exp="" desc="" field="use_1d_flow"/>
    <constraint exp="&quot;start_time&quot;" desc="" field="start_time"/>
    <constraint exp="" desc="" field="use_2d_rain"/>
    <constraint exp="" desc="" field="interception_global"/>
    <constraint exp="" desc="" field="interception_file"/>
    <constraint exp="" desc="" field="kmax"/>
    <constraint exp="" desc="" field="initial_waterlevel_file"/>
    <constraint exp="" desc="" field="sim_time_step"/>
    <constraint exp="" desc="" field="frict_coef"/>
    <constraint exp="" desc="" field="guess_dams"/>
    <constraint exp="" desc="" field="control_group_id"/>
    <constraint exp="" desc="" field="dem_obstacle_height"/>
    <constraint exp="" desc="" field="timestep_plus"/>
    <constraint exp="" desc="" field="name"/>
    <constraint exp="" desc="" field="flooding_threshold"/>
    <constraint exp="" desc="" field="frict_type"/>
    <constraint exp="" desc="" field="use_2d_flow"/>
    <constraint exp="" desc="" field="max_angle_1d_advection"/>
    <constraint exp="" desc="" field="advection_1d"/>
    <constraint exp="" desc="" field="wind_shielding_file"/>
    <constraint exp="" desc="" field="simple_infiltration_settings_id"/>
    <constraint exp="" desc="" field="groundwater_settings_id"/>
    <constraint exp="" desc="" field="manhole_storage_area"/>
    <constraint exp="" desc="" field="use_0d_inflow"/>
    <constraint exp="" desc="" field="table_step_size_1d"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="&quot;maximum_sim_time_step&quot;" sortOrder="0">
    <columns>
      <column width="116" hidden="0" name="maximum_sim_time_step" type="field"/>
      <column width="-1" hidden="0" name="nr_timesteps" type="field"/>
      <column width="-1" hidden="0" name="dem_file" type="field"/>
      <column width="-1" hidden="0" name="minimum_sim_time_step" type="field"/>
      <column width="-1" hidden="0" name="id" type="field"/>
      <column width="-1" hidden="0" name="table_step_size_volume_2d" type="field"/>
      <column width="-1" hidden="0" name="frict_coef_file" type="field"/>
      <column width="-1" hidden="0" name="initial_groundwater_level_file" type="field"/>
      <column width="-1" hidden="0" name="initial_waterlevel" type="field"/>
      <column width="-1" hidden="0" name="epsg_code" type="field"/>
      <column width="-1" hidden="0" name="numerical_settings_id" type="field"/>
      <column width="-1" hidden="0" name="dem_obstacle_detection" type="field"/>
      <column width="-1" hidden="0" name="frict_avg" type="field"/>
      <column width="-1" hidden="0" name="initial_groundwater_level_type" type="field"/>
      <column width="-1" hidden="0" name="water_level_ini_type" type="field"/>
      <column width="-1" hidden="0" name="grid_space" type="field"/>
      <column width="-1" hidden="0" name="advection_2d" type="field"/>
      <column width="-1" hidden="0" name="embedded_cutoff_threshold" type="field"/>
      <column width="-1" hidden="0" name="dist_calc_points" type="field"/>
      <column width="-1" hidden="0" name="start_date" type="field"/>
      <column width="-1" hidden="0" name="initial_groundwater_level" type="field"/>
      <column width="-1" hidden="0" name="output_time_step" type="field"/>
      <column width="-1" hidden="0" name="interflow_settings_id" type="field"/>
      <column width="-1" hidden="0" name="table_step_size" type="field"/>
      <column width="-1" hidden="0" name="use_1d_flow" type="field"/>
      <column width="-1" hidden="0" name="start_time" type="field"/>
      <column width="-1" hidden="0" name="use_2d_rain" type="field"/>
      <column width="-1" hidden="0" name="kmax" type="field"/>
      <column width="-1" hidden="0" name="initial_waterlevel_file" type="field"/>
      <column width="-1" hidden="0" name="sim_time_step" type="field"/>
      <column width="-1" hidden="0" name="frict_coef" type="field"/>
      <column width="-1" hidden="0" name="guess_dams" type="field"/>
      <column width="-1" hidden="0" name="control_group_id" type="field"/>
      <column width="-1" hidden="0" name="dem_obstacle_height" type="field"/>
      <column width="-1" hidden="0" name="timestep_plus" type="field"/>
      <column width="-1" hidden="0" name="name" type="field"/>
      <column width="-1" hidden="0" name="flooding_threshold" type="field"/>
      <column width="-1" hidden="0" name="frict_type" type="field"/>
      <column width="-1" hidden="0" name="use_2d_flow" type="field"/>
      <column width="-1" hidden="0" name="max_angle_1d_advection" type="field"/>
      <column width="-1" hidden="0" name="advection_1d" type="field"/>
      <column width="-1" hidden="0" name="wind_shielding_file" type="field"/>
      <column width="-1" hidden="0" name="simple_infiltration_settings_id" type="field"/>
      <column width="-1" hidden="0" name="groundwater_settings_id" type="field"/>
      <column width="-1" hidden="0" name="manhole_storage_area" type="field"/>
      <column width="-1" hidden="0" name="use_0d_inflow" type="field"/>
      <column width="-1" hidden="0" name="table_step_size_1d" type="field"/>
      <column width="-1" hidden="1" type="actions"/>
      <column width="-1" hidden="0" name="interception_global" type="field"/>
      <column width="-1" hidden="0" name="interception_file" type="field"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
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
    <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="General" groupBox="0" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="4" name="id"/>
      <attributeEditorField showLabel="1" index="37" name="name"/>
      <attributeEditorField showLabel="1" index="47" name="use_0d_inflow"/>
      <attributeEditorField showLabel="1" index="24" name="use_1d_flow"/>
      <attributeEditorField showLabel="1" index="26" name="use_2d_rain"/>
      <attributeEditorField showLabel="1" index="40" name="use_2d_flow"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="Grid" groupBox="0" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="15" name="grid_space"/>
      <attributeEditorField showLabel="1" index="29" name="kmax"/>
      <attributeEditorField showLabel="1" index="23" name="table_step_size"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="&quot;advection_1d&quot;" name="Terrain information" groupBox="0" visibilityExpressionEnabled="0">
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="DEM" groupBox="1" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="2" name="dem_file"/>
        <attributeEditorField showLabel="1" index="9" name="epsg_code"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="Friction" groupBox="1" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="6" name="frict_coef_file"/>
        <attributeEditorField showLabel="1" index="32" name="frict_coef"/>
        <attributeEditorField showLabel="1" index="39" name="frict_type"/>
        <attributeEditorField showLabel="1" index="12" name="frict_avg"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="Groundwater" groupBox="1" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="7" name="initial_groundwater_level_file"/>
        <attributeEditorField showLabel="1" index="20" name="initial_groundwater_level"/>
        <attributeEditorField showLabel="1" index="13" name="initial_groundwater_level_type"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="Initial waterlevel" groupBox="1" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="30" name="initial_waterlevel_file"/>
        <attributeEditorField showLabel="1" index="8" name="initial_waterlevel"/>
        <attributeEditorField showLabel="1" index="14" name="water_level_ini_type"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="Interception" groupBox="1" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="28" name="interception_file"/>
        <attributeEditorField showLabel="1" index="27" name="interception_global"/>
        <attributeEditorField showLabel="1" index="-1" name="max_interception"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="Wind" groupBox="1" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="43" name="wind_shielding_file"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="Time" groupBox="0" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="19" name="start_date"/>
      <attributeEditorField showLabel="1" index="25" name="start_time"/>
      <attributeEditorField showLabel="1" index="31" name="sim_time_step"/>
      <attributeEditorField showLabel="1" index="36" name="timestep_plus"/>
      <attributeEditorField showLabel="1" index="3" name="minimum_sim_time_step"/>
      <attributeEditorField showLabel="1" index="0" name="maximum_sim_time_step"/>
      <attributeEditorField showLabel="1" index="1" name="nr_timesteps"/>
      <attributeEditorField showLabel="1" index="21" name="output_time_step"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="Settings id's" groupBox="0" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="22" name="interflow_settings_id"/>
      <attributeEditorField showLabel="1" index="45" name="groundwater_settings_id"/>
      <attributeEditorField showLabel="1" index="10" name="numerical_settings_id"/>
      <attributeEditorField showLabel="1" index="44" name="simple_infiltration_settings_id"/>
      <attributeEditorField showLabel="1" index="34" name="control_group_id"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="Extra options 1D" groupBox="0" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="42" name="advection_1d"/>
      <attributeEditorField showLabel="1" index="18" name="dist_calc_points"/>
      <attributeEditorField showLabel="1" index="46" name="manhole_storage_area"/>
      <attributeEditorField showLabel="1" index="41" name="max_angle_1d_advection"/>
      <attributeEditorField showLabel="1" index="48" name="table_step_size_1d"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="Extra options 2D" groupBox="0" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="16" name="advection_2d"/>
      <attributeEditorField showLabel="1" index="11" name="dem_obstacle_detection"/>
      <attributeEditorField showLabel="1" index="33" name="guess_dams"/>
      <attributeEditorField showLabel="1" index="35" name="dem_obstacle_height"/>
      <attributeEditorField showLabel="1" index="17" name="embedded_cutoff_threshold"/>
      <attributeEditorField showLabel="1" index="38" name="flooding_threshold"/>
      <attributeEditorField showLabel="1" index="5" name="table_step_size_volume_2d"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="advection_1d"/>
    <field editable="1" name="advection_2d"/>
    <field editable="1" name="control_group_id"/>
    <field editable="1" name="dem_file"/>
    <field editable="1" name="dem_obstacle_detection"/>
    <field editable="1" name="dem_obstacle_height"/>
    <field editable="1" name="dist_calc_points"/>
    <field editable="1" name="embedded_cutoff_threshold"/>
    <field editable="1" name="epsg_code"/>
    <field editable="1" name="flooding_threshold"/>
    <field editable="1" name="frict_avg"/>
    <field editable="1" name="frict_coef"/>
    <field editable="1" name="frict_coef_file"/>
    <field editable="1" name="frict_type"/>
    <field editable="1" name="grid_space"/>
    <field editable="1" name="groundwater_settings_id"/>
    <field editable="1" name="guess_dams"/>
    <field editable="1" name="id"/>
    <field editable="1" name="initial_groundwater_level"/>
    <field editable="1" name="initial_groundwater_level_file"/>
    <field editable="1" name="initial_groundwater_level_type"/>
    <field editable="1" name="initial_waterlevel"/>
    <field editable="1" name="initial_waterlevel_file"/>
    <field editable="1" name="interception_file"/>
    <field editable="1" name="interception_global"/>
    <field editable="1" name="interflow_settings_id"/>
    <field editable="1" name="kmax"/>
    <field editable="1" name="manhole_storage_area"/>
    <field editable="1" name="max_angle_1d_advection"/>
    <field editable="1" name="max_interception"/>
    <field editable="1" name="max_interception_file"/>
    <field editable="1" name="maximum_sim_time_step"/>
    <field editable="1" name="minimum_sim_time_step"/>
    <field editable="1" name="name"/>
    <field editable="1" name="nr_timesteps"/>
    <field editable="1" name="numerical_settings_id"/>
    <field editable="1" name="output_time_step"/>
    <field editable="1" name="sim_time_step"/>
    <field editable="1" name="simple_infiltration_settings_id"/>
    <field editable="1" name="start_date"/>
    <field editable="1" name="start_time"/>
    <field editable="1" name="table_step_size"/>
    <field editable="1" name="table_step_size_1d"/>
    <field editable="1" name="table_step_size_volume_2d"/>
    <field editable="1" name="timestep_plus"/>
    <field editable="1" name="use_0d_inflow"/>
    <field editable="1" name="use_1d_flow"/>
    <field editable="1" name="use_2d_flow"/>
    <field editable="1" name="use_2d_rain"/>
    <field editable="1" name="water_level_ini_type"/>
    <field editable="1" name="wind_shielding_file"/>
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
  <widgets/>
  <previewExpression>id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
