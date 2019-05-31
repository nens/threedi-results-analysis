# (c) Nelen & Schuurmans, see LICENSE.rst.

from sqlalchemy import select
from sqlalchemy import update
from ThreeDiToolbox.sql_models.constants import Constants
from ThreeDiToolbox.sql_models.model_schematisation import BoundaryCondition1D
from ThreeDiToolbox.sql_models.model_schematisation import ConnectionNode
from ThreeDiToolbox.sql_models.model_schematisation import Manhole
from ThreeDiToolbox.sql_models.model_schematisation import Pipe
from ThreeDiToolbox.sql_models.model_schematisation import Pumpstation

import logging


logger = logging.getLogger(__name__)


class Guesser(object):
    """
    Class for guessing manhole indicator, pipe friction and manhole storage
    area.
    """

    def __init__(self, threedi_database):
        """Init method.

        :param threedi_database - ThreediDatabase instance (sqlalchemy database
            engine)
        """
        self.db = threedi_database
        self.messages = []

    def reset_messages(self):
        """Reset messages."""
        self.messages = []

    def guess_manhole_indicator(self, only_empty_fields=True):
        """Guess the manhole indicator."""
        session = self.db.get_session()
        update_counter = 0

        # note: sqlite can not use a join with another table in an update
        # statement, so use 'in'
        up = (
            update(Manhole)
            .where(
                Manhole.connection_node_id.in_(
                    select([Pumpstation.connection_node_start_id]).correlate()
                )
            )
            .values(manhole_indicator=Constants.MANHOLE_INDICATOR_PUMPSTATION)
        )
        if only_empty_fields:
            up = up.where(Manhole.manhole_indicator.is_(None))
        ret = session.execute(up)
        update_counter += ret.rowcount
        session.commit()

        up = (
            update(Manhole)
            .where(
                Manhole.connection_node_id.in_(
                    select([BoundaryCondition1D.connection_node_id]).correlate()
                )
            )
            .values(manhole_indicator=Constants.MANHOLE_INDICATOR_OUTLET)
        )
        if only_empty_fields:
            up = up.where(Manhole.manhole_indicator.is_(None))
        ret = session.execute(up)
        update_counter += ret.rowcount
        session.commit()

        up = (
            update(Manhole)
            .where(Manhole.manhole_indicator.is_(None))
            .values(manhole_indicator=Constants.MANHOLE_INDICATOR_MANHOLE)
        )
        if only_empty_fields:
            up = up.where(Manhole.manhole_indicator.is_(None))
        ret = session.execute(up)
        update_counter += ret.rowcount
        session.commit()

        session.close()

        self.messages.append(
            "Manhole indicator updated {0} manholes.".format(update_counter)
        )

    def guess_pipe_friction(self, only_empty_fields=True):
        """Guess the pipe friction."""
        session = self.db.get_session()
        update_counter = 0

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
            up = (
                update(Pipe)
                .where(Pipe.material == material_code)
                .values(
                    friction_value=friction,
                    friction_type=Constants.FRICTION_TYPE_MANNING,
                )
            )
            if only_empty_fields:
                up = up.where(Pipe.friction_value.is_(None))
            ret = session.execute(up)
            update_counter += ret.rowcount

        session.commit()
        session.close()

        self.messages.append("Pipe friction updated {0} pipes.".format(update_counter))

    def guess_manhole_area(self, only_empty_fields=True):
        """Guess the manhole area."""
        session = self.db.get_session()
        update_counter = 0

        manhole_list = (
            session.query(Manhole)
            .join(Manhole.connection_node)
            .filter(ConnectionNode.storage_area.is_(None))
        )

        # '01' and '02' are the old identifiers, based on the sufhyd
        # standard
        for manhole in manhole_list:
            if (
                manhole.shape in [Constants.MANHOLE_SHAPE_ROUND, "01"]
                and manhole.width is not None
            ):
                storage_area = 0.5 * 3.14 * manhole.width * manhole.width
            elif (
                manhole.shape in [Constants.MANHOLE_SHAPE_RECTANGLE, "02"]
                and manhole.width is not None
                and manhole.length is not None
            ):
                storage_area = manhole.width * manhole.length
            elif manhole.width is not None:
                storage_area = manhole.width * manhole.width
            else:
                continue

            up = (
                update(ConnectionNode)
                .where(ConnectionNode.id == manhole.connection_node_id)
                .values(storage_area=storage_area)
            )
            ret = session.execute(up)
            update_counter += ret.rowcount

        session.commit()
        session.close()

        self.messages.append(
            "Manhole area updated {0} manholes.".format(update_counter)
        )

    def run(self, checks, only_empty_fields=True):
        """Run the guess checks."""
        self.reset_messages()  # start with no messages

        for check in checks:
            guess_method_name = "guess_{}".format(check)
            if not hasattr(self, guess_method_name):
                self.messages.append("[ERROR] could not handle {} guess.".format(check))
                continue

            guess_method = getattr(self, guess_method_name)
            try:
                guess_method(only_empty_fields)
            except Exception as e:
                logger.exception("Guessing for %s failed", check)
                self.messages.append("[ERROR] guessing {}: {}.".format(check, e))

        if self.messages:
            return " ".join(self.messages)
        else:
            return "no messages"
