"""Create dataframe with messages required to run local position tests.

Store topics required for local position tests. 
Add missing messages to the dataframe which are required for local position tests. 

"""
import pandas as pd
import numpy as np
import argparse
import os
import pyulog
from pyulgresample import ulogconv as conv
from pyulgresample import mathpandas as mpd
from pyulgresample import plotwrapper as pltw
from pyulgresample import loginfo
from pyulgresample import dfUlg

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

parser = argparse.ArgumentParser(description="Script to process attitude")
parser.add_argument("filename", metavar="file.ulg", help="ulog file")


class dfUlgPosition(dfUlg.dfUlgBase):
    """dfUlgBase-Childclass for local position- and setpoint-topics.

    Store required topics and messages, 
    compute new messages and add them to the dataframe.

    Arguments:
    dfUlg.dfUlgBase -- Parentclass

    """

    @classmethod
    def get_required_topics(cls):
        """Return a list with the required topics."""
        return ["vehicle_local_position", "vehicle_local_position_setpoint"]

    @classmethod
    def get_required_zoh_topics(cls):
        """Return a list of topics for which zero order hold is applied."""
        return []

    @classmethod
    def get_nan_topic_msgs(self):
        """Return a list of TopicMsgs wich are nan."""
        return [
            dfUlg.TopicMsgs("vehicle_local_position_setpoint", ["x", "y", "z"])
        ]


def print_pdf(df, pdf, topic_1, topic_2, title, y_label, iterator):
    """Create a plot in a pdf with the information passed as arguments.
    
    Arguments:
    df -- dataframe containing messages from the required topics
    pdf -- pdf file
    topic_1 -- name of one of the messages whose data will be plotted
    topic_2 -- name of one of the messages whose data will be plotted
    title -- title of the plot
    y_label -- label for the y axis
    iterator -- number of the plot in the pdf

    """
    # desired and measured x position
    plt.figure(iterator, figsize=(20, 13))
    df_tmp = df[["timestamp", topic_1, topic_2]].copy()
    df_tmp.plot(x="timestamp", linewidth=0.8)
    pltw.plot_time_series(df_tmp, plt)
    plt.title(title)
    plt.ylabel(y_label)
    pdf.savefig()
    plt.close(iterator)


def add_horizontal_distance(df):
    """Compute the horizontal distance between the aircraft and the home point.
                
    Arguments:
    df -- dataframe containing messages from the required topics
    
    """
    abs_horizontal_dist = pd.Series(
        np.zeros(df.shape[0]),
        index=df["timestamp"],
        name="T_vehicle_local_position_0__NF_abs_horizontal_dist",
    )

    abs_horizontal_dist = mpd.series_pythagoras(
        df["T_vehicle_local_position_0__F_x"],
        df["T_vehicle_local_position_0__F_y"],
    )
    df[
        "T_vehicle_local_position_0__NF_abs_horizontal_dist"
    ] = abs_horizontal_dist.values


def main():
    """Call methods and create pdf with plots showing relevant data."""
    args = parser.parse_args()
    # create dataframe-ulog class for Position/Position-setpoint topic
    pos = dfUlgPosition.create(args.filename)

    with PdfPages("px4_position.pdf") as pdf:

        add_horizontal_distance(pos.df)

        # TODO: make print_pdf adapt to different numbers of messages
        # desired and measured x position
        print_pdf(
            pos.df,
            pdf,
            "T_vehicle_local_position_0__F_x",
            "T_vehicle_local_position_setpoint_0__F_x",
            "x position",
            "meters",
            0,
        )

        # desired and measured y position
        print_pdf(
            pos.df,
            pdf,
            "T_vehicle_local_position_0__F_y",
            "T_vehicle_local_position_setpoint_0__F_y",
            "y position",
            "meters",
            1,
        )

        # desired and measured z position
        print_pdf(
            pos.df,
            pdf,
            "T_vehicle_local_position_0__F_z",
            "T_vehicle_local_position_setpoint_0__F_z",
            "z position",
            "meters",
            2,
        )

        # horizontal distance to home
        print_pdf(
            pos.df,
            pdf,
            "T_vehicle_local_position_0__NF_abs_horizontal_dist",
            "T_vehicle_local_position_0__NF_abs_horizontal_dist",
            "absolute horizontal distance",
            "meters",
            3,
        )

        print("px4_position.pdf was created")
