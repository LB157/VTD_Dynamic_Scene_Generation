# zolty add v into vtd
import csv
import os
from time import sleep
from pyproj import Proj
import math

# rcs值 、角度值、速度值、距离值
def scp_tools(cmd):
    temp = "/home/hil/VTD.2020/Runtime/Tools/ScpGenerator/scpGenerator -w -p 48179 -i '%s'"
    temp = temp % cmd
    print(temp)
    os.system(temp)

def txt2_csv():
    # 打开文本文件以进行读取
    with open('./csv/input_dataRD.txt', 'r') as file:
        # 读取每一行并拆分成列,直接转化为数组
        lines=[]
        for line in file.readlines():
            linea = [float(value) for value in line.strip().split(' ') if value]
            lines.append(linea)
        
        
        # lines = [line.strip().split() for line in file.readlines()]
    # 将数据保存为CSV
    with open('intput_vtd.csv', 'w', newline='') as csvfile:
        # 使用逗号分隔符创建CSV写入对象
        csvwriter = csv.writer(csvfile,delimiter=',')
        # 写入数据行
        for line in lines:
            # 现在再转化为数组
            # data = [float(item) for item in str(line).strip().split(' ') if item]  
            csvwriter.writerow(line)



def car_init():
    cmd = '<Player name="vr" visible="true"><Create category="vehicle" vehicle="MB_Actros_2007_white" adaptDriverToVehicleType="true" control="internal" /></Player>'
    scp_tools(cmd)


def car_run(x, y, h):
    cmd = '<Set entity="player" name="vr"><PosInertial x="%s" y="%s" z="0" hDeg="%s" pDeg="0" rDeg="0" /><Speed value="%s" /></Set>'
    cmd = cmd % (x, y, h)
    scp_tools(cmd)


def wgs2tm(lon, lat):
    proj_param = '+proj=tmerc +lat_0=31.283368 +lon_0=121.181409 +k=1 +x_0=-36929.656 +y_0=22782.930 +ellps=WGS84 +units=m +units=m'
    p = Proj(proj_param)
    return p(lon, lat)


def message2terminal():
    # <Query entity="palyer" name=""> <PosInertial /><Speed /></Query>
    print('d')



def load_csv(filepath):
    Point2front=3.536
    Point2behind=0.858
    x0=250.157
    y0=152.084
    x2ego=250.157
    y2ego=152.084+Point2front
    with open(filepath, encoding="utf-8-sig") as f:
        rows = csv.reader(f)
        for r in rows:
            angle=float(r[1])
            speed=float(r[2])
            dist=float(r[3])
            # 角度的大小（以弧度为单位）
            angle_in_radians = math.radians(angle)
            # 计算正弦值
            sin_value = math.sin(angle_in_radians)
            # 计算余弦值
            cos_value = math.cos(angle_in_radians)

            if(speed<=0):
                rotate_angle=270-angle
                dist_player=dist+Point2front
            if(speed>0):
                rotate_angle=90-angle
                dist_player=dist+Point2behind  
            x2player=x2ego+sin_value*dist_player
            y2player=y2ego+cos_value*dist_player
            # x = float(r[0]) - 37272
            # y = float(r[1]) + 22529
            car_run(x2player, y2player,rotate_angle,speed)
            sleep(100)


if __name__ == '__main__':
    # txt2_csv()
    # car_init()
    load_csv("intput_vtd.csv")

