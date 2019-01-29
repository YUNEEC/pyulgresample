"""Convert ulog file to different data structure."""
import pyulog
import pandas as pd
import re
import numpy as np


def createPandaDict(ULog, nan_topic_msgs=None):
    """Convert ulog to dictionary of topic based panda-dataframes.

    rename topic-name such that each topic starts with `T_` and ends with instance ID.
    i.e. vehicle_local_position and instance 0 -> T_vehicle_local_position_0
    rename topic-fields such that vector indicices are replaced with underline and each field stars
    with letter F for denoting fields
    i.e.: fieldmsg[0] -> F_fieldmsg_0; fieldmsg[1] -> F_fieldmsg_1

    Arguments:
    ULog -- ulog file from which the dataframe should be created

    Keyword arguments:
    nan_topic_msgs -- messages which contain nan values (default None)

    """
    # column replacement
    col_rename = {"[": "_", "]": "", ".": "_"}
    col_rename_pattern = re.compile(
        r"(" + "|".join([re.escape(key) for key in col_rename.keys()]) + r")"
    )

    pandadict = {}
    for msg in ULog.data_list:
        msg_data = pd.DataFrame.from_dict(msg.data)
        msg_data.columns = [
            col_rename_pattern.sub(lambda x: col_rename[x.group()], col)
            for col in msg_data.columns
        ]

        if nan_topic_msgs:
            for nant in nan_topic_msgs:
                if nant.topic == msg.name:
                    for m in nant.msgs:
                        msg_data.loc[np.isnan(msg_data[m]), m] = np.inf

        ncol = {}
        for col in msg_data.columns:
            if col == "timestamp":
                ncol[col] = col
            else:
                ncol[col] = "F_" + col
        msg_data.rename(columns=ncol, inplace=True)
        msg_data.index = pd.TimedeltaIndex(
            msg_data["timestamp"] * 1e3, unit="ns"
        )
        pandadict["T_{:s}_{:d}".format(msg.name, msg.multi_id)] = msg_data

    return pandadict


# Currently not used
#
# def merge_asof(pandadict, on=None, direction=None):
#     """use pandadict merge_asof to merge data.

#     Arguments:
#     @params pandadict: dictionary of panda-dataframes

#     Keyword arguments:
#     @params on: Topic that defines timestamp (default None)
#     @params direction: see pandas merge_asof (default None)

#     """
#     if on is None:
#         raise IOError("Must pass a topic name to merg on")
#     if direction is None:
#         direction = "backwards"

#     combineTopicFieldName(pandadict)
#     m = pd.DataFrame(data=pandadict[on].timestamp, columns=["timestamp"])
#     for topic in pandadict:
#         m = pd.merge_asof(m, pandadict[topic], on="timestamp")
#     m.index = pd.TimedeltaIndex(m.timestamp * 1e3, unit="ns")
#     return m


def merge(pandadict, topics_zero_order_hold=None, nan_topic_msgs=None):
    """Use pandas merge method applied to pandadict.

    Arguments:
    @params pandadict: a dictionary of pandas dataframe

    Keyword arguments:
    @params topics_zero_order_hold: by default merge will use linear interpolation
    @params nan_topic_msgs: list of TopicMsgs where the msgs contain NAN values
            interpolation. column_zero_order_hold specifies which messages
            of pandadict are interpolated with zero-order-hold method

    """
    combineTopicFieldName(pandadict)
    skip = True
    for topic in pandadict:
        if skip:
            m = pandadict[topic]
            skip = False
        else:
            m = pd.merge_ordered(
                m, pandadict[topic], on="timestamp", how="outer"
            )
    m.index = pd.TimedeltaIndex(m.timestamp * 1e3, unit="ns")

    # apply zero order hold for topics that contain NAN
    # TODO: handle NANs for linear interpolation
    if nan_topic_msgs:
        for t_nan in nan_topic_msgs:
            regex = t_nan.topic + ".+"
            if t_nan.msgs:
                regex = regex + "["
                for msg in t_nan.msgs:
                    regex = "{0}({1})".format(regex, msg)
                regex = regex + "]"
            m[list(m.filter(regex=regex).columns)] = m[
                list(m.filter(regex=regex).columns)
            ].fillna(method="ffill")

    # apply zero order hold for some selected topics
    if topics_zero_order_hold is not None:

        for t in topics_zero_order_hold:
            msg = "T_" + t + "*"
            m[list(m.filter(regex=msg).columns)] = m[
                list(m.filter(regex=msg).columns)
            ].fillna(method="ffill")

    # apply interpolation to the whole dataframe (only NaN values get interpolated,
    # thus the zero order hold values from before do not get overwritten)
    m = m.interpolate(method="linear")

    # drop all values that are still NaN
    m.dropna()

    # replace the inf-values with NAN. Note: compare to the dropped NAN-values, the inf-values
    # were originally NAN-values that were logged as part of the message
    m.replace(np.inf, np.nan, inplace=True)
    return m


def combineTopicFieldName(pandadict):
    """Add topic name to field-name except for timestamp field.

    Arguments:
    pandadict -- a dictionary of pandas dataframe

    """
    for topic in pandadict.keys():
        ncol = {}
        for col in pandadict[topic].columns:
            if col == "timestamp":
                ncol[col] = col
            else:
                ncol[col] = topic + "__" + col
        pandadict[topic].rename(columns=ncol, inplace=True)
    return
