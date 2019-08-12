<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="0" styleCategories="AllStyleCategories" simplifyDrawingTol="1" simplifyAlgorithm="0" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" simplifyMaxScale="1" minScale="1e+08" readOnly="0" version="3.4.5-Madeira" maxScale="0" simplifyDrawingHints="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" type="RuleRenderer" enableorderby="0" symbollevels="0">
    <rules key="{ef7b6218-5639-4216-a577-db0c96e2a759}">
      <rule label="hellend" filter="surface_inclination = 'hellend'" symbol="0" key="{68cb011a-8a27-4aa2-a23d-858ba251f42b}"/>
      <rule label="vlak" filter="surface_inclination = 'vlak'" symbol="1" key="{91463b0e-a824-4df0-a0bd-8dcb0b5f2094}"/>
      <rule label="uitgestrekt" filter="surface_inclination = 'uitgestrekt'" symbol="2" key="{1dde8d91-4769-421d-bad7-5aa700191647}"/>
      <rule label="gesloten verharding" filter="surface_class = 'gesloten verharding'" symbol="3" key="{9c187ace-e49a-4660-8aed-a23359e3828d}"/>
      <rule label="open verharding" filter="surface_class = 'open verharding'" symbol="4" key="{bfb69c3c-b9b3-4865-94cb-7ea349f429dc}"/>
      <rule label="onverhard" filter="surface_class = 'half verhard' OR surface_class = 'onverhard'" symbol="5" key="{1ee7fc0c-ce99-4a36-83c1-10163a3ae8b3}"/>
      <rule label="pand" filter="surface_class = 'pand'" symbol="6" key="{32d556c3-f4d6-49ff-808b-ebc499c1f5f1}"/>
    </rules>
    <symbols>
      <symbol name="0" force_rhr="0" alpha="1" type="fill" clip_to_extent="1">
        <layer class="SimpleLine" pass="0" locked="0" enabled="1">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="128,152,72,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.26"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleFill" pass="0" locked="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="128,128,128,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="no"/>
          <prop k="outline_width" v="1"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="no"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="1" force_rhr="0" alpha="1" type="fill" clip_to_extent="1">
        <layer class="SimpleLine" pass="0" locked="0" enabled="1">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="0,0,0,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.26"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="2" force_rhr="0" alpha="1" type="fill" clip_to_extent="1">
        <layer class="SimpleLine" pass="0" locked="0" enabled="1">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="0"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="175,179,138,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.26"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleFill" pass="0" locked="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="128,128,128,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="no"/>
          <prop k="outline_width" v="1"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="no"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="3" force_rhr="0" alpha="1" type="fill" clip_to_extent="1">
        <layer class="SimpleFill" pass="0" locked="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="117,117,117,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="117,117,117,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.26"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="4" force_rhr="0" alpha="1" type="fill" clip_to_extent="1">
        <layer class="SimpleFill" pass="0" locked="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="182,182,182,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="182,182,182,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.26"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="5" force_rhr="0" alpha="1" type="fill" clip_to_extent="1">
        <layer class="SimpleFill" pass="0" locked="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="186,221,105,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="186,221,105,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.26"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="6" force_rhr="0" alpha="1" type="fill" clip_to_extent="1">
        <layer class="SimpleFill" pass="0" locked="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="170,85,255,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="170,85,255,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.26"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
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
    <DiagramCategory lineSizeType="MM" diagramOrientation="Up" labelPlacementMethod="XHeight" scaleDependency="Area" lineSizeScale="3x:0,0,0,0,0,0" backgroundColor="#ffffff" width="15" maxScaleDenominator="1e+08" height="15" sizeType="MM" rotationOffset="270" penWidth="0" enabled="0" minimumSize="0" backgroundAlpha="255" minScaleDenominator="0" sizeScale="3x:0,0,0,0,0,0" scaleBasedVisibility="0" penColor="#000000" opacity="1" penAlpha="255" barWidth="5">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" field="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings placement="0" dist="0" obstacle="0" showAll="1" priority="0" zIndex="0" linePlacementFlags="2">
    <properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties" type="Map">
          <Option name="show" type="Map">
            <Option name="active" value="true" type="bool"/>
            <Option name="field" value="function" type="QString"/>
            <Option name="type" value="2" type="int"/>
          </Option>
        </Option>
        <Option name="type" value="collection" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="function">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="surface_class">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="gesloten verharding" value="gesloten verharding" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="open verharding" value="open verharding" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="half verhard" value="half verhard" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="onverhard" value="onverhard" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="pand" value="pand" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="surface_sub_class">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="zoom_category">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="-1" value="-1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="0" value="0" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="1" value="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="2" value="2" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="3" value="3" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="4" value="4" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="5" value="5" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="nr_of_inhabitants">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="area">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dry_weather_flow">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="surface_inclination">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="vlak" value="vlak" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="hellend" value="hellend" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="uitgestrekt" value="uitgestrekt" type="QString"/>
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
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" index="0" field="function"/>
    <alias name="" index="1" field="surface_class"/>
    <alias name="" index="2" field="code"/>
    <alias name="" index="3" field="display_name"/>
    <alias name="" index="4" field="surface_sub_class"/>
    <alias name="" index="5" field="zoom_category"/>
    <alias name="" index="6" field="nr_of_inhabitants"/>
    <alias name="" index="7" field="area"/>
    <alias name="" index="8" field="dry_weather_flow"/>
    <alias name="" index="9" field="surface_inclination"/>
    <alias name="" index="10" field="id"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="function" expression=""/>
    <default applyOnUpdate="0" field="surface_class" expression=""/>
    <default applyOnUpdate="0" field="code" expression="'new'"/>
    <default applyOnUpdate="0" field="display_name" expression="'new'"/>
    <default applyOnUpdate="0" field="surface_sub_class" expression=""/>
    <default applyOnUpdate="0" field="zoom_category" expression="-1"/>
    <default applyOnUpdate="0" field="nr_of_inhabitants" expression="0"/>
    <default applyOnUpdate="0" field="area" expression="$area"/>
    <default applyOnUpdate="0" field="dry_weather_flow" expression=""/>
    <default applyOnUpdate="0" field="surface_inclination" expression=""/>
    <default applyOnUpdate="0" field="id" expression="if(maximum(id) is null,1, maximum(id)+1)"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" constraints="0" exp_strength="0" field="function" unique_strength="0"/>
    <constraint notnull_strength="2" constraints="1" exp_strength="0" field="surface_class" unique_strength="0"/>
    <constraint notnull_strength="2" constraints="1" exp_strength="0" field="code" unique_strength="0"/>
    <constraint notnull_strength="2" constraints="1" exp_strength="0" field="display_name" unique_strength="0"/>
    <constraint notnull_strength="0" constraints="0" exp_strength="0" field="surface_sub_class" unique_strength="0"/>
    <constraint notnull_strength="2" constraints="1" exp_strength="0" field="zoom_category" unique_strength="0"/>
    <constraint notnull_strength="0" constraints="0" exp_strength="0" field="nr_of_inhabitants" unique_strength="0"/>
    <constraint notnull_strength="2" constraints="1" exp_strength="0" field="area" unique_strength="0"/>
    <constraint notnull_strength="0" constraints="0" exp_strength="0" field="dry_weather_flow" unique_strength="0"/>
    <constraint notnull_strength="2" constraints="1" exp_strength="0" field="surface_inclination" unique_strength="0"/>
    <constraint notnull_strength="1" constraints="3" exp_strength="0" field="id" unique_strength="1"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="function" desc=""/>
    <constraint exp="" field="surface_class" desc=""/>
    <constraint exp="" field="code" desc=""/>
    <constraint exp="" field="display_name" desc=""/>
    <constraint exp="" field="surface_sub_class" desc=""/>
    <constraint exp="" field="zoom_category" desc=""/>
    <constraint exp="" field="nr_of_inhabitants" desc=""/>
    <constraint exp="" field="area" desc=""/>
    <constraint exp="" field="dry_weather_flow" desc=""/>
    <constraint exp="" field="surface_inclination" desc=""/>
    <constraint exp="" field="id" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortExpression="" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column name="function" hidden="0" width="-1" type="field"/>
      <column name="surface_class" hidden="0" width="-1" type="field"/>
      <column name="code" hidden="0" width="-1" type="field"/>
      <column name="display_name" hidden="0" width="-1" type="field"/>
      <column name="surface_sub_class" hidden="0" width="-1" type="field"/>
      <column name="zoom_category" hidden="0" width="-1" type="field"/>
      <column name="nr_of_inhabitants" hidden="0" width="-1" type="field"/>
      <column name="area" hidden="0" width="-1" type="field"/>
      <column name="dry_weather_flow" hidden="0" width="-1" type="field"/>
      <column name="surface_inclination" hidden="0" width="-1" type="field"/>
      <column name="id" hidden="0" width="-1" type="field"/>
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
Formulieren van QGIS mogen een functie van Python hebben die wordt aangeroepen wanneer het formulier wordt geopend.

Gebruik deze functie om extra logica aan uw formulieren toe te voegen.

Voer de naam van de functie in in het veld "Python Init functie".
Een voorbeeld volgt:
"""
from PyQt4.QtGui import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer name="Impervious surface" groupBox="1" columnCount="1" visibilityExpressionEnabled="0" visibilityExpression="" showLabel="1">
      <attributeEditorContainer name="General" groupBox="1" columnCount="1" visibilityExpressionEnabled="0" visibilityExpression="" showLabel="1">
        <attributeEditorField name="id" index="10" showLabel="1"/>
        <attributeEditorField name="display_name" index="3" showLabel="1"/>
        <attributeEditorField name="code" index="2" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Characteristics" groupBox="1" columnCount="1" visibilityExpressionEnabled="0" visibilityExpression="" showLabel="1">
        <attributeEditorContainer name="Storm water" groupBox="1" columnCount="1" visibilityExpressionEnabled="0" visibilityExpression="" showLabel="1">
          <attributeEditorField name="surface_class" index="1" showLabel="1"/>
          <attributeEditorField name="surface_sub_class" index="4" showLabel="1"/>
          <attributeEditorField name="surface_inclination" index="9" showLabel="1"/>
          <attributeEditorField name="area" index="7" showLabel="1"/>
        </attributeEditorContainer>
        <attributeEditorContainer name="Municipal water" groupBox="1" columnCount="1" visibilityExpressionEnabled="0" visibilityExpression="" showLabel="1">
          <attributeEditorField name="dry_weather_flow" index="8" showLabel="1"/>
          <attributeEditorField name="nr_of_inhabitants" index="6" showLabel="1"/>
        </attributeEditorContainer>
      </attributeEditorContainer>
      <attributeEditorContainer name="Visualization" groupBox="1" columnCount="1" visibilityExpressionEnabled="0" visibilityExpression="" showLabel="1">
        <attributeEditorField name="zoom_category" index="5" showLabel="1"/>
        <attributeEditorField name="function" index="0" showLabel="1"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="area" editable="1"/>
    <field name="code" editable="1"/>
    <field name="display_name" editable="1"/>
    <field name="dry_weather_flow" editable="1"/>
    <field name="function" editable="1"/>
    <field name="id" editable="1"/>
    <field name="nr_of_inhabitants" editable="1"/>
    <field name="surface_class" editable="1"/>
    <field name="surface_inclination" editable="1"/>
    <field name="surface_sub_class" editable="1"/>
    <field name="zoom_category" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="area" labelOnTop="0"/>
    <field name="code" labelOnTop="0"/>
    <field name="display_name" labelOnTop="0"/>
    <field name="dry_weather_flow" labelOnTop="0"/>
    <field name="function" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="nr_of_inhabitants" labelOnTop="0"/>
    <field name="surface_class" labelOnTop="0"/>
    <field name="surface_inclination" labelOnTop="0"/>
    <field name="surface_sub_class" labelOnTop="0"/>
    <field name="zoom_category" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>display_name</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
