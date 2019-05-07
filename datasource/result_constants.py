from collections import namedtuple


# Explanation: aggregation using the cumulative method integrates the variable
# over time. Therefore the units must be multiplied by the time also.
CUMULATIVE_AGGREGATION_UNITS = {
    "s1": "m MSL",
    "q": "m3",
    "u1": "m",
    "vol": "m3",
    "q_pump": "m3",
    "qp": "m3",
    "up1": "m",
    "q_lat": "m3",
    "vol1": "m3",
    "rain": "m3",
    "infiltration_rate": "m3",
    "infiltration_rate_simple": "m3",
    "leak": "m3",
    "su": "",
    "au": "",
    "intercepted_volume": "m3",
    "q_sss": "m3",
}
