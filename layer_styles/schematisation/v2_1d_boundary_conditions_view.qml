<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" simplifyDrawingTol="1" version="3.4.5-Madeira" simplifyAlgorithm="0" simplifyMaxScale="1" maxScale="-4.65661e-10" labelsEnabled="0" simplifyDrawingHints="0" simplifyLocal="1" styleCategories="AllStyleCategories" minScale="1e+08" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" type="singleSymbol" forceraster="0" symbollevels="0">
    <symbols>
      <symbol clip_to_extent="1" force_rhr="0" type="marker" alpha="1" name="0">
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
          <prop k="scale_method" v="area"/>
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
    </symbols>
    <rotation/>
    <sizescale/>
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
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="boundary_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="1" type="QString" name="1: waterlevel"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: velocity"/>
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3: discharge"/>
              </Option>
              <Option type="Map">
                <Option value="5" type="QString" name="5: sommerfeld"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="timeseries">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="ROWID" index="0"/>
    <alias name="" field="id" index="1"/>
    <alias name="" field="connection_node_id" index="2"/>
    <alias name="" field="boundary_type" index="3"/>
    <alias name="" field="timeseries" index="4"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="ROWID"/>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
    <default expression="" applyOnUpdate="0" field="connection_node_id"/>
    <default expression="" applyOnUpdate="0" field="boundary_type"/>
    <default expression="'0,1&#xd;&#xa;9999,1'" applyOnUpdate="0" field="timeseries"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="0" constraints="0" field="ROWID"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="id"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="connection_node_id"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="boundary_type"/>
    <constraint exp_strength="0" unique_strength="0" notnull_strength="2" constraints="1" field="timeseries"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="ROWID"/>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="connection_node_id"/>
    <constraint exp="" desc="" field="boundary_type"/>
    <constraint exp="" desc="" field="timeseries"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column width="-1" type="field" hidden="0" name="ROWID"/>
      <column width="-1" type="field" hidden="0" name="id"/>
      <column width="-1" type="field" hidden="0" name="connection_node_id"/>
      <column width="-1" type="field" hidden="0" name="boundary_type"/>
      <column width="-1" type="field" hidden="0" name="timeseries"/>
      <column width="-1" type="actions" hidden="1"/>
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
from PyQt4.QtGui import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer groupBox="0" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" name="General" columnCount="1">
      <attributeEditorField showLabel="1" name="id" index="1"/>
      <attributeEditorField showLabel="1" name="connection_node_id" index="2"/>
      <attributeEditorField showLabel="1" name="boundary_type" index="3"/>
      <attributeEditorField showLabel="1" name="timeseries" index="4"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="ROWID" editable="1"/>
    <field name="boundary_type" editable="1"/>
    <field name="connection_node_id" editable="1"/>
    <field name="id" editable="1"/>
    <field name="timeseries" editable="1"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="ROWID"/>
    <field labelOnTop="0" name="boundary_type"/>
    <field labelOnTop="0" name="connection_node_id"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="timeseries"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>ROWID</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
