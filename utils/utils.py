"""Imported in __init__.py"""
from uuid import uuid4
import logging
import os
import shutil

logger = logging.getLogger(__name__)


def backup_sqlite(filename):
    """Make a backup of the sqlite database."""
    backup_folder = os.path.join(os.path.dirname(os.path.dirname(filename)), "_backup")
    os.makedirs(backup_folder, exist_ok=True)
    prefix = str(uuid4())[:8]
    backup_sqlite_path = os.path.join(
        backup_folder, f"{prefix}_{os.path.basename(filename)}"
    )
    shutil.copyfile(filename, backup_sqlite_path)
    return backup_sqlite_path
