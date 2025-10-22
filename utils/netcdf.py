from pathlib import Path
from typing import Dict

import h5py


def substances_from_netcdf(netcdf: str | Path) -> Dict[str, str]:
    """
    Get a {substance id: substance name} Dict for a water_quality_results_3di.nc file
    """
    f = h5py.File(netcdf)
    substances = {}
    for key in f.keys():
        if key.startswith("substance"):
            substance_id = key.split("_")[0]
            substance_name = f[key].attrs["substance_name"]
            substances[substance_id] = substance_name
    return substances
