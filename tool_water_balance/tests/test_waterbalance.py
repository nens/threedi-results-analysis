from pathlib import Path
from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsCoordinateTransform
from qgis.core import QgsGeometry
from qgis.core import QgsPointXY
from qgis.core import QgsProject
from ThreeDiToolbox.tests.test_init import TEST_DATA_DIR
from ThreeDiToolbox.tool_result_selection.models import TimeseriesDatasourceModel
from ThreeDiToolbox.tool_water_balance.tools.waterbalance import WaterBalanceCalculation

import mock
import unittest


testmodel_dir = TEST_DATA_DIR.joinpath("testmodel", "v2_bergermeer")


def get_wb_polygon():
    POINTS_IN_WGS84 = True
    polygon_points = [
        QgsPointXY(4.70635793604164299, 52.64214387449186461),
        QgsPointXY(4.70644905107772882, 52.64329192394655621),
        QgsPointXY(4.70765176955406783, 52.64332836996099019),
        QgsPointXY(4.70806178721645541, 52.6419889789305202),
        QgsPointXY(4.70725997489889636, 52.64173385682948236),
        QgsPointXY(4.70635793604164299, 52.64214387449186461),
    ]
    polygon = QgsGeometry.fromPolygonXY([polygon_points])
    if not POINTS_IN_WGS84:
        tr = QgsCoordinateTransform(
            QgsCoordinateReferenceSystem(
                28992, QgsCoordinateReferenceSystem.PostgisCrsId
            ),
            QgsCoordinateReferenceSystem(
                4326, QgsCoordinateReferenceSystem.PostgisCrsId
            ),
            QgsProject.instance(),
        )
        polygon.transform(tr)
    return polygon


class WaterbalanceClassTest(unittest.TestCase):
    """Test the QGIS Environment"""

    def setUp(self):
        assert Path.is_dir(testmodel_dir), 'testmodel dir not found'
        self.ts_datasources = TimeseriesDatasourceModel()
        self.ts_datasources.spatialite_filepath = testmodel_dir / "v2_bergermeer.sqlite"
        assert Path.is_file(self.ts_datasources.spatialite_filepath), 'spatialite not found'
        items = [
            {
                "type": "netcdf-groundwater",
                "name": "results_3di",
                "file_path": str(testmodel_dir / "results_3di.nc")
            }
        ]
        self.ts_datasources.insertRows(items)
        self.polygon = get_wb_polygon()
        assert self.polygon.isGeosValid(), 'get_wb_polygon produces an invalid polygon'

    @mock.patch(
        "ThreeDiToolbox.tool_result_selection.models.StatusProgressBar")
    def test_get_incoming_and_outcoming_link_ids(self, progress_bar_mock):
        """We mock StatusProgressBar which is not refered from
        'utils.user_messages.StatusProgressBar', but from
        .tool_result_selection.models.StatusProgressBar' """
        calc = WaterBalanceCalculation(self.ts_datasources)
        links = calc.get_incoming_and_outcoming_link_ids(self.polygon, None)
        # TODO: find out why no link ids are found..
        self.assertListEqual(links["2d_in"], [2253, 2254, 2255, 2256, 9610])
        self.assertListEqual(links["2d_out"], [2265, 2266, 2267, 2268, 12861])

    @mock.patch(
        "ThreeDiToolbox.tool_result_selection.models.StatusProgressBar")
    def test_get_nodes(self, progress_bar_mock):
        calc = WaterBalanceCalculation(self.ts_datasources)
        nodes = calc.get_nodes(self.polygon, None)
        # TODO: find out why no link ids are found..
        self.assertListEqual(nodes["2d_in"], [2253, 2254, 2255, 2256, 9610])
        self.assertListEqual(nodes["2d_out"], [2265, 2266, 2267, 2268, 12861])

    @mock.patch(
        "ThreeDiToolbox.tool_result_selection.models.StatusProgressBar")
    def test_get_aggregated_flows(self, progress_bar_mock):
        calc = WaterBalanceCalculation(self.ts_datasources)
        aggregated_flows = calc.get_aggregated_flows(self.polygon, None)
        # TODO: find out why no link ids are found..
        self.assertListEqual(aggregated_flows["2d_in"], [2253, 2254, 2255, 2256, 9610])
        self.assertListEqual(aggregated_flows["2d_out"], [2265, 2266, 2267, 2268, 12861])

