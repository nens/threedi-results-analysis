<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.4.5-Madeira" labelsEnabled="0" styleCategories="AllStyleCategories" simplifyLocal="1" simplifyMaxScale="1" simplifyDrawingHints="0" simplifyDrawingTol="1" simplifyAlgorithm="0" hasScaleBasedVisibilityFlag="0" maxScale="0" readOnly="0" minScale="1e+08">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 type="singleSymbol" forceraster="0" symbollevels="0" enableorderby="0">
    <symbols>
      <symbol type="marker" name="0" force_rhr="0" alpha="1" clip_to_extent="1">
        <layer enabled="1" locked="0" pass="0" class="SimpleMarker">
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
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
    <property value="id" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Pie" attributeLegend="1">
    <DiagramCategory scaleBasedVisibility="0" sizeType="MM" lineSizeType="MM" diagramOrientation="Up" barWidth="5" maxScaleDenominator="1e+08" labelPlacementMethod="XHeight" width="15" penAlpha="255" backgroundAlpha="255" penColor="#000000" penWidth="0" sizeScale="3x:0,0,0,0,0,0" scaleDependency="Area" minimumSize="0" rotationOffset="270" minScaleDenominator="0" opacity="1" backgroundColor="#ffffff" lineSizeScale="3x:0,0,0,0,0,0" enabled="0" height="15">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute label="" color="#000000" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings zIndex="0" obstacle="0" showAll="1" priority="0" placement="0" dist="0" linePlacementFlags="2">
    <properties>
      <Option type="Map">
        <Option type="QString" name="name" value=""/>
        <Option name="properties"/>
        <Option type="QString" name="type" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="reference_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="channel_id">
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
    <field name="friction_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="1: Chèzy" value="1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="2: Manning" value="2"/>
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
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="bank_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id">
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
    <alias name="" field="reference_level" index="0"/>
    <alias name="" field="definition_id" index="1"/>
    <alias name="" field="channel_id" index="2"/>
    <alias name="" field="code" index="3"/>
    <alias name="" field="friction_type" index="4"/>
    <alias name="" field="friction_value" index="5"/>
    <alias name="" field="bank_level" index="6"/>
    <alias name="" field="id" index="7"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="reference_level" applyOnUpdate="0" expression=""/>
    <default field="definition_id" applyOnUpdate="0" expression=""/>
    <default field="channel_id" applyOnUpdate="0" expression="aggregate('v2_channel','min',&quot;id&quot;, intersects($geometry,geometry(@parent)))"/>
    <default field="code" applyOnUpdate="0" expression="'new'"/>
    <default field="friction_type" applyOnUpdate="0" expression="2"/>
    <default field="friction_value" applyOnUpdate="0" expression=""/>
    <default field="bank_level" applyOnUpdate="0" expression=""/>
    <default field="id" applyOnUpdate="0" expression="if(maximum(id) is null,1, maximum(id)+1)"/>
  </defaults>
  <constraints>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="reference_level" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="definition_id" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="channel_id" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="code" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="friction_type" exp_strength="0"/>
    <constraint constraints="1" unique_strength="0" notnull_strength="2" field="friction_value" exp_strength="0"/>
    <constraint constraints="4" unique_strength="0" notnull_strength="0" field="bank_level" exp_strength="2"/>
    <constraint constraints="3" unique_strength="1" notnull_strength="1" field="id" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="reference_level" desc=""/>
    <constraint exp="" field="definition_id" desc=""/>
    <constraint exp="" field="channel_id" desc=""/>
    <constraint exp="" field="code" desc=""/>
    <constraint exp="" field="friction_type" desc=""/>
    <constraint exp="" field="friction_value" desc=""/>
    <constraint exp="&quot;bank_level&quot;>&quot;reference_level&quot; or &quot;bank_level&quot;  is null or &quot;reference_level&quot; is null" field="bank_level" desc="exceeds reference"/>
    <constraint exp="" field="id" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="" sortOrder="0">
    <columns>
      <column type="field" name="reference_level" width="-1" hidden="0"/>
      <column type="field" name="definition_id" width="-1" hidden="0"/>
      <column type="field" name="channel_id" width="-1" hidden="0"/>
      <column type="field" name="code" width="-1" hidden="0"/>
      <column type="field" name="friction_type" width="-1" hidden="0"/>
      <column type="field" name="friction_value" width="-1" hidden="0"/>
      <column type="field" name="bank_level" width="-1" hidden="0"/>
      <column type="field" name="id" width="-1" hidden="0"/>
      <column type="actions" width="-1" hidden="1"/>
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
    <attributeEditorContainer columnCount="1" visibilityExpression="" name="General" groupBox="1" visibilityExpressionEnabled="0" showLabel="1">
      <attributeEditorField name="id" index="7" showLabel="1"/>
      <attributeEditorField name="code" index="3" showLabel="1"/>
      <attributeEditorField name="reference_level" index="0" showLabel="1"/>
      <attributeEditorField name="bank_level" index="6" showLabel="1"/>
      <attributeEditorField name="friction_type" index="4" showLabel="1"/>
      <attributeEditorField name="friction_value" index="5" showLabel="1"/>
      <attributeEditorField name="definition_id" index="1" showLabel="1"/>
      <attributeEditorField name="channel_id" index="2" showLabel="1"/>
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
    <field labelOnTop="0" name="bank_level"/>
    <field labelOnTop="0" name="channel_id"/>
    <field labelOnTop="0" name="code"/>
    <field labelOnTop="0" name="definition_id"/>
    <field labelOnTop="0" name="friction_type"/>
    <field labelOnTop="0" name="friction_value"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="reference_level"/>
    <field labelOnTop="0" name="v2_cross_section_definition_code"/>
    <field labelOnTop="0" name="v2_cross_section_definition_height"/>
    <field labelOnTop="0" name="v2_cross_section_definition_shape"/>
    <field labelOnTop="0" name="v2_cross_section_definition_width"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
