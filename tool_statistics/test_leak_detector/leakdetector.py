from pathlib import Path

from osgeo import gdal
from threedigrid.admin.gridadmin import GridH5Admin

from leak_detector import LeakDetector

DATA_DIR = Path(__file__).parent / 'data'
DEM_FILENAME = DATA_DIR / 'dem_0_01.tif'
DEM_DATASOURCE = gdal.Open(str(DEM_FILENAME), gdal.GA_ReadOnly)
GRIDADMIN_FILENAME = DATA_DIR / 'gridadmin.h5'
GR = GridH5Admin(GRIDADMIN_FILENAME)
MIN_PEAK_PROMINENCE = 0.05
SEARCH_PRECISION = 0.001
MIN_OBSTACLE_HEIGHT = 0.05


def run():
    leak_detector = LeakDetector(
        gridadmin=GR,
        dem=DEM_DATASOURCE,
        cell_ids=list(GR.cells.id),
        # cell_ids=[42, 43],
        min_obstacle_height=MIN_OBSTACLE_HEIGHT,
        search_precision=SEARCH_PRECISION,
        min_peak_prominence=MIN_PEAK_PROMINENCE
    )
    leak_detector.run()
    for result in leak_detector.result_edges():
        print(result)


if __name__ == "__main__":
    run()
