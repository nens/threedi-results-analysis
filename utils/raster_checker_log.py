import time
import os
import logging
from jinja2 import Template

from ThreeDiToolbox.utils.constants import RASTER_CHECKER_MAPPER

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

    def check_incomming(self, **kwargs):
        setting_id = kwargs.get('setting_id')
        if not setting_id: raise AssertionError("setting_id unknown")

        raster = kwargs.get('raster')
        if not raster: raise AssertionError("raster unknown")

        check_id = kwargs.get('check_id')
        # TODO: let this range below depend on the map dict keys
        if not check_id: raise AssertionError("check unknown")
        if not check_id in range(1, 17): raise AssertionError(
            "check_id unknown")

        result = kwargs.get('result')
        if not isinstance(result, bool): raise AssertionError("result unknown")

        add_result = {
            'setting_id': setting_id,
            'raster': raster,
            'check_id': check_id,
            'result': result
        }

        if add_result in self.result_list:
            raise AssertionError("result already exists")
        else:
            return add_result

    def _add(self, **kwargs):
        result = self.check_incomming(**kwargs)
        self.result_list.append(result)

    def _sort(self):
        # sorts a list with dicts based on 3 keys (setting_id, raster filename,
        # check nr) so that log file becomes easier to read
        self.result_list = sorted(
            self.result_list, key=lambda elem: "%02d %s %02d" % (
                int(elem['setting_id']), elem['raster'], int(elem['check_id'])))

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

    def result_row_to_msg(self, result_row):
        setting_id = result_row.get('setting_id')
        check_id = result_row.get('check_id')
        raster = result_row.get('raster')
        result = result_row.get('result')
        feedback_dict = self.get_feedback_dict(check_id)
        feedback_level = self.get_feedback_level(feedback_dict, result)
        template_feedback = self.get_template_feedback(
            feedback_dict, feedback_level)
        rendered_feedback = self.get_rendered_feedback(
            raster, template_feedback)
        msg = '%s, %s, %02d, %s \n' % (
            feedback_level, setting_id, check_id, rendered_feedback)
        return msg

    def get_intro_lines(self, check_phase):
        checkid_description = [(chck.get('check_id'), chck.get('description'))
                               for chck in RASTER_CHECKER_MAPPER if
                               chck.get('phase') in check_phase]
        return checkid_description

    def write_intro_lines(self, checkid_description):
        for (check_id, check_description) in checkid_description:
            temp_msg = Template(check_description)
            render_msg = temp_msg.render(check_id=check_id)
            self.log_file.write(render_msg + '\n')

    def add_intro(self):
        """enters some (general) explaining lines."""
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

        msg = '\n-- Raster comparison: -- \n'
        self.log_file.write(msg)
        checkid_description = self.get_intro_lines(check_phase=[3])
        self.write_intro_lines(checkid_description)

        msg = '\n-- Pixel allignment: -- \n'
        self.log_file.write(msg)
        checkid_description = self.get_intro_lines(check_phase=[4])
        self.write_intro_lines(checkid_description)

        msg = '\n-- Report: -- \n' \
              'level, setting_id, check_id, feedback \n'
        self.log_file.write(msg)

    def write_log(self):
        timestr = time.strftime("_%Y%m%d_%H%M%S")
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
        for result_row in self.result_list:
            log_row = self.result_row_to_msg(result_row)
            self.log_file.write(log_row)

