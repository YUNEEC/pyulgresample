"""
Get general ulog info
"""
import pyulog
import numpy as np
import datetime


def get_starttime(ulog):
    m1, s1 = divmod(int(ulog.start_timestamp / 1e6), 60)
    h1, m1 = divmod(m1, 60)
    return "{:d}:{:02d}:{:02d}".format(h1, m1, s1)


def get_duration(ulog):
    m2, s2 = divmod(
        int((ulog.last_timestamp - ulog.start_timestamp) / 1e6), 60
    )
    h2, m2 = divmod(m2, 60)
    return "{:d}:{:02d}:{:02d}".format(h2, m2, s2)


def get_date(log):
    gps_data = log.get_dataset("vehicle_gps_position")
    indices = np.nonzero(gps_data.data["time_utc_usec"])
    if len(indices[0]) > 0:
        return datetime.datetime.fromtimestamp(
            gps_data.data["time_utc_usec"][0] / 1000000
        )
    else:
        return None


def get_param(log, parameter_name, default):
    if parameter_name in log.initial_parameters.keys():
        return log.initial_parameters[parameter_name]
    else:
        return default
