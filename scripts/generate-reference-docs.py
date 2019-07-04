from ThreeDiToolbox import PLUGIN_DIR


DOC_SOURCE_DIR = PLUGIN_DIR / "doc" / "source"



def generate_subdir_readme_symlinks():
    """Create a symlink for every README in a direct subdirectory."""
    for readme in PLUGIN_DIR.glob('*/README.rst'):
        subdir_name = readme.parent.name
        target_name = f"linked_{subdir_name}_readme.rst"
        target = DOC_SOURCE_DIR / target_name
        # Relative: an absolute symlink (in the docker) doesn't work locally.
        relative_symlink = f"../../{subdir_name}/README.rst"
        if not target.exists():
            target.symlink_to(relative_symlink)
            print(f"Added symlink {target_name} to {relative_symlink}")


def main():
    generate_subdir_readme_symlinks()


if __name__ == "__main__":
    main()
