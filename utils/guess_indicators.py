# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

import ogr
import osr
import logging
from sqlalchemy.orm import load_only
from sqlalchemy import update, select



from ThreeDiToolbox.utils.importer.sufhyd import SufhydReader
from ThreeDiToolbox.sql_models.model_schematisation import (
    ConnectionNode, Manhole,
    BoundaryCondition1D, Pipe, CrossSectionDefinition, Orifice, Weir,
    Pumpstation, ImperviousSurface, ImperviousSurfaceMap)
from ThreeDiToolbox.sql_models.constants import Constants


logger = logging.getLogger(__name__)


class Guesser(object):

    def __init__(self, threedi_database):
        self.db = threedi_database

    def run(self, checks, only_empty_fields=True):

        self.db.create_and_check_fields()
        session = self.db.get_session()

        if 'manhole_indicator' in checks:

            up = update(Manhole).\
                where(Manhole.connection_node_id ==
                      Pumpstation.connection_node_start_id).\
                values(manhole_indicator=Constants.MANHOLE_INDICATOR_PUMPSTATION)
            session.execute(up)
            up = update(Manhole).\
                where(Manhole.connection_node_id == BoundaryCondition1D.connection_node_id).\
                values(manhole_indicator=Constants.MANHOLE_INDICATOR_OUTLET)
            session.execute(up)
            up = update(Manhole). \
                where(Manhole.manhole_indicator == None). \
                values(manhole_indicator=Constants.MANHOLE_INDICATOR_MANHOLE)
            session.execute(up)
            session.commit()

        if 'pipe_friction' in checks:

            table_manning = {
                (Constants.MATERIAL_TYPE_CONCRETE, 0.0145),
                (Constants.MATERIAL_TYPE_PVC, 0.0110),
                (Constants.MATERIAL_TYPE_STONEWARE, 0.0115),
                (Constants.MATERIAL_TYPE_CAST_IRON, 0.0135),
                (Constants.MATERIAL_TYPE_BRICKWORK, 0.0160),
                (Constants.MATERIAL_TYPE_HPE, 0.0110),
                (Constants.MATERIAL_TYPE_HPDE, 0.0110),
                (Constants.MATERIAL_TYPE_SHEET_IRON, 0.0135),
                (Constants.MATERIAL_TYPE_STEEL, 0.0130),
            }

            for material_code, friction in table_manning:
                up = update(Pipe). \
                    where(Pipe.material == material_code). \
                    values(friction_value=friction,
                           friction_type=Constants.FRICTION_TYPE_MANNING)
                session.execute(up)

            session.commit()

        if 'manhole_area' in checks:

            up = update(ConnectionNode). \
                where(ConnectionNode.id == Manhole.connection_node_id). \
                where(ConnectionNode.storage_area == None). \
                where(Manhole.length == None). \
                where(Manhole.width != None). \
                values(storage_area=Manhole.width * Manhole.width)
            session.execute(up)

            up = update(ConnectionNode). \
                where(ConnectionNode.id == Manhole.connection_node_id). \
                where(ConnectionNode.storage_area == None). \
                where(Manhole.length != None). \
                where(Manhole.width != None). \
                values(storage_area=Manhole.width * Manhole.length)
            session.execute(up)

            session.commit()

