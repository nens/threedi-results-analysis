<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="0" simplifyDrawingHints="1" simplifyAlgorithm="0" maxScale="0" simplifyMaxScale="1" simplifyLocal="1" hasScaleBasedVisibilityFlag="0" simplifyDrawingTol="1" minScale="1e+08" version="3.4.5-Madeira" styleCategories="AllStyleCategories" readOnly="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" type="RuleRenderer" symbollevels="0" forceraster="0">
    <rules key="{ef7b6218-5639-4216-a577-db0c96e2a759}">
      <rule label="hellend" symbol="0" filter="surface_inclination = 'hellend'" key="{68cb011a-8a27-4aa2-a23d-858ba251f42b}"/>
      <rule label="vlak" symbol="1" filter="surface_inclination = 'vlak'" key="{91463b0e-a824-4df0-a0bd-8dcb0b5f2094}"/>
      <rule label="uitgestrekt" symbol="2" filter="surface_inclination = 'uitgestrekt'" key="{1dde8d91-4769-421d-bad7-5aa700191647}"/>
      <rule label="gesloten verharding" symbol="3" filter="surface_class = 'gesloten verharding'" key="{9c187ace-e49a-4660-8aed-a23359e3828d}"/>
      <rule label="open verharding" symbol="4" filter="surface_class = 'open verharding'" key="{bfb69c3c-b9b3-4865-94cb-7ea349f429dc}"/>
      <rule label="onverhard" symbol="5" filter="surface_class = 'half verhard' OR surface_class = 'onverhard'" key="{1ee7fc0c-ce99-4a36-83c1-10163a3ae8b3}"/>
      <rule label="pand" symbol="6" filter="surface_class = 'pand'" key="{32d556c3-f4d6-49ff-808b-ebc499c1f5f1}"/>
    </rules>
    <symbols>
      <symbol force_rhr="0" name="0" clip_to_extent="1" alpha="1" type="fill">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="128,152,72,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.26" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleFill" enabled="1" pass="0" locked="0">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="128,128,128,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="no" k="outline_style"/>
          <prop v="1" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="no" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" name="1" clip_to_extent="1" alpha="1" type="fill">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0,0,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.26" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" name="2" clip_to_extent="1" alpha="1" type="fill">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop v="square" k="capstyle"/>
          <prop v="0" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="175,179,138,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.26" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleFill" enabled="1" pass="0" locked="0">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="128,128,128,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="no" k="outline_style"/>
          <prop v="1" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="no" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" name="3" clip_to_extent="1" alpha="1" type="fill">
        <layer class="SimpleFill" enabled="1" pass="0" locked="0">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="117,117,117,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="117,117,117,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.26" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" name="4" clip_to_extent="1" alpha="1" type="fill">
        <layer class="SimpleFill" enabled="1" pass="0" locked="0">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="182,182,182,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="182,182,182,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.26" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" name="5" clip_to_extent="1" alpha="1" type="fill">
        <layer class="SimpleFill" enabled="1" pass="0" locked="0">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="186,221,105,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="186,221,105,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.26" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" name="6" clip_to_extent="1" alpha="1" type="fill">
        <layer class="SimpleFill" enabled="1" pass="0" locked="0">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="170,85,255,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="170,85,255,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.26" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
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
  </renderer-v2>
  <customproperties>
    <property key="dualview/previewExpressions" value="display_name"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Pie">
    <DiagramCategory scaleDependency="Area" lineSizeScale="3x:0,0,0,0,0,0" barWidth="5" backgroundAlpha="255" diagramOrientation="Up" penAlpha="255" maxScaleDenominator="1e+08" sizeScale="3x:0,0,0,0,0,0" penColor="#000000" opacity="1" enabled="0" labelPlacementMethod="XHeight" penWidth="0" rotationOffset="270" lineSizeType="MM" backgroundColor="#ffffff" height="15" sizeType="MM" minScaleDenominator="0" minimumSize="0" scaleBasedVisibility="0" width="15">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" field="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings placement="0" dist="0" showAll="1" priority="0" obstacle="0" zIndex="0" linePlacementFlags="2">
    <properties>
      <Option type="Map">
        <Option name="name" type="QString" value=""/>
        <Option name="properties" type="Map">
          <Option name="show" type="Map">
            <Option name="active" type="bool" value="true"/>
            <Option name="field" type="QString" value="function"/>
            <Option name="type" type="int" value="2"/>
          </Option>
        </Option>
        <Option name="type" type="QString" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="function">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
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
                <Option name="gesloten verharding" type="QString" value="gesloten verharding"/>
              </Option>
              <Option type="Map">
                <Option name="open verharding" type="QString" value="open verharding"/>
              </Option>
              <Option type="Map">
                <Option name="half verhard" type="QString" value="half verhard"/>
              </Option>
              <Option type="Map">
                <Option name="onverhard" type="QString" value="onverhard"/>
              </Option>
              <Option type="Map">
                <Option name="pand" type="QString" value="pand"/>
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
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="surface_sub_class">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
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
                <Option name="-1" type="QString" value="-1"/>
              </Option>
              <Option type="Map">
                <Option name="0" type="QString" value="0"/>
              </Option>
              <Option type="Map">
                <Option name="1" type="QString" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="2" type="QString" value="2"/>
              </Option>
              <Option type="Map">
                <Option name="3" type="QString" value="3"/>
              </Option>
              <Option type="Map">
                <Option name="4" type="QString" value="4"/>
              </Option>
              <Option type="Map">
                <Option name="5" type="QString" value="5"/>
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
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="area">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dry_weather_flow">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
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
                <Option name="vlak" type="QString" value="vlak"/>
              </Option>
              <Option type="Map">
                <Option name="hellend" type="QString" value="hellend"/>
              </Option>
              <Option type="Map">
                <Option name="uitgestrekt" type="QString" value="uitgestrekt"/>
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
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="" field="function"/>
    <alias index="1" name="" field="surface_class"/>
    <alias index="2" name="" field="code"/>
    <alias index="3" name="" field="display_name"/>
    <alias index="4" name="" field="surface_sub_class"/>
    <alias index="5" name="" field="zoom_category"/>
    <alias index="6" name="" field="nr_of_inhabitants"/>
    <alias index="7" name="" field="area"/>
    <alias index="8" name="" field="dry_weather_flow"/>
    <alias index="9" name="" field="surface_inclination"/>
    <alias index="10" name="" field="id"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="function"/>
    <default expression="" applyOnUpdate="0" field="surface_class"/>
    <default expression="'new'" applyOnUpdate="0" field="code"/>
    <default expression="'new'" applyOnUpdate="0" field="display_name"/>
    <default expression="" applyOnUpdate="0" field="surface_sub_class"/>
    <default expression="-1" applyOnUpdate="0" field="zoom_category"/>
    <default expression="0" applyOnUpdate="0" field="nr_of_inhabitants"/>
    <default expression="round($area,1)" applyOnUpdate="0" field="area"/>
    <default expression="" applyOnUpdate="0" field="dry_weather_flow"/>
    <default expression="" applyOnUpdate="0" field="surface_inclination"/>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" field="function" exp_strength="0" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" field="surface_class" exp_strength="0" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" field="code" exp_strength="0" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" field="display_name" exp_strength="0" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" field="surface_sub_class" exp_strength="0" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" field="zoom_category" exp_strength="0" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" field="nr_of_inhabitants" exp_strength="0" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" field="area" exp_strength="0" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="0" field="dry_weather_flow" exp_strength="0" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" field="surface_inclination" exp_strength="0" notnull_strength="2" constraints="1"/>
    <constraint unique_strength="1" field="id" exp_strength="0" notnull_strength="1" constraints="3"/>
  </constraints>
  <constraintExpressions>
    <constraint field="function" exp="" desc=""/>
    <constraint field="surface_class" exp="" desc=""/>
    <constraint field="code" exp="" desc=""/>
    <constraint field="display_name" exp="" desc=""/>
    <constraint field="surface_sub_class" exp="" desc=""/>
    <constraint field="zoom_category" exp="" desc=""/>
    <constraint field="nr_of_inhabitants" exp="" desc=""/>
    <constraint field="area" exp="" desc=""/>
    <constraint field="dry_weather_flow" exp="" desc=""/>
    <constraint field="surface_inclination" exp="" desc=""/>
    <constraint field="id" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column hidden="0" name="function" type="field" width="-1"/>
      <column hidden="0" name="surface_class" type="field" width="-1"/>
      <column hidden="0" name="code" type="field" width="-1"/>
      <column hidden="0" name="display_name" type="field" width="-1"/>
      <column hidden="0" name="surface_sub_class" type="field" width="-1"/>
      <column hidden="0" name="zoom_category" type="field" width="-1"/>
      <column hidden="0" name="nr_of_inhabitants" type="field" width="-1"/>
      <column hidden="0" name="area" type="field" width="-1"/>
      <column hidden="0" name="dry_weather_flow" type="field" width="-1"/>
      <column hidden="0" name="surface_inclination" type="field" width="-1"/>
      <column hidden="0" name="id" type="field" width="-1"/>
      <column hidden="1" type="actions" width="-1"/>
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
    <attributeEditorContainer showLabel="1" name="Impervious surface" visibilityExpressionEnabled="0" visibilityExpression="" groupBox="1" columnCount="1">
      <attributeEditorContainer showLabel="1" name="General" visibilityExpressionEnabled="0" visibilityExpression="" groupBox="1" columnCount="1">
        <attributeEditorField showLabel="1" index="10" name="id"/>
        <attributeEditorField showLabel="1" index="3" name="display_name"/>
        <attributeEditorField showLabel="1" index="2" name="code"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" name="Characteristics" visibilityExpressionEnabled="0" visibilityExpression="" groupBox="1" columnCount="1">
        <attributeEditorContainer showLabel="1" name="Storm water" visibilityExpressionEnabled="0" visibilityExpression="" groupBox="1" columnCount="1">
          <attributeEditorField showLabel="1" index="1" name="surface_class"/>
          <attributeEditorField showLabel="1" index="4" name="surface_sub_class"/>
          <attributeEditorField showLabel="1" index="9" name="surface_inclination"/>
          <attributeEditorField showLabel="1" index="7" name="area"/>
        </attributeEditorContainer>
        <attributeEditorContainer showLabel="1" name="Municipal water" visibilityExpressionEnabled="0" visibilityExpression="" groupBox="1" columnCount="1">
          <attributeEditorField showLabel="1" index="8" name="dry_weather_flow"/>
          <attributeEditorField showLabel="1" index="6" name="nr_of_inhabitants"/>
        </attributeEditorContainer>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" name="Visualization" visibilityExpressionEnabled="0" visibilityExpression="" groupBox="1" columnCount="1">
        <attributeEditorField showLabel="1" index="5" name="zoom_category"/>
        <attributeEditorField showLabel="1" index="0" name="function"/>
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
