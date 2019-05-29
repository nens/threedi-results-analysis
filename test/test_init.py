# coding=utf-8
"""Tests QGIS plugin init."""

from pathlib import Path

import configparser
import logging
import os
import unittest


logger = logging.getLogger(__name__)

TEST_DATA_DIR = Path(__file__).parent.joinpath("data")


class TestInit(unittest.TestCase):
    """Test that the plugin init is usable for QGIS.

    Based heavily on the validator class by Alessandro
    Passoti available here:

    http://github.com/qgis/qgis-django/blob/master/qgis-app/
             plugins/validator.py

    """

    def test_read_init(self):
        """Test that the plugin __init__ will validate on plugins.qgis.org."""

        # You should update this list according to the latest in
        # https://github.com/qgis/qgis-django/blob/master/qgis-app/
        #        plugins/validator.py

        required_metadata = [
            "name",
            "description",
            "version",
            "qgisMinimumVersion",
            "email",
            "author",
        ]

        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, "metadata.txt")
        )
        logger.info(file_path)
        metadata = []
        parser = configparser.ConfigParser()
        parser.optionxform = str
        parser.read(file_path, encoding="utf-8")
        message = 'Cannot find a section named "general" in %s' % file_path
        assert parser.has_section("general"), message
        metadata.extend(parser.items("general"))

        for expectation in required_metadata:
            message = 'Cannot find metadata "%s" in metadata source (%s).' % (
                expectation,
                file_path,
            )

            self.assertIn(expectation, dict(metadata), message)


if __name__ == "__main__":
    unittest.main()
