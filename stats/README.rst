Stats overview
==============

The stats module supports generating the following variables:

Using ``flow_aggregate.nc``:

================  ============== =========================== ==============================
Variable          Layer type     Required parameter/field    Calculation method
================  ============== =========================== ==============================
q_cum             structures
q_max             structures
q_min             structures
wos_height        manholes       surface_level               s1_max - surface_level
s1_max            manholes
water_depth       manholes       bottom_level                s1_max - bottom_level
q_pump_cum        pumps
================  ============== =========================== ==============================


Using ``subgrid_map.nc``:

=======================  ============== ============================= =======================================================
Variable                 Layer type     Required parameter/field      Calculation method
=======================  ============== ============================= =======================================================
q_cumulative_duration    structures
q_end                    structures
tot_vol_positive         structures
tot_vol_negative         structures
time_q_max               structures
s1_end                   manholes
wos_duration             manholes       surface_level                 sum the timesteps where (s1 - surface_level) > 0
tot_vol_pump             pumps
pump_duration            pumps          pump_capacity                 1000 * vol_pump / pump_capacity, where vol_pump = dt*q
=======================  ============== ============================= =======================================================


Spatialite views
----------------

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
    - wos_duration
    - water_depth
