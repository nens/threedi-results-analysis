# -*- coding: utf-8 -*-


boundary_query_str = """
    -- boundaries
    SELECT
      connection_node_id
      , -1 AS calculation_type
    FROM
      v2_1d_boundary_conditions
    ;
"""

manhole_query_str = """
-- manholes
SELECT
  connection_node_id
  , calculation_type
FROM
  v2_manhole
;
"""

pipe_query_str = """
-- pipes
SELECT
  connection_node_start_id
  , connection_node_end_id
  , calculation_type
  , ST_AsText(cn_start.the_geom) AS the_geom_start
  , ST_AsText(cn_end.the_geom) AS the_geom_end
  , ST_AsText(ST_MakeLine(cn_start.the_geom, cn_end.the_geom)) AS line
  , ST_Length(ST_MakeLine(cn_start.the_geom, cn_end.the_geom)) as length
FROM
  v2_pipe
  ,v2_connection_nodes AS cn_start
  ,v2_connection_nodes AS cn_end
WHERE
  connection_node_start_id = cn_start.id
AND
  connection_node_end_id = cn_end.id
;
"""

culvert_query_str = """
-- culverts
SELECT
  connection_node_start_id
  , connection_node_end_id
  , calculation_type
  , c.the_geom AS the_geom
  , ST_Length(c.the_geom) as length
FROM
  v2_culvert AS c
  ,v2_connection_nodes AS cn_start
  ,v2_connection_nodes AS cn_end
WHERE
  connection_node_start_id = cn_start.id
AND
  connection_node_end_id = cn_end.id
;
"""
