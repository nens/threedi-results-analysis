<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" labelsEnabled="0" simplifyAlgorithm="0" styleCategories="AllStyleCategories" minScale="1e+08" version="3.10.10-A Coruña" maxScale="0" simplifyDrawingHints="1" simplifyDrawingTol="1" readOnly="0" simplifyLocal="1" simplifyMaxScale="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 attr="surface_class" type="categorizedSymbol" enableorderby="0" forceraster="0" symbollevels="0">
    <categories>
      <category render="true" label="unpaved (onverhard)" symbol="0" value="onverhard"/>
      <category render="true" label="semi-pervious paving (half verhard)" symbol="1" value="half verhard"/>
      <category render="true" label="pervious paving (open verharding)" symbol="2" value="open verharding"/>
      <category render="true" label="impervious paving (gesloten verharding)" symbol="3" value="gesloten verharding"/>
      <category render="true" label="building (pand)" symbol="4" value="pand"/>
    </categories>
    <symbols>
      <symbol name="0" alpha="1" type="fill" force_rhr="0" clip_to_extent="1">
        <layer class="SimpleFill" locked="0" pass="0" enabled="1">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="186,221,105,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="222,255,143,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
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
      <symbol name="1" alpha="1" type="fill" force_rhr="0" clip_to_extent="1">
        <layer class="SimpleFill" locked="0" pass="0" enabled="1">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="205,205,205,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="no" k="outline_style"/>
          <prop v="0" k="outline_width"/>
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
        <layer class="PointPatternFill" locked="0" pass="0" enabled="1">
          <prop v="0.75" k="displacement_x"/>
          <prop v="3x:0,0,0,0,0,0" k="displacement_x_map_unit_scale"/>
          <prop v="MM" k="displacement_x_unit"/>
          <prop v="0" k="displacement_y"/>
          <prop v="3x:0,0,0,0,0,0" k="displacement_y_map_unit_scale"/>
          <prop v="MM" k="displacement_y_unit"/>
          <prop v="1.5" k="distance_x"/>
          <prop v="3x:0,0,0,0,0,0" k="distance_x_map_unit_scale"/>
          <prop v="MM" k="distance_x_unit"/>
          <prop v="1.5" k="distance_y"/>
          <prop v="3x:0,0,0,0,0,0" k="distance_y_map_unit_scale"/>
          <prop v="MM" k="distance_y_unit"/>
          <prop v="0" k="offset_x"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_x_map_unit_scale"/>
          <prop v="MM" k="offset_x_unit"/>
          <prop v="0" k="offset_y"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_y_map_unit_scale"/>
          <prop v="MM" k="offset_y_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@1@1" alpha="1" type="marker" force_rhr="0" clip_to_extent="1">
            <layer class="SimpleMarker" locked="0" pass="0" enabled="1">
              <prop v="0" k="angle"/>
              <prop v="240,240,240,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="circle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="no" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="1" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties"/>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
        <layer class="SimpleLine" locked="0" pass="0" enabled="1">
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="255,255,255,255" k="line_color"/>
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
      <symbol name="2" alpha="1" type="fill" force_rhr="0" clip_to_extent="1">
        <layer class="SimpleFill" locked="0" pass="0" enabled="1">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="182,182,182,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="219,219,219,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
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
      <symbol name="3" alpha="1" type="fill" force_rhr="0" clip_to_extent="1">
        <layer class="SimpleFill" locked="0" pass="0" enabled="1">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="117,117,117,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="191,191,191,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
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
      <symbol name="4" alpha="1" type="fill" force_rhr="0" clip_to_extent="1">
        <layer class="SimpleFill" locked="0" pass="0" enabled="1">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="251,154,153,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="251,201,201,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
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
    <source-symbol>
      <symbol name="0" alpha="1" type="fill" force_rhr="0" clip_to_extent="1">
        <layer class="SimpleFill" locked="0" pass="0" enabled="1">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="117,117,117,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
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
    </source-symbol>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="dualview/previewExpressions">
      <value>display_name</value>
    </property>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Pie">
    <DiagramCategory barWidth="5" maxScaleDenominator="1e+08" width="15" backgroundColor="#ffffff" scaleDependency="Area" penColor="#000000" backgroundAlpha="255" height="15" diagramOrientation="Up" minScaleDenominator="0" scaleBasedVisibility="0" lineSizeScale="3x:0,0,0,0,0,0" sizeType="MM" opacity="1" penWidth="0" sizeScale="3x:0,0,0,0,0,0" enabled="0" rotationOffset="270" labelPlacementMethod="XHeight" penAlpha="255" lineSizeType="MM" minimumSize="0">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" color="#000000" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings zIndex="0" dist="0" obstacle="0" priority="0" showAll="1" placement="0" linePlacementFlags="2">
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
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration type="Map">
      <Option name="QgsGeometryGapCheck" type="Map">
        <Option name="allowedGapsBuffer" type="double" value="0"/>
        <Option name="allowedGapsEnabled" type="bool" value="false"/>
        <Option name="allowedGapsLayer" type="QString" value=""/>
      </Option>
    </checkConfiguration>
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
                <Option name="impervious paving (gesloten verharding)" type="QString" value="gesloten verharding"/>
              </Option>
              <Option type="Map">
                <Option name="pervious paving (open verharding)" type="QString" value="open verharding"/>
              </Option>
              <Option type="Map">
                <Option name="semi-pervious paving (half verhard)" type="QString" value="half verhard"/>
              </Option>
              <Option type="Map">
                <Option name="unpaved (onverhard)" type="QString" value="onverhard"/>
              </Option>
              <Option type="Map">
                <Option name="building (pand)" type="QString" value="pand"/>
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
                <Option name="level (vlak)" type="QString" value="vlak"/>
              </Option>
              <Option type="Map">
                <Option name="inclined (hellend)" type="QString" value="hellend"/>
              </Option>
              <Option type="Map">
                <Option name="elongated&#xa; (uitgestrekt)" type="QString" value="uitgestrekt"/>
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
    <default applyOnUpdate="0" expression="" field="function"/>
    <default applyOnUpdate="0" expression="" field="surface_class"/>
    <default applyOnUpdate="0" expression="'new'" field="code"/>
    <default applyOnUpdate="0" expression="'new'" field="display_name"/>
    <default applyOnUpdate="0" expression="" field="surface_sub_class"/>
    <default applyOnUpdate="0" expression="-1" field="zoom_category"/>
    <default applyOnUpdate="0" expression="" field="nr_of_inhabitants"/>
    <default applyOnUpdate="0" expression="$area" field="area"/>
    <default applyOnUpdate="0" expression="" field="dry_weather_flow"/>
    <default applyOnUpdate="0" expression="" field="surface_inclination"/>
    <default applyOnUpdate="0" expression="if(maximum(id) is null,1, maximum(id)+1)" field="id"/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" notnull_strength="0" exp_strength="0" field="function" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="2" exp_strength="0" field="surface_class" constraints="1"/>
    <constraint unique_strength="0" notnull_strength="2" exp_strength="0" field="code" constraints="1"/>
    <constraint unique_strength="0" notnull_strength="2" exp_strength="0" field="display_name" constraints="1"/>
    <constraint unique_strength="0" notnull_strength="0" exp_strength="0" field="surface_sub_class" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="2" exp_strength="0" field="zoom_category" constraints="1"/>
    <constraint unique_strength="0" notnull_strength="0" exp_strength="0" field="nr_of_inhabitants" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="2" exp_strength="0" field="area" constraints="1"/>
    <constraint unique_strength="0" notnull_strength="0" exp_strength="0" field="dry_weather_flow" constraints="0"/>
    <constraint unique_strength="0" notnull_strength="2" exp_strength="0" field="surface_inclination" constraints="1"/>
    <constraint unique_strength="1" notnull_strength="1" exp_strength="0" field="id" constraints="3"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="function"/>
    <constraint exp="" desc="" field="surface_class"/>
    <constraint exp="" desc="" field="code"/>
    <constraint exp="" desc="" field="display_name"/>
    <constraint exp="" desc="" field="surface_sub_class"/>
    <constraint exp="" desc="" field="zoom_category"/>
    <constraint exp="" desc="" field="nr_of_inhabitants"/>
    <constraint exp="" desc="" field="area"/>
    <constraint exp="" desc="" field="dry_weather_flow"/>
    <constraint exp="" desc="" field="surface_inclination"/>
    <constraint exp="" desc="" field="id"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column name="function" type="field" hidden="0" width="-1"/>
      <column name="surface_class" type="field" hidden="0" width="-1"/>
      <column name="code" type="field" hidden="0" width="-1"/>
      <column name="display_name" type="field" hidden="0" width="-1"/>
      <column name="surface_sub_class" type="field" hidden="0" width="-1"/>
      <column name="zoom_category" type="field" hidden="0" width="-1"/>
      <column name="nr_of_inhabitants" type="field" hidden="0" width="-1"/>
      <column name="area" type="field" hidden="0" width="-1"/>
      <column name="dry_weather_flow" type="field" hidden="0" width="-1"/>
      <column name="surface_inclination" type="field" hidden="0" width="-1"/>
      <column name="id" type="field" hidden="0" width="-1"/>
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
    <attributeEditorContainer name="Impervious surface" columnCount="1" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1">
      <attributeEditorContainer name="General" columnCount="1" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1">
        <attributeEditorField name="id" showLabel="1" index="10"/>
        <attributeEditorField name="display_name" showLabel="1" index="3"/>
        <attributeEditorField name="code" showLabel="1" index="2"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Characteristics" columnCount="1" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1">
        <attributeEditorContainer name="Storm water" columnCount="1" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1">
          <attributeEditorField name="surface_class" showLabel="1" index="1"/>
          <attributeEditorField name="surface_sub_class" showLabel="1" index="4"/>
          <attributeEditorField name="surface_inclination" showLabel="1" index="9"/>
          <attributeEditorField name="area" showLabel="1" index="7"/>
        </attributeEditorContainer>
        <attributeEditorContainer name="Municipal water" columnCount="1" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1">
          <attributeEditorField name="dry_weather_flow" showLabel="1" index="8"/>
          <attributeEditorField name="nr_of_inhabitants" showLabel="1" index="6"/>
        </attributeEditorContainer>
      </attributeEditorContainer>
      <attributeEditorContainer name="Visualization" columnCount="1" showLabel="1" visibilityExpression="" visibilityExpressionEnabled="0" groupBox="1">
        <attributeEditorField name="zoom_category" showLabel="1" index="5"/>
        <attributeEditorField name="function" showLabel="1" index="0"/>
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
  <previewExpression>"display_name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
