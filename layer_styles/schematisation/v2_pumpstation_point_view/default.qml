<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyMaxScale="1" simplifyDrawingHints="0" readOnly="0" version="3.10.10-A Coruña" simplifyLocal="1" hasScaleBasedVisibilityFlag="0" maxScale="-4.65661e-10" minScale="1e+08" simplifyAlgorithm="0" simplifyDrawingTol="1" styleCategories="AllStyleCategories" labelsEnabled="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 type="singleSymbol" enableorderby="0" symbollevels="0" forceraster="0">
    <symbols>
      <symbol type="marker" force_rhr="0" name="0" alpha="1" clip_to_extent="1">
        <layer pass="0" class="SimpleMarker" enabled="1" locked="0">
          <prop v="0" k="angle"/>
          <prop v="185,185,185,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="pentagon" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="77,77,77,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.6" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="4" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
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
    <DiagramCategory opacity="1" maxScaleDenominator="1e+08" rotationOffset="270" backgroundAlpha="255" diagramOrientation="Up" width="15" penAlpha="255" height="15" barWidth="5" penColor="#000000" scaleBasedVisibility="0" scaleDependency="Area" lineSizeScale="3x:0,0,0,0,0,0" lineSizeType="MM" minScaleDenominator="-4.65661e-10" enabled="0" sizeScale="3x:0,0,0,0,0,0" backgroundColor="#ffffff" minimumSize="0" labelPlacementMethod="XHeight" sizeType="MM" penWidth="0">
      <fontProperties description="MS Shell Dlg 2,7.5,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" field="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings priority="0" showAll="1" linePlacementFlags="2" dist="0" obstacle="0" zIndex="0" placement="0">
    <properties>
      <Option type="Map">
        <Option type="QString" value="" name="name"/>
        <Option name="properties"/>
        <Option type="QString" value="collection" name="type"/>
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
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pump_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="classification">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="sewerage">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option type="QString" value="1" name="CheckedState"/>
            <Option type="QString" value="0" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="start_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="lower_stop_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="upper_stop_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="capacity">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
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
                <Option type="QString" value="-1" name="-1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="0" name="0"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="1" name="1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="2" name="2"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="3" name="3"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="4" name="4"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="5" name="5"/>
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
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_end_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
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
                <Option type="QString" value="1" name="1: pump reacts only on suction side"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="2" name="2: pump reacts only on delivery side"/>
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
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="storage_area">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="false" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="ROWID" index="0" name=""/>
    <alias field="pump_id" index="1" name="id"/>
    <alias field="display_name" index="2" name=""/>
    <alias field="code" index="3" name=""/>
    <alias field="classification" index="4" name=""/>
    <alias field="sewerage" index="5" name=""/>
    <alias field="start_level" index="6" name=""/>
    <alias field="lower_stop_level" index="7" name=""/>
    <alias field="upper_stop_level" index="8" name=""/>
    <alias field="capacity" index="9" name=""/>
    <alias field="zoom_category" index="10" name=""/>
    <alias field="connection_node_start_id" index="11" name=""/>
    <alias field="connection_node_end_id" index="12" name=""/>
    <alias field="type" index="13" name=""/>
    <alias field="connection_node_id" index="14" name="id"/>
    <alias field="storage_area" index="15" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="ROWID" expression="" applyOnUpdate="0"/>
    <default field="pump_id" expression="if(maximum(pump_id) is null,1, maximum(pump_id)+1)" applyOnUpdate="0"/>
    <default field="display_name" expression="'new'" applyOnUpdate="0"/>
    <default field="code" expression="'new'" applyOnUpdate="0"/>
    <default field="classification" expression="" applyOnUpdate="0"/>
    <default field="sewerage" expression="" applyOnUpdate="0"/>
    <default field="start_level" expression="" applyOnUpdate="0"/>
    <default field="lower_stop_level" expression="" applyOnUpdate="0"/>
    <default field="upper_stop_level" expression="" applyOnUpdate="0"/>
    <default field="capacity" expression="" applyOnUpdate="0"/>
    <default field="zoom_category" expression="2" applyOnUpdate="0"/>
    <default field="connection_node_start_id" expression="'filled automatically'" applyOnUpdate="0"/>
    <default field="connection_node_end_id" expression="'if you want to use an endpoint use v2_pumpstation_view'" applyOnUpdate="0"/>
    <default field="type" expression="1" applyOnUpdate="0"/>
    <default field="connection_node_id" expression="'filled automatically'" applyOnUpdate="0"/>
    <default field="storage_area" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="ROWID" unique_strength="0" notnull_strength="0" exp_strength="0" constraints="0"/>
    <constraint field="pump_id" unique_strength="0" notnull_strength="2" exp_strength="0" constraints="1"/>
    <constraint field="display_name" unique_strength="0" notnull_strength="2" exp_strength="0" constraints="1"/>
    <constraint field="code" unique_strength="0" notnull_strength="2" exp_strength="0" constraints="1"/>
    <constraint field="classification" unique_strength="0" notnull_strength="0" exp_strength="0" constraints="0"/>
    <constraint field="sewerage" unique_strength="0" notnull_strength="0" exp_strength="0" constraints="0"/>
    <constraint field="start_level" unique_strength="0" notnull_strength="2" exp_strength="0" constraints="1"/>
    <constraint field="lower_stop_level" unique_strength="0" notnull_strength="2" exp_strength="2" constraints="5"/>
    <constraint field="upper_stop_level" unique_strength="0" notnull_strength="0" exp_strength="2" constraints="4"/>
    <constraint field="capacity" unique_strength="0" notnull_strength="2" exp_strength="2" constraints="5"/>
    <constraint field="zoom_category" unique_strength="0" notnull_strength="2" exp_strength="0" constraints="1"/>
    <constraint field="connection_node_start_id" unique_strength="0" notnull_strength="0" exp_strength="0" constraints="0"/>
    <constraint field="connection_node_end_id" unique_strength="0" notnull_strength="0" exp_strength="0" constraints="0"/>
    <constraint field="type" unique_strength="0" notnull_strength="2" exp_strength="0" constraints="1"/>
    <constraint field="connection_node_id" unique_strength="0" notnull_strength="2" exp_strength="0" constraints="1"/>
    <constraint field="storage_area" unique_strength="0" notnull_strength="0" exp_strength="0" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="ROWID" exp="" desc=""/>
    <constraint field="pump_id" exp="" desc=""/>
    <constraint field="display_name" exp="" desc=""/>
    <constraint field="code" exp="" desc=""/>
    <constraint field="classification" exp="" desc=""/>
    <constraint field="sewerage" exp="" desc=""/>
    <constraint field="start_level" exp="" desc=""/>
    <constraint field="lower_stop_level" exp="&quot;lower_stop_level&quot;&lt;&quot;start_level&quot;" desc=""/>
    <constraint field="upper_stop_level" exp="&quot;upper_stop_level&quot;>&quot;start_level&quot; or &quot;upper_stop_level&quot; is null&#xd;&#xa;" desc=""/>
    <constraint field="capacity" exp="&quot;capacity&quot;>=0" desc=""/>
    <constraint field="zoom_category" exp="" desc=""/>
    <constraint field="connection_node_start_id" exp="" desc=""/>
    <constraint field="connection_node_end_id" exp="" desc=""/>
    <constraint field="type" exp="" desc=""/>
    <constraint field="connection_node_id" exp="" desc=""/>
    <constraint field="storage_area" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="" sortOrder="0">
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
    <attributeEditorContainer visibilityExpression="" columnCount="1" groupBox="0" name="Pumpstation point view" showLabel="1" visibilityExpressionEnabled="0">
      <attributeEditorContainer visibilityExpression="" columnCount="1" groupBox="1" name="General" showLabel="1" visibilityExpressionEnabled="0">
        <attributeEditorField index="1" name="pump_id" showLabel="1"/>
        <attributeEditorField index="2" name="display_name" showLabel="1"/>
        <attributeEditorField index="3" name="code" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" columnCount="1" groupBox="1" name="Characteristics" showLabel="1" visibilityExpressionEnabled="0">
        <attributeEditorField index="6" name="start_level" showLabel="1"/>
        <attributeEditorField index="7" name="lower_stop_level" showLabel="1"/>
        <attributeEditorField index="8" name="upper_stop_level" showLabel="1"/>
        <attributeEditorField index="9" name="capacity" showLabel="1"/>
        <attributeEditorField index="13" name="type" showLabel="1"/>
        <attributeEditorField index="15" name="storage_area" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" columnCount="1" groupBox="1" name="Visualization" showLabel="1" visibilityExpressionEnabled="0">
        <attributeEditorField index="5" name="sewerage" showLabel="1"/>
        <attributeEditorField index="10" name="zoom_category" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" columnCount="1" groupBox="1" name="Connection nodes" showLabel="1" visibilityExpressionEnabled="0">
        <attributeEditorField index="14" name="connection_node_id" showLabel="1"/>
        <attributeEditorField index="11" name="connection_node_start_id" showLabel="1"/>
        <attributeEditorField index="12" name="connection_node_end_id" showLabel="1"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="ROWID" editable="1"/>
    <field name="capacity" editable="1"/>
    <field name="classification" editable="1"/>
    <field name="code" editable="1"/>
    <field name="connection_node_end_id" editable="0"/>
    <field name="connection_node_id" editable="0"/>
    <field name="connection_node_start_id" editable="0"/>
    <field name="display_name" editable="1"/>
    <field name="lower_stop_level" editable="1"/>
    <field name="pump_id" editable="1"/>
    <field name="sewerage" editable="1"/>
    <field name="start_level" editable="1"/>
    <field name="storage_area" editable="1"/>
    <field name="type" editable="1"/>
    <field name="upper_stop_level" editable="1"/>
    <field name="zoom_category" editable="1"/>
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
