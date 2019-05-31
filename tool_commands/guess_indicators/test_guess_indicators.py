from sqlalchemy import update
from ThreeDiToolbox.sql_models.model_schematisation import ConnectionNode
from ThreeDiToolbox.sql_models.model_schematisation import Manhole
from ThreeDiToolbox.sql_models.model_schematisation import Pumpstation
from ThreeDiToolbox.test.test_init import TEST_DATA_DIR
from ThreeDiToolbox.tool_commands.guess_indicators.guess_indicators_utils import Guesser
from ThreeDiToolbox.utils.threedi_database import ThreediDatabase

import os
import shutil
import tempfile
import unittest.mock


def get_manholes_id_indicator(session):
    """ get manholes that are on same connection node as start point of pumpstation
    :return: a list with tuples (manhole.id, manhole.manhole_indicator)  """
    manholes_id_indicator = {}
    pump_start_ids = session.query(Pumpstation.connection_node_start_id)
    sql_manholes = (
        session.query(Manhole)
        .join(Manhole.connection_node)
        .filter(ConnectionNode.id.in_(pump_start_ids))
    )
    for manhole in sql_manholes:
        # fill dict
        manholes_id_indicator[manhole.id] = manhole.manhole_indicator
    return manholes_id_indicator


class TestGuessser(unittest.TestCase):
    """ We test 3 methods of Guesser that affect ThreediDatabase:
        methodname --> table --> column
            guess_manhole_indicator() --> v2_manhole --> manhole_indicators
            guess_pipe_friction --> v2_pipe --> frictions
            guess_manhole_area --> v2_connection_node --> storage_area """

    def setUp(self):
        sqlite_filename = "v2_bergermeer.sqlite"
        self.test_sqlite_path = os.path.join(
            TEST_DATA_DIR, "testmodel", "v2_bergermeer", sqlite_filename
        )

        tempdir = tempfile.gettempdir()
        tmp_filename = "tmp_sqlite.sqlite"
        tmp_filename_path = os.path.join(tempdir, tmp_filename)
        tmp_sqlite = shutil.copy2(self.test_sqlite_path, tmp_filename_path)

        db_type = "spatialite"
        db_set = {"db_path": tmp_sqlite}
        self.db = ThreediDatabase(db_set, db_type)
        self.guesser = Guesser(self.db)

    def test_manhole_indicator(self):
        session = self.db.get_session()

        manhole_pre_empty = get_manholes_id_indicator(session)
        if not manhole_pre_empty:
            # skip this test
            return
        # now lets empty column 'manhole_indicator'
        manhole_ids = list(manhole_pre_empty)
        up = (
            update(Manhole)
            .where(Manhole.id.in_(manhole_ids))
            .values(manhole_indicator=None)
        )
        session.execute(up)
        session.commit()

        manhole_pre_guess = get_manholes_id_indicator(session)
        # all dict values should be None (<-- still test-prework, not actual testing)
        self.assertFalse(all(list(manhole_pre_guess.values())))

        # now put guesser to work
        self.guesser.guess_manhole_indicator(only_empty_fields=False)

        session = self.db.get_session()
        # all dict values should be not None (<-- this is the actual test)
        manhole_after_guess = get_manholes_id_indicator(session)
        self.assertTrue(all(list(manhole_after_guess.values())))

    def test_pipe_friction(self):
        pass

    def test_manhole_area(self):
        pass
