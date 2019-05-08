"""integration test for the full process of importing sewer data from a
sufhyd file into the database"""
from future import standard_library
from geoalchemy2 import types
from sqlalchemy import select
from ThreeDiToolbox.utils.guess_indicators import Guesser
from ThreeDiToolbox.utils.import_sufhyd import Importer
from ThreeDiToolbox.utils.import_sufhyd import transform
from ThreeDiToolbox.utils.threedi_database import ThreediDatabase

import os.path
import tempfile
import unittest

standard_library.install_aliases()


test_file = os.path.join("c://tmp", "test.hyd")


@unittest.skipIf(not os.path.exists(test_file), "Path to test sufhyd doesn't exist.")
class TestImportNewDB(unittest.TestCase):
    def setUp(self):
        self.tmp_directory = tempfile.mkdtemp()
        self.sufhyd_file = os.path.join("c://tmp", "test.hyd")
        self.db_file = os.path.join("c://tmp", "test.sqlite")
        self.db = ThreediDatabase({"db_file": self.db_file})

    def test_transform(self):
        a = transform("POINT(150000 250000)", 28992, 4326)
        self.assertIsNotNone(a)

    def test_import(self):
        self.db.create_db(overwrite=True)

        importer = Importer(self.sufhyd_file, self.db)

        data = importer.load_sufhyd_data()

        importer.check_import_data(data)

        importer.transform_import_data(data)

        importer.write_data_to_db(data)


@unittest.skipIf(not os.path.exists(test_file), "Path to test sufhyd doesn't exist.")
class TestImportExistingDB(unittest.TestCase):
    def setUp(self):
        self.tmp_directory = tempfile.mkdtemp()
        self.sufhyd_file = os.path.join("c://tmp", "test.hyd")
        self.db_file = os.path.join("c://tmp", "v2_bergermeer.sqlite")
        self.db = ThreediDatabase({"db_path": self.db_file})

    def test_transform(self):
        a = transform("POINT(150000 250000)", 28992, 4326)
        self.assertIsNotNone(a)

    def test_import(self):
        # self.db.create_and_check_fields()

        importer = Importer(self.sufhyd_file, self.db)

        importer.run_import()


@unittest.skipIf(not os.path.exists(test_file), "Path to test sufhyd doesn't exist.")
class TestPostgresConnection(unittest.TestCase):
    def test_setup(self):
        self.db = ThreediDatabase(
            {
                "host": "localhost",
                "port": "5432",
                "database": "test_gis",
                "username": "postgres",
                "password": "postgres",
            },
            "postgres",
        )


@unittest.skipIf(not os.path.exists(test_file), "Path to test sufhyd doesn't exist.")
class TestImportPostgres(unittest.TestCase):
    def setUp(self):
        self.tmp_directory = tempfile.mkdtemp()
        self.sufhyd_file = os.path.join("c://tmp", "test.hyd")
        self.db = ThreediDatabase(
            {
                "host": "localhost",
                "port": "5432",
                "database": "test_gis",
                "username": "postgres",
                "password": "postgres",
            },
            "postgres",
        )

    def test_setup(self):

        importer = Importer(self.sufhyd_file, self.db)

        importer.run_import()


class TestSelectGeometry(unittest.TestCase):
    def test_setup(self):
        from sqlalchemy.dialects import postgresql

        statement = select([types.ST_GeomFromEWKT("POINT")])

        print(statement.compile(dialect=postgresql.dialect()))


@unittest.skipIf(not os.path.exists(test_file), "Path to test sufhyd doesn't exist.")
class TestGuessIndicators(unittest.TestCase):
    def test_read(self):
        self.db = ThreediDatabase(
            {
                "host": "localhost",
                "port": "5432",
                "database": "test_gis",
                "username": "postgres",
                "password": "postgres",
            },
            "postgres",
        )

        guesser = Guesser(self.db)

        guesser.run(["manhole_indicator", "pipe_friction", "manhole_area"], True)
