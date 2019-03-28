<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.4.5-Madeira" styleCategories="AllStyleCategories" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" simplifyAlgorithm="0" labelsEnabled="0" simplifyDrawingTol="1" minScale="1e+08" maxScale="-4.65661e-10" simplifyDrawingHints="0" readOnly="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" enableorderby="0" symbollevels="0" type="RuleRenderer">
    <rules key="{4fbba513-a3b1-4a92-97bc-3d44735ac986}">
      <rule scalemaxdenom="2500" symbol="0" filter="manh_manhole_indicator = 0" label="Inspectieput" key="{a951db60-faa9-4c95-9eaa-a51d84ff90b1}"/>
      <rule scalemaxdenom="15000" symbol="1" filter="manh_manhole_indicator = 1" label="Uitlaat - boundary" key="{c9e7ab73-45d5-45d6-970d-b4e28230c1e5}"/>
      <rule scalemaxdenom="15000" symbol="2" filter="manh_calculation_type = 0" label="Uitlaat - connectie met 2d" key="{bb971e07-f3e6-48c3-b84b-12496560a739}"/>
      <rule symbol="3" filter="manh_manhole_indicator = 2" label="Gemaalkelder" key="{a1d98efc-8098-4201-a75e-93dc7c47f076}"/>
      <rule symbol="4" filter="manh_manhole_indicator = 3" label="Inprikpunt" key="{b15fd57b-e6e4-43b6-8496-7ebf4f15ea68}"/>
      <rule symbol="5" filter="manh_manhole_indicator = 4" label="RWZI" key="{c3de3024-005b-42ac-9705-3bae1dc13053}"/>
    </rules>
    <symbols>
      <symbol clip_to_extent="1" type="marker" force_rhr="0" alpha="1" name="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
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
      <symbol clip_to_extent="1" type="marker" force_rhr="0" alpha="1" name="1">
        <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
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
      <symbol clip_to_extent="1" type="marker" force_rhr="0" alpha="1" name="2">
        <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
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
      <symbol clip_to_extent="1" type="marker" force_rhr="0" alpha="1" name="3">
        <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
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
      <symbol clip_to_extent="1" type="marker" force_rhr="0" alpha="1" name="4">
        <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
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
      <symbol clip_to_extent="1" type="marker" force_rhr="0" alpha="1" name="5">
        <layer pass="0" enabled="1" locked="0" class="SimpleMarker">
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
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Pie">
    <DiagramCategory lineSizeType="MM" lineSizeScale="3x:0,0,0,0,0,0" sizeType="MM" backgroundAlpha="255" penColor="#000000" sizeScale="3x:0,0,0,0,0,0" maxScaleDenominator="1e+08" opacity="1" rotationOffset="270" scaleDependency="Area" minimumSize="0" width="15" minScaleDenominator="-4.65661e-10" backgroundColor="#ffffff" labelPlacementMethod="XHeight" diagramOrientation="Up" barWidth="5" enabled="0" height="15" penWidth="0" penAlpha="255" scaleBasedVisibility="0">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute color="#000000" field="" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings priority="0" linePlacementFlags="2" dist="0" zIndex="0" showAll="1" obstacle="0" placement="0">
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
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="manh_id">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="manh_display_name">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="manh_code">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="manh_connection_node_id">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="manh_shape">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="manh_width">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="manh_length">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="manh_manhole_indicator">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="manh_calculation_type">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="manh_bottom_level">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="manh_surface_level">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="manh_drain_level">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="manh_sediment_level">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="manh_zoom_category">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="node_id">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="node_storage_area">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="node_initial_waterlevel">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="node_code">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="node_the_geom_linestring">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" field="ROWID" name=""/>
    <alias index="1" field="manh_id" name=""/>
    <alias index="2" field="manh_display_name" name=""/>
    <alias index="3" field="manh_code" name=""/>
    <alias index="4" field="manh_connection_node_id" name=""/>
    <alias index="5" field="manh_shape" name=""/>
    <alias index="6" field="manh_width" name=""/>
    <alias index="7" field="manh_length" name=""/>
    <alias index="8" field="manh_manhole_indicator" name=""/>
    <alias index="9" field="manh_calculation_type" name=""/>
    <alias index="10" field="manh_bottom_level" name=""/>
    <alias index="11" field="manh_surface_level" name=""/>
    <alias index="12" field="manh_drain_level" name=""/>
    <alias index="13" field="manh_sediment_level" name=""/>
    <alias index="14" field="manh_zoom_category" name=""/>
    <alias index="15" field="node_id" name=""/>
    <alias index="16" field="node_storage_area" name=""/>
    <alias index="17" field="node_initial_waterlevel" name=""/>
    <alias index="18" field="node_code" name=""/>
    <alias index="19" field="node_the_geom_linestring" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" field="ROWID" applyOnUpdate="0"/>
    <default expression="" field="manh_id" applyOnUpdate="0"/>
    <default expression="" field="manh_display_name" applyOnUpdate="0"/>
    <default expression="" field="manh_code" applyOnUpdate="0"/>
    <default expression="" field="manh_connection_node_id" applyOnUpdate="0"/>
    <default expression="" field="manh_shape" applyOnUpdate="0"/>
    <default expression="" field="manh_width" applyOnUpdate="0"/>
    <default expression="" field="manh_length" applyOnUpdate="0"/>
    <default expression="" field="manh_manhole_indicator" applyOnUpdate="0"/>
    <default expression="" field="manh_calculation_type" applyOnUpdate="0"/>
    <default expression="" field="manh_bottom_level" applyOnUpdate="0"/>
    <default expression="" field="manh_surface_level" applyOnUpdate="0"/>
    <default expression="" field="manh_drain_level" applyOnUpdate="0"/>
    <default expression="" field="manh_sediment_level" applyOnUpdate="0"/>
    <default expression="" field="manh_zoom_category" applyOnUpdate="0"/>
    <default expression="" field="node_id" applyOnUpdate="0"/>
    <default expression="" field="node_storage_area" applyOnUpdate="0"/>
    <default expression="" field="node_initial_waterlevel" applyOnUpdate="0"/>
    <default expression="" field="node_code" applyOnUpdate="0"/>
    <default expression="" field="node_the_geom_linestring" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" field="ROWID" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="manh_id" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="manh_display_name" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="manh_code" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="manh_connection_node_id" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="manh_shape" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="manh_width" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="manh_length" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="manh_manhole_indicator" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="manh_calculation_type" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="manh_bottom_level" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="manh_surface_level" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="manh_drain_level" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="manh_sediment_level" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="manh_zoom_category" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="node_id" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="node_storage_area" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="node_initial_waterlevel" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="node_code" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="node_the_geom_linestring" constraints="0" exp_strength="0" notnull_strength="0"/>
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
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortExpression="" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column hidden="0" width="-1" type="field" name="ROWID"/>
      <column hidden="0" width="-1" type="field" name="manh_id"/>
      <column hidden="0" width="-1" type="field" name="manh_display_name"/>
      <column hidden="0" width="-1" type="field" name="manh_code"/>
      <column hidden="0" width="-1" type="field" name="manh_connection_node_id"/>
      <column hidden="0" width="-1" type="field" name="manh_shape"/>
      <column hidden="0" width="-1" type="field" name="manh_width"/>
      <column hidden="0" width="-1" type="field" name="manh_length"/>
      <column hidden="0" width="-1" type="field" name="manh_manhole_indicator"/>
      <column hidden="0" width="-1" type="field" name="manh_calculation_type"/>
      <column hidden="0" width="-1" type="field" name="manh_bottom_level"/>
      <column hidden="0" width="-1" type="field" name="manh_surface_level"/>
      <column hidden="0" width="-1" type="field" name="manh_drain_level"/>
      <column hidden="0" width="-1" type="field" name="manh_sediment_level"/>
      <column hidden="0" width="-1" type="field" name="manh_zoom_category"/>
      <column hidden="0" width="-1" type="field" name="node_id"/>
      <column hidden="0" width="-1" type="field" name="node_storage_area"/>
      <column hidden="0" width="-1" type="field" name="node_initial_waterlevel"/>
      <column hidden="0" width="-1" type="field" name="node_code"/>
      <column hidden="0" width="-1" type="field" name="node_the_geom_linestring"/>
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
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field editable="1" name="ROWID"/>
    <field editable="1" name="manh_bottom_level"/>
    <field editable="1" name="manh_calculation_type"/>
    <field editable="1" name="manh_code"/>
    <field editable="1" name="manh_connection_node_id"/>
    <field editable="1" name="manh_display_name"/>
    <field editable="1" name="manh_drain_level"/>
    <field editable="1" name="manh_id"/>
    <field editable="1" name="manh_length"/>
    <field editable="1" name="manh_manhole_indicator"/>
    <field editable="1" name="manh_sediment_level"/>
    <field editable="1" name="manh_shape"/>
    <field editable="1" name="manh_surface_level"/>
    <field editable="1" name="manh_width"/>
    <field editable="1" name="manh_zoom_category"/>
    <field editable="1" name="node_code"/>
    <field editable="1" name="node_id"/>
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
  <previewExpression>manh_display_name</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
