from typing import List, Tuple
from pathlib import Path
from time import sleep

import numpy as np
from osgeo import gdal
from threedigrid.admin.gridadmin import GridH5Admin

from threedi_results_analysis.processing.deps.discharge.leak_detector import (
    CellPair,
    LeakDetector,
    REFERENCE,
    NEIGH,
    MERGED,
    LEFT,
    RIGHT,
    TOP,
    BOTTOM,
    NA,
    LEFTHANDSIDE,
    RIGHTHANDSIDE
)

DATA_DIR = Path(__file__).parent / 'data'
DEM_FILENAME = DATA_DIR / 'dem_0_01.tif'
DEM_DATASOURCE = gdal.Open(str(DEM_FILENAME), gdal.GA_ReadOnly)
GRIDADMIN_FILENAME = DATA_DIR / 'gridadmin.h5'
GR = GridH5Admin(GRIDADMIN_FILENAME)
MIN_PEAK_PROMINENCE = 0.05
SEARCH_PRECISION = 0.001
MIN_OBSTACLE_HEIGHT = 0.05

SIDE_BOTTOM = 0
SIDE_LEFT = 0
SIDE_MIDDLE = 1
SIDE_TOP = 2
SIDE_RIGHT = 2


def test_width_and_height():
    cell_ids = [158, 159, 204, 205, 206]
    leak_detector = LeakDetector(
        gridadmin=GR,
        dem=DEM_DATASOURCE,
        cell_ids=cell_ids,
        min_obstacle_height=MIN_OBSTACLE_HEIGHT,
        search_precision=SEARCH_PRECISION,
        min_peak_prominence=MIN_PEAK_PROMINENCE
    )

    ref = leak_detector.cell(205)
    neigh = leak_detector.cell(206)
    cell_pair = CellPair(leak_detector, ref, neigh)
    assert cell_pair.width == 20
    assert cell_pair.height == 40


def test_locate_cell():
    cell_ids = [158, 204]
    leak_detector = LeakDetector(
        gridadmin=GR,
        dem=DEM_DATASOURCE,
        cell_ids=cell_ids,
        min_obstacle_height=MIN_OBSTACLE_HEIGHT,
        search_precision=SEARCH_PRECISION,
        min_peak_prominence=MIN_PEAK_PROMINENCE
    )
    ref = leak_detector.cell(158)
    neigh = leak_detector.cell(204)
    cell_pair = CellPair(leak_detector, ref, neigh)
    assert cell_pair.locate_cell(NEIGH) == (RIGHT, TOP)


def test_locate_pos():
    cell_ids = [158, 204]
    leak_detector = LeakDetector(
        gridadmin=GR,
        dem=DEM_DATASOURCE,
        cell_ids=cell_ids,
        min_obstacle_height=MIN_OBSTACLE_HEIGHT,
        search_precision=SEARCH_PRECISION,
        min_peak_prominence=MIN_PEAK_PROMINENCE
    )
    ref = leak_detector.cell(158)
    neigh = leak_detector.cell(204)
    cell_pair = CellPair(leak_detector, ref, neigh)
    assert cell_pair.locate_pos((0, 25)) == REFERENCE
    assert cell_pair.locate_pos((0, 39)) == REFERENCE
    assert cell_pair.locate_pos((0, 40)) == NEIGH
    assert cell_pair.locate_pos((0, 45)) == NEIGH


def test_maxima():
    cell_ids = [156, 157, 158, 159, 190, 199, 200, 203, 204, 205, 206, 219, 220]
    leak_detector = LeakDetector(
        gridadmin=GR,
        dem=DEM_DATASOURCE,
        cell_ids=cell_ids,
        min_obstacle_height=MIN_OBSTACLE_HEIGHT,
        search_precision=SEARCH_PRECISION,
        min_peak_prominence=MIN_PEAK_PROMINENCE
    )

    # Neigh is smaller, location is (RIGHT, TOP)
    ref = leak_detector.cell(158)
    neigh = leak_detector.cell(204)
    cell_pair = CellPair(leak_detector, ref, neigh)
    all_maxima = cell_pair.maxima()
    assert np.all(all_maxima[RIGHTHANDSIDE] == np.array([[39, 7]]))
    assert np.all(all_maxima[LEFTHANDSIDE] == np.array([[0, 54]]))

    # Neigh is smaller, location is (RIGHT, TOP)
    # There are no right-hand-side nor left-hand-side maxima
    ref = leak_detector.cell(159)
    neigh = leak_detector.cell(206)
    cell_pair = CellPair(leak_detector, ref, neigh)
    all_maxima = cell_pair.maxima()
    assert len(all_maxima[RIGHTHANDSIDE]) == 0
    assert len(all_maxima[LEFTHANDSIDE]) == 0

    # Neigh is same size, location is (TOP, N/A)
    ref = leak_detector.cell(205)
    neigh = leak_detector.cell(206)
    cell_pair = CellPair(leak_detector, ref, neigh)
    all_maxima = cell_pair.maxima()
    assert np.all(all_maxima[RIGHTHANDSIDE] == np.array([[16, 19]]))
    assert np.all(all_maxima[LEFTHANDSIDE] == np.array([[11, 0]]))

    # Neigh is smaller, location is (RIGHT, BOTTOM)
    ref = leak_detector.cell(156)
    neigh = leak_detector.cell(199)
    cell_pair = CellPair(leak_detector, ref, neigh)
    all_maxima = cell_pair.maxima()
    assert np.all(all_maxima[RIGHTHANDSIDE] == np.array([[39, 51]]))
    assert np.all(all_maxima[LEFTHANDSIDE] == np.array([[0, 4]]))

    # Neigh is bigger, location is (RIGHT, N/A)
    # Ref location is (LEFT, TOP)
    ref = leak_detector.cell(220)
    neigh = leak_detector.cell(190)
    cell_pair = CellPair(leak_detector, ref, neigh)
    all_maxima = cell_pair.maxima()
    assert np.all(all_maxima[RIGHTHANDSIDE] == np.array([[39, 52]]))
    assert np.all(all_maxima[LEFTHANDSIDE] == np.array([[0, 38]]))


def find_obstacles_helper(
        cell_ids: List[int],
        result_obstacle_side: int,
        result_nr_obstacles: int,
        result_crest_levels: List[float],
        extra_edges_with_obstacles: List[Tuple[int, int]] = None
):
    leak_detector = LeakDetector(
        gridadmin=GR,
        dem=DEM_DATASOURCE,
        cell_ids=cell_ids,
        min_obstacle_height=MIN_OBSTACLE_HEIGHT,
        search_precision=SEARCH_PRECISION,
        min_peak_prominence=MIN_PEAK_PROMINENCE
    )

    ref = leak_detector.cell(cell_ids[0])
    neigh = leak_detector.cell(cell_ids[1])
    cell_pair = CellPair(leak_detector, ref, neigh)
    cell_pair.find_obstacles()
    edge = cell_pair.edges[result_obstacle_side][0]
    try:
        assert len(edge.obstacles) == result_nr_obstacles
    except AssertionError:
        print(f"len(edge.obstacles): {len(edge.obstacles)}")
        raise
    crest_levels = [obstacle.crest_level for obstacle in edge.obstacles]
    crest_levels.sort()
    result_crest_levels.sort()
    assert crest_levels == result_crest_levels

    if extra_edges_with_obstacles:
        for e in extra_edges_with_obstacles:
            edge = leak_detector.edge(*e)
            assert len(edge.obstacles) > 0


def test_find_obstacles():
    find_obstacles_helper(
        cell_ids=[55, 56],
        result_obstacle_side=SIDE_TOP,
        result_nr_obstacles=1,
        result_crest_levels=[5.0]
    )

    find_obstacles_helper(
        cell_ids=[56, 57],
        result_obstacle_side=SIDE_MIDDLE,
        result_nr_obstacles=2,
        result_crest_levels=[5.0, 5.0]
    )

    find_obstacles_helper(
        cell_ids=[38, 39],
        result_obstacle_side=SIDE_MIDDLE,
        result_nr_obstacles=1,
        result_crest_levels=[5.0]
    )

    find_obstacles_helper(
        cell_ids=[34, 54],
        result_obstacle_side=SIDE_MIDDLE,
        result_nr_obstacles=1,
        result_crest_levels=[5.0]
    )

    for side in [SIDE_LEFT, SIDE_MIDDLE, SIDE_TOP]:
        find_obstacles_helper(
            cell_ids=[35, 55],
            result_obstacle_side=side,
            result_nr_obstacles=0,
            result_crest_levels=[]
        )

    find_obstacles_helper(
        cell_ids=[159, 206],
        result_obstacle_side=SIDE_MIDDLE,
        result_nr_obstacles=0,
        result_crest_levels=[]
    )

    find_obstacles_helper(
        cell_ids=[158, 204],
        result_obstacle_side=SIDE_MIDDLE,
        result_nr_obstacles=1,
        result_crest_levels=[5.0],
        extra_edges_with_obstacles=[(158, 203)]
    )

    find_obstacles_helper(
        cell_ids=[156, 199],
        result_obstacle_side=SIDE_MIDDLE,
        result_nr_obstacles=1,
        result_crest_levels=[5.0],
        extra_edges_with_obstacles=[(156, 200)]
    )

    find_obstacles_helper(
        cell_ids=[172, 193],
        result_obstacle_side=SIDE_MIDDLE,
        result_nr_obstacles=1,
        result_crest_levels=[3.0]
    )

    find_obstacles_helper(
        cell_ids=[212, 186],
        result_obstacle_side=SIDE_MIDDLE,
        result_nr_obstacles=1,
        result_crest_levels=[5.0]
    )


def test_find_connecting_obstacles():
    cell_ids = [29, 30, 49, 50]
    leak_detector = LeakDetector(
        gridadmin=GR,
        dem=DEM_DATASOURCE,
        cell_ids=cell_ids,
        min_obstacle_height=MIN_OBSTACLE_HEIGHT,
        search_precision=SEARCH_PRECISION,
        min_peak_prominence=MIN_PEAK_PROMINENCE
    )

    for ref_id, neigh_id in [(29, 30), (29, 49), (30, 50)]:
        ref = leak_detector.cell(ref_id)
        neigh = leak_detector.cell(neigh_id)
        cell_pair = CellPair(leak_detector, ref, neigh)
        cell_pair.find_obstacles()

    assert len(leak_detector.edge(29, 30).obstacles) == 0

    ref = leak_detector.cell(29)
    neigh = leak_detector.cell(30)
    cell_pair = CellPair(leak_detector, ref, neigh)
    cell_pair.find_connecting_obstacles()

    print(leak_detector.edge(29, 30).obstacles)
    assert len(leak_detector.edge(29, 30).obstacles) == 1


def test_transform():
    cell_ids = [158, 204]
    leak_detector = LeakDetector(
        gridadmin=GR,
        dem=DEM_DATASOURCE,
        cell_ids=cell_ids,
        min_obstacle_height=MIN_OBSTACLE_HEIGHT,
        search_precision=SEARCH_PRECISION,
        min_peak_prominence=MIN_PEAK_PROMINENCE
    )
    ref = leak_detector.cell(158)
    neigh = leak_detector.cell(204)
    cell_pair = CellPair(leak_detector, ref, neigh)

    # shape of cell 158: 40 x 40
    # shape of cell 204: 20 x 20
    # location of cell 204 is (RIGHT, TOP)
    in_list = [
        {"pos": (13, 17), "from_array": REFERENCE, "to_array": MERGED},
        {"pos": (13, 17), "from_array": MERGED, "to_array": REFERENCE},
        {"pos": (13, 17), "from_array": NEIGH, "to_array": MERGED},
        {"pos": (13, 57), "from_array": MERGED, "to_array": NEIGH},
        {"pos": np.array([[13, 13], [17, 18]]), "from_array": REFERENCE, "to_array": MERGED},
        {"pos": np.array([[13, 13], [17, 18]]), "from_array": NEIGH, "to_array": MERGED},
    ]
    out_list = [
        (13, 17),
        (13, 17),
        (13, 57),
        (13, 17),
        np.array([[13, 13], [17, 18]]),
        np.array([[13, 13], [57, 58]]),
    ]
    for i, in_args in enumerate(in_list):
        transformed = cell_pair.transform(**in_args)
        try:
            assert np.all(np.array(transformed) == np.array(out_list[i]))
        except AssertionError as e:
            print(f"In: {in_list[i]}\nOut: {transformed}\nExpected: {out_list[i]}")
            sleep(0.3)
            raise e


def test_squash_indices():
    cell_ids = [158, 204, 171, 172, 193]
    leak_detector = LeakDetector(
        gridadmin=GR,
        dem=DEM_DATASOURCE,
        cell_ids=cell_ids,
        min_obstacle_height=MIN_OBSTACLE_HEIGHT,
        search_precision=SEARCH_PRECISION,
        min_peak_prominence=MIN_PEAK_PROMINENCE
    )

    # shape of cell 158: 40 x 40
    # shape of cell 204: 20 x 20
    # location of cell 204 is (RIGHT, TOP)
    ref = leak_detector.cell(158)
    neigh = leak_detector.cell(204)
    cell_pair = CellPair(leak_detector, ref, neigh)
    expected_results = [
        np.array([np.arange(40), np.zeros(40)]),
        np.array([np.arange(40), np.hstack([np.ones(20) * 59, np.ones(20) * 39])]),
    ]
    for i, side in enumerate([LEFT, RIGHT]):
        result = CellPair.squash_indices(
            array_a=cell_pair.transform(pos=ref.side_indices(side), from_array=REFERENCE, to_array=MERGED),
            array_b=cell_pair.transform(pos=neigh.side_indices(side), from_array=NEIGH, to_array=MERGED),
            side=side,
            secondary_location=TOP
        )
        expected = expected_results[i]
        try:
            assert np.all(result == expected)
        except AssertionError as e:
            print(f"In: side: {side}\nOut: {result}\n Expected: {expected}")
            sleep(0.3)
            raise e

    # Same size cells, BOTTOM -> TOP
    ref = leak_detector.cell(171)
    neigh = leak_detector.cell(172)
    cell_pair = CellPair(leak_detector, ref, neigh)
    expected_results = [
        np.array([np.zeros(40), np.arange(40)]),
        np.array([np.ones(40)*79, np.arange(40)]),
    ]
    for i, side in enumerate([TOP, BOTTOM]):
        result = CellPair.squash_indices(
            array_a=cell_pair.transform(pos=ref.side_indices(side), from_array=REFERENCE, to_array=MERGED),
            array_b=cell_pair.transform(pos=neigh.side_indices(side), from_array=NEIGH, to_array=MERGED),
            side=side,
            secondary_location=NA
        )
        expected = expected_results[i]
        try:
            assert np.all(result == expected)
        except AssertionError as e:
            print(f"In: side: {side}\nOut: {result}\n Expected: {expected}")
            sleep(0.3)
            raise e

    # shape of cell 172: 40 x 40
    # shape of cell 193: 20 x 20
    # location of cell 193 is (TOP, LEFT)
    ref = leak_detector.cell(172)
    neigh = leak_detector.cell(193)
    cell_pair = CellPair(leak_detector, ref, neigh)
    expected_results = [
        np.array([np.hstack([np.zeros(20), np.ones(20) * 20]), np.arange(40)]),
        np.array([np.ones(40)*59, np.arange(40)]),
    ]
    for i, side in enumerate([TOP, BOTTOM]):
        result = CellPair.squash_indices(
            array_a=cell_pair.transform(pos=ref.side_indices(side), from_array=REFERENCE, to_array=MERGED),
            array_b=cell_pair.transform(pos=neigh.side_indices(side), from_array=NEIGH, to_array=MERGED),
            side=side,
            secondary_location=LEFT
        )
        expected = expected_results[i]
        try:
            assert np.all(result == expected)
        except AssertionError as e:
            print(f"In: side: {side}\nOut: {result}\n Expected: {expected}")
            sleep(0.3)
            raise e


def test_side_indices():
    # TODO: add tests here
    pass


def test_is_obstacle_relevant():
    # TODO: add tests here
    pass
