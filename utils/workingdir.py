from collections import OrderedDict
from itertools import chain
import json
import re
import os
from threedi_results_analysis.utils.utils import listdirs


class LocalRevision:
    """Local revision directory structure representation."""

    def __init__(self, local_schematisation, revision_number):
        self.local_schematisation = local_schematisation
        self.number = revision_number

    def structure_is_valid(self):
        """Check if all revision subpaths are present."""
        is_valid = all(os.path.exists(p) if p else False for p in self.subpaths)
        return is_valid

    @property
    def sub_dir(self):
        """Get schematisation revision subdirectory name."""
        subdirectory = f"revision {self.number}"
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
    def results_dirs(self):
        """Get all (full) result folders"""
        if not os.path.isdir(self.results_dir):
            return []
        return listdirs(self.results_dir)

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


class LocalSchematisation:
    """Local revision directory structure representation."""

    def __init__(self, working_dir, schematisation_pk, schematisation_name, parent_revision_number=None):
        self.working_directory = working_dir
        self.id = schematisation_pk
        self.name = schematisation_name
        self.revisions = OrderedDict()
        self.wip_revision = WIPRevision(self, parent_revision_number) if parent_revision_number is not None else None

    @classmethod
    def initialize_from_location(cls, schematisation_dir, use_config_for_revisions=True):
        """
        Initialize local schematisation structure from the root schematisation dir.
        In case use_config_for_revisions is True, the revisions are derived from the json file,
        otherwise the schematisation dir is scanned for "revision" folders.
        """
        working_dir = os.path.dirname(schematisation_dir)
        if not os.path.isdir(schematisation_dir):
            return None
        config_path = os.path.join(schematisation_dir, "admin", "schematisation.json")
        schema_metadata = cls.read_schematisation_metadata(config_path)
        fallback_id = fallback_name = os.path.basename(schematisation_dir)
        schematisation_pk = schema_metadata.get("id", fallback_id)
        schematisation_name = schema_metadata.get("name", fallback_name)
        local_schematisation = cls(working_dir, schematisation_pk, schematisation_name)

        if use_config_for_revisions:
            revision_numbers = schema_metadata.get("revisions", [])
        else:
            folders = [
                os.path.basename(d)
                for d in listdirs(schematisation_dir)
                if os.path.basename(d).startswith("revision")
            ]
            revision_numbers = [int(re.findall(r'^revision (\d+)', folder)[0]) for folder in folders]

        for revision_number in revision_numbers:
            local_revision = LocalRevision(local_schematisation, revision_number)
            local_schematisation.revisions[revision_number] = local_revision

        wip_parent_revision_number = schema_metadata.get("wip_parent_revision")
        if wip_parent_revision_number is not None:
            local_schematisation.wip_revision = WIPRevision(local_schematisation, wip_parent_revision_number)

        return local_schematisation

    @staticmethod
    def read_schematisation_metadata(schematisation_config_path):
        """Read schematisation metadata from the JSON file."""
        if not os.path.exists(schematisation_config_path):
            return {}
        with open(schematisation_config_path, "r+") as config_file:
            return json.load(config_file)

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


def list_local_schematisations(working_dir):
    """Get local schematisations present in the given directory."""
    local_schematisations = OrderedDict()
    for basename in os.listdir(working_dir):
        full_path = os.path.join(working_dir, basename)
        local_schematisation = LocalSchematisation.initialize_from_location(full_path, False)
        if local_schematisation is not None:
            local_schematisations[local_schematisation.id] = local_schematisation
    return local_schematisations
