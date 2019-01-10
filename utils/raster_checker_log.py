import time
import os

import logging
log = logging.getLogger(__name__)

class RasterCheckerResults(object):
    def __init__(self, sqlite_path):
        self.sqlite_path = sqlite_path
        self.result_list = []
        self.log_path = None

    def __repr__(self):
        return repr(self.__dict__)

    def __contains__(self, item):
        return item in self.__dict__

    def raster_to_string(self, rasters):
        # TODO: fix this dreadfull solution
        if isinstance(rasters, unicode):
            # in case len(rasters) = 1
            return [str(rasters)]
        elif isinstance(rasters, list):
            # in case len(rasters) > 1
            return [str(raster) for raster in rasters]

    def get_level(self, result):
        if result:
            level = 'Info'
        else:
            level = 'Error'
        return level

    def add(self, **kwargs):

        setting_id = kwargs.get('setting_id')
        if not setting_id: raise AssertionError("setting_id unknown")

        raster = kwargs.get('raster')
        if not raster: raise AssertionError("raster unknown")
        raster = self.raster_to_string(raster)

        check = kwargs.get('check')
        if not check: raise AssertionError("check unknown")
        assert check in range(1, 16)

        result = kwargs.get('result')
        if not isinstance(result, bool): raise AssertionError("result unknown")

        # level = kwargs.get('level')
        # if not level: raise AssertionError("level unknown")
        level = self.get_level(result)
        assert level in ['Error', 'Warning', 'Info', 'Debug']

        add_result = {
            'level': level,
            'setting_id': setting_id,
            'raster': raster,
            'check': check,
            'result': result
        }

        if add_result in self.result_list:
            raise AssertionError("result allready exists")
        else:
            self.result_list.append(add_result)

    def sort(self):
        self.result_list = sorted(
            self.result_list,
            key=lambda elem: "%d %s %s" % (
                elem['setting_id'], elem['raster'], elem['check'])
        )

    def add_messages(self):
        pass

    def result_to_log_row(self, result_line):
        """
        go from dict to list (to add in the .log file) and add a message
        :param result_line: dict
        :return: string
        """
        log_row = []
        level = result_line.get('level')
        setting_id = str(result_line.get('setting_id'))
        raster = result_line.get('raster')
        check = result_line.get('check')
        result = str(result_line.get('result'))
        msg = 'check_message_blabla'
        msg_return = '%s, %s, %s, %s, %s, %s \n' % (
            level, setting_id, raster, check, result, msg)
        return msg_return

    def save(self):
        timestr = time.strftime("_%Y%m%d_%H%M%S")
        log_dir, sqltname_with_ext = os.path.split(self.sqlite_path)
        sqltname_without_ext = os.path.splitext(sqltname_with_ext)[0]
        self.log_path = log_dir + sqltname_without_ext + timestr + '.log'

        # write to log
        try:
            log_file = open(self.log_path, 'w')
            for result_row in self.result_list:
                log_row = self.result_to_log_row(result_row)
                log_file.write(log_row)
            log_file.close()
        except Exception as e:
            log.error(e)
            raise Exception ('cannot write log to file %s' % self.log_path)


#
# sqlite_dir = '/home/renier.kramer/Desktop/raster_checker_data/testdata'
# results = RasterCheckerResults(sqlite_dir)
#
# results.add(level='Error',
#                id=3,
#                raster='xx.tif',
#                check='check4',
#                result= True
#                )
#
#
# results.add(level='Error',
#                id=1,
#                raster='xx.tif',
#                check='check4',
#                result= True
#                )
#
#
# results.add(level='Error',
#                id=1,
#                raster='xx.tif',
#                check='check3',
#                result= True
#                )
#
# results.add(level='Warning',
#                id=2,
#                raster='xx.tif',
#                check='check4',
#                result= True
#                )
#
# results
#
# results.sort()
#
# results
#
# # results.add(id=2,
# #                level='Error',
# #                raster='xx.tif',
# #                check='check4',
# #                msg='hello')
#
# kwargs = {"arg3": 3, "arg2": "two", "arg1": 5}
# results.add(**kwargs)
#
#
#
#
#
#
#     def __setitem__(self, key, item):
#         self.__dict__[key] = item
#
#     def __getitem__(self, key):
#         return self.__dict__[key]
#
#     def __repr__(self):
#         return repr(self.__dict__)
#
#     def clear(self):
#         return self.__dict__.clear()
#
#     def copy(self):
#         return self.__dict__.copy()
#
#     def has_key(self, k):
#         return k in self.__dict__
#
#     def update(self, **kwargs):
#         if self.check_update(**kwargs):
#             return self.__dict__.update(**kwargs)
#         else:
#             raise Exception
#
#     def keys(self):
#         return self.__dict__.keys()
#
#     def values(self):
#         return self.__dict__.values()
#
#     def items(self):
#         return self.__dict__.items()
#
#     def pop(self, *args):
#         return self.__dict__.pop(*args)
#
#     def check_update(self, **kwargs):
#         keys = kwargs.keys()
#         check_white_list = keys() in [
#             'level, setting_id, raster, check, msg']
#         check_duplicate = set(keys) == keys
#         if check_white_list and check_duplicate:
#               return True
#         else:
#             raise Exception
#
#     def sort_logfile(self):
#         pass
#
#     def write_logfile(self):
#         timestr = time.strftime("_%Y%m%d_%H%M%S")
#         pass
#
#     def introduction(self):
#         msg = '-- Intro: --\n' \
#               'The RasterChecker checks your rasters based on the raster ' \
#               'references in your sqlite. \n' \
#               'This is done per v2_global_settings id (model entree). \n' \
#               'The following checks are executed: \n\n' \
#               '-- Per individual raster: -- \n' \
#               'check 1: Does the model entree refer to at least one raster?\n' \
#               'check 2: Do these referenced rasters exists? \n' \
#               'check 3: Is the raster filename valid? \n' \
#               'check 4: Is the raster single band? \n' \
#               'check 5: Is the nodata value -9999? \n' \
#               'check 6: Does raster have UTM projection (unit in meters)? \n' \
#               'check 7: Is the data type float 32? \n' \
#               'check 8: Is the raster compressed? (compression=deflate) \n' \
#               'check 9: Are the pixels square? \n' \
#               'check 10: No extreme pixel values? (dem: -10kmMSL<x<10kmMSL,'\
#               ' other rasters: 0<x<10k) \n\n' \
#               '-- Raster comparison: -- \n' \
#               'check 11: Is the cumulative pixel count of all rasters in one ' \
#               'model entree < 1 billion? \n' \
#               'check 12: Is the projection equal to the dem projection? \n' \
#               'check 13: Is the pixel size equal to the dem pixel size? \n' \
#               'check 14: Is the number of data/nodata pixels equal to the '\
#               'dem? \n' \
#               'check 15: Is the number of rows-colums equal to the dem? \n\n' \
#               '-- Pixel comparison: -- \n' \
#               'check 16: Are pixels correctly aligned when comparing the ' \
#               'dem with another raster: ?\n\n ' \
#               '-- Report: --\n' \
#               'Level, setting_id, raster, check, message \n'
#
#     def __cmp__(self, dict_):
#         return self.__cmp__(self.__dict__, dict_)
#
#     def __contains__(self, item):
#         return item in self.__dict__
#
#     def __iter__(self):
#         return iter(self.__dict__)
#
#     def __unicode__(self):
#         return unicode(repr(self.__dict__))
#
# sqlite_dir = '/home/renier.kramer/Desktop/raster_checker_data/testdata'
# results = RasterCheckerResults(sqlite_dir)
#
# results.add(id=1,
#                level='Error',
#                raster='xx.tif',
#                check='check4',
#                msg='hello')
# results.add(id=2,
#                level='Error',
#                raster='xx.tif',
#                check='check4',
#                msg='hello')
#
# print results
#
# o = Mapping()
# o.foo = "bar"
# o['lumberjack'] = 'foo'
# o.update({'a': 'b'}, c=44)
# print 'lumberjack' in o
# print o
#
# In [187]: run mapping.py
# True
# {'a': 'b', 'lumberjack': 'foo', 'foo': 'bar', 'c': 44}
#
#
#




# class RasterCheckerLog(object):
#     def __init__(self, sqlite_path):
#         self.log_db = {
#             'setting_id': int(),
#             ''
#
#
#
#
#
#     def open_logfile(self):
#         log_path = sqlite_path
#
#             self.sqltname_without_ext + timestr + '.log'
#
#
#         self.log_path = os.path.join(self.sqlite_dir, log_with_ext)
#         # write to log
#         try:
#             log_file = open(self.log_path, 'w')
#             for message_row in self.messages:
#                 log_file.write(message_row)
#             log_file.close()
#         except Exception as e:
#             log.error(e)
#

