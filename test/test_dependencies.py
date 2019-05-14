from ThreeDiToolbox import dependencies

import pkg_resources
import pytest


def test_check_importability_1():
    missing = []
    importable = "numpy"
    dependencies._check_importability(importable, missing)
    assert missing == [], "numpy isn't missing"


def test_check_importability_2():
    missing = []
    not_importable = "reinout"
    dependencies._check_importability(not_importable, missing)
    assert missing == ["reinout"], "reinout is not importable, so missing"


def test_check_requirements_1():
    requirements_that_are_present = ["numpy", "setuptools"]
    dependencies._check_requirements(requirements_that_are_present)


def test_check_requirements_2():
    requirements_some_missing = ["numpy", "reinout"]
    with pytest.raises(pkg_resources.DistributionNotFound):
        dependencies._check_requirements(requirements_some_missing)


def test_try_to_import_dependencies_smoke():
    # Should just run without errors as we have a correct test setup.
    dependencies.try_to_import_dependencies()
