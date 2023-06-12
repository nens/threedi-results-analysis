from pathlib import Path

import numpy as np
from osgeo import gdal
from threedigrid.admin.gridadmin import GridH5Admin
from threedi_results_analysis.processing.deps.discharge.leak_detector import LeakDetector, TOP, BOTTOM, LEFT, RIGHT

DATA_DIR = Path(__file__).parent / 'data'
DEM_FILENAME = DATA_DIR / 'dem_0_01.tif'
DEM_DATASOURCE = gdal.Open(str(DEM_FILENAME), gdal.GA_ReadOnly)
GRIDADMIN_FILENAME = DATA_DIR / 'gridadmin.h5'
GR = GridH5Admin(GRIDADMIN_FILENAME)
MIN_PEAK_PROMINENCE = 0.05
SEARCH_PRECISION = 0.001
MIN_OBSTACLE_HEIGHT = 0.05


def test_neigh_cells():
    cell_ids = [204]
    leak_detector = LeakDetector(
        gridadmin=GR,
        dem=DEM_DATASOURCE,
        cell_ids=cell_ids,
        min_obstacle_height=MIN_OBSTACLE_HEIGHT,
        search_precision=SEARCH_PRECISION,
        min_peak_prominence=MIN_PEAK_PROMINENCE
    )
    cell = leak_detector.cell(204)
    assert cell.neigh_cells[RIGHT][0].id == 220
    assert cell.neigh_cells[TOP][0].id == 205


def test_edge_pixels():
    cell_ids = [156, 157, 158, 159]
    leak_detector = LeakDetector(
        gridadmin=GR,
        dem=DEM_DATASOURCE,
        cell_ids=cell_ids,
        min_obstacle_height=MIN_OBSTACLE_HEIGHT,
        search_precision=SEARCH_PRECISION,
        min_peak_prominence=MIN_PEAK_PROMINENCE
    )

    cell = leak_detector.cell(156)
    assert np.all(
        cell.edge_pixels(TOP) == np.array(
            [
                0, 0, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0.
            ]
        )
    )
    assert np.all(
        cell.edge_pixels(RIGHT) == np.array(
            [
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 0,
                0, 0, 0, 0, 0.
            ]
        )
    )

    cell = leak_detector.cell(158)
    assert np.all(
        cell.edge_pixels(BOTTOM) == np.array(
            [
                0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.
            ]
        )
    )

    cell = leak_detector.cell(159)
    assert np.all(
        cell.edge_pixels(LEFT) == np.array(
            [
                0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.
            ]
        )
    )


def test_side_indices():
    # TODO add tests here
    pass


def test_maxima():
    cell_ids = [156, 157, 158, 159]
    leak_detector = LeakDetector(
        gridadmin=GR,
        dem=DEM_DATASOURCE,
        cell_ids=cell_ids,
        min_obstacle_height=MIN_OBSTACLE_HEIGHT,
        search_precision=SEARCH_PRECISION,
        min_peak_prominence=MIN_PEAK_PROMINENCE
    )

    cell = leak_detector.cell(156)
    assert np.all(cell.maxima(TOP) == np.array([[0, 4]]))
    assert np.all(cell.maxima(RIGHT) == np.array([[28, 39]]))

    cell = leak_detector.cell(158)
    assert np.all(cell.maxima(BOTTOM) == np.array([[39, 7]]))

    cell = leak_detector.cell(159)
    assert np.all(cell.maxima(LEFT) == np.array([[2, 0]]))
