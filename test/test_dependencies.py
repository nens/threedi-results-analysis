from ThreeDiToolbox import dependencies


available_dependency = dependencies.Dependency("numpy", "numpy", "")
missing_dependency = dependencies.Dependency("reinout", "reinout", "")


def test_check_importability_1():
    importable = ["numpy"]
    missing = dependencies._check_importability(importable)
    assert missing == [], "numpy isn't missing"


def test_check_importability_2():
    partially_not_importable = ["numpy", "reinout"]
    missing = dependencies._check_importability(partially_not_importable)
    assert missing == ["reinout"], "reinout is not importable, so it should be missing"


def test_check_presence_1():
    dependencys_that_are_present = [available_dependency]
    dependencies._check_presence(dependencys_that_are_present)


def test_check_presence_2():
    dependencies_some_missing = [available_dependency, missing_dependency]
    missing = dependencies._check_presence(dependencies_some_missing)
    assert missing == [
        missing_dependency
    ], "reinout is not installed, so it should be missing"


def test_try_to_import_dependencies_smoke():
    # Should just run without errors as we have a correct test setup.
    dependencies.try_to_import_dependencies()
