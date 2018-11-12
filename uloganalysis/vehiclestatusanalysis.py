import pandas as pd
import numpy as np
import argparse
import os
import pyulog
from uloganalysis import ulogconv as conv
from uloganalysis import mathpandas as mpd
from uloganalysis import plotwrapper as pltw
from uloganalysis import loginfo

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


parser = argparse.ArgumentParser(description="Script to process attitude")
parser.add_argument("filename", metavar="file.ulg", help="ulog file")


def check_directory(filename):
    if os.path.isfile(filename):
        base, ext = os.path.splitext(filename)
        if ext.lower() not in (".ulg"):
            parser.error("File is not .ulg file")
        else:
            return
    else:
        parser.error("File does not exist")


def print_pdf(df, pdf, topic_1, topic_2, title, y_label, iterator):
    # desired and measured x position
    plt.figure(iterator, figsize=(20, 13))
    df_tmp = df[["timestamp", topic_1, topic_2]].copy()
    df_tmp.plot(x="timestamp", linewidth=0.8)
    pltw.plot_time_series(df_tmp, plt)
    plt.title(title)
    plt.ylabel(y_label)
    pdf.savefig()
    plt.close(iterator)


def main():
    args = parser.parse_args()
    check_directory(args.filename)

    with PdfPages("px4_vehicle_status.pdf") as pdf:

        topics = [
            "vehicle_local_position",
            "vehicle_local_position_setpoint",
            "vehicle_status",
        ]
        ulog = pyulog.ULog(args.filename, topics)
        pandadict = conv.createPandaDict(ulog)
        df = conv.merge(pandadict)
        df.timestamp = (
            df.timestamp - df.timestamp[0]
        ) * 1e-6  # change to seconds

        print_pdf(
            df,
            pdf,
            "T_vehicle_status_0__F_nav_state",
            "T_vehicle_status_0__F_nav_state",
            "vehicle status",
            "-",
            0,
        )

        print("PDF was created")
