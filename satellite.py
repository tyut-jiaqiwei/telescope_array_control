import numpy as np
import random
import time
##1.两个函数一个是大地坐标转换球坐标Geodetic_to_spherical；一个是球坐标转换大地坐标spherical_to_Geodetic。
import math
from math import pi,exp,inf


#######################大地转换球坐标####################################
def Geodetic_to_spherical(latitude,longitude,altitude):
	B=math.radians(latitude)
	L=math.radians(longitude)
	H=altitude
	f=1/298.257223563
	r=6378137
	b=r*(1-f)
	e=math.sqrt(2*f-f*f)
	N=r/math.sqrt(1-e*e*math.sin(B)*math.sin(B))
	#大地坐标转空间直角坐标存放到data数组中
	data =[(N+H)*math.cos(B)*math.cos(L),(N+H)*math.cos(B)*math.sin(L),(N*(1-e*e)+H)*math.sin(B)]
	#直角坐标住那换球坐标存放到data_spherical数组中
	data_spherical = [math.sqrt(data[0]*data[0]+data[1]*data[1]+data[2]*data[2]),
				 math.atan(math.sqrt(data[0]*data[0]+data[1]*data[1])/data[2])*180/math.pi,
				 math.atan(data[1]/data[0])*180/math.pi] #空间直角坐标xyz转换成球坐标 r sita fai

	return data_spherical

##########################球转大地#########################################
def spherical_to_Geodetic(r,p,f):
	f=1/298.257223563
	r=6378137
	b=r*(1-f)
	e=math.sqrt(2*f-f*f)
	e2 = (1/(1-e))-1
	###得到空间直角坐标xyz存到数组data【0~2】中
	data = [r*math.sin(p)*math.cos(f),r*math.sin(p)*math.sin(f),r*math.cos(p)]
	ppp = math.atan(data[2]*r/(b*math.sqrt(data[0]*data[0]+data[1]*data[1])))
	###存放大地坐标的数组data_Geodetic 【0~2】对应L B H
	data_Geodetic = [0,0,0]
	#  大地坐标L=data_Geodetic[0]
	data_Geodetic[0] = math.atan(data[1]/data[0])
	#  大地坐标B=data_Geodetic[1]
	data_Geodetic[1] = math.atan((data[2]+e2*e2*b*math.sin(ppp)*math.sin(ppp)*math.sin(ppp))/(math.sqrt(data[0]*data[0]+data[1]*data[1])-e*e*r*math.cos(ppp)*math.cos(ppp)*math.cos(ppp)))
	B=data_Geodetic[1]
	N = r / math.sqrt(1 - e * e * math.sin(B) * math.sin(B))
	#  大地坐标H=data_Geodetic[2]
	data_Geodetic[2] = (math.sqrt(data[0]*data[0]+data[1]*data[1])/math.cos(B))-N

	return data_Geodetic

# #a1存放待转换的大地坐标
# a1=[100,101,1500]
# a = Geodetic_to_spherical(a1[0],a1[1],a1[2])
#
# #b1存放待转换的大地坐标
# b1= [6359000, 22, 33]
# b = spherical_to_Geodetic(b1[0],b1[1],b1[2])
#
# print('输入大地坐标[L,B,H]：',a1,'  输出的球坐标为[r,sita,fai]:',a)
# print('\n')
# print('输入球坐标[r,sita,fai]：',b1,'  输出的大地坐标[L,B,H]为:',b)

class Object:
    def __init__(self,signal,satellitelist,height,speed):

        self.height = height  # 单位：千米
        self.speed = speed   #  单位：度每分
        self.signal = "S"+str(signal)    # 目标编号
        self.satellitelist = satellitelist  # 已知卫星列表
        # self.bright = bright
        # self.position = position


class satellite(Object):
    def __init__(self, signal, satellitelist,height, speed, fai,Clockwise):
        Object.__init__(self, signal,satellitelist, height, speed)

        # 球坐标
        self.R = 6378 + height    # 地球的长半轴为6378137m
        self.bright = 1000*1/height + 0.0001    # 卫星的亮度，目前写的卫星高度在1000-10000，即亮度在0.01-1之间
        self.sita = random.uniform(0.0, 360.0)  # 角度
        self.fai = fai
        self.Clockwise = Clockwise   # 卫星顺时针还是逆时针

        if self.speed == 0 :   # 如果速度为0（地球同步），默认周期为无限
            self.T = inf
        else:
            self.T = 360/self.speed    # 周期用分钟表示

        # 大地坐标
        self.X,self.Y,self.H = spherical_to_Geodetic(self.R,self.sita,self.fai)[0], \
                               spherical_to_Geodetic(self.R, self.sita, self.fai)[1], \
                               spherical_to_Geodetic(self.R, self.sita, self.fai)[2]

        # 该卫星是否已经被观测
        self.be_observabed = False
        # 该卫星的观测价值
        self.value = 1
        # 这个属性用于卫星价值函数的衰减上
        self.value_sample = 0
        # 卫星编号
        self.signal = "O"+str(signal)  # 目标编号,O为普通卫星

        # .orbit = self.get_orbit()
        # self.



    def get_current_postion(self):
        # 每隔1min更新一次位置，self.speed为度每分钟

        sita_ = self.speed * 1

        if self.Clockwise == True :
            self.sita += sita_
            self.sita %= 360
        else :
            self.sita -= sita_
            self.sita %= 360


        #　得到的是卫星球坐标的位置
        qiu = [self.R,self.sita,self.fai]

        # dadi = spherical_to_Geodetic(self.R,self.sita,self.fai)[0], \
        #                        spherical_to_Geodetic(self.R, self.sita, self.fai)[1], \
        #                        spherical_to_Geodetic(self.R, self.sita, self.fai)[2]


        # self.pos_x = float(self.height * math.sin(self.sita) * math.cos(self.fai))
        # self.pos_y = float(self.height * math.sin(self.sita) * math.sin(self.fai))

        return qiu

    def value_upgrade(self):
        if self.value != 1:
            self.value_sample += 1
            decay = 20
            self.value = 1 - 0.99 * exp(-1. * self.value_sample/decay)
            if self.value >=  1.:
                self.value = 1.
        else:
            self.value_sample = 0


    def get_orbit(self):

        orbit_list = []
        start_sita = self.sita
        while True:
            postion = self.get_current_postion()
            orbit_list.append(postion)
            if abs(self.sita - start_sita) <= self.speed/10.:
                break
        return orbit_list

    def in_list(self):
        for signals in self.satellitelist:
            if self.signal == signals :
                return True
            return False

    def add_list(self):
        if self.in_list() == False:
            self.satellitelist.append(self.signal)


# 地球同步卫星轨道 ,轨道高37586km，轨道角为0或pi
class Geosynchronous_satellite(satellite):
    def __init__(self,signal, satellitelist,height = 37586,speed = 0, fai = 0):
        satellite.__init__(self, signal ,satellitelist,height,speed,fai ,Clockwise=True)

        # 球坐标
        # self.R = height  # 地球的长半轴为6378137，地球同步卫星轨道
        self.sita = random.uniform(0.0, 360.0)  # 角度
        #  self.fai = fai
        self.speed = speed
        self.T = inf

        # 该卫星是否已经被观测
        self.be_observabed = False
        # 该卫星的观测价值
        self.value = 1
        # 卫星编号
        self.signal = "A"+str(signal)   # A类表示为地球同步卫星
        # 已知卫星列表
        self.satellitelist = satellitelist

    def get_current_postion(self):
        return [self.R,self.sita,self.fai]

# 太阳同步卫星 高度小于6000，速度一定（T = 96min），轨道倾角97.8，
# 每天向东移动0.9856度,这个角度正好是地球绕太阳公转每天东移的角度。
class Solar_synchronous_satellite(satellite):
    def __init__(self,signal, satellitelist,height, speed = 360/96, fai = 97.8):
        satellite.__init__(self, signal,satellitelist,height, speed ,fai,Clockwise=True)

        # 球坐标
        # self.R = height  # 地球的长半轴为6378137，地球同步卫星轨道
        self.sita = random.uniform(0.0, 360.0)  # 角度
        #  self.fai = fai

        # 该卫星是否已经被观测
        self.be_observabed = False
        # 该卫星的观测价值
        self.value = 1
        # 卫星编号
        self.signal = "B"+str(signal)   # B类表示为太阳同步卫星
        # 已知卫星列表
        self.satellitelist = satellitelist

# 极地轨道卫星
class Polar_orbiting_satellite(satellite):
    def __init__(self,signal, satellitelist,height, speed , fai = 90):
        satellite.__init__(self, signal,satellitelist,height, speed ,fai,Clockwise=True)

        # 球坐标
        # self.R = height  # 地球的长半轴为6378137，地球同步卫星轨道
        self.sita = random.uniform(0.0, 360.0)  # 角度
        #  self.fai = fai

        # 该卫星是否已经被观测
        self.be_observabed = False
        # 该卫星的观测价值
        self.value = 1
        # 卫星编号
        self.signal = "C"+str(signal)   # C类表示为极地轨道卫星
        # 已知卫星列表
        self.satellitelist = satellitelist
