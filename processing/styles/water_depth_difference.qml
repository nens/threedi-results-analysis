<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.40.6-Bratislava" styleCategories="Symbology|Forms">
  <pipe-data-defined-properties>
    <Option type="Map">
      <Option type="QString" value="" name="name"/>
      <Option name="properties"/>
      <Option type="QString" value="collection" name="type"/>
    </Option>
  </pipe-data-defined-properties>
  <pipe>
    <provider>
      <resampling maxOversampling="2" enabled="false" zoomedOutResamplingMethod="nearestNeighbour" zoomedInResamplingMethod="nearestNeighbour"/>
    </provider>
    <rasterrenderer classificationMin="-0.5" classificationMax="0.5" type="singlebandpseudocolor" alphaBand="-1" nodataColor="" opacity="1" band="1">
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
        <colorrampshader colorRampType="INTERPOLATED" maximumValue="0.5" classificationMode="1" clip="0" minimumValue="-0.5" labelPrecision="2">
          <colorramp type="gradient" name="[source]">
            <Option type="Map">
              <Option type="QString" value="77,172,38,255,rgb:0.30196078431372547,0.67450980392156867,0.14901960784313725,1" name="color1"/>
              <Option type="QString" value="208,28,139,255,rgb:0.81568627450980391,0.10980392156862745,0.54509803921568623,1" name="color2"/>
              <Option type="QString" value="ccw" name="direction"/>
              <Option type="QString" value="0" name="discrete"/>
              <Option type="QString" value="gradient" name="rampType"/>
              <Option type="QString" value="rgb" name="spec"/>
              <Option type="QString" value="0.25;184,225,134,255,rgb:0.72156862745098038,0.88235294117647056,0.52549019607843139,1;rgb;ccw:0.5;247,247,247,255,rgb:0.96862745098039216,0.96862745098039216,0.96862745098039216,1;rgb;ccw:0.75;241,182,218,255,rgb:0.94509803921568625,0.71372549019607845,0.85490196078431369,1;rgb;ccw" name="stops"/>
            </Option>
          </colorramp>
          <item value="-0.5" label="-0.50 m" color="#4dac26" alpha="255"/>
          <item value="-0.25" label="-0.25 m" color="#b8e186" alpha="255"/>
          <item value="0" label="0.00 m" color="#f7f7f7" alpha="255"/>
          <item value="0.25" label="0.25 m" color="#f1b6da" alpha="255"/>
          <item value="0.5" label="0.50 m" color="#d01c8b" alpha="255"/>
          <rampLegendSettings prefix="" direction="0" orientation="2" suffix="" minimumLabel="" maximumLabel="" useContinuousLegend="1">
            <numericFormat id="basic">
              <Option type="Map">
                <Option type="invalid" name="decimal_separator"/>
                <Option type="int" value="6" name="decimals"/>
                <Option type="int" value="0" name="rounding_type"/>
                <Option type="bool" value="false" name="show_plus"/>
                <Option type="bool" value="true" name="show_thousand_separator"/>
                <Option type="bool" value="false" name="show_trailing_zeros"/>
                <Option type="invalid" name="thousand_separator"/>
              </Option>
            </numericFormat>
          </rampLegendSettings>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast gamma="1" brightness="0" contrast="0"/>
    <huesaturation colorizeRed="255" colorizeOn="0" colorizeBlue="128" saturation="0" invertColors="0" colorizeStrength="100" grayscaleMode="0" colorizeGreen="128"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
