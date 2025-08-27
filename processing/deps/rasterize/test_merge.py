from pathlib import Path
from osgeo import gdal
from merge import merge_rasters

gdal.UseExceptions()

TEST_DATA_DIR = Path(__file__).parent


def test_merge_rasters():
    rasters = [gdal.Open(str(TEST_DATA_DIR / f"raster{i}.tif")) for i in range(1, 5)]
    output_filename = TEST_DATA_DIR / "merged.tif"
    merge_rasters(
        rasters,
        tile_size=50,
        aggregation_method="min",
        output_filename=output_filename,
        output_nodatavalue=-9999,
    )
