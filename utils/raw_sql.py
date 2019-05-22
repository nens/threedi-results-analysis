import logging


logger = logging.getLogger(__name__)


def get_query_strings(flavor, epsg_code):
    """
    get sql query strings for all 1D objects that are needed
    to predict the 1D threedicore calculation points. Those are:
        - boundary points
        - manholes
        - channels
        - culverts
        - pipes

    :param flavor: database flavor, either 'spatialite' or 'postgres'
    :return:
    """
    flavor = flavor.lower()
    logger.info("[*] Getting sql queries for {}".format(flavor))

    sql_functions_map = {
        "makeline": {"postgres": "ST_MakeLine", "spatialite": "MakeLine"}
    }
    # ---------- boundary table ------------------
    queries = {}
    boundary_query_str = """
        -- boundaries
        SELECT
          connection_node_id
          , -1 AS calculation_type
          , id
        FROM
          v2_1d_boundary_conditions
        ;
    """
    queries["v2_1d_boundary_conditions"] = boundary_query_str

    # ---------- manhole table ------------------
    manhole_query_str = """
    -- manholes
    SELECT
      connection_node_id
      , calculation_type
      , m.id AS mid
      , ST_AsText(
          ST_Transform(
            cn_end.the_geom, {epsg_code}
          )
        ) AS the_geom_end
      , m.code
    FROM
      v2_manhole AS m
      ,v2_connection_nodes AS cn_end
    WHERE
     connection_node_id = cn_end.id
    ;
    """.format(
        epsg_code=epsg_code
    )
    queries["v2_manhole"] = manhole_query_str

    # ---------- pipe table ------------------
    pipe_query_str = """
    -- pipes
    SELECT
      connection_node_start_id
      , connection_node_end_id
      , calculation_type
      , ST_AsText(
          ST_Transform(
            cn_start.the_geom, {epsg_code}
          )
        ) AS the_geom_start
      , ST_AsText(
          ST_Transform(
            cn_end.the_geom, {epsg_code}
            )
          ) AS the_geom_end
      , ST_AsText(
          ST_Transform(
            {makeline}(
              cn_start.the_geom, cn_end.the_geom
              ), {epsg_code}
          )
        ) AS line
      , ST_Length(
            ST_Transform(
              {makeline}(
                cn_start.the_geom, cn_end.the_geom
                ), {epsg_code}
            )
        ) as length
      , p.id
      , dist_calc_points
      , p.code
    FROM
      v2_pipe AS p
      ,v2_connection_nodes AS cn_start
      ,v2_connection_nodes AS cn_end
    WHERE
      connection_node_start_id = cn_start.id
    AND
      connection_node_end_id = cn_end.id
    ;
    """.format(
        makeline=sql_functions_map["makeline"][flavor], epsg_code=epsg_code
    )
    queries["v2_pipe"] = pipe_query_str

    # ---------- culvert table ------------------
    culvert_query_str = """
    -- culverts
    SELECT
      connection_node_start_id
      , connection_node_end_id
      , 101
      , ST_AsText(
          ST_Transform(
            c.the_geom, {epsg_code}
          )
        ) AS the_geom
      , ST_Length(
          ST_Transform(
            c.the_geom, {epsg_code}
          )
        ) as length
      , c.id
      , dist_calc_points
      , ST_AsText(
          ST_Transform(
            cn_end.the_geom, {epsg_code}
          )
        ) AS the_geom_end
      , c.code
    FROM
      v2_culvert AS c
      ,v2_connection_nodes AS cn_start
      ,v2_connection_nodes AS cn_end
    WHERE
      connection_node_start_id = cn_start.id
    AND
      connection_node_end_id = cn_end.id
    ;
    """.format(
        epsg_code=epsg_code
    )
    queries["v2_culvert"] = culvert_query_str

    # ---------- channel table ------------------
    channel_query_str = """
    -- channels
    SELECT
      connection_node_start_id
      , connection_node_end_id
      , calculation_type
      , ST_AsText(
          ST_Transform(
            cn_start.the_geom, {epsg_code}
          )
        ) AS the_geom_start
      , ST_AsText(
          ST_Transform(
            cn_end.the_geom, {epsg_code}
          )
        ) AS the_geom_end
      , ST_AsText(
          ST_Transform(
            c.the_geom, {epsg_code}
          )
        ) AS line
      , ST_Length(
          ST_Transform(
            c.the_geom, {epsg_code}
          )
        ) as length
      , c.id
      , dist_calc_points
      , c.code
    FROM
      v2_channel AS c
      ,v2_connection_nodes AS cn_start
      ,v2_connection_nodes AS cn_end
    WHERE
      connection_node_start_id = cn_start.id
    AND
      connection_node_end_id = cn_end.id
    ;
    """.format(
        epsg_code=epsg_code
    )
    queries["v2_channel"] = channel_query_str
    return queries
