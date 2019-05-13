"""integration test for the full process of importing sewer data from a
sufhyd file into the database"""
from geoalchemy2 import types
from sqlalchemy import select
from ThreeDiToolbox.utils.guess_indicators import Guesser
from ThreeDiToolbox.utils.import_sufhyd import Importer
from ThreeDiToolbox.utils.import_sufhyd import transform
from ThreeDiToolbox.utils.threedi_database import ThreediDatabase

import os.path
import tempfile
import unittest


class TestSelectGeometry(unittest.TestCase):
    def test_setup(self):
        from sqlalchemy.dialects import postgresql

        statement = select([types.ST_GeomFromEWKT("POINT")])

        print(statement.compile(dialect=postgresql.dialect()))
