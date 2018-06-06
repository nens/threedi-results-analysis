import logging

from sqlalchemy import (
    Boolean, Column, Integer, String, Float, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from geoalchemy2.types import Geometry

logger = logging.getLogger(__name__)
Base = declarative_base()


def prettify(value, postfix, value_format='%0.2f'):
    """
    return prettified string of given value
    value may be None
    postfix can be used for unit for example
    """
    if value is None:
        value_str = '--'
    else:
        value_str = value_format % value
    return '%s %s' % (value_str, postfix)


class Flowline(Base):
    __tablename__ = 'flowlines'
    extend_existing = True

    id = Column(Integer, primary_key=True)
    inp_id = Column(Integer)
    spatialite_id = Column(Integer)
    type = Column(String(25))
    start_node_idx = Column(Integer, nullable=False)
    end_node_idx = Column(Integer, nullable=False)
    the_geom = Column(Geometry(geometry_type='LINESTRING',
                               srid=4326,
                               spatial_index=True),
                      nullable=False)

    stats = relationship("FlowlineStats",
                         uselist=False,
                         back_populates="flowline")

    pipe_stats = relationship("PipeStats",
                              uselist=False,
                              back_populates="flowline")

    weir_stats = relationship("WeirStats",
                              uselist=False,
                              back_populates="flowline")

    def __str__(self):
        return u'Flowline {0} - {1}'.format(
            self.type, self.id)


class PipeStats(Base):
    __tablename__ = 'pipe_stats'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(
        Integer,
        ForeignKey(Flowline.__tablename__ + ".id"),
        primary_key=True,
        nullable=False,
        unique=True)

    flowline = relationship(Flowline,
                            foreign_keys=id,
                            back_populates="pipe_stats")

    code = Column(String(25))
    display_name = Column(String(128))
    sewerage_type = Column(Integer)
    invert_level_start = Column(Float)
    invert_level_end = Column(Float)
    profile_height = Column(Float)
    abs_length = Column(Float)
    # statistics
    max_hydro_gradient = Column(Float)
    max_filling = Column(Float)
    end_filling = Column(Float)

    def __str__(self):
        return u'PipeStats {0} - {1}'.format(
            self.code, self.display_name)


class WeirStats(Base):
    __tablename__ = 'weir_stats'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(
        Integer,
        ForeignKey(Flowline.__tablename__ + ".id"),
        primary_key=True,
        nullable=False,
        unique=True)

    flowline = relationship(Flowline,
                            foreign_keys=id,
                            back_populates="weir_stats")

    code = Column(String(25))
    display_name = Column(String(128))
    crest_level = Column(Float)
    # width = Column(Float)

    # statistics
    perc_volume = Column(Float)
    perc_volume_positive = Column(Float)
    perc_volume_negative = Column(Float)
    max_overfall_height = Column(Float)

    def __str__(self):
        return u'WeirStats {0} - {1}'.format(
            self.code, self.display_name)


class FlowlineStats(Base):
    __tablename__ = 'flowline_stats'

    id = Column(
        Integer,
        ForeignKey(Flowline.__tablename__ + ".id"),
        primary_key=True,
        nullable=False,
        unique=True)

    flowline = relationship(Flowline,
                            foreign_keys=id,
                            back_populates="stats")

    abs_length = Column(Float)

    cum_discharge = Column(Float)
    cum_discharge_positive = Column(Float)
    cum_discharge_negative = Column(Float)
    max_discharge = Column(Float)
    end_discharge = Column(Float)
    max_velocity = Column(Float)
    end_velocity = Column(Float)
    max_head_difference = Column(Float)
    max_waterlevel_start = Column(Float)
    max_waterlevel_end = Column(Float)
    end_waterlevel_start = Column(Float)
    end_waterlevel_end = Column(Float)


    def __str__(self):
        return u'FlowLineStats {0}'.format(
            self.id)


class Node(Base):
    __tablename__ = 'nodes'
    extend_existing = True

    id = Column(Integer, primary_key=True)
    inp_id = Column(Integer)
    spatialite_id = Column(Integer)
    featuretype = Column(String(25))
    type = Column(String(25))
    the_geom = Column(Geometry(geometry_type='POINT',
                               srid=4326,
                               spatial_index=True),
                      nullable=False)

    manhole_stats = relationship("ManholeStats",
                                 uselist=False,
                                 back_populates="node")

    def __str__(self):
        return u'Node {0} - {1}'.format(
            self.type, self.id)


class ManholeStats(Base):
    __tablename__ = 'manhole_stats'

    id = Column(
        Integer,
        ForeignKey(Node.__tablename__ + ".id"),
        primary_key=True,
        nullable=False,
        unique=True)
    node = relationship(Node,
                        foreign_keys=id,
                        back_populates="manhole_stats")

    code = Column(String(25))
    display_name = Column(String(128))
    sewerage_type = Column(Integer)
    bottom_level = Column(Float)
    surface_level = Column(Float)

    # statistics
    duration_water_on_surface = Column(Float)
    max_waterlevel = Column(Float)
    end_waterlevel = Column(Float)

    max_waterdepth_surface = Column(Float)
    end_filling = Column(Float)
    max_filling = Column(Float)

    def __str__(self):
        return u'PipeStats {0} - {1}'.format(
            self.code, self.display_name)


class Pumpline(Base):
    __tablename__ = 'pumplines'
    id = Column(Integer, primary_key=True)
    node_idx1 = Column(Integer, nullable=False)
    node_idx2 = Column(Integer, nullable=True)

    the_geom = Column(Geometry(geometry_type='LINESTRING',
                               srid=4326,
                               spatial_index=True),
                      nullable=False)

    pumpline_stats = relationship("PumplineStats",
                                  uselist=False,
                                  back_populates="pumpline")

    def __str__(self):
        return u'Node {0} - {1}'.format(
            self.type, self.id)


class PumplineStats(Base):
    __tablename__ = 'pumpline_stats'

    id = Column(
        Integer,
        ForeignKey(Pumpline.__tablename__ + ".id"),
        primary_key=True,
        nullable=False,
        unique=True)

    pumpline = relationship(Pumpline,
                            foreign_keys=id,
                            back_populates="pumpline_stats")

    spatialite_id = Column(Integer)
    code = Column(String(25))
    display_name = Column(String(128))
    capacity = Column(Float)

    # statistics
    cum_discharge = Column(Float)
    end_discharge = Column(Float)
    max_discharge = Column(Float)

    perc_cum_discharge = Column(Float)
    perc_max_discharge = Column(Float)
    perc_end_discharge = Column(Float)
    duration_pump_on_max = Column(Float)

    def __str__(self):
        return u'PumpLineStats {0} - {1}'.format(
            self.code, self.display_name)


class StatSource(Base):
    __tablename__ = 'stat_source'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True)
    table = Column(String(25))
    field = Column(String(25))
    from_agg = Column(Boolean)
    input_param = Column(String(25))
    timestep = Column(Integer)

    def __str__(self):
        return u'StatSource {0} - {1}'.format(
            self.table, self.field)
