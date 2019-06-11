"""
Test geo utils.
"""
from ThreeDiToolbox.test.utilities import ensure_qgis_app_is_initialized
from ThreeDiToolbox.utils.geo_utils import get_coord_transformation_instance


def test_it_can_get_coord_transformation_instance(self):
    ensure_qgis_app_is_initialized()
    src_epsg, dest_epsg = 4326, 28992
    inst = get_coord_transformation_instance(src_epsg, dest_epsg)
    self.assertEqual(str(inst.__class__), "<class 'qgis._core.QgsCoordinateTransform'>")
    self.assertTrue(inst.destinationCrs().isValid())
    self.assertTrue(inst.sourceCrs().isValid())
    self.assertEqual(inst.destinationCrs().authid(), "EPSG:28992")
    src_epsg, dest_epsg = 28992, 4326
    inst_rev = get_coord_transformation_instance(src_epsg, dest_epsg)
    self.assertEqual(inst_rev.destinationCrs().authid(), "EPSG:4326")
