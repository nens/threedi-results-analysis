from ThreeDiToolbox.datasource.netcdf_groundwater import NetcdfGroundwaterDataSource

import os
import pytest


current_dir = os.path.dirname(__file__)
data_dir = os.path.join(current_dir, "data")
bergermeer_dir = os.path.join(data_dir, "testmodel", "v2_bergermeer")

gridadmin_path = os.path.join(bergermeer_dir, "gridadmin.h5")
results_3di_path = os.path.join(bergermeer_dir, "results_3di.nc")
aggregate_results_3di_path = os.path.join(bergermeer_dir, "aggregate_results_3di.nc")


@pytest.fixture()
def netcdf_groundwater_ds():
    """Return a instance of NetcdfGroundwaterDataSource

    The instance contains result data of the model 'v2_bergermeer'. It contains
    both results and aggregate result data.
    """
    return NetcdfGroundwaterDataSource(file_path=results_3di_path)
