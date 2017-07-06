Stats overview
==============

The stats module supports generating the following variables:

Using `flow_aggregate.nc`:

================  ============== =========================== ==============================
Variable          Layer type     Required parameter/field    Calculation method
================  ============== =========================== ==============================

q_cum             flowlines
q_max             flowlines
q_min             flowlines

wos_height        nodes          surface_level               s1_max - surface_level
s1_max            nodes
water_depth       nodes          bottom_level                s1_max - bottom_level

q_pump_cum        pumplines

================  ============== =========================== ==============================


Using `subgrid_map.nc`:

=======================  ============== ============================= ==================================================
Variable                 Layer type     Required parameter/field      Calculation method
=======================  ============== ============================= ==================================================

q_cumulative_duration    flowlines
q_end                    flowlines
tot_vol_positive         flowlines
tot_vol_negative         flowlines
time_q_max               flowlines

s1_end                   nodes
wos_duration             nodes          surface_level                 sum the timesteps where (s1 - surface_level) > 0

tot_vol_pump             pumplines
pump_duration            pumplines      pump_capacity                 1000 * vol_pump / pump_capacity, where vol_pump = dt*q

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
