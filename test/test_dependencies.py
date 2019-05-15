from ThreeDiToolbox import dependencies


def test_check_importability_1():
    importable = ["numpy"]
    missing = dependencies._check_importability(importable)
    assert missing == [], "numpy isn't missing"


def test_check_importability_2():
    partially_not_importable = ["numpy", "reinout"]
    missing = dependencies._check_importability(partially_not_importable)
    assert missing == ["reinout"], "reinout is not importable, so it should be missing"


def test_check_requirements_1():
    requirements_that_are_present = ["numpy", "setuptools"]
    dependencies._check_requirements(requirements_that_are_present)


def test_check_requirements_2():
    requirements_some_missing = ["numpy", "reinout"]
    missing = dependencies._check_requirements(requirements_some_missing)
    assert missing == ["reinout"], "reinout is not installed, so it should be missing"


def test_try_to_import_dependencies_smoke():
    # Should just run without errors as we have a correct test setup.
    dependencies.try_to_import_dependencies()
