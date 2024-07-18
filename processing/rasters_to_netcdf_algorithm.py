from typing import List

from threedi_results_analysis.processing.deps.rasters_to_netcdf import rasters_to_netcdf
from qgis.core import (
    QgsMapLayer,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingContext,
    QgsProcessingParameterDateTime,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsRasterLayer,
)


class RastersToNetCDFAlgorithm(QgsProcessingAlgorithm):
    """
    Base algorithm for 'Detect leaking obstacles' algorithms, not to be exposed to users
    """

    INPUT_RASTERS = "INPUT_RASTERS"
    INPUT_START_TIME = "INPUT_START_TIME"
    INPUT_INTERVAL = "INPUT_INTERVAL"
    INPUT_UNITS = "INPUT_UNITS"
    INPUT_OUTPUT_PATH = "INPUT_OUTPUT_PATH"
    INPUT_OFFSET = "INPUT_OFFSET"

    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                name=self.INPUT_RASTERS,
                description="Input rasters",
                layerType=QgsProcessing.TypeRaster,
            )
        )

        self.addParameter(
            QgsProcessingParameterDateTime(
                name=self.INPUT_START_TIME,
                description="Start",
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.INPUT_INTERVAL,
                description="Interval [s]",
                type=QgsProcessingParameterNumber.Integer
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.INPUT_OFFSET,
                description="Offset [s]",
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                name=self.INPUT_UNITS,
                description="Units",
                options=["mm", "m/s", "mm/h", "mm/hr"]
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                name=self.INPUT_OUTPUT_PATH,
                description="Output file",
                fileFilter=".nc"
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        input_raster_layers: List[QgsMapLayer] = self.parameterAsLayerList(parameters, self.INPUT_RASTERS, context)
        rasters = [layer.dataProvider().dataSourceUri() for layer in input_raster_layers]
        start_datetime = self.parameterAsDateTime(parameters, self.INPUT_START_TIME, context) \
            .toPyDateTime() \
            .replace(second=0, microsecond=0)
        interval = self.parameterAsInt(parameters, self.INPUT_INTERVAL, context)
        offset = self.parameterAsInt(parameters, self.INPUT_OFFSET, context)
        units = self.parameterAsEnumString(parameters, self.INPUT_UNITS, context)
        output_path = self.parameterAsFile(parameters, self.INPUT_OUTPUT_PATH, context)
        rasters_to_netcdf(
            rasters=rasters,
            start_time=start_datetime,
            interval=interval,
            units=units,
            output_path=output_path,
            offset=offset
        )

        layer = QgsRasterLayer(output_path, "Spatiotemporal NetCDF")
        context.temporaryLayerStore().addMapLayer(layer)
        layer_details = QgsProcessingContext.LayerDetails(
            "Spatiotemporal NetCDF",
            context.project(),
            self.OUTPUT
        )
        context.addLayerToLoadOnCompletion(
            layer.id(),
            layer_details
        )

        return {
            self.OUTPUT: output_path,
        }

    def group(self):
        return "Pre-process simulation inputs"

    def groupId(self):
        return "pre_process_sim_inputs"

    def shortHelpString(self):
        return """
                <h3>Introduction</h3>
                <p>The elevation at which flow between 2D cells is possible (the 'exchange level'), depends on the elevation of the pixels directly adjacent to the cell edge. Obstacles in the DEM that do not cover the entire edge will therefore not stop the flow, i.e. water 'leaks' through the obstacle. This is more likely to occur if obstacles are diagonal and/or narrow compared to the computational grid size.</p>
                <p>This processing algorithm detects such cases. Please inspect the locations where the algorithm identifies leaking obstacles and add grid refinement and/or obstacles to the schematisation to solve the issue if needed.</p>
                <h3>Parameters</h3>
                <h4>Gridadmin file</h4>
                <p>HDF5-file (*.h5) containing a 3Di computational grid. Note that gridadmin files generated on the server contain exchange levels for 2D flowlines, whereas locally generated gridadmin files do not. In the latter case, the processing algorithm will analyse the DEM to obtain these values.</p>
                <h4>Digital elevation model</h4>
                <p>Raster of the schematisation's digital elevation model (DEM).</p>
                <h4>Linear obstacles</h4>
                <p>Obstacles in this layer will be used to update cell edge exchange levels, <i>in addition to</i> any obstacles already present in the gridadmin file (i.e. in files that were downloaded from the server). This input must be a vector layer with line geometry and a <i>crest_level</i> field</p>
                <h4>Flowlines</h4>
                <p>Can be used to limit the analysis to a specific part of the computational grid. For example, select flowlines that have a total discharge of > 10 m<sup>3</sup></p>
                <h4>Minimum obstacle height (m)</h4>
                <p>Only obstacles with a crest level that is significantly higher than the exchange level will be identified. 'Significantly higher' is defined as <em>crest level &gt; exchange level + minimum obstacle height</em>.</p>
                <h4>Vertical search precision (m)</h4>
                <p>The crest level of the identified obstacle will always be within <em>vertical search precision</em> of the actual crest level. A smaller value will yield more precise results; a higher value will make the algorithm faster to execute.</p>
                <h3>Outputs</h3>
                <h4>Obstacle in DEM&nbsp;</h4>
                <p>Approximate location of the obstacle in the DEM. Its geometry is a straight line between the highest pixels of the obstacle on the cell edges. Attributes:</p>
                <ul>
                <li> id: id of the flowline this obstacle affects. If more than one flowline is affected, the flowline with the lowest exchange level is used. </li>
                <li> crest_level: lowest elevation at which water can flow over the obstacle </li>
                <li> exchange_level: lowest exchange level of the cell edge(s) that this obstacle applies to </li>
                </ul>
                <p>The styling is shows the difference between the crest level and the exchange level</p>
                <h4>Obstacle on cell edge</h4>
                <p>Suggested obstacle to add to the schematisation. In most cases, it is recommended solve any leaking obstacle issues with grid refinement, and only add obstacles if this does not solve the issue.</p>
                <p>The styling shows the difference between the crest level and the exchange level</p>
            """

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm
        """
        return "rasters_to_netcdf"

    def displayName(self):
        """
        Returns the algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return "Rasters to spatiotemporal NetCDF"

    def createInstance(self):
        return RastersToNetCDFAlgorithm()
