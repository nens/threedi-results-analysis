import numpy as np
from threedi_results_analysis.processing.deps.discharge.leak_detector import (
    wet_cross_sectional_area,
    wetted_perimeter,
    discharge_reduction_factor,
)


def test_wet_cross_sectional_area():
    exchange_levels = np.array([2.3, -1.0, -2.0, 3.5, 6.8])
    pixel_size = 10
    water_level = 1.0

    assert wet_cross_sectional_area(exchange_levels, pixel_size, water_level) == 50

    obstacle_crest_level = 0.0
    assert wet_cross_sectional_area(exchange_levels, pixel_size, water_level, obstacle_crest_level) == 20

    water_level = 5.0
    obstacle_crest_level = None
    assert wet_cross_sectional_area(
        exchange_levels,
        pixel_size,
        water_level,
        obstacle_crest_level
    ) == ((water_level-2.3)+(water_level--1.0)+(water_level--2.0)+(water_level-3.5))*pixel_size

    obstacle_crest_level = 2.0
    assert wet_cross_sectional_area(
        exchange_levels,
        pixel_size,
        water_level,
        obstacle_crest_level
    ) == ((water_level-2.3)+(water_level-2.0)+(water_level-2.0)+(water_level-3.5))*pixel_size


def test_wetted_perimeter():
    exchange_levels = np.array([2.3, -1.0, -2.0, 3.5, 6.8])
    pixel_size = 10
    water_level = 1.0
    assert wetted_perimeter(exchange_levels, pixel_size, water_level) == 20

    obstacle_crest_level = 0.0
    assert wetted_perimeter(exchange_levels, pixel_size, water_level, obstacle_crest_level) == 20

    obstacle_crest_level = 1.0
    assert wetted_perimeter(exchange_levels, pixel_size, water_level, obstacle_crest_level) == 0

    obstacle_crest_level = 2.0
    assert wetted_perimeter(exchange_levels, pixel_size, water_level, obstacle_crest_level) == 0

    water_level = 10.0
    assert wetted_perimeter(exchange_levels, pixel_size, water_level, obstacle_crest_level) == 50


def test_discharge_reduction_factor():
    exchange_levels = np.array([2.3, -1.0, -2.0, 3.5, 6.8])
    pixel_size = 10
    water_level = 1.0
    old_obstacle_crest_level = None
    new_obstacle_crest_level = 0.0
    assert discharge_reduction_factor(
        exchange_levels,
        pixel_size,
        water_level,
        old_obstacle_crest_level,
        new_obstacle_crest_level
    ) == 0.6324555320336759

    new_obstacle_crest_level = 1
    assert discharge_reduction_factor(
        exchange_levels,
        pixel_size,
        water_level,
        old_obstacle_crest_level,
        new_obstacle_crest_level
    ) == 0

    new_obstacle_crest_level = 5
    assert discharge_reduction_factor(
        exchange_levels,
        pixel_size,
        water_level,
        old_obstacle_crest_level,
        new_obstacle_crest_level
    ) == 0
