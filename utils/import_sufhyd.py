# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

import ogr
import osr
import logging
from sqlalchemy.orm import load_only

from ThreeDiToolbox.utils.importer.sufhyd import SufhydReader
from ThreeDiToolbox.sql_models.model_schematisation import (
    ConnectionNode, Manhole,
    BoundaryCondition1D, Pipe, CrossSectionDefinition, Orifice, Weir,
    Pumpstation, ImperviousSurface, ImperviousSurfaceMap)
from ThreeDiToolbox.sql_models.constants import Constants

logger = logging.getLogger(__name__)


def transform(wkt, srid_source, srid_dest):
    source_crs = osr.SpatialReference()
    source_crs.ImportFromEPSG(srid_source)
    dest_crs = osr.SpatialReference()
    dest_crs.ImportFromEPSG(srid_dest)
    transformation = osr.CoordinateTransformation(source_crs, dest_crs)

    point = ogr.CreateGeometryFromWkt(wkt)
    point.Transform(transformation)
    return point.ExportToWkt()


class Importer(object):

    def __init__(self, import_file, threedi_database):
        self.import_file = import_file
        self.file_type = 'sufhyd'
        self.db = threedi_database

    def run_import(self):

        self.db.create_and_check_fields()

        if self.file_type == 'sufhyd':
            data = self.load_sufhyd_data()
            self.check_import_data(data)
            self.transform_import_data(data)
            self.write_data_to_db(data)

    def load_sufhyd_data(self):
        reader = SufhydReader(open(self.import_file, 'r').read())
        reader.parse_input()
        return reader.get_data()

    @staticmethod
    def _check_on_unique(records, unique_field, remove_doubles=False,
                         object_name_for_logging='', log_level=logging.WARNING):

        values = [m[unique_field] for m in records]

        if len(set(values)) == len(values):
            return True, set()

        doubles = []
        value_set = set()
        for i in reversed(range(0, len(records))):
            record = records[i]
            if record[unique_field] in value_set:
                logger.log(log_level,
                           'double value in {0}: {1}'.format(
                                object_name_for_logging,
                                record[unique_field]))
                doubles.append(record)
                if remove_doubles:
                    records.remove(record)
            else:
                value_set.add(record[unique_field])

        return False, doubles

    def check_import_data(self, data):

        self._check_on_unique(data['manholes'], 'code', True, 'knoop codes')
        self._check_on_unique(data['storage'], 'node.code', True, 'bergend oppervlak knoop')
        self._check_on_unique(data['outlets'], 'node.code', True, 'uitlaat knoop')

        self._check_on_unique(data['weirs'], 'code', False, 'overstort')
        self._check_on_unique(data['pumpstations'], 'code', False, 'gemaal')
        self._check_on_unique(data['orifices'], 'code', False, 'doorlaat')

    @staticmethod
    def transform_import_data(data):
        profiles = dict()
        profiles['default'] = {
            'width': 1,
            'height': 1,
            'shape': Constants.SHAPE_ROUND,
            '_code': 'default'
        }

        for obj_type in ['pipes', 'orifices', 'weirs']:
            objects = data[obj_type]
            for obj in objects:
                crs = obj['cross_section_details']
                if crs['shape'] == Constants.SHAPE_ROUND:
                    code = 'round_{width}'.format(**crs)
                elif crs['shape'] == Constants.SHAPE_EGG:
                    code = 'egg_w{width}_h{height}'.format(**crs)
                elif crs['shape'] == Constants.SHAPE_RECTANGLE:
                    if crs['height'] is None:
                        code = 'rectangle_w{width}_open'.format(**crs)
                    else:
                        code = 'rectangle_w{width}_h{height}'.format(**crs)
                else:
                    code = 'default'

                # add unique profiles to profile definition
                if code not in profiles:
                    profiles[code] = crs
                    profiles[code]['_code'] = code

                obj['crs_code'] = code

        # generate extra boundary nodes if needed
        for obj_type in ['orifices', 'weirs']:
            objects = data[obj_type]
            for obj in objects:
                if obj['end_node.code'] is None:
                    # add extra node with boundary conditions

                    bound_code = obj['code'] + '_bound'
                    data['manholes'].append({
                        'code': bound_code,
                        'width': 1.0,
                        'length': 1.0,
                        'bottom_level': obj['crest_level'] - 1.0,
                        'surface_level': obj['crest_level'] + 1.0,
                    })
                    obj['end_node.code'] = bound_code

                    if (obj_type == 'orifice' or
                            obj['boundary_details']['value'] is None):
                        if obj['crest_level'] is not None:
                            waterlevel = obj['crest_level'] - 0.5
                        else:
                            waterlevel = -999.0
                    else:
                        waterlevel = obj['boundary_details']['value']

                    data['outlets'].append({
                        'node.code': bound_code,
                        'boundary_type': Constants.BOUNDARY_TYPE_WATERLEVEL,
                        'timeseries': '0 %.2f' % waterlevel
                    })

                    if 'boundary_details' in obj:
                        del obj['boundary_details']

        # link_node_conversion
        link_dict = {k['end_node.code']: k['start_node.code'] for
                     k in data['links']}

        storage_dict = {k['node.code']: k for k in data['storage']}

        for manhole in data['manholes']:
            if manhole['code'] in link_dict:
                print "delete node %s" % manhole['code']
                del manhole
                continue

            # add storage area
            manh = manhole
            if manh['code'] in storage_dict:
                manh['storage_area'] = storage_dict[manh['code']]['storage_area']
            elif manh['width'] is not None:
                if manh['length'] is not None:
                    manh['storage_area'] = manh['width'] * manh['length']
                else:
                    manh['storage_area'] = manh['width'] * manh['width']
            else:
                manh['storage_area'] = None

        data['profiles'] = profiles

    def write_data_to_db(self, data):
        session = self.db.get_session()

        crs_list = []
        for crs in data['profiles'].values():
            crs_list.append(CrossSectionDefinition(**crs))

        session.bulk_save_objects(crs_list)
        session.commit()

        crs_list = session.query(CrossSectionDefinition).options(
                load_only("id", "_code")).all()
        crs_dict = {m._code: m.id for m in crs_list}
        del crs_list

        con_list = []
        for manhole in data['manholes']:
            wkt = transform("POINT({0} {1})".format(*manhole['geom']),
                            manhole['geom'][2],
                            4326)
            con_list.append(ConnectionNode(_code=manhole['code'],
                            storage_area=manhole['storage_area'],
                            the_geom="srid=4326;" + wkt,
                            _basin_code=manhole['_basin_code']))

        session.bulk_save_objects(con_list)
        session.commit()

        con_list = session.query(ConnectionNode).options(
                load_only("id", "_code")).all()
        con_dict = {m._code: m.id for m in con_list}
        del con_list

        # add extra references for link nodes (one node, multiple linked codes
        con_dict.update(
            {k['end_node.code']: con_dict[k['start_node.code']]
             for k in data['links']})
        con_dict[None] = None
        con_dict[''] = None

        man_list = []
        for manhole in data['manholes']:
            del manhole['geom']
            del manhole['_basin_code']
            del manhole['storage_area']

            manhole['connection_node_id'] = con_dict[manhole['code']]
            man_list.append(Manhole(**manhole))

        session.bulk_save_objects(man_list)
        session.commit()
        del man_list

        outlet_list = []
        for outlet in data['outlets']:
            outlet['connection_node_id'] = con_dict[outlet['node.code']]

            del outlet['node.code']
            outlet_list.append(BoundaryCondition1D(**outlet))

        pipe_list = []
        for pipe in data['pipes']:
            pipe['connection_node_start_id'] = con_dict[pipe['start_node.code']]
            pipe['connection_node_end_id'] = con_dict[pipe['end_node.code']]
            pipe['cross_section_definition_id'] = crs_dict[pipe['crs_code']]

            del pipe['start_node.code']
            del pipe['end_node.code']
            del pipe['crs_code']
            del pipe['cross_section_details']

            pipe_list.append(Pipe(**pipe))

        session.bulk_save_objects(pipe_list)
        session.commit()
        del pipe_list

        obj_list = []
        for pump in data['pumpstations']:
            pump['connection_node_start_id'] = con_dict[pump['start_node.code']]
            pump['connection_node_end_id'] = con_dict[pump['end_node.code']]

            del pump['start_node.code']
            del pump['end_node.code']

            obj_list.append(Pumpstation(**pump))

        for weir in data['weirs']:
            weir['connection_node_start_id'] = con_dict[weir['start_node.code']]
            weir['connection_node_end_id'] = con_dict[weir['end_node.code']]
            weir['cross_section_definition_id'] = crs_dict[weir['crs_code']]

            del weir['start_node.code']
            del weir['end_node.code']
            del weir['crs_code']
            del weir['cross_section_details']
            del weir['boundary_details']

            obj_list.append(Weir(**weir))

        for orif in data['orifices']:
            orif['connection_node_start_id'] = con_dict[orif['start_node.code']]
            orif['connection_node_end_id'] = con_dict[orif['end_node.code']]
            orif['cross_section_definition_id'] = crs_dict[orif['crs_code']]

            del orif['start_node.code']
            del orif['end_node.code']
            del orif['crs_code']
            del orif['cross_section_details']

            obj_list.append(Orifice(**orif))

        session.bulk_save_objects(obj_list)
        session.commit()
        del obj_list

        imp_list = []
        for imp in data['impervious_surfaces']:
            imp_list.append(ImperviousSurface(**imp))

        session.bulk_save_objects(imp_list)
        session.commit()

        imp_list = session.query(ImperviousSurface).options(
                load_only("id", "code")).all()
        imp_dict = {m.code: m.id for m in imp_list}
        del imp_list

        map_list = []
        for imp_map in data['impervious_surface_maps']:
            try:
                imp_map['connection_node_id'] = con_dict[imp_map['node.code']]
            except KeyError:
                logger.log(logging.ERROR, 'node {0} not found for connecting '
                           'impervious service'.format(imp_map['node.code']))

            imp_map['impervious_surface_id'] = imp_dict[imp_map['imp_surface.code']]
            del imp_map['node.code']
            del imp_map['imp_surface.code']

            map_list.append(ImperviousSurfaceMap(**imp_map))

        session.bulk_save_objects(map_list)
        session.commit()
