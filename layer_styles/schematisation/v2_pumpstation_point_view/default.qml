<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" simplifyLocal="1" labelsEnabled="0" simplifyDrawingTol="1" version="3.10.10-A Coruña" simplifyAlgorithm="0" minScale="1e+08" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" maxScale="-4.65661e-10" simplifyDrawingHints="0" simplifyMaxScale="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" type="singleSymbol" symbollevels="0" enableorderby="0">
    <symbols>
      <symbol type="marker" clip_to_extent="1" name="0" force_rhr="0" alpha="1">
        <layer class="SimpleMarker" pass="0" enabled="1" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="185,185,185,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="pentagon"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="77,77,77,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.6"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="4"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
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
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property value="display_name" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Pie" attributeLegend="1">
    <DiagramCategory width="15" diagramOrientation="Up" rotationOffset="270" penAlpha="255" labelPlacementMethod="XHeight" minScaleDenominator="-4.65661e-10" opacity="1" sizeScale="3x:0,0,0,0,0,0" penColor="#000000" lineSizeScale="3x:0,0,0,0,0,0" enabled="0" barWidth="5" penWidth="0" scaleBasedVisibility="0" backgroundColor="#ffffff" sizeType="MM" minimumSize="0" scaleDependency="Area" maxScaleDenominator="1e+08" lineSizeType="MM" height="15" backgroundAlpha="255">
      <fontProperties description="MS Shell Dlg 2,7.5,-1,5,50,0,0,0,0,0" style=""/>
      <attribute field="" label="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings obstacle="0" priority="0" showAll="1" placement="0" zIndex="0" linePlacementFlags="2" dist="0">
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
    <field name="pump_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="classification">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="sewerage">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option type="QString" name="CheckedState" value="1"/>
            <Option type="QString" name="UncheckedState" value="0"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="lower_stop_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="upper_stop_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="capacity">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="zoom_category">
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
    <field name="connection_node_start_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_end_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="1: pump reacts only on suction side" value="1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="2: pump reacts only on delivery side" value="2"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="storage_area">
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
    <alias name="id" field="pump_id" index="1"/>
    <alias name="" field="display_name" index="2"/>
    <alias name="" field="code" index="3"/>
    <alias name="" field="classification" index="4"/>
    <alias name="" field="sewerage" index="5"/>
    <alias name="" field="start_level" index="6"/>
    <alias name="" field="lower_stop_level" index="7"/>
    <alias name="" field="upper_stop_level" index="8"/>
    <alias name="" field="capacity" index="9"/>
    <alias name="" field="zoom_category" index="10"/>
    <alias name="" field="connection_node_start_id" index="11"/>
    <alias name="" field="connection_node_end_id" index="12"/>
    <alias name="" field="type" index="13"/>
    <alias name="id" field="connection_node_id" index="14"/>
    <alias name="" field="storage_area" index="15"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="ROWID" expression=""/>
    <default applyOnUpdate="0" field="pump_id" expression="if(maximum(pump_id) is null,1, maximum(pump_id)+1)"/>
    <default applyOnUpdate="0" field="display_name" expression="'new'"/>
    <default applyOnUpdate="0" field="code" expression="'new'"/>
    <default applyOnUpdate="0" field="classification" expression=""/>
    <default applyOnUpdate="0" field="sewerage" expression=""/>
    <default applyOnUpdate="0" field="start_level" expression=""/>
    <default applyOnUpdate="0" field="lower_stop_level" expression=""/>
    <default applyOnUpdate="0" field="upper_stop_level" expression=""/>
    <default applyOnUpdate="0" field="capacity" expression=""/>
    <default applyOnUpdate="0" field="zoom_category" expression="2"/>
    <default applyOnUpdate="0" field="connection_node_start_id" expression="'filled automatically'"/>
    <default applyOnUpdate="0" field="connection_node_end_id" expression="'if you want to use an endpoint use v2_pumpstation_view'"/>
    <default applyOnUpdate="0" field="type" expression="1"/>
    <default applyOnUpdate="0" field="connection_node_id" expression="'filled automatically'"/>
    <default applyOnUpdate="0" field="storage_area" expression=""/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" constraints="0" field="ROWID" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" field="pump_id" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" field="display_name" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" field="code" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="classification" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="sewerage" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" field="start_level" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" constraints="5" field="lower_stop_level" notnull_strength="2" exp_strength="2"/>
    <constraint unique_strength="0" constraints="4" field="upper_stop_level" notnull_strength="0" exp_strength="2"/>
    <constraint unique_strength="0" constraints="5" field="capacity" notnull_strength="2" exp_strength="2"/>
    <constraint unique_strength="0" constraints="1" field="zoom_category" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="connection_node_start_id" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="connection_node_end_id" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" field="type" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" field="connection_node_id" notnull_strength="2" exp_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="storage_area" notnull_strength="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="ROWID" exp=""/>
    <constraint desc="" field="pump_id" exp=""/>
    <constraint desc="" field="display_name" exp=""/>
    <constraint desc="" field="code" exp=""/>
    <constraint desc="" field="classification" exp=""/>
    <constraint desc="" field="sewerage" exp=""/>
    <constraint desc="" field="start_level" exp=""/>
    <constraint desc="" field="lower_stop_level" exp="&quot;lower_stop_level&quot;&lt;&quot;start_level&quot;"/>
    <constraint desc="" field="upper_stop_level" exp="&quot;upper_stop_level&quot;>&quot;start_level&quot; or &quot;upper_stop_level&quot; is null&#xd;&#xa;"/>
    <constraint desc="" field="capacity" exp="&quot;capacity&quot;>=0"/>
    <constraint desc="" field="zoom_category" exp=""/>
    <constraint desc="" field="connection_node_start_id" exp=""/>
    <constraint desc="" field="connection_node_end_id" exp=""/>
    <constraint desc="" field="type" exp=""/>
    <constraint desc="" field="connection_node_id" exp=""/>
    <constraint desc="" field="storage_area" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column type="field" name="ROWID" hidden="0" width="-1"/>
      <column type="field" name="pump_id" hidden="0" width="-1"/>
      <column type="field" name="display_name" hidden="0" width="-1"/>
      <column type="field" name="code" hidden="0" width="-1"/>
      <column type="field" name="classification" hidden="0" width="-1"/>
      <column type="field" name="sewerage" hidden="0" width="-1"/>
      <column type="field" name="start_level" hidden="0" width="-1"/>
      <column type="field" name="lower_stop_level" hidden="0" width="-1"/>
      <column type="field" name="upper_stop_level" hidden="0" width="-1"/>
      <column type="field" name="capacity" hidden="0" width="-1"/>
      <column type="field" name="zoom_category" hidden="0" width="-1"/>
      <column type="field" name="connection_node_start_id" hidden="0" width="-1"/>
      <column type="field" name="connection_node_end_id" hidden="0" width="-1"/>
      <column type="field" name="type" hidden="0" width="-1"/>
      <column type="field" name="connection_node_id" hidden="0" width="-1"/>
      <column type="field" name="storage_area" hidden="0" width="-1"/>
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
    <attributeEditorContainer groupBox="0" visibilityExpressionEnabled="0" showLabel="1" name="Pumpstation point view" visibilityExpression="" columnCount="1">
      <attributeEditorContainer groupBox="1" visibilityExpressionEnabled="0" showLabel="1" name="General" visibilityExpression="" columnCount="1">
        <attributeEditorField showLabel="1" name="pump_id" index="1"/>
        <attributeEditorField showLabel="1" name="display_name" index="2"/>
        <attributeEditorField showLabel="1" name="code" index="3"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpressionEnabled="0" showLabel="1" name="Characteristics" visibilityExpression="" columnCount="1">
        <attributeEditorField showLabel="1" name="start_level" index="6"/>
        <attributeEditorField showLabel="1" name="lower_stop_level" index="7"/>
        <attributeEditorField showLabel="1" name="upper_stop_level" index="8"/>
        <attributeEditorField showLabel="1" name="capacity" index="9"/>
        <attributeEditorField showLabel="1" name="type" index="13"/>
        <attributeEditorField showLabel="1" name="storage_area" index="15"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpressionEnabled="0" showLabel="1" name="Visualization" visibilityExpression="" columnCount="1">
        <attributeEditorField showLabel="1" name="sewerage" index="5"/>
        <attributeEditorField showLabel="1" name="zoom_category" index="10"/>
      </attributeEditorContainer>
      <attributeEditorContainer groupBox="1" visibilityExpressionEnabled="0" showLabel="1" name="Connection nodes" visibilityExpression="" columnCount="1">
        <attributeEditorField showLabel="1" name="connection_node_id" index="14"/>
        <attributeEditorField showLabel="1" name="connection_node_start_id" index="11"/>
        <attributeEditorField showLabel="1" name="connection_node_end_id" index="12"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="ROWID"/>
    <field editable="1" name="capacity"/>
    <field editable="1" name="classification"/>
    <field editable="1" name="code"/>
    <field editable="0" name="connection_node_end_id"/>
    <field editable="0" name="connection_node_id"/>
    <field editable="0" name="connection_node_start_id"/>
    <field editable="1" name="display_name"/>
    <field editable="1" name="lower_stop_level"/>
    <field editable="1" name="pump_id"/>
    <field editable="1" name="sewerage"/>
    <field editable="1" name="start_level"/>
    <field editable="1" name="storage_area"/>
    <field editable="1" name="type"/>
    <field editable="1" name="upper_stop_level"/>
    <field editable="1" name="zoom_category"/>
  </editable>
  <labelOnTop>
    <field name="ROWID" labelOnTop="0"/>
    <field name="capacity" labelOnTop="0"/>
    <field name="classification" labelOnTop="0"/>
    <field name="code" labelOnTop="0"/>
    <field name="connection_node_end_id" labelOnTop="0"/>
    <field name="connection_node_id" labelOnTop="0"/>
    <field name="connection_node_start_id" labelOnTop="0"/>
    <field name="display_name" labelOnTop="0"/>
    <field name="lower_stop_level" labelOnTop="0"/>
    <field name="pump_id" labelOnTop="0"/>
    <field name="sewerage" labelOnTop="0"/>
    <field name="start_level" labelOnTop="0"/>
    <field name="storage_area" labelOnTop="0"/>
    <field name="type" labelOnTop="0"/>
    <field name="upper_stop_level" labelOnTop="0"/>
    <field name="zoom_category" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>"display_name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
