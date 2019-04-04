"""
Only purpose this module serves is to patch Lines.line_geometries, because
h5py on QGIS on Windows can't handle that field (it's a hdf5 VLEN/numpy
'object' dtype kind of field).

To make sure this patch is applied every time we import stuff from threedigrid,
the best way for now is to import ``GridH5Admin`` from this module, e.g.:

    >>> from ThreeDiToolbox.utils.patched_threedigrid import GridH5Admin

"""


from threedigrid.admin.lines.models import Lines

# we need try except for Plugin Reloader (dev). If we don't then Plugin
# Reloader crashes on the del statement
try:
    del Lines.line_geometries
except AttributeError:
    pass
from threedigrid.admin.gridresultadmin import GridH5AggregateResultAdmin  # noqa
from threedigrid.admin.gridadmin import GridH5Admin  # noqa
from threedigrid.admin.gridresultadmin import GridH5ResultAdmin  # noqa
