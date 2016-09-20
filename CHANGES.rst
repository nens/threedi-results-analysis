threedi-qgis-plugin changelog
=============================


0.8.2 (unreleased)
------------------

- Bugfix relative path exception.


0.8.1 (2016-09-13)
------------------

- Fixes sufhyd import.


0.8 (2016-09-13)
----------------

- Added pump statistics.

- Connected python logging handler to qgis logging

- Import of sufhyd files with logging

- Made reading netCDF properties more robust.

- Reuse previously generated csv stats files.

- Added auto statistic generation via layer tree manager.

- Refactored statistic generation (put logic in separate modules).

- Refactored timeseries methods of NetcdfDataSource, more consistent
  ``get_values_of`` methods.

- Made ``get_timeseries`` only accept one netCDF variable name.

- Add Layer Manager, which loads the model and result layers.

- Add map animator for showing results on the map (first version, work in progress).

- Made the parameter config variable for the Graph and Map animator tools. Add
  parameters so almost all results from netCDF and result netCDF can be displayed.

- Optimizations in getting the time array from netCDF.

- Refactored NetcdfDataSource and included support for getting all variables
  from both regular and aggregation netCDF including getting the timeseries.

- Removed support for spatialite datasource with results.

- Changed id behavior for netcdf datasources and requesting tools. Now the
  netcdf_id or spatialite id is used (so no magic with -1, etc.)

- Added ``water op straat`` statistic to manhole statistics; refactored NcStats
  a bit.

- Updated some method names.

- Updated NetcdfDataSource so that it keeps some netCDF attributes in memory.

- Stores selected model and results in Qgs project file (\*.qgs).

- Cache generated model layers in spatialite.

- Add point markers to selected sideview points.

- Show marker of current location when hovering over graph.


0.7.1 (2016-07-25)
------------------

- Support of interflow results in graphs

- Bug fix: after closing sideview and reopening, errors were generated

- Bug fix: support of square profiles by sideview

- Bug fix: support of pure 2d models

- Bug fix: support sideview with pipes and openwater in one sideview

- Bug fix: calculation of  length of openwater channels


0.7 (2016-06-09)
----------------

- Bug fix highlight graph location on table hover


0.6 (2016-06-02)
----------------

- Bug fix stat layer joining in Windows.

- Add multiple clicks in sideview tool.

- Add channels to the sideviews.


0.5 (2016-05-20)
----------------

- Bugfix transformation clicked coordinate in RouteTool.

- Statistic scripts performance improved.

- Various bug fixes (e.g. sideview)

- Side view clicking improvements.

- Pumplines.


0.4 (2016-05-10)
----------------

- Several new features were added (side view, netCDF network generation,
  etc.), plus improvements in existing features.


0.3 (2016-04-13)
----------------

- Add tool version number to about box.

- Add support of multiple result files.

- Warn user on adding to many locations to graph.

- Only new locations will be added to graph.

- Improved color selections for timeseries after the first 20.


0.2 (2016-04-12)
----------------

- Another test release.


0.1 (2016-04-11)
----------------

- Test release.
