from ThreeDiToolbox.test.test_init import TEST_DATA_DIR
from ThreeDiToolbox.tool_commands.guess_indicators.guess_indicators_utils import Guesser
from ThreeDiToolbox.utils.threedi_database import ThreediDatabase

import os
import unittest.mock


class TestGuessser(unittest.TestCase):
    """Test the QGIS Environment"""

    def setUp(self):
        sqlite_filename = "v2_bergermeer.sqlite"
        self.test_sqlite_path = os.path.join(
            TEST_DATA_DIR, "testmodel", "v2_bergermeer", sqlite_filename
        )
        db_type = "spatialite"
        db_set = {"db_path": self.test_sqlite_path}
        db = ThreediDatabase(db_set, db_type)
        self.guesser = Guesser(db)

    def test_guess_manhole_indicator(self):
        self.guesser.guess_manhole_indicator()

    def test_guess_manhole_indicator(self):
        self.guesser.guess_manhole_area()

    def test_guess_manhole_indicator(self):
        self.guesser.guess_pipe_friction()
