<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" version="3.4.12-Madeira" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" minScale="1e+08">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property value="false" key="WMSBackgroundLayer"/>
    <property value="false" key="WMSPublishDataSourceUrl"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property value="Value" key="identify/format"/>
  </customproperties>
  <pipe>
    <rasterrenderer alphaBand="-1" band="1" classificationMax="0.5" type="singlebandpseudocolor" opacity="1" classificationMin="-0.5">
      <rasterTransparency>
        <singleValuePixelList>
          <pixelListEntry max="0.01" min="-0.01" percentTransparent="100"/>
        </singleValuePixelList>
      </rasterTransparency>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader clip="0" classificationMode="1" colorRampType="INTERPOLATED">
          <colorramp name="[source]" type="gradient">
            <prop v="77,172,38,255" k="color1"/>
            <prop v="208,28,139,255" k="color2"/>
            <prop v="0" k="discrete"/>
            <prop v="gradient" k="rampType"/>
            <prop v="0.25;184,225,134,255:0.5;247,247,247,255:0.75;241,182,218,255" k="stops"/>
          </colorramp>
          <item alpha="255" color="#4dac26" label="-0.5" value="-0.5"/>
          <item alpha="255" color="#b8e186" label="-0.25" value="-0.25"/>
          <item alpha="255" color="#f7f7f7" label="0" value="0"/>
          <item alpha="255" color="#f1b6da" label="0.25" value="0.25"/>
          <item alpha="255" color="#d01c8b" label="0.5" value="0.5"/>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast contrast="0" brightness="0"/>
    <huesaturation saturation="0" colorizeBlue="128" colorizeOn="0" colorizeRed="255" grayscaleMode="0" colorizeStrength="100" colorizeGreen="128"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>