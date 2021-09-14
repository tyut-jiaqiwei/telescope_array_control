import numpy as np
import random
import time
from math import pi,sin,cos
from telescope import telescope
from  satellite import satellite,Geosynchronous_satellite,Solar_synchronous_satellite,Polar_orbiting_satellite



class env:
    def __init__(self,O_Snumber = 0,A_Snumber = 0,B_Snumber = 0,C_Snumber = 0,T_number = 0):

        self.all_satellitelist = []   # 环境中构建出来的所有卫星存储在该列表中
        self.satellitelist = []       # 已探察到的卫星的列表，存储的是已知卫星的编号
        self.step = 0                 # 目前一个step为1min
        self.obs_orbit = {}           # 已知卫星的编号和轨道，轨道用列表存储，列表长度为周期（min）

        self.O_Snumber = O_Snumber  # 普通卫星数量
        self.A_Snumber = A_Snumber  # 地球同步数量
        self.B_Snumber = B_Snumber  # 太阳同步数量
        self.C_Snumber = C_Snumber  # 极地卫星数量
        self.T_number  = T_number   # 望远镜数量

        self.all_telescope = []

    # 该函数目的：创建普通卫星，高度，速度，角度随机
    def create_satellite(self,number):
        for i in range(number):
            height = random.uniform(1000,10000)     # 海拔
            speed = random.uniform(0.01, 6)  # 角度
            signal = self.O_Snumber
            satellitelist = self.satellitelist
            fai = random.uniform(0.0, 360)   # 角度

            satellite_i = satellite(signal,satellitelist,height,speed,fai,True)
            self.all_satellitelist.append(satellite_i)
            self.O_Snumber += 1

    # 该函数目的：创建地球同步卫星
    def create_Geosynchronous_satellite(self,number):
        for i in range(number):
            signal = self.A_Snumber
            satellitelist = self.satellitelist

            satellite_i = Geosynchronous_satellite(signal, satellitelist)
            self.all_satellitelist.append(satellite_i)
            self.A_Snumber += 1

    # # 该函数目的：创建太阳同步卫星，高度随机
    def create_Solar_synchronous_satellite(self,number):
        for i in range(number):
            signal = self.B_Snumber
            satellitelist = self.satellitelist
            height = random.uniform(1000, 6000)
            satellite_i = Solar_synchronous_satellite(signal,satellitelist,height)
            self.all_satellitelist.append(satellite_i)
            self.B_Snumber += 1

    # 创建极地卫星
    def create_Polar_orbiting_satellite(self,number):
        for i in range(number):
            signal = self.C_Snumber
            satellitelist = self.satellitelist
            height = random.uniform(1000, 10000)
            speed = random.uniform(0.01, 6)  # 角度
            satellite_i = Polar_orbiting_satellite(signal,satellitelist,height,speed)
            self.all_satellitelist.append(satellite_i)
            self.C_Snumber += 1

    # 创建望远镜
    def create_telescope(self,number):
        for i in range(number):
            telescope_signal = 'T'+str(self.T_number)
            telescope_i = telescope(telescope_signal,[6378,30,30],5,self.satellitelist,1)
            self.all_telescope.append(telescope_i)
            self.T_number += 1

    # 该函数目的旨在更新系统环境，更新卫星的位置和望远镜观测位置
    def upgrade(self):
        self.step += 1
        for satellite in self.all_satellitelist:
            qiu =satellite.get_current_postion()    # 更新每颗卫星的当前价值
            satellite.value_upgrade()  # 更新每颗卫星的观测价值

            # if satellite.signal == "A50":
            #     print(satellite.signal,qiu,self.step)
            #     print(satellite.speed,len(satellite.get_orbit()))
        return self

    # 改函数旨在新增不同类型的卫星,弃用
    def add_new_satellite(self,type,height = 0,speed = 0,fai =0):
        satellitelist = self.satellitelist
        if type == "O":
            self.O_Snumber += 1
            signal = "O"+str(self.O_Snumber)
            new_satellite = satellite(signal,satellitelist,height,speed,fai,True)
            self.all_satellitelist.append(new_satellite)
        elif type == "A":
            self.A_Snumber += 1
            signal = "A" + str(self.A_Snumber)
            new_satellite = Geosynchronous_satellite(signal,satellitelist)
            self.all_satellitelist.append(new_satellite)
        elif type == "B":
            self.B_Snumber += 1
            signal = "B" + str(self.B_Snumber)
            new_satellite = Solar_synchronous_satellite(signal,satellitelist,height)
            self.all_satellitelist.append(new_satellite)
        elif type == "C":
            self.C_Snumber += 1
            signal = "C" + str(self.C_Snumber)
            new_satellite = Polar_orbiting_satellite(signal,satellitelist,height,speed)
            self.all_satellitelist.append(new_satellite)

    # 函数判断环境中的望远镜是否监测到卫星，是否监测到新的卫星。如果监测到已知列表存在的卫星，则将该卫星的be_observabed置为 T
    # 并下调其观测价值；如果监测到新卫星，则将其添加到卫星列表，并计算其卫星轨道。
    # 望远镜的观测状态，0：什么都没观测到；1：观测到旧卫星；2.观测到新卫星
    def Observation(self):
        # 遍历所有望远镜
        for telescope in self.all_telescope:
            telescope.observation_state = 0
            # 遍历所有卫星
            for satellite in self.all_satellitelist:

                # 如果观测到的亮度太低，那么即使卫星在区域内，望远镜也观测不到
                if telescope.caliber * satellite.bright < 0.05 :
                    break

                # 获取当前卫星的当前位置
                pos = [satellite.R,satellite.sita,satellite.fai]
                if telescope.observabe_area(pos) == True :
                    if satellite.signal in self.satellitelist:
                        print("!!!!!找到旧卫星"+satellite.signal)
                    #     # 如果监测到已知卫星，则将卫星和望远镜标记为观测状态，并下调卫星的观测价值
                        satellite.be_observabed = True
                        satellite.value = 0.01
                        telescope.observabing = True
                        telescope.observation_state = 1
                        # 如果监测到未知卫星，则将卫星和望远镜标记为观测状态，并计算卫星的轨道，将卫星符号添加到已知卫星列表中
                    else:
                        print("!!!!!!!找到新卫星"+satellite.signal)
                        satellite.be_observabed = True
                        telescope.observabing = True
                        telescope.observation_state = 2
                        satellite_orbit = self.cal_obs_orbit(telescope,satellite)
                        self.obs_orbit.update({satellite.signal:satellite_orbit})
                        self.satellitelist.append(satellite.signal)

                else:
                    # 没有观测到卫星
                    pass

    def cal_obs_orbit(self,telescope,satellite):
        print(telescope.signal+"开始计算"+satellite.signal+"的轨道")
        obs_orbit_list = []
        # 观测误差由口径和目标亮度决定，口径越大，目标亮度越大。
        obs_error = telescope.caliber * satellite.bright / 1000.
        start_sita = satellite.sita  # 第一个坐标的sita值
        while True:
            pos = [r, sita, fai] = satellite.get_current_postion()
            satellite.orbit_step = self.step  # 开始记录轨道时的step，周期为len（obs_orbit_list）
            obs_r, obs_sita, obs_fai = random.uniform(r - obs_error, r + obs_error), \
                                       random.uniform(sita - obs_error, sita + obs_error), \
                                       random.uniform(fai - obs_error, fai + obs_error)
            obs_pos = [obs_r, obs_sita, obs_fai]
            obs_orbit_list.append(obs_pos)
            # 当最后的sita和开始sita几乎重合，我们认为找到完整轨迹
            if abs(satellite.sita - start_sita) <= satellite.speed/10.:
                break

        return obs_orbit_list



if __name__ == '__main__':
    satellitelist = []
    env = env()
    env.create_satellite(500)
    env.create_Geosynchronous_satellite(50)
    env.create_Solar_synchronous_satellite(50)
    env.create_Polar_orbiting_satellite(50)
    env.create_telescope(5)


    # 增加一个观测地球同步卫星，观察望远镜能否观察到该卫星
    # signal = str(env.A_Snumber)
    # test_G = Geosynchronous_satellite(signal,env.satellitelist)
    # test_G.sita = 10
    # test_G.fai = 0
    # env.all_satellitelist.append(test_G)
    # # len = len(env.all_satellitelist)
    # env.A_Snumber += 1
    # print("卫星编号： " + test_G.signal)
    # print("卫星当前位置： " + str(test_G.get_current_postion()))


    # 增加一个观测太阳同步卫星的望远镜，观察其能否观察到卫星
    # telescope_signal = 'T' + str(env.T_number)
    # test_tele = telescope(telescope_signal,[6378,10,97.8],5,env.satellitelist,3)
    # env.all_telescope.append(test_tele)
    # env.T_number += 1
    #
    # test_tele.sita = 10
    # test_tele.fai  = 97.8
    # print("望远镜编号： " + test_tele.signal)
    # print("望远镜当前位置： " + str(test_tele.position))
    # print("望远镜指向： " + str(test_tele.sita)+' '+str(test_tele.fai))

    while True:
        env.upgrade()
        env.Observation()
        # if env.step % 100 == 0 :
        #     env.create_Geosynchronous_satellite(1)
        print("运行到第几步： " + str(env.step))
        if env.step == 5000:
            print(len(env.all_satellitelist))
            break
        # print(env.obs_orbit)

    print('共探测到卫星数'+str(len(env.satellitelist)))

