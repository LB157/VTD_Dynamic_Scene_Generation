# zolty add v into vtd
import csv
import os
from time import sleep

from pyproj import Proj


def scp_tools(cmd):
    temp = "/home/hil/VTD.2.2/Runtime/Tools/ScpGenerator/scpGenerator -w -p 48179 -i '%s'"
    temp = temp % cmd
    print(temp)
    # os.system(temp)


def car_init():
    cmd = '<Player name="vr" visible="true"><Create category="vehicle" vehicle="MB_Actros_2007_white" adaptDriverToVehicleType="true" control="internal" /></Player>'
    scp_tools(cmd)


def car_run(x, y, h):
    cmd = '<Set entity="player" name="vr"><PosInertial x="%s" y="%s" z="0" hDeg="%s" pDeg="0" rDeg="0" /> <Speed value="%s"/> </Set>'
    # cmd = '<Set entity="player" name="vr"><PosInertial x="%s" y="%s" z="0" hDeg="%s" pDeg="0" rDeg="0" /> <SpeedRelative  pivot="%s" value="%s"/> </Set>'
    # cmd = '<Set entity="player" name="vr"><PosInertial x="%s" y="%s" z="0" hDeg="%s" pDeg="0" rDeg="0" /></Set>'
    cmd = cmd % (x, y, h)
    scp_tools(cmd)


def wgs2tm(lon, lat):
    proj_param = '+proj=tmerc +lat_0=31.283368 +lon_0=121.181409 +k=1 +x_0=-36929.656 +y_0=22782.930 +ellps=WGS84 +units=m +units=m'
    p = Proj(proj_param)
    return p(lon, lat)


def load_csv(filepath):
    with open(filepath) as f:
        rows = csv.reader(f)
        for r in rows:
            car_run(r[0], r[1], r[2])
            sleep(1)


if __name__ == '__main__':
    car_init()
    load_csv("hv.csv")

