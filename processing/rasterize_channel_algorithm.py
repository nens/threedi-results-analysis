# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""
from typing import List, Union, Tuple
from uuid import uuid4

import numpy as np
from osgeo import gdal
from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (
    Qgis,
    QgsApplication,
    QgsCoordinateTransform,
    QgsGeometry,
    QgsMesh,
    QgsMeshLayer,
    QgsProcessingMultiStepFeedback,
    QgsFeature,
    QgsFeatureSink,
    QgsFeatureSource,
    QgsField,
    QgsFields,
    QgsPoint,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingFeedback,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
    QgsProcessingUtils,
    QgsProviderRegistry,
    QgsRectangle,
    QgsVectorLayer,
    QgsWkbTypes,
)
import processing
from shapely import __version__ as shapely_version, geos_version

from .rasterize_channel import (
    Channel,
    CrossSectionLocation,
    EmptyOffsetError,
    InvalidOffsetError,
    WidthsNotIncreasingError,
    NoCrossSectionLocationsError,
    fill_wedges, IntersectingSidesError,
)
from .rasterize_channel_utils import merge_rasters


DEBUG_MODE = False


def align_qgs_rectangle(extent: QgsRectangle, xres, yres):
    """round the coordinates of an extent tuple (minx, miny, maxx, maxy) to a multiple of the resolution (pixel size) in
    such a way that the new extent contains the input extent"""
    minx = float(np.trunc(extent.xMinimum() / xres) * xres)
    miny = float(np.trunc(extent.yMinimum() / yres) * yres)
    maxx = float(np.ceil(extent.xMaximum() / xres) * xres)
    maxy = float(np.ceil(extent.yMaximum() / yres) * yres)
    return QgsRectangle(minx, miny, maxx, maxy)


def read_channels(
        channel_features: QgsFeatureSource,
        cross_section_location_features: QgsFeatureSource,
        pixel_size: float,
        feedback: Union[QgsProcessingFeedback, QgsProcessingMultiStepFeedback],
) -> Tuple[List[Channel], List[int]]:
    channels = []
    errors = []
    for i, channel_feature in enumerate(channel_features.getFeatures()):
        if feedback.isCanceled():
            return []
        channel_id = channel_feature.attribute("id")
        feedback.setProgressText(
            f"Reading channel and cross-section data for channel {channel_id}..."
        )
        channel = Channel.from_qgs_feature(channel_feature)
        for cross_section_location_feature in cross_section_location_features.getFeatures():
            if channel_id == cross_section_location_feature.attribute("channel_id"):
                cross_section_location = CrossSectionLocation.from_qgs_feature(
                    cross_section_location_feature,
                    wall_displacement=pixel_size / 4.0,
                    simplify_tolerance=0.01
                )
                channel.add_cross_section_location(cross_section_location)
        channel.geometry = channel.geometry.simplify(pixel_size)
        try:
            if DEBUG_MODE:
                feedback.pushInfo(f"Channel has {len(channel.cross_section_locations)} cross-section locations")
            channels += channel.make_valid()
        except EmptyOffsetError:
            errors.append(channel_id)
            feedback.reportError(
                f"ERROR: Could not read channel with id {channel.id[0]}: no valid parallel offset can be generated "
                f"for some cross-sections. "
            )
        except InvalidOffsetError:
            errors.append(channel_id)
            feedback.reportError(
                f"ERROR: Could not read channel with id {channel.id[0]}: no valid parallel offset can be generated "
                f"for some cross-sections. It may help to split the channel in the middle of its bends."
            )
        except WidthsNotIncreasingError:
            errors.append(channel_id)
            feedback.reportError(
                f"ERROR: Could not read channel with id {channel.id[0]}: the widths in the cross-section table for one "
                f"or more cross-section locations are not all increasing with height."
            )
        except NoCrossSectionLocationsError:
            errors.append(channel_id)
            feedback.reportError(
                f"ERROR: Channel with id {channel.id[0]} has no cross-section locations."
            )
        except Exception as e:
            errors.append(channel_id)
            feedback.reportError(f"ERROR: Channel with id {channel_id} could not be read. Error details: {repr(e)}")
        feedback.setProgress(100 * i / channel_features.featureCount())
    return channels, errors


def rasterize(
        channels: List[Channel],
        pixel_size: float,
        crs,
        errors: List[int],
        warnings: List[int],
        feedback: Union[QgsProcessingFeedback, QgsProcessingMultiStepFeedback],
        context,
        points_sink: QgsFeatureSink = None,
        points_fields: QgsFields = None,
        triangles_sink: QgsFeatureSink = None,
        triangles_fields: QgsFields = None,
        outline_sink: QgsFeatureSink = None,
        outline_fields: QgsFields = None,
) -> Tuple[List[str], int]:

    rasters = []
    total_missing_pixels = 0
    for i, channel in enumerate(channels):
        if feedback.isCanceled():
            return {}
        if channel.id[1] == 0:
            feedback.setProgressText(f"Rasterizing channel {channel.id[0]}...")
        else:
            feedback.setProgressText(
                f"Rasterizing part {channel.id[1] + 1} of channel {channel.id[0]}..."
            )
        points = [QgsPoint(*point.geom.coords[0]) for point in channel.points]
        if DEBUG_MODE:
            for (point_idx, qgs_point) in [
                (point.index, QgsPoint(*point.geom.coords[0])) for point in channel.points
            ]:
                point_feature = QgsFeature()
                point_feature.setFields(points_fields)
                point_feature.setAttribute(0, i)
                point_feature.setAttribute(1, point_idx)
                point_feature.setGeometry(qgs_point)
                points_sink.addFeature(point_feature, QgsFeatureSink.FastInsert)

        # create temporary mesh file
        provider_meta = QgsProviderRegistry.instance().providerMetadata("mdal")
        mesh = QgsMesh()
        temp_mesh_filename = f"{uuid4()}.nc"
        temp_mesh_fullpath = QgsProcessingUtils.generateTempFilename(
            temp_mesh_filename
        )
        mesh_format = "Ugrid"
        provider_meta.createMeshData(mesh=mesh, fileName=temp_mesh_fullpath, driverName=mesh_format, crs=crs)
        mesh_layer = QgsMeshLayer(temp_mesh_fullpath, "editable mesh", "mdal")

        # add points to mesh
        transform = QgsCoordinateTransform()
        mesh_layer.startFrameEditing(transform)
        editor = mesh_layer.meshEditor()
        points_added = editor.addPointsAsVertices(points, 0.0000001)
        if points_added != len(points):
            feedback.pushWarning(
                f"Warning: Added only {points_added} points from a total of {len(points)}!"
            )

        # add faces to mesh
        try:
            triangles_dict = {k: v for k, v in enumerate(channel.triangles)}
            if DEBUG_MODE:
                for triangle_nr, triangle in triangles_dict.items():
                    triangle_feature = QgsFeature()
                    triangle_feature.setFields(triangles_fields)
                    triangle_feature.setAttribute(0, i)
                    triangle_feature.setAttribute(1, triangle_nr)
                    triangle_geometry = QgsGeometry()
                    triangle_geometry.fromWkb(triangle.geometry.wkb)
                    triangle_feature.setGeometry(triangle_geometry)
                    triangles_sink.addFeature(triangle_feature, QgsFeatureSink.FastInsert)
                outline_feature = QgsFeature()
                outline_feature.setFields(outline_fields)
                outline_feature.setAttribute(0, i)
                outline_geometry = QgsGeometry()
                outline_geometry.fromWkb(channel.outline.wkb)
                outline_feature.setGeometry(outline_geometry)
                outline_sink.addFeature(outline_feature, QgsFeatureSink.FastInsert)

            total_triangles = len(triangles_dict)
            faces_added = 0
            occupied_vertices = np.array([], dtype=int)
            finished = False
            processed_triangles = []
            while not finished:
                if feedback.isCanceled():
                    return {}
                finished = True
                for k in processed_triangles:
                    triangles_dict.pop(k)
                processed_triangles = []
                for j, triangle in triangles_dict.items():
                    if (
                        j == 0
                        or np.sum(np.in1d(triangle.vertex_indices, occupied_vertices)) >= 2
                    ):
                        error = editor.addFace(triangle.vertex_indices)
                        # To list error types, run [e for e in Qgis.MeshEditingErrorType]
                        if error.errorType == Qgis.MeshEditingErrorType.NoError:
                            finished = False
                            processed_triangles.append(j)
                            faces_added += 1
                            occupied_vertices = np.append(occupied_vertices, triangle.vertex_indices)
                        elif DEBUG_MODE:
                            feedback.pushInfo(
                                f"Could not (yet) add triangle {j}.\n"
                                f"Error type {str(error.errorType)}.\n"
                                f"Error element index: {error.elementIndex}\n"
                                f"Error point: {[p.geom for p in triangle.points if p.index == error.elementIndex]}\n"
                                f"WKT: {triangle.geometry.wkt}\n"
                                f"Vertex indices: {triangle.vertex_indices}\n"
                                f"Points: {[pnt.geom.wkt for pnt in channel.points if pnt.index in [p.index for p in triangle.points]]}"
                            )

            if faces_added != total_triangles:
                missing_area = np.sum(
                    np.array([tri.geometry.area for tri in triangles_dict.values()])
                )
                if DEBUG_MODE:
                    feedback.pushInfo("Missing triangles:")
                    tri_queries = [f"SELECT ST_GeomFromText('{tri.geometry.wkt}') as geom /*:polygon:28992*/" for tri in
                                   triangles_dict.values()]
                    feedback.pushInfo("\nUNION\n".join(tri_queries))
                if missing_area > (pixel_size**2):
                    warnings.append(channel.id),
                    missing_pixels = int(missing_area / (pixel_size**2))
                    total_missing_pixels += missing_pixels
                    warning_msg = (f"Up to {missing_pixels} pixel(s) may be missing from the raster for "
                                   f"channel {channel.id[0]}")
                    if channel.id[1] > 0:
                        warning_msg += f", part {channel.id[1] + 1}"
                    feedback.pushWarning(f"Warning: {warning_msg}!")

            mesh_layer.commitFrameEditing(transform, continueEditing=False)
            context.temporaryLayerStore().addMapLayer(
                mesh_layer
            )  # otherwise it cannot be used in processing alg

            extent = align_qgs_rectangle(
                mesh_layer.extent(), xres=pixel_size, yres=pixel_size
            )
            rasterize_mesh_params = {
                "INPUT": mesh_layer.id(),
                "DATASET_GROUPS": [0],
                "DATASET_TIME": {"type": "static"},
                "EXTENT": extent,
                "PIXEL_SIZE": pixel_size,
                "CRS_OUTPUT": crs,
                "OUTPUT": "TEMPORARY_OUTPUT",
            }

            # Do not pass feedback to child algorithm to keep the logging clean
            rasterized = processing.run(
                "native:meshrasterize", rasterize_mesh_params, context=context
            )["OUTPUT"]

            crs_auth_id = crs.authid()
            uri = f"polygon?crs={crs_auth_id}"
            clip_extent_layer = QgsVectorLayer(uri, "Clip extent", "memory")
            clip_feature = QgsFeature(QgsFields())
            outline_geometry = QgsGeometry.fromWkt(channel.outline.wkt)
            clip_feature.setGeometry(outline_geometry)
            clip_extent_layer.dataProvider().addFeatures([clip_feature])

            clip_parameters = {
                "INPUT": rasterized,
                "MASK": clip_extent_layer,
                "SOURCE_CRS": None,
                "TARGET_CRS": None,
                "NODATA": -9999,
                "ALPHA_BAND": False,
                "CROP_TO_CUTLINE": False,
                "KEEP_RESOLUTION": True,
                "SET_RESOLUTION": False,
                "X_RESOLUTION": None,
                "Y_RESOLUTION": None,
                "MULTITHREADING": False,
                "OPTIONS": "COMPRESS=DEFLATE|PREDICTOR=2|ZLEVEL=9",
                "DATA_TYPE": 6,  # Float32
                "OUTPUT": "TEMPORARY_OUTPUT",
            }

            # use QgsProcessingAlgorithm.run() instead of processing.run() to be able to hide feedback but still be
            # able to check if algorithm ran succesfully (ok == True)
            reg = QgsApplication.processingRegistry()
            alg_cliprasterbymasklayer = reg.algorithmById(
                "gdal:cliprasterbymasklayer"
            )
            results, ok = alg_cliprasterbymasklayer.run(
                clip_parameters, context=context, feedback=QgsProcessingFeedback()
            )
            if not ok:
                feedback.reportError(
                    f"Error when clipping channel raster by outline for channel {channel.id}",
                    fatalError=False,
                )
                continue
            rasters.append(results["OUTPUT"])

        except IntersectingSidesError as e:
            errors.append(channel.id)
            feedback.reportError(
                f"Error: could not rasterize channel {channel.id} (IntersectingSidesError)",
                fatalError=False
            )
            feedback.reportError(
                str(e)
            )
        except Exception as e:
            errors.append(channel.id)
            feedback.reportError(
                f"ERROR: Channel with id {channel.id} could not be rasterized. Error details: {repr(e)}"
            )

        feedback.setProgress(100 * i / len(channels))
    return rasters, total_missing_pixels


class RasterizeChannelsAlgorithm(QgsProcessingAlgorithm):
    """
    Rasterize channels using its cross-sections
    """

    INPUT_CHANNELS = "INPUT_CHANNELS"
    INPUT_CROSS_SECTION_LOCATIONS = "INPUT_CROSS_SECTION_LOCATIONS"
    INPUT_DEM = "INPUT_DEM"
    INPUT_PIXEL_SIZE = "PIXEL_SIZE"

    OUTPUT = "OUTPUT"

    if DEBUG_MODE:
        TRIANGLE_OUTPUT = "TRIANGLE_OUTPUT"
        OUTLINE_OUTPUT = "OUTLINE_OUTPUT"
        POINTS_OUTPUT = "POINTS_OUTPUT"

    def initAlgorithm(self, config):

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_CHANNELS, self.tr("Channels"), [QgsProcessing.TypeVectorLine]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_CROSS_SECTION_LOCATIONS,
                self.tr("Cross-section locations"),
                [QgsProcessing.TypeVectorPoint],
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_DEM, self.tr("Digital Elevation Model"), optional=True
            )
        )

        pixel_size_param = QgsProcessingParameterNumber(
            self.INPUT_PIXEL_SIZE,
            self.tr("Pixel size"),
            type=QgsProcessingParameterNumber.Double,
            optional=True,
        )
        pixel_size_param.setMetadata({"widget_wrapper": {"decimals": 2}})
        self.addParameter(pixel_size_param)

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT,
                self.tr("Rasterized channels"),
            )
        )

        if DEBUG_MODE:
            self.addParameter(
                QgsProcessingParameterFeatureSink(
                    self.TRIANGLE_OUTPUT,
                    self.tr('Triangle output')
                )
            )

            self.addParameter(
                QgsProcessingParameterFeatureSink(
                    self.OUTLINE_OUTPUT,
                    self.tr('Outline output')
                )
            )

            self.addParameter(
                QgsProcessingParameterFeatureSink(
                    self.POINTS_OUTPUT,
                    self.tr('Points output')
                )
            )

    def processAlgorithm(self, parameters, context, feedback):
        if int(shapely_version.split(".")[0]) < 2:
            feedback.reportError(
                f"Required Shapely version >= 2.0.0. Installed Shapely version: {shapely_version}",
                fatalError=True
            )
        if not (geos_version[0] > 3 or (geos_version[0] == 3 and geos_version[1] >= 12)):
            feedback.reportError(
                f"Required GEOS version >= 3.12.0. Installed GEOS version: {'.'.join(geos_version)}. "
                f"Please use QGIS 3.28.13 or higher, which is shipped with the correct GEOS version.",
                fatalError=True
            )
        channel_features = self.parameterAsSource(
            parameters, self.INPUT_CHANNELS, context
        )
        cross_section_location_features = self.parameterAsSource(
            parameters, self.INPUT_CROSS_SECTION_LOCATIONS, context
        )

        output_raster = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)

        if DEBUG_MODE:

            outline_fields = QgsFields()
            outline_fields.append(
                QgsField(
                    name="channel_nr",
                    type=QVariant.Int
                )
            )
            (outline_sink, outline_dest_id) = self.parameterAsSink(
                parameters,
                self.OUTLINE_OUTPUT,
                context,
                outline_fields,
                QgsWkbTypes.PolygonZ,
                cross_section_location_features.sourceCrs()
            )

            triangles_fields = QgsFields()
            triangles_fields.append(
                QgsField(
                    name="channel_nr",
                    type=QVariant.Int
                )
            )
            triangles_fields.append(
                QgsField(
                    name="triangle_nr",
                    type=QVariant.Int
                )
            )
            (triangles_sink, triangles_dest_id) = self.parameterAsSink(
                parameters,
                self.TRIANGLE_OUTPUT,
                context,
                triangles_fields,
                QgsWkbTypes.PolygonZ,
                cross_section_location_features.sourceCrs()
            )

            points_fields = QgsFields()
            points_fields.append(
                QgsField(
                    name="channel_nr",
                    type=QVariant.Int
                )
            )
            points_fields.append(
                QgsField(
                    name="index",
                    type=QVariant.Int
                )
            )
            (points_sink, points_dest_id) = self.parameterAsSink(
                parameters,
                self.POINTS_OUTPUT,
                context,
                points_fields,
                QgsWkbTypes.PointZ,
                cross_section_location_features.sourceCrs()
            )

        dem = self.parameterAsRasterLayer(parameters, self.INPUT_DEM, context)
        user_pixel_size = self.parameterAsDouble(
            parameters, self.INPUT_PIXEL_SIZE, context
        )
        if dem:
            if np.abs(dem.rasterUnitsPerPixelX() - dem.rasterUnitsPerPixelY()) > 0.0001:  # 1/10 mm tolerance
                feedback.reportError(
                    f"Input Digital Elevation Model has different X and Y resolutions. "
                    f"X resolution: {dem.rasterUnitsPerPixelX()}"
                    f"Y resolution: {dem.rasterUnitsPerPixelY()}",
                    fatalError=True,
                )
                raise QgsProcessingException()
            pixel_size = dem.rasterUnitsPerPixelX()
            feedback.pushInfo("Using pixel size from input Digital Elevation Model")
        elif user_pixel_size:
            pixel_size = user_pixel_size
        else:
            feedback.reportError(
                "Either 'Digital Elevation Model' or 'Pixel size' has to be specified", fatalError=True
            )
            raise QgsProcessingException()

        feedback.pushInfo("Step 1/4: Read channel and cross-section data")

        channels, errors = read_channels(
            channel_features=channel_features,
            cross_section_location_features=cross_section_location_features,
            pixel_size=pixel_size,
            feedback=feedback
        )
        if feedback.isCanceled():
            return {}

        fill_wedges(channels, feedback=feedback)
        if feedback.isCanceled():
            return {}

        if len(channels) == 0:
            feedback.reportError(
                "No valid channels to process", fatalError=True
            )
            raise QgsProcessingException()

        feedback.pushInfo("Step 2/4: Rasterize channels")
        warnings = []
        rasters, total_missing_pixels = rasterize(
            channels=channels,
            pixel_size=pixel_size,
            crs=channel_features.sourceCrs(),
            errors=errors,
            warnings=warnings,
            feedback=feedback,
            context=context,
            points_sink=points_sink if DEBUG_MODE else None,
            points_fields=points_fields if DEBUG_MODE else None,
            triangles_sink=triangles_sink if DEBUG_MODE else None,
            triangles_fields=triangles_fields if DEBUG_MODE else None,
            outline_sink=outline_sink if DEBUG_MODE else None,
            outline_fields=outline_fields if DEBUG_MODE else None,
        )
        feedback.setProgressText("Step 3/4: Merge rasters...")
        if len(rasters) == 0:
            feedback.reportError(
                "No valid channels to process", fatalError=True
            )
            raise QgsProcessingException()
        rasters_datasets = [gdal.Open(raster) for raster in rasters]
        if dem:
            uri = dem.dataProvider().dataSourceUri()
            dem_gdal_datasource = gdal.Open(uri)
            rasters_datasets.append(dem_gdal_datasource)
        merge_rasters(
            rasters_datasets,
            tile_size=1000,
            aggregation_method="min",
            output_filename=output_raster,
            output_nodatavalue=-9999,
            output_pixel_size=pixel_size,
            feedback=feedback,
        )

        if errors:
            feedback.pushWarning(
                f"Warning: The following channels where not rasterized: {', '.join([str(i) for i in errors])}. "
                f"See previous log messages for more information."
            )

        if warnings:
            feedback.pushWarning(
                f"Warning: The following channels may have missing pixels: {', '.join([str(i) for i in warnings])}. "
                f"In total, up to {total_missing_pixels} pixels may be missing. See previous log messages for more "
                f"information."
            )

        return {self.OUTPUT: output_raster}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "rasterize_channels"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Rasterize channels")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "Conversion 1D-2D"

    def shortHelpString(self):
        return self.tr(
            """
            <h3>Please note</h3>
            <ul>
            <li>Please run the 3Di Check Schematisation algorithm and resolve any issues relating to channels or cross-section locations before running this algorithm</li>
            <li>Use the <em>3Di Schematisation Editor &gt; Load from spatialite</em> to create the required input layers for the algorithm.</li>
            <li>Some channels cannot be (fully) rasterized, e.g. wide cross-section definitions on channels with sharp bends may lead to self-intersection of the described cross-section</li>
            <li>Tabulated trapezium, Tabulated rectangle, and YZ cross-sections are supported, as long as they always become wider when going up (vertical segments are allowed).</li>
            <li>Other cross-section shapes are not supported</li>
            </ul>
            <h3>Parameters</h3>
            <h4>Channels</h4>
            <p>Channel layer as generated by the 3Di Schematisation Editor. You may limit processing to a selection of the input features.</p>
            <h4>Cross-section locations</h4>
            <p>Cross-section location layer as generated by the 3Di Schematisation Editor. You may limit processing to a selection of the input features. This may be useful if the channel has one or several cross-section locations with non-tabulated cross-section shapes.</p>
            <h4>Digital elevation model</h4>
            <p>Optional input. If used, the pixel size will be taken from the DEM. The rasterized channels will be carved into the DEM using a 'deepen-only' approach: pixel values will only be changed where the rasterized channels are lower than the DEM. This is evaluated pixel by pixel.</p>
            <p>If not used, <em>Pixel size&nbsp;</em>has to be filled in.</p>
            <h4>Pixel size</h4>
            <p>Optional input. If&nbsp;<em>Digital elevation model</em> is not specified, specify the pixel size of the output raster.</p>
            <h4>Rasterized channels</h4>
            <p>Output file location. A temporary output can also be chosen - note that in that case, the file will be deleted when closing the project.</p>
            """
        )

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return RasterizeChannelsAlgorithm()
