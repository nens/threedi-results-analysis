from pathlib import Path
from ThreeDiToolbox import dependencies


available_dependency = dependencies.Dependency("numpy", "numpy", "")
missing_dependency = dependencies.Dependency("reinout", "reinout", "")


def test_check_importability():
    # Everything should just be importable.
    dependencies.check_importability()


def test_check_presence_1():
    dependencys_that_are_present = [available_dependency]
    dependencies._check_presence(dependencys_that_are_present)


def test_check_presence_2():
    dependencies_some_missing = [available_dependency, missing_dependency]
    missing = dependencies._check_presence(dependencies_some_missing)
    assert missing == [
        missing_dependency
    ], "reinout is not installed, so it should be missing"


def test_ensure_everything_installed_smoke():
    # Should just run without errors as we have a correct test setup.
    dependencies.ensure_everything_installed()


def test_install_dependencies(tmpdir):
    small_dependencies = [
        dependency
        for dependency in dependencies.DEPENDENCIES
        if dependency.name == "lizard-connector"
    ]
    dependencies._install_dependencies(small_dependencies, target_dir=tmpdir)
    installed_directory = Path(tmpdir) / "lizard_connector"
    assert installed_directory.exists()


def test_generate_constraints_txt(tmpdir):
    target_dir = Path(tmpdir)
    dependencies.generate_constraints_txt(target_dir=target_dir)
    generated_file = target_dir / "constraints.txt"
    assert "lizard-connector" in generated_file.read_text()
