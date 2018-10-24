from uloganalysis import ulogconv as conv
import pandas as pd 
import numpy as np 
import argparse
import os
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import pyulog

parser = argparse.ArgumentParser(description='Script to process position')
parser.add_argument('filename', metavar='file.ulg', help='ulog file')

def check_directory(filename):
    if os.path.isfile(filename):
        base, ext = os.path.splitext(filename)
        if ext.lower() not in ('.ulg'):
            parser.error('File is not .ulg file')
        else:
            return
    else:
        parser.error('File does not exist')

def get_position_state_setpoint_from_file(f):
    """
    return position state, setpoint and error 
    """

    topics = ['vehicle_local_position', 'vehicle_local_position_setpoint']
    ulog = pyulog.ULog(f, topics)
    pandadict = conv.createPandaDict(ulog)
    return conv.merge(pandadict)