import pandas as pd
import numpy as np
import argparse
import os
import matplotlib.pyplot as plt
import pyulog
from uloganalysis import ulogconv as conv
from uloganalysis import mathpandas as mpd

parser = argparse.ArgumentParser(description='Script to process attitude')
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


def get_attitude_state_setpoint_from_file(f):
    """
    return attitude-euler, setpoint and error
    """

    topics = ['vehicle_attitude', 'vehicle_attitude_setpoint']
    ulog = pyulog.ULog(f, topics)
    pandadict = conv.createPandaDict(ulog)
    return conv.merge(pandadict)


def add_roll_pitch_yaw(df):
    df['T_vehicle_attitude_0__F_roll'],
    df['T_vehicle_attitude_0__F_pitch'],
    df['T_vehicle_attitude_0__F_yaw'] = mpd.series_quat2euler(
        df['T_vehicle_attitude_0__F_q_0'],
        df['T_vehicle_attitude_0__F_q_1'],
        df['T_vehicle_attitude_0__F_q_2'],
        df['T_vehicle_attitude_0__F_q_3'])


def add_euler_error(df):
    df['T_vehicle_attitude_setpoint_0__F_e_roll'] = mpd.angle_wrap(
        df['T_vehicle_attitude_setpoint_0__F_roll_body'] -
        df['T_vehicle_attitude_0__F_roll'])
    df['T_vehicle_attitude_setpoint_0__F_e_pitch'] = mpd.angle_wrap(
        df['T_vehicle_attitude_setpoint_0__F_pitch_body'] -
        df['T_vehicle_attitude_0__F_pitch'])
    df['T_vehicle_attitude_setpoint_0__F_e_yaw'] = mpd.angle_wrap(
        df['T_vehicle_attitude_setpoint_0__F_yaw_body'] -
        df['T_vehicle_attitude_0__F_yaw'])


def add_vehicle_z_axis(df):
    x = pd.Series(np.zeros(df.shape[0]), index=df['timestamp'],
                  name='T_vehicle_attitude_0__F_body_z_axis_x')
    y = pd.Series(np.zeros(df.shape[0]), index=df['timestamp'],
                  name='T_vehicle_attitude_0__F_body_z_axis_y')
    z = pd.Series(np.ones(df.shape[0]), index=df['timestamp'],
                  name='T_vehicle_attitude_0__F_body_z_axis_z')
    x, y, z = mpd.series_quatrot(x, y, z,
                            df['T_vehicle_attitude_0__F_q_0'],
                            df['T_vehicle_attitude_0__F_q_1'],
                            df['T_vehicle_attitude_0__F_q_2'],
                            df['T_vehicle_attitude_0__F_q_3'])

    df[x.name] = x.values
    df[y.name] = y.values
    df[z.name] = z.values


def add_desired_tilt(df):

    if 'T_vehicle_attitude_setpoint_0__F_body_z_axis_sp_x' not in df:
        add_desired_z_axis(df)

    x = pd.Series(np.zeros(df.shape[0]), index=df['timestamp'], name='x')
    y = pd.Series(np.zeros(df.shape[0]), index=df['timestamp'], name='y')
    z = pd.Series(np.ones(df.shape[0]), index=df['timestamp'], name='z')

    tilt = mpd.series_dot(
        x,
        y,
        z,
        df['T_vehicle_attitude_setpoint_0__F_body_z_axis_sp_x'],
        df['T_vehicle_attitude_setpoint_0__F_body_z_axis_sp_y'],
        df['T_vehicle_attitude_setpoint_0__F_body_z_axis_sp_z'])
    df['T_vehicle_attitude_setpoint_0__F_tilt_desired'] = tilt.values
    df['T_vehicle_attitude_setpoint_0__F_tilt_desired'] = df['T_vehicle_attitude_setpoint_0__F_tilt_desired'].apply(
        np.arccos)


def add_tilt(df):

    if 'T_vehicle_attitude_0__F_body_z_axis_x' not in df:
        add_vehicle_z_axis(df)

    x = pd.Series(np.zeros(df.shape[0]), index=df['timestamp'], name='x')
    y = pd.Series(np.zeros(df.shape[0]), index=df['timestamp'], name='y')
    z = pd.Series(np.ones(df.shape[0]), index=df['timestamp'], name='z')

    tilt = mpd.series_dot(x, y, z,
                          df['T_vehicle_attitude_0__F_body_z_axis_x'],
                          df['T_vehicle_attitude_0__F_body_z_axis_y'],
                          df['T_vehicle_attitude_0__F_body_z_axis_z'])
    df['T_vehicle_attitude_0__F_tilt'] = tilt.values
    df['T_vehicle_attitude_0__F_tilt'] = df['T_vehicle_attitude_0__F_tilt'].apply(
        np.arccos)


def add_vehicle_inverted(df):

    if 'T_vehicle_attitude_0__F_body_z_axis_z' not in df:
        add_vehicle_z_axis(df)

    df['T_vehicle_attitude_0__F_tilt_more_90'] = df.T_vehicle_attitude_0__F_body_z_axis_z.values
    df[df[['T_vehicle_attitude_0__F_tilt_more_90']] >= 0] = 0
    df[df[['T_vehicle_attitude_0__F_tilt_more_90']] < 0] = 1


def add_desired_z_axis(df):
    x = pd.Series(np.zeros(df.shape[0]), index=df['timestamp'],
                  name='T_vehicle_attitude_setpoint_0__F_body_z_axis_sp_x')
    y = pd.Series(np.zeros(df.shape[0]), index=df['timestamp'],
                  name='T_vehicle_attitude_setpoint_0__F_body_z_axis_sp_y')
    z = pd.Series(np.ones(df.shape[0]), index=df['timestamp'],
                  name='T_vehicle_attitude_setpoint_0__F_body_z_axis_sp_z')

    x, y, z = mpd.series_quatrot(x, y, z,
                                 df['T_vehicle_attitude_setpoint_0__F_q_d_0'],
                                 df['T_vehicle_attitude_setpoint_0__F_q_d_1'],
                                 df['T_vehicle_attitude_setpoint_0__F_q_d_2'],
                                 df['T_vehicle_attitude_setpoint_0__F_q_d_3'])
    df[x.name] = x.values
    df[y.name] = y.values
    df[z.name] = z.values


def main():
    args = parser.parse_args()
    check_directory(args.filename)

    df = get_attitude_state_setpoint_from_file(args.filename)
    df.timestamp = (df.timestamp - df.timestamp[0]) * 1e-6  # change to seconds
    # add_roll_pitch_yaw(df)
    # add_euler_error(df)
    # add_vehicle_z_axis(df)
    # add_vehicle_inverted(df)
    # dd_desired_z_axis(df)
    # add_desired_tilt(df)
    add_tilt(df)
    print(df['T_vehicle_attitude_0__F_tilt'] * (180 / np.pi))

    # # plot roll / pitch / yaw error
    # df_euler = df[['timestamp','T_vehicle_attitude_setpoint_0__F_e_roll',
    #                  'T_vehicle_attitude_setpoint_0__F_e_pitch',
    #                  'T_vehicle_attitude_setpoint_0__F_e_yaw']]
    # df_euler.plot(x='timestamp')

    # # plot inverted
    # df_inverted = df[['timestamp','T_vehicle_attitude_0__F_tilt_more_90']]
    # df_inverted.plot(x='timestamp', y='T_vehicle_attitude_0__F_tilt_more_90')

    # # plot desired z-axis
    # df[['timestamp', 'T_vehicle_attitude_setpoint_0__F_body_z_axis_sp_x',
    #                  'T_vehicle_attitude_setpoint_0__F_body_z_axis_sp_y',
    #                  'T_vehicle_attitude_setpoint_0__F_body_z_axis_sp_z']].plot(x='timestamp')

    # # plot tilt and desired tilt
    # df[['timestamp', 'T_vehicle_attitude_setpoint_0__F_tilt_desired']].plot(x='timestamp')
    df[['timestamp', 'T_vehicle_attitude_0__F_tilt']].plot(x='timestamp')

    # # add radians
    # df['T_vehicle_attitude_setpoint_0__F_tilt_desired_deg'] = df['T_vehicle_attitude_setpoint_0__F_tilt_desired'].values * 180 /np.pi
    # df['T_vehicle_attitude_0__F_tilt_deg'] = df['T_vehicle_attitude_0__F_tilt'].values * 180 /np.pi
    # df[['timestamp', 'T_vehicle_attitude_0__F_tilt_deg', 'T_vehicle_attitude_setpoint_0__F_tilt_desired_deg']].plot(x='timestamp')

    plt.show()  # show all plots
