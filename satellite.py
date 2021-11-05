import ephem
from numpy import exp,nan,inf
import random


class Object():
    def __init__(self,signal,satellitelist,tle):
        self.signal = signal   # 目标编号
        self.satellitelist = satellitelist  # 已知卫星列表
        self.tle = tle
        # self.time = time
        # self.bright = bright
        # self.position = position


class satellite(Object):
    def __init__(self, signal, satellitelist,tle,scale):
        Object.__init__(self, signal,satellitelist, tle)

        height = random.uniform(100,1000)
        self.scale = scale  # 卫星的尺寸，0.1-1
        self.bright = 100 * self.scale / height + 0.000001  # 卫星的亮度，

        # 该卫星是否已经被观测
        self.be_observabed = False
        # 该属性表示已知卫星多少个step没有被监测过
        self.have_observabed = 0
        # 该卫星的观测价值
        self.value = 10
        # 这个属性用于卫星价值函数的衰减上
        self.value_sample = 0
        # 卫星的测量误差
        self.error = inf


    def get_current_postion(self,time):
        try :
            line1 = self.tle['line1']
            line2 = self.tle['line2']
            line3 = self.tle['line3']
            iss = ephem.readtle(line1, line2, line3)
            iss.compute(time)
            self.a_ra, self.a_dec = iss.a_ra, iss.a_dec
        except:
            self.a_ra, self.a_dec = None,None

        return self.a_ra, self.a_dec


    def value_upgrade(self):
        decay = 20  # 当decay设置为20，sample大约为200，满足条件到1
        if self.value == 10:
            self.value = 10
            self.value_sample = 0
        elif 1 - self.value <= 1e-4:
            self.value = 1.
            self.value_sample = 0
        elif self.value < 1 and self.value != -1:
            self.value = 1 - 2 * exp(-1. * self.value_sample/decay)
            self.value_sample += 1
        elif self.value == -1 :
            self.value_sample = 1
            self.value = 1 - 2 * exp(-1. * self.value_sample /decay)

