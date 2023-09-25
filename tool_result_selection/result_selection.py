# (c) Nelen & Schuurmans, see LICENSE.rst.
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtCore import QObject
from qgis.core import QgsSettings
from qgis.PyQt.QtWidgets import QFileDialog
from threedi_schema import ThreediDatabase
from threedi_schema import errors
from ThreeDiToolbox.utils.user_messages import pop_up_info
from ThreeDiToolbox.utils.user_messages import pop_up_question
from ThreeDiToolbox.utils.utils import backup_sqlite
import os
import logging
import shutil

logger = logging.getLogger(__name__)


class ThreeDiResultSelection(QObject):

    schematisation_selected = pyqtSignal(str)

    def __init__(self, iface, layer_manager):

        super().__init__()
        self.iface = iface

        self.icon_path = ":/plugins/ThreeDiToolbox/icons/icon_add_datasource.png"
        self.menu_text = u"Select 3Di schematisation"
        self.layer_manager = layer_manager

    def run(self):
        # Show dialog and load schematisation
        settings = QgsSettings("3di", "qgisplugin")

        try:
            init_path = settings.value("last_used_spatialite_path", type=str)
        except TypeError:
            logger.debug(
                "Last used datasource path is no string, setting it to our home dir."
            )
            init_path = os.path.expanduser("~")

        filepath, __ = QFileDialog.getOpenFileName(
            None, "Open 3Di model spatialite file", init_path, "Spatialite (*.sqlite)"
        )

        if filepath == "":
            return False

        model_checker_db = ThreediDatabase(filepath)
        schema = model_checker_db.schema
        try:
            schema.validate_schema()
            schema.set_spatial_indexes()
        except errors.MigrationMissingError:
            warn_and_ask_msg = (
                "The selected spatialite cannot be used because its database schema version is out of date. "
                "Would you like to migrate your spatialite to the current schema version?"
            )
            do_migration = pop_up_question(warn_and_ask_msg, "Warning")
            if not do_migration:
                return False
            backup_filepath = backup_sqlite(filepath)
            schema.upgrade(backup=False, upgrade_spatialite_version=True)
            schema.set_spatial_indexes()
            shutil.rmtree(os.path.dirname(backup_filepath))
        except errors.UpgradeFailedError:
            msg = (
                "There are errors in the spatialite. Please re-open this file in QGIS 3.16, run the model checker and "
                "fix error messages. Then attempt to upgrade again. For questions please contact the servicedesk."
            )
            pop_up_info(msg, "Warning")
            return False


        self.add_spatialite_connection(filepath, self.iface)
        settings.setValue("last_used_spatialite_path", os.path.dirname(filepath))

        self.layer_manager._on_set_schematisation(filepath)

    def add_spatialite_connection(self, spatialite_path, iface):
        """Add spatialite_path as a spatialite connection in the qgis-browser"""
        filename = os.path.basename(spatialite_path)
        QgsSettings().setValue(
            f"SpatiaLite/connections/{filename}/sqlitepath", spatialite_path
        )
        iface.reloadConnections()


       