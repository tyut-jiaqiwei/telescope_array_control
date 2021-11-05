import ephem
import random
from numpy import pi


class telescope:
    def __init__(self,signal,position,caliber,satellitelist,field):
        self.signal = signal       # 望远镜编号
        self.position = position   # 望远镜所在位置,经纬度
        self.satellitelist = satellitelist   # 已知卫星列表
        self.observabing = False   # 是否已经观测到卫星
        self.observation_state = 0
        self.caliber = caliber    # 口径,口径越大，能观测到的亮度越低（在我这里，将卫星亮度和望远镜口径相乘为最后亮度）
        self.field = field  # 视场，视场越大，范围越大
        # self.bright = 1/caliber


        self.find_new = 0
        self.find_old = 0

        self.sita = 0
        self.fai  = 0

    #返回望远镜当前能观测的区域。参数：口径r，角度sita，fai。
    # 但是不会这么写，目前是传入卫星的位置，判断是否再该区域
    def observabe_area(self,satellite_pos):
        pass

    # 返回该望远镜可观测的全部区域。参数：位置position，望远镜天顶角范围为+-60度
    # 但是不会把区域整个求出来，目前是传入卫星的位置，判断是否再该区域
    def all_area(self,satellite_pos):
        pass

    # 移动望远镜，每15分钟一次
    # 瞬移还是慢移
    def telescope_move(self):
        pass

    # 当观测到一颗新卫星时，计算其观测轨道
    def cal_orbit(self,satellite_signal):
        pass