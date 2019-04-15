# coding=utf-8
"""Common functionality used by regression tests."""
from __future__ import absolute_import

from contextlib import contextmanager
from qgis.core import QgsApplication
import logging
import shutil
import sys
import tempfile

logger = logging.getLogger(__name__)
_singletons = {}


def ensure_qgis_app_is_initialized():
    """Make sure qgis is initialized for testing."""
    if 'app' not in _singletons:
        app = QgsApplication([], False)
        app.initQgis()
        logger.debug("Initialized qgis (for testing). Settings: %s",
                     app.showSettings())
        _singletons['app'] = app


@contextmanager
def TemporaryDirectory():
    name = tempfile.mkdtemp()
    try:
        yield name
    finally:
        shutil.rmtree(name)
