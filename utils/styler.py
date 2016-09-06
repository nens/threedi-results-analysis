import os
import logging

log = logging.getLogger(__name__)



class Styler(object):

    root = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.path.pardir, 'layer_styles')

    @classmethod
    def apply_style(cls, layer, style_name, stype='tools'):
        style = os.path.join(os.path.join(cls.root,
                                          stype,
                                          "{0}.qml".format(style_name)))
        if os.path.exists(style):
            layer.loadNamedStyle(style)
        else:
            log.info("Style not exist {0}".format(style))

        return
