<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" labelsEnabled="0" readOnly="0" version="3.4.11-Madeira" simplifyMaxScale="1" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" simplifyDrawingHints="0" simplifyAlgorithm="0" minScale="1e+8" simplifyDrawingTol="1" simplifyLocal="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" symbollevels="0" forceraster="0" type="singleSymbol">
    <symbols>
      <symbol clip_to_extent="1" alpha="1" name="0" type="marker" force_rhr="0">
        <layer enabled="1" locked="0" pass="0" class="SimpleMarker">
          <prop k="angle" v="180"/>
          <prop k="color" v="113,111,253,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="arrow"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="5"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
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
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory opacity="1" barWidth="5" backgroundColor="#ffffff" height="15" enabled="0" lineSizeType="MM" width="15" labelPlacementMethod="XHeight" backgroundAlpha="255" scaleDependency="Area" rotationOffset="270" sizeScale="3x:0,0,0,0,0,0" diagramOrientation="Up" penWidth="0" penAlpha="255" penColor="#000000" minScaleDenominator="0" lineSizeScale="3x:0,0,0,0,0,0" sizeType="MM" scaleBasedVisibility="0" minimumSize="0" maxScaleDenominator="1e+8">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute color="#000000" label="" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings showAll="1" zIndex="0" placement="0" priority="0" obstacle="0" dist="0" linePlacementFlags="2">
    <properties>
      <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="1" name="1: Surface" type="QString"/>
              </Option>
            </Option>
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
    <field name="timeseries">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="true" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="" field="type"/>
    <alias index="1" name="" field="id"/>
    <alias index="2" name="" field="timeseries"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" expression="1" field="type"/>
    <default applyOnUpdate="0" expression="if(maximum(id) is null,1, maximum(id)+1)" field="id"/>
    <default applyOnUpdate="0" expression="" field="timeseries"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" notnull_strength="2" field="type" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" notnull_strength="1" field="id" constraints="3" unique_strength="1"/>
    <constraint exp_strength="0" notnull_strength="2" field="timeseries" constraints="1" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="type"/>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="timeseries"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="" sortOrder="0">
    <columns>
      <column width="-1" hidden="0" name="type" type="field"/>
      <column width="-1" hidden="0" name="id" type="field"/>
      <column width="-1" hidden="0" name="timeseries" type="field"/>
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
    <attributeEditorContainer showLabel="1" columnCount="1" visibilityExpression="" name="General" groupBox="0" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="1" name="id"/>
      <attributeEditorField showLabel="1" index="0" name="type"/>
      <attributeEditorField showLabel="1" index="2" name="timeseries"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="id"/>
    <field editable="1" name="timeseries"/>
    <field editable="1" name="type"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="timeseries"/>
    <field labelOnTop="0" name="type"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
