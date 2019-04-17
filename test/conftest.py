import os

import pytest

from ThreeDiToolbox.datasource.netcdf_groundwater import NetcdfGroundwaterDataSource


cur_dir = os.path.dirname(__file__)
data_dir = os.path.join(cur_dir, 'data')
simulation_dir = os.path.join(data_dir, 'simulation')

gridadmin_path = os.path.join(simulation_dir, 'gridadmin.h5')
results_3di_path = os.path.join(simulation_dir, 'results_3di.nc')
aggregate_results_3di_path = os.path.join(simulation_dir, 'aggregate_results_3di.nc')


@pytest.fixture()
def netcdf_groundwater_ds():
    return NetcdfGroundwaterDataSource(file_path=results_3di_path)
