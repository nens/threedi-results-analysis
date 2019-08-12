<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyMaxScale="1" simplifyDrawingTol="1" simplifyDrawingHints="0" hasScaleBasedVisibilityFlag="0" simplifyAlgorithm="0" maxScale="0" minScale="1e+08" readOnly="0" simplifyLocal="1" styleCategories="AllStyleCategories" labelsEnabled="0" version="3.4.5-Madeira">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 type="singleSymbol" forceraster="0" enableorderby="0" symbollevels="0">
    <symbols>
      <symbol name="0" type="marker" alpha="1" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="19,61,142,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="diamond"/>
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property value="id" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Pie">
    <DiagramCategory maxScaleDenominator="1e+08" penColor="#000000" opacity="1" lineSizeScale="3x:0,0,0,0,0,0" minimumSize="0" barWidth="5" diagramOrientation="Up" scaleBasedVisibility="0" lineSizeType="MM" width="15" penAlpha="255" rotationOffset="270" sizeScale="3x:0,0,0,0,0,0" backgroundAlpha="255" scaleDependency="Area" height="15" enabled="0" backgroundColor="#ffffff" labelPlacementMethod="XHeight" minScaleDenominator="0" sizeType="MM" penWidth="0">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" field="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings placement="0" showAll="1" linePlacementFlags="2" dist="0" obstacle="0" priority="0" zIndex="0">
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
    <field name="reference_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="channel_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="friction_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="1: Chezy" type="QString" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="2: Manning" type="QString" value="2"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="bank_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id">
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
    <alias index="0" name="" field="reference_level"/>
    <alias index="1" name="" field="definition_id"/>
    <alias index="2" name="" field="channel_id"/>
    <alias index="3" name="" field="code"/>
    <alias index="4" name="" field="friction_type"/>
    <alias index="5" name="" field="friction_value"/>
    <alias index="6" name="" field="bank_level"/>
    <alias index="7" name="" field="id"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="reference_level" expression="" applyOnUpdate="0"/>
    <default field="definition_id" expression="" applyOnUpdate="0"/>
    <default field="channel_id" expression="" applyOnUpdate="0"/>
    <default field="code" expression="'new'" applyOnUpdate="0"/>
    <default field="friction_type" expression="2" applyOnUpdate="0"/>
    <default field="friction_value" expression="" applyOnUpdate="0"/>
    <default field="bank_level" expression="" applyOnUpdate="0"/>
    <default field="id" expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint constraints="1" notnull_strength="2" field="reference_level" exp_strength="0" unique_strength="0"/>
    <constraint constraints="1" notnull_strength="2" field="definition_id" exp_strength="0" unique_strength="0"/>
    <constraint constraints="1" notnull_strength="2" field="channel_id" exp_strength="0" unique_strength="0"/>
    <constraint constraints="1" notnull_strength="2" field="code" exp_strength="0" unique_strength="0"/>
    <constraint constraints="1" notnull_strength="2" field="friction_type" exp_strength="0" unique_strength="0"/>
    <constraint constraints="1" notnull_strength="2" field="friction_value" exp_strength="0" unique_strength="0"/>
    <constraint constraints="4" notnull_strength="0" field="bank_level" exp_strength="2" unique_strength="0"/>
    <constraint constraints="3" notnull_strength="1" field="id" exp_strength="0" unique_strength="1"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="reference_level"/>
    <constraint exp="" desc="" field="definition_id"/>
    <constraint exp="" desc="" field="channel_id"/>
    <constraint exp="" desc="" field="code"/>
    <constraint exp="" desc="" field="friction_type"/>
    <constraint exp="" desc="" field="friction_value"/>
    <constraint exp="&quot;bank_level&quot;>&quot;reference_level&quot; or &quot;bank_level&quot;  is null or &quot;reference_level&quot; is null" desc="exceeds reference" field="bank_level"/>
    <constraint exp="" desc="" field="id"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortExpression="" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column name="reference_level" type="field" hidden="0" width="-1"/>
      <column name="definition_id" type="field" hidden="0" width="-1"/>
      <column name="channel_id" type="field" hidden="0" width="-1"/>
      <column name="code" type="field" hidden="0" width="-1"/>
      <column name="friction_type" type="field" hidden="0" width="-1"/>
      <column name="friction_value" type="field" hidden="0" width="-1"/>
      <column name="bank_level" type="field" hidden="0" width="-1"/>
      <column name="id" type="field" hidden="0" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
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
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer name="General" visibilityExpression="" visibilityExpressionEnabled="0" columnCount="1" groupBox="1" showLabel="1">
      <attributeEditorField index="7" name="id" showLabel="1"/>
      <attributeEditorField index="3" name="code" showLabel="1"/>
      <attributeEditorField index="0" name="reference_level" showLabel="1"/>
      <attributeEditorField index="6" name="bank_level" showLabel="1"/>
      <attributeEditorField index="4" name="friction_type" showLabel="1"/>
      <attributeEditorField index="5" name="friction_value" showLabel="1"/>
      <attributeEditorField index="1" name="definition_id" showLabel="1"/>
      <attributeEditorField index="2" name="channel_id" showLabel="1"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="bank_level" editable="1"/>
    <field name="channel_id" editable="1"/>
    <field name="code" editable="1"/>
    <field name="definition_id" editable="1"/>
    <field name="friction_type" editable="1"/>
    <field name="friction_value" editable="1"/>
    <field name="id" editable="1"/>
    <field name="reference_level" editable="1"/>
    <field name="v2_cross_section_definition_code" editable="0"/>
    <field name="v2_cross_section_definition_height" editable="0"/>
    <field name="v2_cross_section_definition_shape" editable="0"/>
    <field name="v2_cross_section_definition_width" editable="0"/>
  </editable>
  <labelOnTop>
    <field name="bank_level" labelOnTop="0"/>
    <field name="channel_id" labelOnTop="0"/>
    <field name="code" labelOnTop="0"/>
    <field name="definition_id" labelOnTop="0"/>
    <field name="friction_type" labelOnTop="0"/>
    <field name="friction_value" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="reference_level" labelOnTop="0"/>
    <field name="v2_cross_section_definition_code" labelOnTop="0"/>
    <field name="v2_cross_section_definition_height" labelOnTop="0"/>
    <field name="v2_cross_section_definition_shape" labelOnTop="0"/>
    <field name="v2_cross_section_definition_width" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
