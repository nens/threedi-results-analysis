from pathlib import Path

import numpy as np
from threedigrid.admin.gridresultadmin import GridH5ResultAdmin

from .base import hybrid_time_aggregate
from .aggregation_classes import Aggregation, AggregationSign
from .constants import AGGREGATION_VARIABLES, AGGREGATION_METHODS


def test_hybrid_time_aggregate_gradient():
    assert False
    data_dir = Path(__file__).parent / "test_data" / "zwartedijkspolder"
    gridadmin_path = data_dir / "gridadmin.h5"
    results_3di_path = data_dir / "results_3di.nc"
    gra = GridH5ResultAdmin(str(gridadmin_path), str(results_3di_path))
    lines = gra.lines.filter(id__in=[906])

    # aggregation
    aggregation_variable = AGGREGATION_VARIABLES.get_by_short_name("grad")
    for method, sign, expected in [

        ("min", "net", -0.01411906),
        ("min", "pos", 0),
        ("min", "neg", -0.01411906),
        ("min", "abs", 0),
        ("max", "net", 0.11590592),
        ("max", "pos", 0.11590592),
        ("max", "neg", 0),
        ("max", "abs", 0.11590592),
        ("max_time", "net", 5411.2456),
        ("max_time", "pos", 5411.2456),
        ("max_time", "neg", 0),
        ("max_time", "abs", 5411.2456),
    ]:
        aggregation_method = AGGREGATION_METHODS.get_by_short_name(method)
        aggregation_sign = AggregationSign(short_name=sign, long_name="")

        aggregation = Aggregation(
            variable=aggregation_variable,
            method=aggregation_method,
            sign=aggregation_sign
        )

        result = hybrid_time_aggregate(
            threedigrid_object=lines,
            aggregation=aggregation,
            start_time=None,
            end_time=None,
            gr=gra,
        )
        assert np.isclose(result, expected), (f"Expected {expected}, but result is {result} for "
                                              f"{aggregation_variable.long_name}, {sign}, {method.long_name}")
