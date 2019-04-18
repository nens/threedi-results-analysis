import unittest
import tempfile
import os.path

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from geoalchemy2.types import Geometry

from ThreeDiToolbox.utils.threedi_database import ThreediDatabase

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<User(name='%s')>" % (self.name)


class GeoTable(Base):
    __tablename__ = "geotable"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    geom = Column(
        Geometry(
            geometry_type="POINT",
            srid=4326,
            management=True,
            spatial_index=True,
            use_st_prefix=False,
        )
    )

    def __repr__(self):
        return "<User(geom='%s')>" % (self.geom)


def load_spatialite(con, connection_record):
    import sqlite3

    con.enable_load_extension(True)
    cur = con.cursor()
    libs = [
        # SpatiaLite >= 4.2 and Sqlite >= 3.7.17, should work on all platforms
        ("mod_spatialite", "sqlite3_modspatialite_init"),
        # SpatiaLite >= 4.2 and Sqlite < 3.7.17 (Travis)
        ("mod_spatialite.so", "sqlite3_modspatialite_init"),
        # SpatiaLite < 4.2 (linux)
        ("libspatialite.so", "sqlite3_extension_init"),
    ]
    found = False
    for lib, entry_point in libs:
        try:
            cur.execute("select load_extension('{}', '{}')".format(lib, entry_point))
        except sqlite3.OperationalError:
            continue
        else:
            found = True
            break
    if not found:
        raise RuntimeError("Cannot find any suitable spatialite module")
    cur.close()
    con.enable_load_extension(False)


class TestSpatialAlchemyWithSpatialite(unittest.TestCase):
    def setUp(self):
        self.tmp_directory = tempfile.mkdtemp()
        self.file_path = os.path.join(self.tmp_directory, "testdb.sqlite")

        db = ThreediDatabase(
            {"db_file": self.file_path, "db_path": self.file_path}, echo=True
        )
        db.create_db()
        self.engine = db.get_engine()
        self.session = db.get_session()

        Base.metadata.bind = self.engine
        Base.metadata.create_all(self.engine)

    def test_insert_and_get_normal_table(self):
        user = User(name="test")
        self.session.add(user)
        self.session.commit()

        self.assertIsNotNone(user.id)
        self.assertEqual(self.session.query(User).count(), 1)
        user = self.session.query(User).limit(1)[0]

        self.assertEqual(user.name, "test")

    def test_insert_and_get_geo_data(self):
        geo_table = GeoTable(geom="srid=4326;POINT(1.01234567 4.01234567)")
        self.session.add(geo_table)
        self.session.commit()

        self.assertIsNotNone(geo_table.id)

        self.assertEqual(self.session.query(GeoTable).count(), 1)
        geo_table = self.session.query(GeoTable).limit(1)[0]
        self.assertIsNotNone(geo_table.geom)

    def tearDown(self):
        self.session.close_all()
        os.remove(self.file_path)
