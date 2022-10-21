from qgis.core import Qgis, QgsVectorLayer, QgsProject, QgsCoordinateReferenceSystem
from qgis.utils import iface

from osgeo import ogr

from threedigrid.admin.exporters.geopackage import GeopackageExporter

from ThreeDiToolbox.utils.user_messages import StatusProgressBar, pop_up_critical


def add_layers_from_gpkg(path) -> bool:
    """Retrieves layers from gpk and add to project.

    Checks whether all layers contain the same CRS, if
    so, sets this CRS on the project
    """

    gpkg_layers = [lr.GetName() for lr in ogr.Open(str(path))]
    srs_ids = set()
    for layer in gpkg_layers:

        # Using the QgsInterface function addVectorLayer shows (annoying) confirmation dialogs
        # iface.addVectorLayer(gpkg_file + "|layername=" + layer, layer, 'ogr')
        vector_layer = QgsVectorLayer(str(path) + "|layername=" + layer, layer, "ogr")
        if not vector_layer.isValid():
            return False

        # TODO: styling?

        layer_srs_id = vector_layer.crs().srsid()
        srs_ids.add(layer_srs_id)

        QgsProject.instance().addMapLayer(vector_layer)

    if len(srs_ids) == 1:
        srs_id = srs_ids.pop()
        crs = QgsCoordinateReferenceSystem.fromSrsId(srs_id)
        if crs.isValid():
            QgsProject.instance().setCrs(crs)
            iface.messageBar().pushMessage(
                "GeoPackage",
                "Setting project CRS according to the source geopackage",
                Qgis.Info,
            )
        else:
            iface.messageBar().pushMessage(
                "GeoPackage",
                "Skipping setting project CRS - does gridadmin file contains a valid SRS?",
                Qgis.Warning,
            )
            return False
    else:
        iface.messageBar().pushMessage(
            "GeoPackage",
            f"Skipping setting project CRS - the source file {str(path)} SRS codes are inconsistent.",
            Qgis.Warning,
        )
        return False

    return True


def import_grid_item(threedi_grid_item):
    path_h5 = threedi_grid_item.path
    path_gpkg = path_h5.with_suffix(".gpkg")

    progress_bar = StatusProgressBar(100, "Generating geopackage")
    exporter = GeopackageExporter(str(path_h5), str(path_gpkg))
    exporter.export(
        lambda count, total, pb=progress_bar: pb.set_value((count * 100) // total)
    )
    del progress_bar

    iface.messageBar().pushMessage("GeoPackage", "Generated geopackage", Qgis.Info)

    if not add_layers_from_gpkg(path_gpkg):
        pop_up_critical("Failed adding the layers to the project.")
        return False

    iface.messageBar().pushMessage(
        "GeoPackage", "Added layers to the project", Qgis.Info
    )

    return True
