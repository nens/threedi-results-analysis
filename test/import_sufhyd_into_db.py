"""integration test for the full process of importing sewer data from a
sufhyd file into the database"""

import unittest
import tempfile
import os.path
import cPickle

from ThreeDiToolbox.utils.import_sufhyd import Importer, transform
from ThreeDiToolbox.utils.threedi_database import ThreediDatabase
from ThreeDiToolbox.sql_models.model_schematisation import ConnectionNode
from ThreeDiToolbox.external.spatialalchemy import types
from sqlalchemy import select


class TestImportNewDB(unittest.TestCase):

    def setUp(self):
        self.tmp_directory = tempfile.mkdtemp()
        self.sufhyd_file = os.path.join('c://tmp', 'test.hyd')
        self.db_file = os.path.join('c://tmp', 'test.sqlite')
        self.db = ThreediDatabase({'db_file': self.db_file})

    def test_transform(self):
        a = transform('POINT(150000 250000)', 28992, 4326)
        self.assertIsNotNone(a)

    def test_import(self):
        self.db.create_db(overwrite=True)

        importer = Importer(self.sufhyd_file, self.db)

        data = importer.load_sufhyd_data()

        importer.check_import_data(data)

        importer.transform_import_data(data)

        importer.write_data_to_db(data)


class TestImportExistingDB(unittest.TestCase):

    def setUp(self):
        self.tmp_directory = tempfile.mkdtemp()
        self.sufhyd_file = os.path.join('c://tmp', 'test.hyd')
        self.db_file = os.path.join('c://tmp', 'v2_bergermeer.sqlite')
        self.db = ThreediDatabase({'db_file': self.db_file})

    def test_transform(self):
        a = transform('POINT(150000 250000)', 28992, 4326)
        self.assertIsNotNone(a)

    def test_import(self):
        # self.db.create_and_check_fields()

        # a = ConnectionNode()
        # session = self.db.get_session()
        # session.add(a)
        # session.commit()

        data = []

        importer = Importer(self.sufhyd_file, self.db)

        # data = importer.load_sufhyd_data()

        # importer.check_import_data(data)

        # importer.transform_import_data(data)

        importer.write_data_to_db(data)



class TestPostgresConnection(unittest.TestCase):

    def test_setup(self):
        self.db = ThreediDatabase({'host': 'localhost',
                                   'port': '5432',
                                   'database': 'test_gis',
                                   'username': 'postgres',
                                   'password': 'postgres'},
                                  'postgres')

class TestImportPostgres(unittest.TestCase):

    def setUp(self):
        self.tmp_directory = tempfile.mkdtemp()
        self.sufhyd_file = os.path.join('c://tmp', 'test.hyd')
        self.db = ThreediDatabase({'host': 'localhost',
                                   'port': '5432',
                                   'database': 'test_gis',
                                   'username': 'postgres',
                                   'password': 'postgres'},
                                  'postgres')

    def test_setup(self):

        importer = Importer(self.sufhyd_file, self.db)

        data = importer.load_sufhyd_data()

        importer.check_import_data(data)

        importer.transform_import_data(data)

        importer.write_data_to_db(data)


class TestSelectGeometry(unittest.TestCase):


    def test_setup(self):
        from sqlalchemy.dialects import postgresql


        statement = select([types.ST_GeomFromEWKT('POINT')])

        print statement.compile(dialect=postgresql.dialect())

