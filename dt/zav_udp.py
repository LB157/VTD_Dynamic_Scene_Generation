# zolty add v into vtd by udp
from pyproj import Proj
import os
import socket
import struct
import time


def scp_tools(cmd):
    temp = "/home/hil/VTD.2020/Runtime/Tools/ScpGenerator/scpGenerator -w -p 48179 -i '%s'"
    temp = temp % cmd
    print(temp)
    os.system(temp)


def car_init():
    cmd = '<Player name="vr" visible="true"><Create category="vehicle" vehicle="Peugeot_207_2011_snow white" adaptDriverToVehicleType="true" control="internal" /></Player>'
    scp_tools(cmd)


def car_run(x, y, h):
    cmd = '<Set entity="player" name="vr"><PosInertial x="%s" y="%s" z="14.0233" hDeg="%s" pDeg="0" rDeg="0" /></Set>'
    cmd = cmd % (x, y, h)
    scp_tools(cmd)


def wgs2tm(lon, lat):
    proj_param = '+proj=tmerc +lat_0=31.283368 +lon_0=121.181409 +k=1 +x_0=-36929.656 +y_0=22782.930 +ellps=WGS84 +units=m +units=m'
    p = Proj(proj_param)
    return p(lon, lat)


def udp_recv():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = ('0.0.0.0', 7778)
    s.bind(address)
    s.settimeout(5)
    flag = True
    while flag:
        try:
            data, addr = s.recvfrom(1024)
            content = struct.unpack("<3i", data)
            lon = content[1]/10000000.0
            lat = content[0]/10000000.0
            heading = content[2]/80.0
            x , y = wgs2tm(lon, lat)
            car_run(x , y, heading)
        except socket.timeout:
            print("Recv DUTPos TimeOut!")
        time.sleep(0.05)


if __name__ == '__main__':
    car_init()
    udp_recv()
