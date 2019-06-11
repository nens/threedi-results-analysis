# Pytest configuration file. The sole purpose is to prevent Qgis from grabbing
# python's import mechanism (which breaks pytest).
import os

os.environ["QGIS_NO_OVERRIDE_IMPORT"] = "KEEPYOURPAWSOFF"
