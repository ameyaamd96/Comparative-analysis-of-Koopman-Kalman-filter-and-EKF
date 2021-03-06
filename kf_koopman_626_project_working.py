# -*- coding: utf-8 -*-
"""kf_koopman_626_project_working

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Y9rZzQsTILIyJQskl2p_SzYx5CxkvRUh
"""

"""
Extended kalman filter (EKF) localization sample
author: Atsushi Sakai (@Atsushi_twi)
"""

import math

import matplotlib.pyplot as plt
import numpy as np

# Covariance for EKF simulation
Q = np.diag([
    0.1,  # variance of location on x-axis
    0.1,  # variance of location on y-axis
    np.deg2rad(1.0),  # variance of yaw angle
    np.sin(np.deg2rad(1.0)), 
    np.cos(np.deg2rad(1.0))
]) ** 2  # predict state covariance
R = np.diag([1.0, 1.0]) ** 2  # Observation x,y position covariance

#  Simulation parameter
INPUT_NOISE = np.diag([1.0, np.deg2rad(30.0)]) ** 2
GPS_NOISE = np.diag([0.5, 0.5]) ** 2

DT = 0.1  # time tick [s]
SIM_TIME = 10.0  # simulation time [s]

show_animation = True


def calc_input():
    v = 10.0  # [m/s]
    yawrate = 0.1  # [rad/s]
    u = np.array([[v], [yawrate]])
    return u


def observation(xTrue, xd, u):
    xTrue = motion_model(xTrue, u)
    
    # add noise to gps x-y
    z = observation_model(xTrue) + GPS_NOISE @ np.random.randn(2, 1)

    # add noise to input
    ud = u + INPUT_NOISE @ np.random.randn(2, 1)

    xd = motion_model(xd, ud)
    # xd = xd[0:2]
    # xTrue = xTrue[0:2]
    return xTrue, z, xd, ud


def motion_model(x, u):
    F = np.array([[1.0, 0, 0, 0, u[0]*DT],
                  [0, 1.0, 0, u[0]*DT, 0],
                  [0, 0, 1.0, 0, 0],
                  [0, 0, 0, np.cos(u[1]*DT), np.sin(u[1]*DT)],
                  [0, 0, 0, -np.sin(u[1]*DT), np.cos(u[1]*DT)]])

    B = np.array([[0.0, 0.0],
                  [0.0, 0.0],
                  [0.0, u[1]*DT],
                  [0.0, 0.0],
                  [0.0, 0.0]])

    x = F @ x + B @ u

    return x


def observation_model(x):
    H = np.array([
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0]
    ])

    z = H @ x

    return z


def jacob_f(x, u):
    yaw = x[2, 0]
    v = u[0, 0]
    jF = np.array([[1.0, 0, 0, 0, 1.0],
                  [0, 1.0, 0, 1.0, 0],
                  [0, 0, 1.0, 0, 0],
                  [0, 0, 0, np.cos(0.1*DT), np.sin(0.1*DT)],
                  [0, 0, 0, -np.sin(0.1*DT), np.cos(0.1*DT)]])

    return jF


def jacob_h():
    # Jacobian of Observation Model
    jH = np.array([
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0]
    ])

    return jH


def kkf_estimation(xEst, PEst, z, u):
    #  Predict
    xPred = motion_model(xEst, u)
    jF = jacob_f(xPred, u)
    PPred = jF @ PEst @ jF.T + Q

    #  Update
    jH = jacob_h()
    zPred = observation_model(xPred)
    y = z - zPred
    S = jH @ PPred @ jH.T + R
    K = PPred @ jH.T @ np.linalg.inv(S)
    xEst = xPred + K @ y
    PEst = (np.eye(len(xEst)) - K @ jH) @ PPred

    return xEst, PEst


def plot_covariance_ellipse(xEst, PEst):  # pragma: no cover
    # Ch = np.array([
    #     [1.0, 0.0, 0.0, 0.0, 0.0],
    #     [0.0, 1.0, 0.0, 0.0, 0.0],
    #     [0.0, 0.0, 1.0, 0.0, 0.0]], dtype='float')
    # Pxy = (Ch.dot(PEst)).dot(np.transpose(Ch))
    Pxy=PEst[0:2,0:2]
    eigval, eigvec = np.linalg.eig(Pxy)

    if eigval[0] >= eigval[1]:
        bigind = 0
        smallind = 1
    else:
        bigind = 1
        smallind = 0

    t = np.arange(0, 2 * math.pi + 0.1, 0.1)
    a = math.sqrt(eigval[bigind])
    b = math.sqrt(eigval[smallind])
    x = [a * math.cos(it) for it in t]
    y = [b * math.sin(it) for it in t]
    angle = math.atan2(eigvec[bigind, 1], eigvec[bigind, 0])
    rot = np.array([[math.cos(angle), math.sin(angle)],
                    [-math.sin(angle), math.cos(angle)]])
    fx = rot @ (np.array([x, y]))
    px = np.array(fx[0, :] + xEst[0, 0]).flatten()
    py = np.array(fx[1, :] + xEst[1, 0]).flatten()
    plt.plot(px, py, "--y")


def main():
    print(" start!!")

    time = 0.0

    # State Vector [x y yaw v]'
    # x0_mean = np.array([[0.0], [0.0], [0.0], [0.0], [1.0]], dtype='float')
    xEst = np.array([[0.0], [0.0], [0.0], [0.0], [1.0]], dtype='float')*np.random.rand()*5
    xTrue = np.array([[0.0], [0.0], [0.0], [0.0], [1.0]], dtype='float')*np.random.rand()*5
    PEst_init = np.eye(3)

    Ch = np.array([
        [1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0]], dtype='float')
    Ch_inv = np.linalg.pinv(Ch)
    PEst_tt = (Ch_inv).dot((PEst_init))
    PEst = PEst_tt.dot((np.transpose(Ch_inv)))
    xDR = np.array([[0.0], [0.0], [0.0], [0.0], [1.0]], dtype='float')*np.random.rand()*5 # Dead reckoning
    diff = np.linalg.norm(xTrue-xEst)
    # history
    hxEst = xEst
    hxTrue = xTrue
    hxDR = xTrue
    hz = np.zeros((2, 1))
    hdiff = diff
    htime = time
    hdiff_t = hdiff

    for i in range(50):
        while SIM_TIME >= time:
            time += DT
            u = calc_input()

            xTrue, z, xDR, ud = observation(xTrue, xDR, u)

            xEst, PEst = kkf_estimation(xEst, PEst, z, ud)
            diff = np.linalg.norm(xTrue-xEst)
            # store data history
            hxEst = np.hstack((hxEst, xEst))
            hxDR = np.hstack((hxDR, xDR))
            hxTrue = np.hstack((hxTrue, xTrue))
            hz = np.hstack((hz, z))
            hdiff = np.hstack((hdiff, diff))
            htime = np.hstack((htime, time))
        hdiff_t = hdiff_t + hdiff
    if show_animation:
        plt.cla()
        # plt.plot(hz[0, :], hz[1, :], ".g")
        # plt.plot(hxTrue[0, :].flatten(),
        #          hxTrue[1, :].flatten(), "-b")
        # plt.plot(hxDR[0, :].flatten(),
        #          hxDR[1, :].flatten(), "-k")
        # plt.plot(hxEst[0, :].flatten(),
        #           hxEst[1, :].flatten(), "-r")
        plt.plot(htime.flatten(),
                (hdiff_t.flatten())/50, "-b")
        # plot_covariance_ellipse(xEst, PEst)
        plt.axis("equal")
        plt.grid(True)
        plt.pause(0.1)
        

if __name__ == '__main__':
    main()

hxEst.shape

