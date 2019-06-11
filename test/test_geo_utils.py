"""
Test geo utils.
"""
from ThreeDiToolbox.test.utilities import ensure_qgis_app_is_initialized
from ThreeDiToolbox.utils.geo_utils import get_coord_transformation_instance


def test_it_can_get_coord_transformation_instance():
    ensure_qgis_app_is_initialized()
    src_epsg, dest_epsg = 4326, 28992
    inst = get_coord_transformation_instance(src_epsg, dest_epsg)
    assert (str(inst.__class__) is "<class 'qgis._core.QgsCoordinateTransform'>")
    assert (inst.destinationCrs().isValid())
    assert (inst.sourceCrs().isValid())
    assert (inst.destinationCrs().authid() == "EPSG:28992")
    src_epsg, dest_epsg = 28992, 4326
    inst_rev = get_coord_transformation_instance(src_epsg, dest_epsg)
    assert (inst_rev.destinationCrs().authid() == "EPSG:4326")
