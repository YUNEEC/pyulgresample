"""wrapper for plotting."""
import numpy as np


def plot_time_series(df, plt):
    """Plot a time series.

    Arguments:
    df -- dataframe containing messages from the required topics
    plt -- plot

    """
    # Remove the plot frame lines
    delta = (df["timestamp"].max() - df["timestamp"].min()) / 10
    plt.xticks(
        np.arange(
            df["timestamp"].min(),
            df["timestamp"].max(),
            step=np.around(delta, decimals=1),
        )
    )
    plt.grid()
