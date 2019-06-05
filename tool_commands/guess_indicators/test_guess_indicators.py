from sqlalchemy import update
from ThreeDiToolbox.sql_models.model_schematisation import ConnectionNode
from ThreeDiToolbox.sql_models.model_schematisation import Manhole
from ThreeDiToolbox.sql_models.model_schematisation import Pumpstation
from ThreeDiToolbox.sql_models.model_schematisation import BoundaryCondition1D
from ThreeDiToolbox.test.test_init import TEST_DATA_DIR
from ThreeDiToolbox.tool_commands.guess_indicators.guess_indicators_utils import Guesser
from ThreeDiToolbox.utils.threedi_database import ThreediDatabase
from ThreeDiToolbox.sql_models.constants import Constants

import shutil
import pytest
from pathlib import Path


def get_pump_or_outlet_manholes(session, ids):
    """
    :param ids: [list] this contains ids from either manhole_outlet or manhole_pump
    :return: a list with tuples (manhole.id, manhole.manhole_indicator)
    """
    manholes_id_indicator = {}
    # only return manhole
    sql_manholes = (
        session.query(Manhole)
        .join(Manhole.connection_node)
        .filter(ConnectionNode.id.in_(ids))
    )
    for manhole in sql_manholes:
        # fill dict
        manholes_id_indicator[manhole.id] = manhole.manhole_indicator
    return manholes_id_indicator


def get_all_manholes(session):
    """ get all manholes from sqlite (also manhole_outlet, manhole_pump)
    :return: a list with tuples (manhole.id, manhole.manhole_indicator) """
    manholes_id_indicator = {}
    sql_manholes = session.query(Manhole)
    for manhole in sql_manholes:
        # fill dict
        manholes_id_indicator[manhole.id] = manhole.manhole_indicator
    return manholes_id_indicator


def get_manholes(session, outlet_bool=False, pump_bool=False, all_bool=False):
    """ get manholes from sqlite: OR only manhole_outlet, OR only manhole_pumps, OR
    all manholes (manhole_outlet + manhole_pump + other manholes)
    :return: a list with tuples (manhole.id, manhole.manhole_indicator)  """
    # only 1 of kwargs may be True
    assert sum([outlet_bool, pump_bool, all_bool]) == 1
    if pump_bool:
        ids = session.query(Pumpstation.connection_node_start_id)
    elif outlet_bool:
        ids = session.query(BoundaryCondition1D.connection_node_id)
    if pump_bool or outlet_bool:
        manholes_id_indicator = get_pump_or_outlet_manholes(session, ids)
    if all_bool:
        manholes_id_indicator = get_all_manholes(session)
    return manholes_id_indicator


def empty_manhole_selection(session, manholes_pre_empty):
    """ empty column manhole_indicator (set is to NULL) of table v2_manhole """
    manholes_ids = list(manholes_pre_empty)
    up = (
        update(Manhole)
        .where(Manhole.id.in_(manholes_ids))
        .values(manhole_indicator=None)
    )
    session.execute(up)
    session.commit()


@pytest.fixture()
def tmp_sqlite_path(tmpdir):
    sqlite_filename = "v2_bergermeer.sqlite"
    orig_sqlite_path = TEST_DATA_DIR.joinpath(
        "testmodel", "v2_bergermeer", sqlite_filename
    )
    tmp_sqlite_dir = Path(tmpdir)
    tmp_sqlite_path = tmp_sqlite_dir.joinpath(sqlite_filename)
    shutil.copy2(orig_sqlite_path, tmp_sqlite_path)
    return tmp_sqlite_path


@pytest.fixture()
def db(tmp_sqlite_path):
    db_type = "spatialite"
    db_set = {"db_path": tmp_sqlite_path}
    db = ThreediDatabase(db_set, db_type)
    return db


@pytest.fixture()
def guesser(db):
    return Guesser(db)


def test_guess_manhole_indicator(db, guesser):
    session = db.get_session()

    # before we empty manholes, first get their [(id, manhole_indicator)]
    manholes_pumps_pre_empty = get_manholes(session, pump_bool=True)
    manholes_outlets_pre_empty = get_manholes(session, outlet_bool=True)
    all_manholes_pre_empty = get_manholes(session, all_bool=True)
    if not all_manholes_pre_empty:
        # skip this test as there are no manholes in sqlite..
        return
    # now lets empty column in all manholes the column 'manhole_indicator'
    empty_manhole_selection(session, all_manholes_pre_empty)

    all_manholes_pre_guess = get_manholes(session, all_bool=True)
    # all dict values should be None (<-- still test-prework, not actual testing), If
    # it fails then empty_manhole_selection() does not a good job
    assert not (all(list(all_manholes_pre_guess.values())))

    # now put guesser to work
    guesser.guess_manhole_indicator(only_empty_fields=False)

    # get a new session
    session = db.get_session()

    manholes_pumps_after_guess = get_manholes(session, pump_bool=True)
    manholes_outlet_after_guess = get_manholes(session, outlet_bool=True)
    all_manholes_after_guess = get_manholes(session, all_bool=True)

    # manholes_pumps should have been updated to MANHOLE_INDICATOR_PUMPSTATION
    if manholes_pumps_pre_empty:
        result_list = list(manholes_pumps_after_guess.values())
        expected_value = Constants.MANHOLE_INDICATOR_PUMPSTATION
        assert all([expected_value == ele for ele in result_list])

    # manholes_outlets should have been updated to MANHOLE_INDICATOR_OUTLET
    if manholes_outlets_pre_empty:
        result_list = list(manholes_outlet_after_guess.values())
        expected_value = Constants.MANHOLE_INDICATOR_OUTLET
        assert all([expected_value == ele for ele in result_list])

        for k in manholes_outlets_pre_empty:
            all_manholes_after_guess.pop(k, None)

    # rest of the manholes should have been updated to MANHOLE_INDICATOR_MANHOLE
    for my_dict in [manholes_pumps_pre_empty, manholes_outlets_pre_empty]:
        for k in my_dict:
            all_manholes_after_guess.pop(k, None)
    result_list = list(all_manholes_after_guess.values())
    expected_value = Constants.MANHOLE_INDICATOR_MANHOLE
    assert all([expected_value == ele for ele in result_list])
