from collections import OrderedDict, defaultdict
from itertools import chain
import json
import shutil
import os
from uuid import uuid4

UNC_PREFIX = "\\\\?\\"
FILE_MAX_PATH = 260
DIR_MAX_PATH = 248


def bypass_max_path_limit(path, is_file=False):
    """Check and modify path to bypass Windows MAX_PATH limitation."""
    path_str = str(path)
    if path_str.startswith(UNC_PREFIX):
        valid_path = path_str
    else:
        if is_file:
            if len(path_str) >= FILE_MAX_PATH:
                valid_path = f"{UNC_PREFIX}{path_str}"
            else:
                valid_path = path_str
        else:
            if len(path_str) > DIR_MAX_PATH:
                valid_path = f"{UNC_PREFIX}{path_str}"
            else:
                valid_path = path_str
    return valid_path


class LocalRevision:
    """Local revision directory structure representation."""

    def __init__(self, local_schematisation, revision_number=None, sqlite_filename=None):
        self.local_schematisation = local_schematisation
        self.number = revision_number
        self.sqlite_filename = sqlite_filename
        if not self.sqlite_filename and self.structure_is_valid():
            self.discover_sqlite()

    def structure_is_valid(self):
        """Check if all revision subpaths are present."""
        is_valid = all(os.path.exists(p) if p else False for p in self.subpaths)
        return is_valid

    @property
    def sub_dir(self):
        """Get schematisation revision subdirectory name."""
        if self.number:
            subdirectory = f"revision {self.number}"
            return subdirectory

    @property
    def main_dir(self):
        """Get schematisation revision main directory path."""
        if self.number:
            schematisation_dir_path = self.local_schematisation.main_dir
            schematisation_revision_dir_path = os.path.join(schematisation_dir_path, self.sub_dir)
            return schematisation_revision_dir_path

    @property
    def admin_dir(self):
        """Get schematisation revision admin directory path."""
        if self.number:
            admin_dir_path = os.path.join(self.main_dir, "admin")
            return admin_dir_path

    @property
    def grid_dir(self):
        """Get schematisation revision grid directory path."""
        if self.number:
            grid_dir_path = os.path.join(self.main_dir, "grid")
            return grid_dir_path

    @property
    def results_dir(self):
        """Get schematisation revision results directory path."""
        if self.number:
            grid_dir_path = os.path.join(self.main_dir, "results")
            return grid_dir_path

    @property
    def schematisation_dir(self):
        """Get schematisation revision schematisation directory path."""
        if self.number:
            grid_dir_path = os.path.join(self.main_dir, "schematisation")
            return grid_dir_path

    @property
    def raster_dir(self):
        """Get schematisation revision raster directory path."""
        if self.number:
            rasters_dir_path = os.path.join(self.main_dir, "schematisation", "rasters")
            return rasters_dir_path

    @property
    def sqlite(self):
        """Get schematisation revision sqlite filepath."""
        if not self.number:
            self.discover_sqlite()
            sqlite_filepath = (
                os.path.join(self.schematisation_dir, self.sqlite_filename) if self.sqlite_filename else None
            )
            return sqlite_filepath

    @property
    def subpaths(self):
        """Revision directory sub-paths."""
        paths = [
            self.admin_dir,
            self.grid_dir,
            self.results_dir,
            self.schematisation_dir,
            self.raster_dir,
        ]
        return paths

    def make_revision_structure(self, exist_ok=True):
        """Function for schematisation dir structure creation."""
        for subpath in self.subpaths:
            if subpath:
                os.makedirs(bypass_max_path_limit(subpath), exist_ok=exist_ok)

    def discover_sqlite(self):
        """Find schematisation revision sqlite filepath."""
        if self.number:
            for sqlite_candidate in os.listdir(self.schematisation_dir):
                if sqlite_candidate.endswith(".sqlite"):
                    self.sqlite_filename = sqlite_candidate
                    break

    def backup_sqlite(self):
        """Make a backup of the sqlite database."""
        backup_sqlite_path = None
        if self.sqlite_filename:
            backup_folder = os.path.join(self.schematisation_dir, "_backup")
            os.makedirs(bypass_max_path_limit(backup_folder), exist_ok=True)
            prefix = str(uuid4())[:8]
            backup_sqlite_path = os.path.join(backup_folder, f"{prefix}_{self.sqlite_filename}")
            shutil.copyfile(self.sqlite, bypass_max_path_limit(backup_sqlite_path, is_file=True))
        return backup_sqlite_path


class WIPRevision(LocalRevision):
    """Local Work In Progress directory structure representation."""

    @property
    def sub_dir(self):
        """Get schematisation revision subdirectory name."""
        subdirectory = "work in progress"
        return subdirectory

    @property
    def main_dir(self):
        """Get schematisation revision main directory path."""
        schematisation_dir_path = self.local_schematisation.main_dir
        schematisation_revision_dir_path = os.path.join(schematisation_dir_path, self.sub_dir)
        return schematisation_revision_dir_path

    @property
    def admin_dir(self):
        """Get schematisation revision admin directory path."""
        admin_dir_path = os.path.join(self.main_dir, "admin")
        return admin_dir_path

    @property
    def grid_dir(self):
        """Get schematisation revision grid directory path."""
        grid_dir_path = os.path.join(self.main_dir, "grid")
        return grid_dir_path

    @property
    def results_dir(self):
        """Get schematisation revision results directory path."""
        grid_dir_path = os.path.join(self.main_dir, "results")
        return grid_dir_path

    @property
    def schematisation_dir(self):
        """Get schematisation revision schematisation directory path."""
        grid_dir_path = os.path.join(self.main_dir, "schematisation")
        return grid_dir_path

    @property
    def raster_dir(self):
        """Get schematisation revision raster directory path."""
        rasters_dir_path = os.path.join(self.main_dir, "schematisation", "rasters")
        return rasters_dir_path

    @property
    def sqlite(self):
        """Get schematisation revision sqlite filepath."""
        self.discover_sqlite()
        sqlite_filepath = os.path.join(self.schematisation_dir, self.sqlite_filename) if self.sqlite_filename else None
        return sqlite_filepath

    def discover_sqlite(self):
        """Find schematisation revision sqlite filepath."""
        for sqlite_candidate in os.listdir(self.schematisation_dir):
            if sqlite_candidate.endswith(".sqlite"):
                self.sqlite_filename = sqlite_candidate
                break


class LocalSchematisation:
    """Local revision directory structure representation."""

    def __init__(self, working_dir, schematisation_pk, schematisation_name, parent_revision_number=None, create=False):
        self.working_directory = working_dir
        self.id = schematisation_pk
        self.name = schematisation_name
        self.revisions = OrderedDict()
        self.wip_revision = WIPRevision(self, parent_revision_number) if parent_revision_number is not None else None
        if create:
            self.build_schematisation_structure()

    def add_revision(self, revision_number):
        """Add a new revision."""
        local_revision = LocalRevision(self, revision_number)
        if revision_number in self.revisions and os.path.exists(local_revision.main_dir):
            shutil.rmtree(local_revision.main_dir)
        local_revision.make_revision_structure()
        self.revisions[revision_number] = local_revision
        self.write_schematisation_metadata()
        return local_revision

    def set_wip_revision(self, revision_number):
        """Set a new work in progress revision."""
        if self.wip_revision is not None and os.path.exists(self.wip_revision.main_dir):
            shutil.rmtree(self.wip_revision.main_dir)
        self.wip_revision = WIPRevision(self, revision_number)
        self.wip_revision.make_revision_structure()
        self.wip_revision.discover_sqlite()
        self.write_schematisation_metadata()
        return self.wip_revision

    def update_wip_revision(self, revision_number):
        """Update a work in progress revision number."""
        if self.wip_revision is not None and os.path.exists(self.wip_revision.main_dir):
            self.wip_revision.number = revision_number
            self.write_schematisation_metadata()
            return True
        else:
            return False

    @classmethod
    def initialize_from_location(cls, schematisation_dir):
        """Initialize local schematisation structure from the root schematisation dir."""
        local_schematisation = None
        if os.path.isdir(schematisation_dir):
            expected_config_path = os.path.join(schematisation_dir, "admin", "schematisation.json")
            if os.path.exists(expected_config_path):
                schema_metadata = cls.read_schematisation_metadata(expected_config_path)
                working_dir = os.path.dirname(schematisation_dir)
                schematisation_pk = schema_metadata["id"]
                schematisation_name = schema_metadata["name"]
                local_schematisation = cls(working_dir, schematisation_pk, schematisation_name)
                revision_numbers = schema_metadata["revisions"] or []
                for revision_number in revision_numbers:
                    local_revision = LocalRevision(local_schematisation, revision_number)
                    local_schematisation.revisions[revision_number] = local_revision
                wip_parent_revision_number = schema_metadata["wip_parent_revision"]
                if wip_parent_revision_number is not None:
                    local_schematisation.wip_revision = WIPRevision(local_schematisation, wip_parent_revision_number)
        return local_schematisation

    @staticmethod
    def read_schematisation_metadata(schematisation_config_path):
        """Read schematisation metadata from the JSON file."""
        schematisation_metadata = defaultdict(lambda: None)
        if os.path.exists(schematisation_config_path):
            with open(schematisation_config_path, "r+") as config_file:
                schematisation_metadata.update(json.load(config_file))
        return schematisation_metadata

    def write_schematisation_metadata(self):
        """Write schematisation metadata to the JSON file."""
        schematisation_metadata = {
            "id": self.id,
            "name": self.name,
            "revisions": [local_revision.number for local_revision in self.revisions.values()],
            "wip_parent_revision": self.wip_revision.number if self.wip_revision is not None else None,
        }
        with open(bypass_max_path_limit(self.schematisation_config_path, is_file=True), "w") as config_file:
            config_file_dump = json.dumps(schematisation_metadata)
            config_file.write(config_file_dump)

    def structure_is_valid(self):
        """Check if all schematisation subpaths are present."""
        subpaths_collections = [self.subpaths]
        subpaths_collections += [local_revision.subpaths for local_revision in self.revisions.values()]
        subpaths_collections.append(self.wip_revision.subpaths)
        is_valid = all(os.path.exists(p) if p else False for p in chain.from_iterable(subpaths_collections))
        return is_valid

    @property
    def main_dir(self):
        """Get schematisation main directory."""
        schematisation_dir_path = os.path.normpath(os.path.join(self.working_directory, self.name))
        return schematisation_dir_path

    @property
    def admin_dir(self):
        """Get schematisation admin directory path."""
        admin_dir_path = os.path.join(self.main_dir, "admin")
        return admin_dir_path

    @property
    def subpaths(self):
        """Get schematisation directory sub-paths."""
        paths = [self.admin_dir]
        return paths

    @property
    def schematisation_config_path(self):
        """Get schematisation configuration filepath."""
        config_path = os.path.join(self.admin_dir, "schematisation.json")
        return config_path

    @property
    def sqlite(self):
        """Get schematisation work in progress revision sqlite filepath."""
        return self.wip_revision.sqlite

    def build_schematisation_structure(self):
        """Function for schematisation dir structure creation."""
        for schema_subpath in self.subpaths:
            os.makedirs(bypass_max_path_limit(schema_subpath), exist_ok=True)
        for local_revision in self.revisions:
            local_revision.make_revision_structure()
        if self.wip_revision is not None:
            self.wip_revision.make_revision_structure()
        self.write_schematisation_metadata()


def list_local_schematisations(working_dir):
    """Get local schematisations present in the given directory."""
    local_schematisations = OrderedDict()
    for basename in os.listdir(working_dir):
        full_path = os.path.join(working_dir, basename)
        local_schematisation = LocalSchematisation.initialize_from_location(full_path)
        if local_schematisation is not None:
            local_schematisations[local_schematisation.id] = local_schematisation
    return local_schematisations


def replace_revision_data(source_revision, target_revision):
    """Replace target revision content with the source revision data."""
    shutil.rmtree(target_revision.main_dir)
    shutil.copytree(source_revision.main_dir, target_revision.main_dir)


def parse_version_number(version_str):
    """Parse version number in a string format and convert it into list of an integers."""
    version = [int(i) for i in version_str.split(".") if i.isnumeric()]
    return version
