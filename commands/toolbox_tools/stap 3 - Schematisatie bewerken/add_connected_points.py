# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

import logging

from qgis.core import QgsMapLayerRegistry, QgsFeatureRequest
from PyQt4.QtCore import QPyNullVariant

from ThreeDiToolbox.utils.user_messages import messagebar_message
from ThreeDiToolbox.views.predict_calc_points_dialog import (
    AddCoonnectedPointsDialogWidget)
from ThreeDiToolbox.commands.base.custom_command import (
    CustomCommandBase)
from ThreeDiToolbox.utils.predictions import Predictor
from ThreeDiToolbox.utils import constants

log = logging.getLogger(__name__)


class CustomCommand(CustomCommandBase):
    """
    command to that will load and start an edit session for the connected
    point layer and verify the data added to that layer 
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.iface = kwargs.get('iface')
        self.ts_datasource = kwargs.get('ts_datasource')
        self.tool_dialog_widget = None

    def run(self):
        self.table_name = "v2_connected_pnt"
        connected_pnt_lyr = QgsMapLayerRegistry.instance().mapLayersByName(
            self.table_name
        )
        if connected_pnt_lyr:
            self.connected_pnt_lyr = connected_pnt_lyr[0]
            msg = 'Auto detected loaded connected_pnt layer!'
            self.supervising_user_input(msg)
        else:
            self.show_gui()


    def show_gui(self):
        self.tool_dialog_widget = AddCoonnectedPointsDialogWidget(command=self)
        self.tool_dialog_widget.exec_()  # block execution

    def run_it(self, db_set, db_type):
        pal = Predictor(flavor=db_type)
        uri = pal.get_uri(**db_set)
        self.connected_pnt_lyr = pal.get_layer_from_uri(
            uri, self.table_name, 'the_geom')
        QgsMapLayerRegistry.instance().addMapLayer(self.connected_pnt_lyr)
        msg = 'Loaded connected_pnt layer from {}!'.format(db_set['database'])
        self.supervising_user_input(msg)

    def supervising_user_input(self, msg):
        messagebar_message("Ready",  msg, level=0, duration=4)
        iter = self.connected_pnt_lyr.getFeatures()
        try:
            _feat = max(iter, key=lambda f: f['id'])
            self._feat_id = _feat['id'] + 1
        except ValueError:
            self._feat_id = 1
        self.connected_pnt_lyr.startEditing()

        self._added_features = []
        self.connected_pnt_lyr.featureAdded.connect(self.add_feature)
        self.connected_pnt_lyr.editCommandEnded.connect(
            self.on_edit_command_ended
        )

        self.field_names = [
            field.name() for field in self.connected_pnt_lyr.pendingFields()
        ]

    def add_feature(self, feature_id):
        """
        Currently it is not safe to do calls that modify vector layer data
        in slots connected to signals notifying about data change
        (such as featureAdded). The issue is that at the point when
        those signals are emitted, their underlying undo commands
        were not yet pushed onto the stack, so doing further editing calls
        causes corruption of undo stack (undo command for follow up operation
        is placed before the first operation).
        """
        if feature_id < 0:
            self._added_features.append(feature_id)

    def on_edit_command_ended(self):
        """
        Send all added features in the stack to _handle_added(). Really, this
        is just a delayed implementation of the action itself.
        """

        while self._added_features:
            fid = self._added_features.pop()
            self._handle_added(fid)
            self._feat_id += 1


    def _handle_added(self, feature_id):
        """
        Actually add the feature to the layer.
        """
        try:
            self.connected_pnt_lyr.beginEditCommand(
                u"Add to connected_pnt_lyr"
            )
            feat = self.connected_pnt_lyr.getFeatures(
                QgsFeatureRequest(feature_id)
            ).next()
            connected_pnt = dict(zip(self.field_names, feat.attributes()))

            calculation_pnt_id = connected_pnt['calculation_pnt_id']
            request = QgsFeatureRequest().setFilterExpression(
                u'"calculation_pnt_id" = {}'.format(calculation_pnt_id))
            selected_features = self.connected_pnt_lyr.getFeatures(request)
            # QgsFeatureRequest has no count so we have to loop through the
            # feature set to get a count
            unique_ids = set()
            calc_type = None
            for item in selected_features:
                _item = dict(zip(self.field_names, item.attributes()))
                unique_ids.add(_item['id'])
                if calc_type is None or isinstance(calc_type, QPyNullVariant):
                    calc_type = _item['calc_type']
            thresh = constants.CONNECTED_PNTS_THRESHOLD[calc_type]
            if len(unique_ids) > thresh:
                msg = \
                    "Calculation type {} allows only for {} " \
                    "connected points! " \
                    "Deleting point...".format(calc_type, thresh)
                messagebar_message("Error",  msg, level=2, duration=3)
                self.connected_pnt_lyr.deleteFeature(feature_id)
            feat.setAttribute('calc_type', calc_type)
            feat.setAttribute('id', self._feat_id)
            exchange_depth = connected_pnt['exchange_depth']
            if isinstance(exchange_depth, QPyNullVariant):
                exchange_depth = -9999
            feat.setAttribute('exchange_depth', exchange_depth)
            self.connected_pnt_lyr.updateFeature(feat)

            self.connected_pnt_lyr.endEditCommand()
        except:
            self.connected_pnt_lyr.destroyEditCommand()
            raise
