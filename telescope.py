import math
import random
from math import sin,cos,pi,atan,radians
import numpy as np

# 球坐标转直角坐标
def Spherical_to_rectangular(pos):
    r = pos[0]
    sita = radians(pos[1])
    fai = radians(pos[2])
    x = r * sin(sita) * cos(fai)
    y = r * sin(sita) * sin(fai)
    z = r * cos(sita)
    return [x,y,z]

# 直角坐标转求球坐标
def rectangular_to_Spherical(pos):
    x = pos[0]
    y = pos[1]
    z = pos[2]
    r = np.sqrt(x**2 + y**2 + z**2)
    sita = atan(np.sqrt(x**2 + y**2)/z)*180/pi   # 弧度转成角度
    fai = atan(y/x)*180/pi
    return [r,sita,fai]


class telescope:
    def __init__(self,signal,position,caliber,satellitelist,field):
        self.signal = signal       # 望远镜编号
        self.position = position   # 望远镜所在位置
        self.satellitelist = satellitelist   # 已知卫星列表
        self.observabing = False   # 是否已经观测到卫星
        self.caliber = caliber    # 口径,口径越大，能观测到的亮度越低（在我这里，将卫星亮度和望远镜口径相乘为最后亮度）
        self.field = field  # 视场，视场越大，范围越大
        # self.bright = 1/caliber


        self.sita = random.uniform(-90, 90)  # 角度
        self.fai = random.uniform(0.0,360)   # 角度

    #返回望远镜当前能观测的区域。参数：口径r，角度sita，fai。
    # 但是不会这么写，目前是传入卫星的位置，判断是否再该区域
    def observabe_area(self,satellite_pos):

        min_sita,max_sita = self.sita - self.field/10 , self.sita + self.field/10

        [x, y, z] = Spherical_to_rectangular(satellite_pos)
        [x_, y_, z_] = Spherical_to_rectangular(self.position)
        [x0, y0, z0] = [x-x_, y-y_, z-z_]
        [r0, sita0, fai0] = rectangular_to_Spherical([x0, y0, z0])
        if min_sita <= sita0 <= max_sita :
            return True
        else:
            return False



    # 返回该望远镜可观测的全部区域。参数：位置position，望远镜天顶角范围为+-60度
    # 但是不会把区域整个求出来，目前是传入卫星的位置，判断是否再该区域
    def all_area(self,satellite_pos):
        [x, y, z] = Spherical_to_rectangular(satellite_pos)
        [x_, y_, z_] = Spherical_to_rectangular(self.position)
        [x0, y0, z0] = [x - x_, y - y_, z - z_]
        [r0, sita0, fai0] = rectangular_to_Spherical([x0, y0, z0])
        if -60 <= sita0 <= 60:
            return True
        else:
            return False

    # 移动望远镜，每15分钟一次
    # 瞬移还是慢移
    def telescope_move(self):
        pass

    # 当观测到一颗新卫星时，计算其观测轨道
    def cal_orbit(self,satellite_signal):
        pass





