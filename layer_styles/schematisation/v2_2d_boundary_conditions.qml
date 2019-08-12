<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" version="3.4.5-Madeira" labelsEnabled="0" simplifyDrawingHints="1" simplifyDrawingTol="1" simplifyLocal="1" minScale="1e+08" maxScale="0" simplifyMaxScale="1" readOnly="0" hasScaleBasedVisibilityFlag="0" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" type="singleSymbol" symbollevels="0" forceraster="0">
    <symbols>
      <symbol clip_to_extent="1" force_rhr="0" type="line" name="0" alpha="1">
        <layer enabled="1" pass="0" locked="0" class="SimpleLine">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="255,0,0,255"/>
          <prop k="line_style" v="dash"/>
          <prop k="line_width" v="0.66"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
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
    <property key="dualview/previewExpressions" value="&quot;display_name&quot;"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory labelPlacementMethod="XHeight" scaleBasedVisibility="0" opacity="1" penColor="#000000" lineSizeScale="3x:0,0,0,0,0,0" minimumSize="0" backgroundColor="#ffffff" width="15" sizeType="MM" scaleDependency="Area" penAlpha="255" sizeScale="3x:0,0,0,0,0,0" diagramOrientation="Up" height="15" minScaleDenominator="0" penWidth="0" lineSizeType="MM" rotationOffset="270" enabled="0" barWidth="5" maxScaleDenominator="1e+08" backgroundAlpha="255">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute label="" color="#000000" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings placement="2" linePlacementFlags="2" showAll="1" dist="0" priority="0" obstacle="0" zIndex="0">
    <properties>
      <Option type="Map">
        <Option type="QString" value="" name="name"/>
        <Option name="properties"/>
        <Option type="QString" value="collection" name="type"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="id">
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
    <field name="timeseries">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" value="true" name="IsMultiline"/>
            <Option type="bool" value="false" name="UseHtml"/>
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
                <Option type="QString" value="1" name="1: Waterlevel"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="2" name="2: Velocity"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="3" name="3: Discharge"/>
              </Option>
              <Option type="Map">
                <Option type="QString" value="5" name="5: Sommerfeld"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="id" index="0" name=""/>
    <alias field="display_name" index="1" name=""/>
    <alias field="timeseries" index="2" name=""/>
    <alias field="boundary_type" index="3" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
    <default expression="" applyOnUpdate="0" field="display_name"/>
    <default expression="'0,1&#xd;&#xa;9999,1'" applyOnUpdate="0" field="timeseries"/>
    <default expression="" applyOnUpdate="0" field="boundary_type"/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" constraints="3" notnull_strength="1" field="id" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="display_name" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="timeseries" exp_strength="0"/>
    <constraint unique_strength="0" constraints="1" notnull_strength="2" field="boundary_type" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="id" exp=""/>
    <constraint desc="" field="display_name" exp=""/>
    <constraint desc="" field="timeseries" exp=""/>
    <constraint desc="" field="boundary_type" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column width="-1" hidden="0" type="field" name="id"/>
      <column width="-1" hidden="0" type="field" name="display_name"/>
      <column width="-1" hidden="0" type="field" name="timeseries"/>
      <column width="-1" hidden="0" type="field" name="boundary_type"/>
      <column width="-1" hidden="1" type="actions"/>
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
    <attributeEditorContainer visibilityExpression="" visibilityExpressionEnabled="0" columnCount="1" name="General" showLabel="1" groupBox="0">
      <attributeEditorField index="0" name="id" showLabel="1"/>
      <attributeEditorField index="1" name="display_name" showLabel="1"/>
      <attributeEditorField index="3" name="boundary_type" showLabel="1"/>
      <attributeEditorField index="2" name="timeseries" showLabel="1"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="boundary_type"/>
    <field editable="1" name="display_name"/>
    <field editable="1" name="id"/>
    <field editable="1" name="timeseries"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="boundary_type"/>
    <field labelOnTop="0" name="display_name"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="timeseries"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>display_name</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
