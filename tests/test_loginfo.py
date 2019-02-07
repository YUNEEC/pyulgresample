"""test_loginfo."""
from context import loginfo
import pytest
import warnings
from numpy.testing import assert_almost_equal
from context import localposition


def test_get_ulog_wrong_topic():
    """test for get_ulog.

    If a topic is provided which does not exist, then raise a user warning.
    """
    file = "testlgs/position.ulg"
    topics = ["vehicle_local_position", "vv"]

    warnings.simplefilter("error")  # turn warning into exception

    with pytest.raises(Exception):
        loginfo.get_ulog(file, topics)


def test_no_topic_present():
    """test if no topic is present."""
    file = "testlogs/position.ulg"
    topics = ["vv"]
    warnings.simplefilter("error")  # turn warning into exception

    with pytest.raises(Exception):
        loginfo.get_ulog(file, topics)


def test_get_ulog():
    """test get_ulog as expected."""
    file = "testlogs/position.ulg"
    topics = ["vehicle_local_position"]
    # should have valid topics
    ulog = loginfo.get_ulog(file, topics)
    assert ulog.data_list is not None
    # should have valid topics
    ulog = loginfo.get_ulog(file)
    assert ulog.data_list is not None


def test_ulog_getters():
    """test simple getters."""
    file = "testlogs/position.ulg"
    ulog = loginfo.get_ulog(file)
    starttime = loginfo.get_starttime(ulog)
    assert starttime == "0:00:01"

    duration = loginfo.get_duration(ulog)
    assert duration == "0:01:01"

    mpc_xy_p = loginfo.get_param(ulog, "MPC_XY_P", 0)
    assert_almost_equal(mpc_xy_p, 0.8)


def test_add_parameter():
    """test add parameter to dataframe."""
    file = "testlogs/parameterchange.ulg"
    lm = localposition.dfUlgPosition.create(file)

    # we should have three different groups
    loginfo.add_param(lm, "MPC_YAW_MODE")
    group = lm.df.groupby("MPC_YAW_MODE")
    assert group.ngroups == 3

    # should have two values of MPC_YAW_EXPO
    loginfo.add_param(lm, "MPC_YAW_EXPO")
    group = lm.df.groupby("MPC_YAW_EXPO")
    assert group.ngroups == 2

    # should have only one value for MPC_XY_P
    loginfo.add_param(lm, "MPC_XY_P")
    lm.df["MPC_XY_P"].to_csv("tt.txt")
    group = lm.df.groupby("MPC_XY_P")
    assert group.ngroups == 1
