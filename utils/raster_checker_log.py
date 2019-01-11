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

        check = kwargs.get('check')
        # TODO: let this range below depend on the map dict keys
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
            raise AssertionError("result already exists")
        else:
            self.result_list.append(add_result)

    def sort(self):
        # sorts a list with dicts based on 3 keys so that when we transfer
        # these dicts into a log file, the log file is more user-friendly
        self.result_list = sorted(
            self.result_list, key=lambda elem: "%d %s %s" % (
                int(elem['setting_id']), elem['raster'], int(elem['check'])))
        print 'hallo'
        for i in self.result_list:
            print i

        self.result_list = sorted(
            self.result_list, key=lambda elem: "%d %s %s" % (
                int(elem['setting_id']), elem['raster'], int(elem['check'])))
        print 'hallo'
        for i in self.result_list:
            print i


    def add_messages(self):
        pass

    def result_row_to_log_row(self, result_line):
        """
        go from dict to list (to add in the .log file) and add a message
        :param result_line: dict
        :return: string
        """
        level = result_line.get('level')
        setting_id = str(result_line.get('setting_id'))
        raster = result_line.get('raster')
        check = str(result_line.get('check'))
        msg = 'check_message_blabla'
        msg_return = '%s, %s, %s, %s, %s \n' % (
            level, setting_id, check, raster, msg)
        return msg_return

    def add_intro(self):
        """enters some (general) explaining lines."""
        msg = '-- Intro: --\n' \
              'The RasterChecker checks your rasters based on the raster ' \
              'references in your sqlite. \n' \
              'This is done per v2_global_settings id. The following ' \
              'checks are executed: \n\n' \
              '-- Per individual raster: -- \n' \
              'check 1: Does the referenced rasters (in all v2_tables) ' \
              'exist on your machine?\n' \
              'check 2: Is the extension .tif or .tiff? \n' \
              'check 3: Is the raster filename valid? \n' \
              'check 4: Is the raster single band? \n' \
              'check 5: Is the nodata value -9999? \n' \
              'check 6: Does raster have UTM projection (unit: meters)? \n' \
              'check 7: Is the data type float 32? \n' \
              'check 8: Is the raster compressed? (compression=deflate) \n' \
              'check 9: Are the pixels square? \n' \
              'check 10: Does the pixelsize have max 3 decimal places? \n' \
              'check 11: No extreme pixel values? (dem: -10kmMSL<x<10kmMSL,' \
              ' other rasters: 0<x<10k) \n\n' \
              '-- Raster comparison: -- \n' \
              'check 12: Is the projection equal to the dem projection? \n' \
              'check 13: Is the pixel size equal to the dem pixel size? \n' \
              'check 14: Is the number of data/nodata pixels equal to the ' \
              'dem? \n' \
              'check 15: Is the number of rows-colums equal to the dem? \n\n' \
              '-- Pixel comparison: -- \n' \
              'check 16: Are pixels correctly aligned when comparing the ' \
              'dem with another raster:?\n\n ' \
              '-- Report: --\n' \
              'Level, setting_id, check_nr, raster, message \n'
        self.log_file = open(self.log_path, 'w')
        self.log_file.write(msg)
        self.log_file.close()

    def save(self):
        timestr = time.strftime("_%Y%m%d_%H%M%S")
        log_dir, sqltname_with_ext = os.path.split(self.sqlite_path)
        sqltname_without_ext = os.path.splitext(sqltname_with_ext)[0]
        self.log_path = log_dir + '/' + sqltname_without_ext + timestr + '.log'

        # write to log
        try:
            self.add_intro()
            self.log_file = open(self.log_path, 'a+')
            for result_row in self.result_list:
                log_row = self.result_row_to_log_row(result_row)
                self.log_file.write(log_row)
            self.log_file.close()
        except Exception as e:
            log.error(e)
            raise Exception ('RasterChecker succeeded, but can not write '
                             'logfile to dir %s' % self.log_path)
