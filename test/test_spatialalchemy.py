import unittest
import tempfile
import os.path
import sys

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'external')
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from geoalchemy2.types import Geometry

from ThreeDiToolbox.utils.threedi_database import ThreediDatabase

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<User(name='%s')>" % (
            self.name)


class GeoTable(Base):
    __tablename__ = 'geotable'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    geom = Column(Geometry(
        geometry_type='POINT',
        srid=4326,
        management=True,
        spatial_index=True,
        use_st_prefix=False))

    def __repr__(self):
        return "<User(geom='%s')>" % (
            self.geom)

# TODO: only works on linux, fix this also for Windows.
def load_spatialite(dbapi_conn, connection_record):
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension('/usr/lib/x86_64-linux-gnu/mod_spatialite.so')


class TestSpatialAlchemyWithSpatialite(unittest.TestCase):

    def setUp(self):
        self.tmp_directory = tempfile.mkdtemp()
        self.file_path = os.path.join(self.tmp_directory, 'testdb.sqlite')

        db = ThreediDatabase({'db_file': self.file_path,
                              'db_path': self.file_path},
                             echo=True)
        db.create_db()
        self.engine = db.get_engine()
        self.session = db.get_session()

        Base.metadata.bind = self.engine
        Base.metadata.create_all(self.engine)

    def test_insert_and_get_normal_table(self):
        user = User(name='test')
        self.session.add(user)
        self.session.commit()

        self.assertIsNotNone(user.id)
        self.assertEqual(self.session.query(User).count(), 1)
        user = self.session.query(User).limit(1)[0]

        self.assertEqual(user.name, 'test')

    def test_insert_and_get_geo_data(self):
        geo_table = GeoTable(geom='srid=4326;POINT(1.01234567 4.01234567)')
        self.session.add(geo_table)
        self.session.commit()

        self.assertIsNotNone(geo_table.id)

        self.assertEqual(self.session.query(GeoTable).count(), 1)
        geo_table = self.session.query(GeoTable).limit(1)[0]
        self.assertIsNotNone(geo_table.geom)

    def tearDown(self):
        self.session.close_all()
        os.remove(self.file_path)
