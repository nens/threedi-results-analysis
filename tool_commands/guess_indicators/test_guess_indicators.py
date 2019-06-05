from sqlalchemy import update
from ThreeDiToolbox.sql_models.model_schematisation import ConnectionNode
from ThreeDiToolbox.sql_models.model_schematisation import Manhole
from ThreeDiToolbox.sql_models.model_schematisation import Pumpstation
from ThreeDiToolbox.test.test_init import TEST_DATA_DIR
from ThreeDiToolbox.tool_commands.guess_indicators.guess_indicators_utils import Guesser
from ThreeDiToolbox.utils.threedi_database import ThreediDatabase
from ThreeDiToolbox.sql_models.constants import Constants

import shutil
import pytest
from pathlib import Path


def get_manholes_pumpstation(session):
    """ get manholes that are on same connection node as start point of pumpstation
    :return: a list with tuples (manhole.id, manhole.manhole_indicator)  """
    manholes_id_indicator = {}
    pump_start_ids = session.query(Pumpstation.connection_node_start_id)
    sql_manholes = (
        session.query(Manhole)
        .join(Manhole.connection_node)
        .filter(ConnectionNode.id.in_(pump_start_ids))
    )
    for manhole in sql_manholes:
        # fill dict
        manholes_id_indicator[manhole.id] = manhole.manhole_indicator
    return manholes_id_indicator


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


def test_manhole_indicator_pumpstation(db, guesser):
    session = db.get_session()

    # before we empty manholes, first get their [(id, manhole_indicator)]
    manholes_pre_empty = get_manholes_pumpstation(session)
    if not manholes_pre_empty:
        # skip this test as there are no manholes in sqlite..
        return
    # now lets empty column 'manhole_indicator'
    manholes_ids = list(manholes_pre_empty)
    up = (
        update(Manhole)
        .where(Manhole.id.in_(manholes_ids))
        .values(manhole_indicator=None)
    )
    session.execute(up)
    session.commit()

    manhole_pre_guess = get_manholes_pumpstation(session)
    # all dict values should be None (<-- still test-prework, not actual testing)
    assert not (all(list(manhole_pre_guess.values())))

    # now put guesser to work
    guesser.guess_manhole_indicator(only_empty_fields=False)

    # get a new session
    session = db.get_session()
    manhole_after_guess = get_manholes_pumpstation(session)
    result_list = list(manhole_after_guess.values())
    expected_value = Constants.MANHOLE_INDICATOR_PUMPSTATION
    # actual test: all updated manhole_indicators should match expected_value
    assert all([expected_value == ele for ele in result_list])


# def test_manhole_indicator_outlet(db, guesser):
#     session = db.get_session()
#
#     # before we empty manholes, first get their [(id, manhole_indicator)]
#     manholes_pre_empty = get_manholes_pumpstation(session)
#     if not manholes_pre_empty:
#         # skip this test as there are no manholes in sqlite..
#         return
#

