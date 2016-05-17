Stats overview
==============

The statistics scripts support the following netCDF aggregation variables:

================  ============== =============================
NetCDF Agg. Var.  Layer type     Toolbox script
================  ============== =============================
q_cum             flowlines      calc_structure_statistics.py
q_max             flowlines      calc_structure_statistics.py
q_min             flowlines      calc_structure_statistics.py
s1_max            nodes          calc_manhole_statistics.py
================  ============== =============================


Spatialite views
>>>>>>>>>>>>>>>>

Additionally, you get the *old* behaviour if you use the Spatialite views:

calc_structure_statistics.py:

    - tot_vol
    - q_max
    - cumulative_duration
    - q_end
    - tot_vol_positive
    - tot_vol_negative
    - time_q_max

calc_manhole_statistics.py:

    - s1_max
    - wos_height
    - water_depth
