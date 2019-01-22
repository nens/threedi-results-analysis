import time
import os
import logging
from jinja2 import Template

from ThreeDiToolbox.utils.constants import RASTER_CHECKER_MAPPER

log = logging.getLogger(__name__)


class RasterCheckerResults(object):
    def __init__(self, sqlite_path):
        self.sqlite_path = sqlite_path
        self.result_per_check = []
        self.result_per_phase = []
        self.log_path = None
        self._last_phase = None

    def __repr__(self):
        return repr(self.__dict__)

    def __contains__(self, item):
        return item in self.__dict__

    def check_incomming(self, **kwargs):
        setting_id = kwargs.get('setting_id')
        if not setting_id: raise AssertionError("setting_id unknown")

        raster = kwargs.get('raster')
        if not raster: raise AssertionError("raster unknown")

        check_id = kwargs.get('check_id')
        # TODO: let this range below depend on the map dict keys
        if not check_id: raise AssertionError("check unknown")
        if not check_id in range(1, 18): raise AssertionError(
            "check_id unknown")

        result = kwargs.get('result')
        if not isinstance(result, bool): raise AssertionError("result unknown")

        detail = kwargs.get('detail')
        if not isinstance(detail, str):
            raise AssertionError("details wrong type")

        add_result = {'setting_id': setting_id,
                      'raster': raster,
                      'check_id': check_id,
                      'result': result,
                      'detail': detail,
                      }

        if self.not_already_exists(add_result):
            return add_result

    def not_already_exists(self, add_result):
        # on purpose only include keys: setting_id, raster, and check_id. Why?
        # - We do not want e.g. 2 results (True and False) for setting_id=1,
        #   raster=abc.tif, and check_id=2
        check_keys = ['setting_id', 'raster', 'check_id']
        check_dict = dict((key, value) for key, value in
                          add_result.iteritems() if key in check_keys)
        if check_dict in self.result_per_check:
            raise AssertionError("result already exists")
        else:
            return True

    def _add(self, **kwargs):
        result = self.check_incomming(**kwargs)
        self.result_per_check.append(result)

    def sort_results(self):
        """
        sort 2 lists with result dicts (result_per_check and result_per_phase)
        so that when we convert dict to log file, this log file becomes
        easier to read
        :param: -
        :return: -
        """
        self.result_per_check = sorted(
            self.result_per_check, key=lambda elem: "%02d %s %02d" % (
                int(elem['setting_id']), elem['raster'], int(elem['check_id'])))
        self.result_per_phase = sorted(
            self.result_per_phase, key=lambda elem: "%02d %02d %s" % (
                int(elem['phase']), int(elem['setting_id']), elem['raster']))

    def get_block_check_ids(self, check_phase):
        """
        get id of all checks that are blocking per phase
        Wheter a check is blocking is defined in RASTER_CHECKER_MAPPER
        :param check_phase: int
        :return: list with int e.g [1, 2, 3] of blocking check per phase
        """
        return [chck.get('check_id') for chck in RASTER_CHECKER_MAPPER if
                chck.get('phase') == check_phase and
                chck.get('blocking') is True]

    def update_result_per_phase(self, setting_id, rasters, phase):
        """
        blabla
        :param setting_id: int
        :param rasters: list of strings (relative path of raster)
        :param phase: int
        :return:
        """
        block_check_ids_phase = self.get_block_check_ids(phase)
        # in phase 3, 4 and 5 the dem is never added to self.result_per_check
        # as other rasters are then compared with the dem
        # the dem is first element of rasters
        if phase in [3, 4, 5]:
            rasters = rasters[1:]
        for rast_item in rasters:
            cnt_succes = len([result for result in self.result_per_check if
                          result['result'] is True and
                          result['check_id'] in block_check_ids_phase and
                          result['setting_id'] == setting_id and
                          result['raster'] == rast_item])
            phase_result = (cnt_succes == len(block_check_ids_phase))
            to_add = {
                'phase': phase,
                'setting_id': setting_id,
                'raster': rast_item,
                'result': phase_result
            }
            self.result_per_phase.append(to_add)

    def get_rasters_ready(self, setting_id, phase):
        rasters_ready = [result.get('raster') for result in
                         self.result_per_phase if
                         result['result'] is True and
                         result['setting_id'] == setting_id and
                         result['phase'] == (phase-1)]  # check previous phase
        return list(set(rasters_ready))

    def get_feedback_level(self, feedback_dict, result):
        if result:
            feedback_level = 'info'
        else:
            if feedback_dict.get('error'):
                feedback_level = 'error'
            elif feedback_dict.get('warning'):
                feedback_level = 'warning'
            else:
                raise AssertionError('feedback dict cannot have both warning '
                                     'and error message')
        return feedback_level

    def get_template_feedback(self, feedback_dict, feedback_level):
        feedback = feedback_dict.get(feedback_level)
        template_feedback = Template(feedback)
        return template_feedback

    def get_feedback_dict(self, check_id):
        # Each method (raster_check) has its own user feedback
        feedback_dict = [chck.get('feedback') for chck in RASTER_CHECKER_MAPPER
                         if check_id == chck.get('check_id')]
        if len(feedback_dict) != 1:
            raise AssertionError("too little/many rows")
        return feedback_dict[0]

    def get_rendered_feedback(self, raster, template_feedback):
        rendered_feedback = template_feedback.render(
            raster=raster, result=template_feedback)
        return rendered_feedback

    def result_per_check_to_msg(self, result_row):
        """
        this function converts a single result (unique per setting_id,
        check_id, and raster) to string
        :param result_row: dict
        :return: msg: string
        """
        setting_id = result_row.get('setting_id')
        check_id = result_row.get('check_id')
        raster = result_row.get('raster')
        result = result_row.get('result')
        detail = result_row.get('detail')

        feedback_dict = self.get_feedback_dict(check_id)
        feedback_level = self.get_feedback_level(feedback_dict, result)
        template_feedback = self.get_template_feedback(
            feedback_dict, feedback_level)
        rendered_feedback = self.get_rendered_feedback(
            raster, template_feedback)
        msg = '%s, %s, %02d, %s %s \n' % (
            feedback_level, setting_id, check_id, rendered_feedback, detail)
        return msg

    def add_found_rasters(self, all_raster_ref):
        msg = '\n-- Found following raster references: -- \n'
        self.log_file.write(msg)
        for xx in all_raster_ref:
            table = xx[0]
            setting_id = xx[1]
            column = xx[2]
            raster = xx[3]
            msg = 'table:%s, id:%d, column:%s, raster:%s \n' % (
                table, setting_id, column, raster)
            self.log_file.write(msg)

    def get_intro_lines(self, check_phase):
        """
        :param check_phase: list with int(s)
        :return: check_description: string
        """
        checkid_description = [(chck.get('check_id'), chck.get('description'))
                               for chck in RASTER_CHECKER_MAPPER if
                               chck.get('phase') in check_phase]
        if checkid_description is None:
            raise AssertionError('each check should have a description')
        return checkid_description

    def write_intro_lines(self, checkid_description):
        for (check_id, check_description) in checkid_description:
            temp_msg = Template(check_description)
            render_msg = temp_msg.render(check_id=check_id)
            self.log_file.write(render_msg + '\n')

    @property
    def last_check_phase(self):
        """ returns last checkphase (int) of RASTER_CHECKER_MAPPER """
        if self._last_phase is None:
            self._last_phase = max([chck.get('phase') for chck in
            RASTER_CHECKER_MAPPER])
        return self._last_phase

    def add_intro(self):
        """ enters some (general) explaining lines."""
        msg = '-- Intro: --\n' \
              'The RasterChecker checks your rasters based on the raster ' \
              'references in your sqlite. \n' \
              'This is done for all v2_global_setting rows. The following ' \
              'checks are executed: \n'
        self.log_file.write(msg)

        msg = '\n-- Per individual raster: -- \n'
        self.log_file.write(msg)
        checkid_description = self.get_intro_lines(check_phase=[1, 2])
        self.write_intro_lines(checkid_description)

        msg = '\n-- All rasters per setting_id at once: -- \n'
        self.log_file.write(msg)
        checkid_description = self.get_intro_lines(check_phase=[3])
        self.write_intro_lines(checkid_description)

        msg = '\n-- Raster comparison: -- \n'
        self.log_file.write(msg)
        checkid_description = self.get_intro_lines(check_phase=[4])
        self.write_intro_lines(checkid_description)

        msg = '\n-- Pixel allignment: -- \n'
        self.log_file.write(msg)
        checkid_description = self.get_intro_lines(check_phase=[5])
        self.write_intro_lines(checkid_description)

    def result_per_check_to_log(self):
        # add self.result_per_check to log_file
        msg = '\n-- Report: -- \n' \
              'level, setting_id, check_id, feedback \n'
        self.log_file.write(msg)
        for result_row in self.result_per_check:
            log_row = self.result_per_check_to_msg(result_row)
            self.log_file.write(log_row)

    def result_per_phase_to_log(self):
        # add self.result_per_phase to log_file
        msg = '\n -- Sequence details: -- \n'
        self.log_file.write(msg)
        added_something = False

        skip_raster_id = []

        for result_row in self.result_per_phase:
            if result_row.get('result') is False:
                phase = result_row.get('phase')
                setting_id = result_row.get('setting_id')
                raster = result_row.get('raster')
                if phase in [1, 2] and \
                        (setting_id, raster) not in skip_raster_id:
                    added_something = True
                    check_ids = self.get_block_check_ids(phase)
                    msg = 'setting_id %d: %s failed on at least one of ' \
                          'checks %s. Therefore we could not continue ' \
                          'with this raster \n' % (
                        setting_id, raster, str(check_ids))
                    self.log_file.write(msg)
                    skip_raster_id.append((setting_id, raster))
                elif phase in [3, 4] and \
                        (setting_id, raster) not in skip_raster_id:
                    added_something = True
                    check_ids = self.get_block_check_ids(phase)
                    msg = 'setting_id %d: either %s failed on at least one of ' \
                          'checks %s, or dem of this setting_id did not ' \
                          'reach these checks. Therefore we could not ' \
                          'continue with this raster \n' % (
                              setting_id, raster, str(check_ids))
                    self.log_file.write(msg)
                    skip_raster_id.append((setting_id, raster))
        if not added_something:
            msg = 'all checks have been done on all rasters'
            self.log_file.write(msg)

    def write_log(self, all_raster_ref):
        timestr = time.strftime("_%Y%m%d_%H%M")
        log_dir, sqltname_with_ext = os.path.split(self.sqlite_path)
        sqltname_without_ext = os.path.splitext(sqltname_with_ext)[0]
        self.log_path = log_dir + '/' + sqltname_without_ext + timestr + '.log'

        try:
            self.log_file = open(self.log_path, 'a+')
        except Exception as e:
            log.error(e)
            raise Exception('RasterChecker can not write to logfile '
                            'directory %s' % self.log_path)

        self.add_intro()
        self.add_found_rasters(all_raster_ref)
        self.result_per_check_to_log()
        self.result_per_phase_to_log()
        self.log_file.close()

