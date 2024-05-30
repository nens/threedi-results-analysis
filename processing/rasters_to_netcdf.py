from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Union

import numpy as np
import netCDF4
from osgeo import gdal, osr
from pyproj import CRS

gdal.UseExceptions()
osr.UseExceptions()


def get_datasets(filepaths: List[Union[str, Path]]) -> List[gdal.Dataset]:
    result = list()
    for filepath in filepaths:
        dataset = gdal.Open(str(filepath))
        if not dataset:
            raise Exception(f"Unable to open {filepath}")
        result.append(dataset)
    return result


def get_srs(dataset: gdal.Dataset) -> osr.SpatialReference:
    projection = dataset.GetProjection()
    srs = osr.SpatialReference()
    srs.ImportFromWkt(projection)
    return srs


def rasters_have_same_srs(datasets: List[gdal.Dataset]) -> bool:
    if not datasets:
        raise ValueError("The filepaths list is empty.")

    base_crs = get_srs(datasets[0])

    for dataset in datasets[1:]:
        current_crs = get_srs(dataset)
        if not base_crs.IsSame(current_crs):
            return False
    return True


def rasters_have_same_geotransform(datasets: List[gdal.Dataset]) -> bool:
    if not datasets:
        raise ValueError("The filepaths list is empty.")

    base_geotransform = datasets[0].GetGeoTransform()

    for dataset in datasets[1:]:
        current_geotransform = dataset.GetGeoTransform()
        if base_geotransform != current_geotransform:
            return False
    return True


def rasters_have_same_dimensions(datasets: List[gdal.Dataset]):
    if not datasets:
        raise ValueError("The filepaths list is empty.")

    base_dimensions = datasets[0].RasterXSize, datasets[0].RasterYSize

    for dataset in datasets[1:]:
        current_dimensions = dataset.RasterXSize, dataset.RasterYSize
        if base_dimensions != current_dimensions:
            return False
    return True


def rasters_to_netcdf(
        rasters: List[Union[str, Path]],
        start_time: datetime,
        interval: int,
        output_path: Union[str, Path]
):
    """
    :param interval: interval in seconds
    Assumption:
        - all asc files have the same extent and pixel size
        - rainfall values are in mm per interval
    """
    datasets = get_datasets(rasters)
    assert rasters_have_same_srs(datasets), "Not all input rasters have the same Spatial Reference System"
    assert rasters_have_same_geotransform(datasets), "Not all input rasters have the same origin, pixel size, and skew"
    assert rasters_have_same_dimensions(datasets), "Not all input rasters have the same width and height"

    # create netcdf
    output_dataset = netCDF4.Dataset(
        filename=str(output_path),
        mode='w',
        format="NETCDF4"
    )

    # set dimensions
    output_dataset.createDimension(dimname='lon', size=datasets[0].RasterXSize)
    output_dataset.createDimension(dimname='lat', size=datasets[0].RasterYSize)
    output_dataset.createDimension(dimname='time', size=len(filepaths))

    # myvar = output_dataset.createVariable('myvar', 'float32', ('time', 'lat', 'lon'))
    # myvar.setncattr('units', 'mm')
    # myvar[:] = dataout

    # x and y or lon and lat
    srs = get_srs(datasets[0])
    crs = CRS.from_wkt(srs.ExportToWkt())
    geotransform = datasets[0].GetGeoTransform()
    x_attrs, y_attrs = crs.cs_to_cf()

    max_x_ordinate = geotransform[0] + datasets[0].RasterXSize * geotransform[1]
    x_ordinates = np.arange(
        start=geotransform[0],
        stop=max_x_ordinate - 0.5 * geotransform[1],  # to prevent unexpected behaviour due to rounding differences
        step=geotransform[1]
    )
    lon_var = output_dataset.createVariable(varname='lon', datatype='float32', dimensions=tuple('lon'))
    lon_var[:] = x_ordinates
    for attr_name, attr_value in x_attrs.items():
        lon_var.setncattr(attr_name, attr_value)

    max_y_ordinate = geotransform[3] + datasets[0].RasterYSize * geotransform[5]
    y_ordinates = np.arange(
        start=geotransform[3],
        stop=max_y_ordinate - 0.5 * geotransform[5],  # to prevent unexpected behaviour due to rounding differences
        step=geotransform[5]
    )
    lat_var = output_dataset.createVariable(varname='lat', datatype='float32', dimensions=tuple('lat'))
    lat_var[:] = y_ordinates
    for attr_name, attr_value in y_attrs.items():
        lat_var.setncattr(attr_name, attr_value)

    # time
    units = 'seconds since 1970-01-01 00:00:00.0 +0000'
    calendar = 'standard'
    time_var = output_dataset.createVariable(varname='time', datatype='float64', dimensions=tuple('time'))
    time_attrs = {
        'standard_name': 'time',
        'long_name': 'Time',
        'units': units,
        'calendar': calendar,
        'axis': 'T'
    }
    for attr_name, attr_value in time_attrs.items():
        time_var.setncattr(attr_name, attr_value)

    time_delta = timedelta(seconds=interval)
    end_time = start_time + len(filepaths) * time_delta
    time_steps_numpy = np.arange(start_time, end_time, time_delta, dtype='datetime64[s]')
    time_steps_datetime = [datetime.utcfromtimestamp(dt.astype('int')) for dt in time_steps_numpy]
    time_steps_float = netCDF4.date2num(time_steps_datetime, units=units, calendar=calendar)

    time_var[:] = time_steps_float


#     rainfall_data = np.zeros((len(time_steps), len(y_var_values), len(x_var_values)), dtype=np.float32)
#
#     for i, asc_file in enumerate(asc_files):
#         asc_grid = np.loadtxt(asc_file, skiprows=nr_header_lines)
#         interval_hr = interval / 60 / 60
#         asc_grid_intensity = asc_grid / interval_hr
#         rainfall_data[i] = asc_grid_intensity
#
#     # 创建空的 Dataset
#     ds = xr.Dataset()
#
#     # 添加时间变量并设置属性
#     time_var = xr.DataArray(time_steps_seconds, dims='time', attrs={
#         'standard_name': 'time',
#         'long_name': 'Time',
#         'units': 'seconds since 1970-01-01 00:00:00.0 +0000',
#         'calendar': 'standard',
#         'axis': 'T'
#     })
#     ds['time'] = time_var.astype('double')  # 指定数据类型为 float64
#
#
#     # 添加数据变量并设置属性
#     values_var = xr.DataArray(rainfall_data, dims=('time', y_dim_name, x_dim_name), attrs={
#         'long_name': 'rain',
#         'grid_mapping': 'crs',
#         '_FillValue': asc_meta["NODATA_value"],  # 你自己定义的 fill_value
#         'missing_value': asc_meta["NODATA_value"],  # 只有 FillValue 被考虑
#         'units': 'mm/h'  # 'mm', 'm/s', 'mm/h', 'mm/hr' 中的一个，如果是 'mm'，速率由下一个 `time` 值确定
#     })
#     ds['values'] = values_var.astype('double')  # 指定数据类型为 float32
#
#     ulx_reprojected, uly_reprojected = transformer.transform(asc_meta["xllcorner"], max_latitude)
#
#     asc_meta.pop("NODATA_value")
#     if target_crs.is_projected:
#         cell_size_x, cell_size_y = estimate_cell_size(**asc_meta)
#     else:
#         cell_size_x = asc_meta["cellsize"]
#         cell_size_y = asc_meta["cellsize"]
#
#     ds['crs'] = 1
#     ds['crs'].attrs = target_crs.to_cf()
#     ds['crs'].attrs['spatial_ref'] = f"EPSG:{target_crs.to_epsg()}"
#     ds['crs'].attrs['GeoTransform'] = f"{ulx_reprojected} {cell_size_x} 0 {uly_reprojected} 0 -{cell_size_y}"
#
#     # 添加全局属性
#     ds.attrs = {
#         'OFFSET': 0  # 可选地覆盖模拟内的偏移量（以秒为单位）
#     }
#
#     # 保存为NetCDF文件
#     ds.to_netcdf(output_path, format='NETCDF4')

datadir = Path(r"C:\Users\leendert.vanwolfswin\Documents\OZ 3Di AI\asc to netcdf")
filepaths = [
    datadir / "reprojected.tif",
    datadir / "reprojected.tif",
    datadir / "reprojected.tif"
]

datasets = get_datasets(filepaths=filepaths)
print(rasters_have_same_srs(datasets))
print(rasters_have_same_dimensions(datasets))

rasters_to_netcdf(
    rasters=filepaths,
    start_time=datetime.strptime('2020-01-01T12:00:00', "%Y-%m-%dT%H:%M:%S"),
    interval=3600,
    output_path=datadir / "output.nc"
)



