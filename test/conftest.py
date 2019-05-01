import os

import pytest

from ThreeDiToolbox.datasource.netcdf_groundwater import NetcdfGroundwaterDataSource
from ThreeDiToolbox.utils.patched_threedigrid import (
    GridH5ResultAdmin,
    GridH5AggregateResultAdmin,
)


cur_dir = os.path.dirname(__file__)
data_dir = os.path.join(cur_dir, "data")
bergermeer_dir = os.path.join(data_dir, "testmodel", "v2_bergermeer")

gridadmin_path = os.path.join(bergermeer_dir, "gridadmin.h5")
results_3di_path = os.path.join(bergermeer_dir, "results_3di.nc")
aggregate_results_3di_path = os.path.join(bergermeer_dir, "aggregate_results_3di.nc")


@pytest.fixture()
def netcdf_groundwater_ds():
    return NetcdfGroundwaterDataSource(file_path=results_3di_path)


@pytest.fixture()
def grid_result():
    return GridH5ResultAdmin(gridadmin_path, results_3di_path)


def grid_aggr_result():
    return GridH5AggregateResultAdmin(gridadmin_path, aggregate_results_3di_path)
