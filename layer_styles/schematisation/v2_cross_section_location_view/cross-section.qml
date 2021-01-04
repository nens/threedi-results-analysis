<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis minScale="1e+08" simplifyDrawingTol="1" maxScale="0" labelsEnabled="1" simplifyMaxScale="1" simplifyDrawingHints="0" readOnly="0" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" version="3.10.10-A Coruña" simplifyAlgorithm="0" simplifyLocal="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" type="singleSymbol" symbollevels="0" forceraster="0">
    <symbols>
      <symbol type="marker" name="0" force_rhr="0" alpha="1" clip_to_extent="1">
        <layer enabled="1" pass="0" locked="0" class="SimpleMarker">
          <prop k="angle" v="0"/>
          <prop k="color" v="19,61,142,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="RenderMetersInMapUnits"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="try(&#xd;&#xa;&#x9;coalesce(&#xd;&#xa;&#x9;&#x9;CASE WHEN def_shape = 1 THEN to_real(def_width)&#xd;&#xa;&#x9;&#x9;WHEN def_shape = 2 THEN to_real(def_width) &#xd;&#xa;&#x9;&#x9;WHEN def_shape = 3 THEN to_real(def_width)&#xd;&#xa;&#x9;&#x9;WHEN def_shape in (5, 6) THEN &#xd;&#xa;&#x9;&#x9;&#x9;to_real(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;array_last(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;array_sort(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;string_to_array(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;def_width,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;' '&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;END, &#xd;&#xa; &#x9;&#x9;1&#xd;&#xa;&#x9;), &#xd;&#xa;&#x9;1&#xd;&#xa;)"/>
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
  <labeling type="rule-based">
    <rules key="{537fb1c3-2599-41cd-aec9-e64c53192898}">
      <rule description="Crosssection" scalemaxdenom="10000" key="{a7f91f2b-eb32-4a2c-98ee-f5aebefd878c}">
        <settings calloutType="simple">
          <text-style fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontItalic="0" fontLetterSpacing="0" fontCapitals="0" textOrientation="horizontal" fontKerning="1" fontFamily="MS Gothic" textOpacity="1" fontSizeUnit="Point" fontWordSpacing="0" fontStrikeout="0" useSubstitutions="0" fontWeight="50" fieldName="represent_value(def_shape)&#xd;&#xa;|| '\n' || &#xd;&#xa;CASE WHEN def_shape = 1 THEN 'w: '||format_number(to_real(def_width),2) &#xd;&#xa;WHEN def_shape = 2 THEN 'Ø'||format_number(to_real(def_width),2) &#xd;&#xa;WHEN def_shape = 3 THEN 'w: ' || format_number(to_real(def_width),2) &#xd;&#xa;WHEN def_shape in (5, 6) THEN &#xd;&#xa;&#x9;'w: ' || &#xd;&#xa;&#x9;format_number(&#xd;&#xa;&#x9;&#x9;to_real(&#xd;&#xa;&#x9;&#x9;&#x9;array_last(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;array_sort(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;string_to_array(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;def_width,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;' '&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;),&#xd;&#xa;&#x9;&#x9;2&#xd;&#xa;&#x9;)&#xd;&#xa;END&#xd;&#xa;||  '\n' || &#xd;&#xa;CASE WHEN def_shape = 1 THEN 'h: '||format_number(to_real(def_height),2) &#xd;&#xa;WHEN def_shape = 2 THEN '' &#xd;&#xa;WHEN def_shape = 3 THEN 'h: ' || format_number(to_real(def_width*1.5),2) &#xd;&#xa;WHEN def_shape in (5, 6) THEN &#xd;&#xa;&#x9;'h: ' || &#xd;&#xa;&#x9;format_number(&#xd;&#xa;&#x9;&#x9;to_real(&#xd;&#xa;&#x9;&#x9;&#x9;array_last(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;array_sort(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;string_to_array(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;def_height,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;' '&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;),&#xd;&#xa;&#x9;&#x9;2&#xd;&#xa;&#x9;)&#xd;&#xa;END" textColor="0,0,0,255" previewBkgrdColor="255,255,255,255" fontSize="7" blendMode="0" multilineHeight="1" isExpression="1" namedStyle="Regular" fontUnderline="0">
            <text-buffer bufferDraw="1" bufferSizeUnits="MM" bufferSize="0.7" bufferColor="255,255,255,255" bufferNoFill="0" bufferOpacity="1" bufferJoinStyle="128" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferBlendMode="0"/>
            <background shapeOpacity="1" shapeSizeUnit="MM" shapeJoinStyle="64" shapeDraw="0" shapeRotation="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetUnit="MM" shapeBorderWidth="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeSVGFile="" shapeRotationType="0" shapeSizeType="0" shapeRadiiY="0" shapeFillColor="255,255,255,255" shapeSizeX="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetY="0" shapeRadiiUnit="MM" shapeType="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeSizeY="0" shapeOffsetX="0" shapeBorderColor="128,128,128,255" shapeBorderWidthUnit="MM" shapeRadiiX="0" shapeBlendMode="0">
              <symbol type="marker" name="markerSymbol" force_rhr="0" alpha="1" clip_to_extent="1">
                <layer enabled="1" pass="0" locked="0" class="SimpleMarker">
                  <prop k="angle" v="0"/>
                  <prop k="color" v="133,182,111,255"/>
                  <prop k="horizontal_anchor_point" v="1"/>
                  <prop k="joinstyle" v="bevel"/>
                  <prop k="name" v="circle"/>
                  <prop k="offset" v="0,0"/>
                  <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="offset_unit" v="MM"/>
                  <prop k="outline_color" v="35,35,35,255"/>
                  <prop k="outline_style" v="solid"/>
                  <prop k="outline_width" v="0"/>
                  <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="outline_width_unit" v="MM"/>
                  <prop k="scale_method" v="diameter"/>
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
            </background>
            <shadow shadowUnder="0" shadowOffsetDist="1" shadowOffsetGlobal="1" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetAngle="135" shadowBlendMode="6" shadowDraw="0" shadowRadiusUnit="MM" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowScale="100" shadowOffsetUnit="MM" shadowRadius="1.5" shadowColor="0,0,0,255" shadowOpacity="0.7" shadowRadiusAlphaOnly="0"/>
            <dd_properties>
              <Option type="Map">
                <Option type="QString" name="name" value=""/>
                <Option name="properties"/>
                <Option type="QString" name="type" value="collection"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format reverseDirectionSymbol="0" placeDirectionSymbol="0" decimals="3" plussign="0" multilineAlign="0" autoWrapLength="0" rightDirectionSymbol=">" useMaxLineLengthForAutoWrap="1" wrapChar="" formatNumbers="0" leftDirectionSymbol="&lt;" addDirectionSymbol="0"/>
          <placement overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" distMapUnitScale="3x:0,0,0,0,0,0" preserveRotation="1" overrunDistanceUnit="MM" geometryGeneratorEnabled="0" maxCurvedCharAngleOut="-25" dist="0" geometryGeneratorType="PointGeometry" centroidWhole="0" priority="5" xOffset="0" placement="0" quadOffset="4" layerType="PointGeometry" placementFlags="9" repeatDistance="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" yOffset="0" centroidInside="0" geometryGenerator="" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" maxCurvedCharAngleIn="25" overrunDistance="0" rotationAngle="0" repeatDistanceUnits="MM" offsetType="0" offsetUnits="MapUnit" fitInPolygonOnly="0" distUnits="MM"/>
          <rendering zIndex="0" mergeLines="0" fontMinPixelSize="3" scaleMax="10000000" limitNumLabels="0" labelPerPart="0" drawLabels="1" obstacleFactor="1" obstacleType="0" scaleVisibility="0" fontLimitPixelSize="0" displayAll="0" maxNumLabels="2000" scaleMin="1" minFeatureSize="0" upsidedownLabels="0" fontMaxPixelSize="10000" obstacle="1"/>
          <dd_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="Color">
                  <Option type="bool" name="active" value="false"/>
                  <Option type="QString" name="expression" value="case &#xd;&#xa;when &quot;pipe_sewerage_type&quot; = 0 then '#ffaa00'&#xd;&#xa;when &quot;pipe_sewerage_type&quot; = 0 then '#55aaff'&#xd;&#xa;when &quot;pipe_sewerage_type&quot; = 0 then '#ff0000'&#xd;&#xa;when &quot;pipe_sewerage_type&quot; = 0 then '#999999'&#xd;&#xa;else '#000000'&#xd;&#xa;end"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option type="QString" name="anchorPoint" value="pole_of_inaccessibility"/>
              <Option type="Map" name="ddProperties">
                <Option type="QString" name="name" value=""/>
                <Option name="properties"/>
                <Option type="QString" name="type" value="collection"/>
              </Option>
              <Option type="bool" name="drawToAllParts" value="false"/>
              <Option type="QString" name="enabled" value="0"/>
              <Option type="QString" name="lineSymbol" value="&lt;symbol type=&quot;line&quot; name=&quot;symbol&quot; force_rhr=&quot;0&quot; alpha=&quot;1&quot; clip_to_extent=&quot;1&quot;>&lt;layer enabled=&quot;1&quot; pass=&quot;0&quot; locked=&quot;0&quot; class=&quot;SimpleLine&quot;>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option type=&quot;QString&quot; name=&quot;name&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;type&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
              <Option type="double" name="minLength" value="0"/>
              <Option type="QString" name="minLengthMapUnitScale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="minLengthUnit" value="MM"/>
              <Option type="double" name="offsetFromAnchor" value="0"/>
              <Option type="QString" name="offsetFromAnchorMapUnitScale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="offsetFromAnchorUnit" value="MM"/>
              <Option type="double" name="offsetFromLabel" value="0"/>
              <Option type="QString" name="offsetFromLabelMapUnitScale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="offsetFromLabelUnit" value="MM"/>
            </Option>
          </callout>
        </settings>
      </rule>
    </rules>
  </labeling>
  <customproperties>
    <property key="dualview/previewExpressions" value="id"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory diagramOrientation="Up" height="15" lineSizeScale="3x:0,0,0,0,0,0" barWidth="5" scaleBasedVisibility="0" minScaleDenominator="0" penWidth="0" penColor="#000000" sizeType="MM" labelPlacementMethod="XHeight" opacity="1" lineSizeType="MM" backgroundAlpha="255" sizeScale="3x:0,0,0,0,0,0" rotationOffset="270" penAlpha="255" width="15" enabled="0" maxScaleDenominator="1e+08" backgroundColor="#ffffff" minimumSize="0" scaleDependency="Area">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" field="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings linePlacementFlags="18" priority="0" zIndex="0" placement="0" dist="0" obstacle="0" showAll="1">
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
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="loc_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_reference_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_bank_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_friction_type">
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
    <field name="loc_friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="loc_channel_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_shape">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="1: rectangle" value="1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="2: round" value="2"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="3: egg" value="3"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="5: tabulated rectangle" value="5"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="6: tabulated trapezium" value="6"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_width">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="def_height">
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
    <alias index="0" name="" field="ROWID"/>
    <alias index="1" name="id" field="loc_id"/>
    <alias index="2" name="code" field="loc_code"/>
    <alias index="3" name="reference_level" field="loc_reference_level"/>
    <alias index="4" name="bank_level" field="loc_bank_level"/>
    <alias index="5" name="friction_type" field="loc_friction_type"/>
    <alias index="6" name="friction_value" field="loc_friction_value"/>
    <alias index="7" name="definition_id" field="loc_definition_id"/>
    <alias index="8" name="channel_id" field="loc_channel_id"/>
    <alias index="9" name="" field="def_id"/>
    <alias index="10" name="" field="def_shape"/>
    <alias index="11" name="" field="def_width"/>
    <alias index="12" name="" field="def_code"/>
    <alias index="13" name="" field="def_height"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="ROWID"/>
    <default expression="if(maximum(loc_id) is null,1,maximum(loc_id)+1)" applyOnUpdate="0" field="loc_id"/>
    <default expression="'new'" applyOnUpdate="0" field="loc_code"/>
    <default expression="" applyOnUpdate="0" field="loc_reference_level"/>
    <default expression="" applyOnUpdate="0" field="loc_bank_level"/>
    <default expression="2" applyOnUpdate="0" field="loc_friction_type"/>
    <default expression="" applyOnUpdate="0" field="loc_friction_value"/>
    <default expression="" applyOnUpdate="0" field="loc_definition_id"/>
    <default expression="aggregate('v2_channel','min',&quot;id&quot;, intersects($geometry,geometry(@parent)))" applyOnUpdate="0" field="loc_channel_id"/>
    <default expression="" applyOnUpdate="0" field="def_id"/>
    <default expression="" applyOnUpdate="0" field="def_shape"/>
    <default expression="" applyOnUpdate="0" field="def_width"/>
    <default expression="" applyOnUpdate="0" field="def_code"/>
    <default expression="" applyOnUpdate="0" field="def_height"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" notnull_strength="0" unique_strength="0" constraints="0" field="ROWID"/>
    <constraint exp_strength="0" notnull_strength="2" unique_strength="0" constraints="1" field="loc_id"/>
    <constraint exp_strength="0" notnull_strength="0" unique_strength="0" constraints="0" field="loc_code"/>
    <constraint exp_strength="0" notnull_strength="2" unique_strength="0" constraints="1" field="loc_reference_level"/>
    <constraint exp_strength="0" notnull_strength="0" unique_strength="0" constraints="0" field="loc_bank_level"/>
    <constraint exp_strength="0" notnull_strength="0" unique_strength="0" constraints="0" field="loc_friction_type"/>
    <constraint exp_strength="0" notnull_strength="2" unique_strength="0" constraints="1" field="loc_friction_value"/>
    <constraint exp_strength="0" notnull_strength="2" unique_strength="0" constraints="1" field="loc_definition_id"/>
    <constraint exp_strength="0" notnull_strength="2" unique_strength="0" constraints="1" field="loc_channel_id"/>
    <constraint exp_strength="0" notnull_strength="0" unique_strength="0" constraints="0" field="def_id"/>
    <constraint exp_strength="0" notnull_strength="0" unique_strength="0" constraints="0" field="def_shape"/>
    <constraint exp_strength="0" notnull_strength="0" unique_strength="0" constraints="0" field="def_width"/>
    <constraint exp_strength="0" notnull_strength="0" unique_strength="0" constraints="0" field="def_code"/>
    <constraint exp_strength="0" notnull_strength="0" unique_strength="0" constraints="0" field="def_height"/>
  </constraints>
  <constraintExpressions>
    <constraint field="ROWID" desc="" exp=""/>
    <constraint field="loc_id" desc="" exp=""/>
    <constraint field="loc_code" desc="" exp=""/>
    <constraint field="loc_reference_level" desc="" exp=""/>
    <constraint field="loc_bank_level" desc="" exp=""/>
    <constraint field="loc_friction_type" desc="" exp=""/>
    <constraint field="loc_friction_value" desc="" exp=""/>
    <constraint field="loc_definition_id" desc="" exp=""/>
    <constraint field="loc_channel_id" desc="" exp=""/>
    <constraint field="def_id" desc="" exp=""/>
    <constraint field="def_shape" desc="" exp=""/>
    <constraint field="def_width" desc="" exp=""/>
    <constraint field="def_code" desc="" exp=""/>
    <constraint field="def_height" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortExpression="" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column type="actions" hidden="1" width="-1"/>
      <column type="field" name="def_id" hidden="0" width="-1"/>
      <column type="field" name="def_shape" hidden="0" width="-1"/>
      <column type="field" name="def_width" hidden="0" width="-1"/>
      <column type="field" name="def_code" hidden="0" width="-1"/>
      <column type="field" name="def_height" hidden="0" width="-1"/>
      <column type="field" name="ROWID" hidden="0" width="-1"/>
      <column type="field" name="loc_id" hidden="0" width="-1"/>
      <column type="field" name="loc_code" hidden="0" width="-1"/>
      <column type="field" name="loc_reference_level" hidden="0" width="-1"/>
      <column type="field" name="loc_bank_level" hidden="0" width="-1"/>
      <column type="field" name="loc_friction_type" hidden="0" width="-1"/>
      <column type="field" name="loc_friction_value" hidden="0" width="-1"/>
      <column type="field" name="loc_definition_id" hidden="0" width="-1"/>
      <column type="field" name="loc_channel_id" hidden="0" width="-1"/>
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
    <attributeEditorContainer showLabel="1" visibilityExpressionEnabled="0" name="Cross section location view" visibilityExpression="" columnCount="1" groupBox="0">
      <attributeEditorContainer showLabel="1" visibilityExpressionEnabled="0" name="General" visibilityExpression="" columnCount="1" groupBox="1">
        <attributeEditorField showLabel="1" name="loc_id" index="1"/>
        <attributeEditorField showLabel="1" name="loc_code" index="2"/>
        <attributeEditorField showLabel="1" name="loc_reference_level" index="3"/>
        <attributeEditorField showLabel="1" name="loc_bank_level" index="4"/>
        <attributeEditorField showLabel="1" name="loc_friction_type" index="5"/>
        <attributeEditorField showLabel="1" name="loc_friction_value" index="6"/>
        <attributeEditorField showLabel="1" name="loc_channel_id" index="8"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" visibilityExpressionEnabled="0" name="Cross section" visibilityExpression="" columnCount="1" groupBox="1">
        <attributeEditorField showLabel="1" name="loc_definition_id" index="7"/>
        <attributeEditorField showLabel="1" name="def_code" index="12"/>
        <attributeEditorField showLabel="1" name="def_shape" index="10"/>
        <attributeEditorField showLabel="1" name="def_width" index="11"/>
        <attributeEditorField showLabel="1" name="def_height" index="13"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="ROWID"/>
    <field editable="1" name="bank_level"/>
    <field editable="1" name="channel_id"/>
    <field editable="1" name="code"/>
    <field editable="0" name="def_code"/>
    <field editable="0" name="def_height"/>
    <field editable="1" name="def_id"/>
    <field editable="0" name="def_shape"/>
    <field editable="0" name="def_width"/>
    <field editable="1" name="definition_id"/>
    <field editable="1" name="friction_type"/>
    <field editable="1" name="friction_value"/>
    <field editable="1" name="id"/>
    <field editable="1" name="loc_bank_level"/>
    <field editable="1" name="loc_channel_id"/>
    <field editable="1" name="loc_code"/>
    <field editable="1" name="loc_definition_id"/>
    <field editable="1" name="loc_friction_type"/>
    <field editable="1" name="loc_friction_value"/>
    <field editable="1" name="loc_id"/>
    <field editable="1" name="loc_reference_level"/>
    <field editable="1" name="location_bank_level"/>
    <field editable="1" name="location_channel_id"/>
    <field editable="1" name="location_code"/>
    <field editable="1" name="location_definition_id"/>
    <field editable="1" name="location_friction_type"/>
    <field editable="1" name="location_friction_value"/>
    <field editable="1" name="location_id"/>
    <field editable="1" name="location_reference_level"/>
    <field editable="1" name="reference_level"/>
    <field editable="0" name="v2_cross_section_definition_code"/>
    <field editable="0" name="v2_cross_section_definition_height"/>
    <field editable="0" name="v2_cross_section_definition_shape"/>
    <field editable="0" name="v2_cross_section_definition_width"/>
  </editable>
  <labelOnTop>
    <field name="ROWID" labelOnTop="0"/>
    <field name="bank_level" labelOnTop="0"/>
    <field name="channel_id" labelOnTop="0"/>
    <field name="code" labelOnTop="0"/>
    <field name="def_code" labelOnTop="0"/>
    <field name="def_height" labelOnTop="0"/>
    <field name="def_id" labelOnTop="0"/>
    <field name="def_shape" labelOnTop="0"/>
    <field name="def_width" labelOnTop="0"/>
    <field name="definition_id" labelOnTop="0"/>
    <field name="friction_type" labelOnTop="0"/>
    <field name="friction_value" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="loc_bank_level" labelOnTop="0"/>
    <field name="loc_channel_id" labelOnTop="0"/>
    <field name="loc_code" labelOnTop="0"/>
    <field name="loc_definition_id" labelOnTop="0"/>
    <field name="loc_friction_type" labelOnTop="0"/>
    <field name="loc_friction_value" labelOnTop="0"/>
    <field name="loc_id" labelOnTop="0"/>
    <field name="loc_reference_level" labelOnTop="0"/>
    <field name="location_bank_level" labelOnTop="0"/>
    <field name="location_channel_id" labelOnTop="0"/>
    <field name="location_code" labelOnTop="0"/>
    <field name="location_definition_id" labelOnTop="0"/>
    <field name="location_friction_type" labelOnTop="0"/>
    <field name="location_friction_value" labelOnTop="0"/>
    <field name="location_id" labelOnTop="0"/>
    <field name="location_reference_level" labelOnTop="0"/>
    <field name="reference_level" labelOnTop="0"/>
    <field name="v2_cross_section_definition_code" labelOnTop="0"/>
    <field name="v2_cross_section_definition_height" labelOnTop="0"/>
    <field name="v2_cross_section_definition_shape" labelOnTop="0"/>
    <field name="v2_cross_section_definition_width" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>location_id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
