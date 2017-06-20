import unittest
import tempfile
import os.path
import sys

sys.path.insert(
    0,
    os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'external', 'sqlalchemy', 'lib')
)
sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'external', 'geoalchemy2')
)

import ogr

from pyspatialite import dbapi2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, MetaData
from geoalchemy2.types import Geometry

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
        geometry_type='POINT', srid=4326, management=True, spatial_index=True))

    def __repr__(self):
        return "<User(geom='%s')>" % (
            self.geom)


class TestSpatialAlchemyWithSpatialite(unittest.TestCase):

    def setUp(self):
        self.tmp_directory = tempfile.mkdtemp()
        self.file_path = os.path.join(self.tmp_directory, 'testdb.sqlite')

        drv = ogr.GetDriverByName('SQLite')
        db = drv.CreateDataSource(self.file_path, ["SPATIALITE=YES"])
        del db

        self.engine = create_engine('sqlite:///{0}'.format(self.file_path),
                                    module=dbapi2,
                                    echo=True)

        Base.metadata.bind = self.engine
        Base.metadata.reflect(extend_existing=True)

        self.session = sessionmaker(bind=self.engine)()

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

    def TearDown(self):
        self.session.close_all()
        os.remove(self.file_path)
