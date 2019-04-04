import unittest
import logging
from ThreeDiToolbox.utils.qlogging import setup_logging


class TestLogging(unittest.TestCase):
    def test_logging(self):

        setup_logging()

        log = logging.getLogger("test")

        log.warning("test message")

        self.assertEqual(1, 1)
