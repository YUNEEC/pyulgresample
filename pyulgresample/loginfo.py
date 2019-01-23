"""Get general ulog info."""
import pyulog
import numpy as np
import datetime


def get_ulog(filepath, topics):
    """Read a .ulg file from the given filepath and return it as a ulog structure.

    It can be that sometimes, topics are missing. 
    Thus, check if the required topic are available in the ulog file. 

    Arguments:
    filepath -- absoulte path to the .ulg file
    topics -- list of required topics
    
    """
    ulog = pyulog.ULog(filepath, topics)

    if not ulog.data_list:
        print("\033[93m" + "Not a single desired topic present" + "\033[0m")
        return None

    tmp = topics.copy()

    for topic in ulog.data_list:
        if topic.name in tmp:
            idx = tmp.index(topic.name)
            tmp.pop(idx)

    if len(tmp) > 0:
        print(
            "\033[93m"
            + "The following topics do not exist in the provided ulog file: "
            + "\033[0m"
        )
        print(tmp)
        return None

    return ulog


def get_starttime(ulog):
    """Recover the start time stored in the ulog structure.
    
    Arguments:
    ulog -- messages stored in ulog structure

    """
    m1, s1 = divmod(int(ulog.start_timestamp / 1e6), 60)
    h1, m1 = divmod(m1, 60)
    return "{:d}:{:02d}:{:02d}".format(h1, m1, s1)


def get_duration(ulog):
    """Compute the duration for which data was logged.
    
    Arguments:
    ulog -- messages stored in ulog structure

    """
    m2, s2 = divmod(
        int((ulog.last_timestamp - ulog.start_timestamp) / 1e6), 60
    )
    h2, m2 = divmod(m2, 60)
    return "{:d}:{:02d}:{:02d}".format(h2, m2, s2)


def get_date(ulog):
    """Recover the date at which the .ulg file has been created.
    
    Arguments:
    ulog -- messages stored in ulog structure

    """
    gps_data = ulog.get_dataset("vehicle_gps_position")
    indices = np.nonzero(gps_data.data["time_utc_usec"])
    if len(indices[0]) > 0:
        return datetime.datetime.fromtimestamp(
            gps_data.data["time_utc_usec"][0] / 1000000
        )
    else:
        return None


def get_param(ulog, parameter_name, default):
    """Recover a parameter from the ulog structure.
    
    Arguments:
    ulog -- messages stored in ulog structure
    parameter_name -- name of the parameter that should be recovered
    default -- default value that will be returned if the parameter is not available

    """
    if parameter_name in ulog.initial_parameters.keys():
        return ulog.initial_parameters[parameter_name]
    else:
        return default


def add_param(ulog, parameter_name, dataframe):
    """add a parameter from the ulog structure to the dataframe.

    If parameters have changed, update them in the dataframe.
    
    Arguments:
    ulog -- messages stored in ulog structure
    parameter_name -- name of the parameter that should be recovered
    dataframe -- pandas dataframe which contains all messages of the required topics

    """
    dataframe["parameter_name"] = get_param(ulog, parameter_name, 0)
    if len(ulog.changed_parameters) > 0:
        for time, name, value in ulog.changed_parameters:
            if name == parameter_name:
                dataframe[dataframe[parameter_name]]
