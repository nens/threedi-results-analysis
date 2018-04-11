"""
Only purpose this module serves is to patch Lines.line_geometries, because
h5py on QGIS on Windows can't handle that field (it's a hdf5 VLEN/numpy
'object' dtype kind of field).

To make sure this patch is applied every time we import stuff from threedigrid,
the best way for now is to import ``GridH5Admin`` from this module, e.g.:

    >>> from ThreeDiToolbox.utils.patched_threedigrid import GridH5Admin

"""

from threedigrid.admin.lines import Lines
del Lines.line_geometries
from threedigrid import *  # noqa
