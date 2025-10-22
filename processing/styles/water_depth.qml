<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="Symbology|Symbology3D|Labeling|Fields|Forms|Actions|Diagrams|Rendering|GeometryOptions|Relations|Legend" maxScale="0" autoRefreshMode="Disabled" minScale="1e+08" version="3.40.6-Bratislava" autoRefreshTime="0" hasScaleBasedVisibilityFlag="0">
  <pipe-data-defined-properties>
    <Option type="Map">
      <Option type="QString" name="name" value=""/>
      <Option name="properties"/>
      <Option type="QString" name="type" value="collection"/>
    </Option>
  </pipe-data-defined-properties>
  <pipe>
    <provider>
      <resampling enabled="false" maxOversampling="2" zoomedOutResamplingMethod="nearestNeighbour" zoomedInResamplingMethod="nearestNeighbour"/>
    </provider>
    <rasterrenderer type="singlebandpseudocolor" opacity="1" classificationMax="0.3" alphaBand="-1" classificationMin="0" band="1" nodataColor="">
      <rasterTransparency>
        <singleValuePixelList>
          <pixelListEntry min="0" percentTransparent="100" max="0.01"/>
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
        <colorrampshader clip="0" colorRampType="INTERPOLATED" labelPrecision="4" classificationMode="1" minimumValue="0" maximumValue="0.29999999999999999">
          <colorramp type="gradient" name="[source]">
            <Option type="Map">
              <Option type="QString" name="color1" value="247,251,255,255,rgb:0.96862745098039216,0.98431372549019602,1,1"/>
              <Option type="QString" name="color2" value="8,48,107,255,rgb:0.03137254901960784,0.18823529411764706,0.41960784313725491,1"/>
              <Option type="QString" name="direction" value="ccw"/>
              <Option type="QString" name="discrete" value="0"/>
              <Option type="QString" name="rampType" value="gradient"/>
              <Option type="QString" name="spec" value="rgb"/>
              <Option type="QString" name="stops" value="0.13;222,235,247,255,rgb:0.87058823529411766,0.92156862745098034,0.96862745098039216,1;rgb;ccw:0.26;198,219,239,255,rgb:0.77647058823529413,0.85882352941176465,0.93725490196078431,1;rgb;ccw:0.39;158,202,225,255,rgb:0.61960784313725492,0.792156862745098,0.88235294117647056,1;rgb;ccw:0.52;107,174,214,255,rgb:0.41960784313725491,0.68235294117647061,0.83921568627450982,1;rgb;ccw:0.65;66,146,198,255,rgb:0.25882352941176473,0.5725490196078431,0.77647058823529413,1;rgb;ccw:0.78;33,113,181,255,rgb:0.12941176470588237,0.44313725490196076,0.70980392156862748,1;rgb;ccw:0.9;8,81,156,255,rgb:0.03137254901960784,0.31764705882352939,0.61176470588235299,1;rgb;ccw"/>
            </Option>
          </colorramp>
          <item alpha="255" color="#f7fbff" label="0.0000" value="0"/>
          <item alpha="255" color="#deebf7" label="0.0390" value="0.039"/>
          <item alpha="255" color="#c6dbef" label="0.0780" value="0.078"/>
          <item alpha="255" color="#9ecae1" label="0.1170" value="0.117"/>
          <item alpha="255" color="#6baed6" label="0.1560" value="0.156"/>
          <item alpha="255" color="#4292c6" label="0.1950" value="0.195"/>
          <item alpha="255" color="#2171b5" label="0.2340" value="0.234"/>
          <item alpha="255" color="#08519c" label="0.2700" value="0.27"/>
          <item alpha="255" color="#08306b" label="0.3000" value="0.3"/>
          <rampLegendSettings suffix=" m" orientation="2" direction="0" useContinuousLegend="1" maximumLabel="" minimumLabel="" prefix="">
            <numericFormat id="basic">
              <Option type="Map">
                <Option type="invalid" name="decimal_separator"/>
                <Option type="int" name="decimals" value="6"/>
                <Option type="int" name="rounding_type" value="0"/>
                <Option type="bool" name="show_plus" value="false"/>
                <Option type="bool" name="show_thousand_separator" value="true"/>
                <Option type="bool" name="show_trailing_zeros" value="false"/>
                <Option type="invalid" name="thousand_separator"/>
              </Option>
            </numericFormat>
          </rampLegendSettings>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast contrast="0" gamma="1" brightness="0"/>
    <huesaturation colorizeBlue="128" colorizeRed="255" invertColors="0" colorizeOn="0" saturation="0" colorizeStrength="100" grayscaleMode="0" colorizeGreen="128"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
