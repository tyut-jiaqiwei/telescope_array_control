import ephem
from ephem import degrees
from  satellite import satellite
from telescope import telescope
from read_tle import read_tle
import random
import time
from numpy import pi,inf
import numpy as np
from gym import spaces
from gym.utils import seeding
import math

hours = 1/24
minutes = hours/60
star_tle = read_tle("3le.txt")
# select_tle = random.sample(star_tle, 5000)

class Env:
    def __init__(self,object_number,start_time,end_time,step_time):

        self.start_time = ephem.Date(start_time)
        self.end_time = ephem.Date(end_time)
        self.step_time = step_time
        self.time = self.start_time

        self.obs_orbit = {}           # 已知卫星的编号和轨道，轨道用列表存储，列表长度为周期（min）

        self.all_tle = random.sample(star_tle, object_number)  # 从全部tle数据中挑选固定数目做测试
        self.all_satellitelist = []  # 环境中构建出来的所有卫星存储在该列表中
        self.satellitelist = []  # 已探察到的卫星的列表，存储的是已知卫星的编号
        self.all_telescope = []      # 已望远镜列表，存储的是望远镜的编号

        self.observation_space = spaces.Box(
            low=0,
            high=inf, shape=(3,),
            dtype=np.float32
        )

        # self.action_space = spaces.Box(
        #     low=-0,
        #     high=0, shape=(2,),
        #     dtype=np.float32
        # )

    def create_satellite(self):
        signal = 0
        for tle in self.all_tle:
            signal += 1
            scale = 1.5
            satellite_i = satellite(signal,self.satellitelist,tle,scale)
            self.all_satellitelist.append(satellite_i)

    def create_telescope(self,position, caliber, field):
        signal = len(self.all_telescope)+1
        telescope_i = telescope(signal, position, caliber, self.satellitelist, field)
        self.all_telescope.append(telescope_i)

        self.action_space = spaces.Box(
            low=-0,
            high=0, shape=(2 ** len(self.all_telescope),),
            dtype=np.float32
        )

    def telescope_factory(self,number,position):
        for signal in range(len(self.all_telescope), len(self.all_telescope)+number):
            signal += 1
            caliber = 5.
            field = '5.'
            self.create_telescope(position, caliber, field)

    def change_telescope(self,signal,position, caliber, field):
        for telescope in self.all_telescope:
            if telescope.signal == signal:
                telescope.position = position
                telescope.caliber = caliber
                telescope.field = field


    def upgrade(self):
        for satellite in self.all_satellitelist:
            # satellite.a_ra, satellite.a_dec =satellite.get_current_postion(self.time)    # 更新每颗卫星的当前位置
            satellite.value_upgrade()  # 更新每颗卫星的观测价值
            # if satellite.signal == 5 :
            #     print(satellite.a_ra, satellite.a_dec)
            #     print(self.time)
        return self

    def observation_state(self):
        for telescope in self.all_telescope:
            telescope.observation_state = 0
            Telescope = ephem.Observer()
            Telescope.lat,Telescope.lon,Telescope.date= telescope.position[0],telescope.position[1],self.time
            # Telescope.lon = telescope.position[1]
            # Telescope.date = self.time
            for satellite in self.all_satellitelist:
                old_value = satellite.value
                # 如果观测到的亮度太低，那么即使卫星在区域内，望远镜也观测不到
                if telescope.caliber * satellite.bright < 0.0000001:
                    break
                iss = ephem.readtle(satellite.tle['line1'],satellite.tle['line2'],satellite.tle['line3'])
                iss.compute(Telescope)
                if abs(degrees(iss.az - telescope.sita)) <= abs(degrees(telescope.field)) \
                        and abs(degrees(iss.alt - telescope.fai)) <= abs(degrees(telescope.field)) :
                    if satellite in self.satellitelist:
                        satellite.be_observabed = True
                        telescope.observabing = True
                        telescope.observation_state = 1
                        satellite.value = -1
                        # telescope.find_old = 0
                        # print("望远镜状态：%d，望远镜编号：%d，卫星编号：%d，观测前价值，%5f,观测后价值：%5f,价值采样数：%d"
                        #       % (telescope.observation_state, telescope.signal, satellite.signal, old_value,
                        #          satellite.value,satellite.value_sample))
                    else:
                        satellite.be_observabed = True
                        telescope.observabing = True
                        telescope.observation_state = 10
                        satellite.value = -1
                        self.satellitelist.append(satellite)
                        telescope.find_new = 0
                        # print("望远镜状态：%d，望远镜编号：%d，卫星编号：%d，观测前价值，%5f,观测后价值：%5f,价值采样数：%d"
                        #       % (telescope.observation_state, telescope.signal, satellite.signal, old_value,
                        #          satellite.value,satellite.value_sample))
                    # 探索过程中找到不值得观测旧卫星不扣分
                    if old_value < 0 :
                        old_value = 0
                    self.reward += old_value * 2
                    # self.reward += len(self.satellitelist) * 2
            if telescope.observation_state != 10:
                # telescope.find_old += 1
                telescope.find_new += 1
            # if telescope.observation_state == 1:
            #     telescope.find_old += 1


    def tele_observation(self,telescope):
        telescope.observation_state = 0
        Telescope = ephem.Observer()
        Telescope.lat,Telescope.lon,Telescope.date= telescope.position[0],telescope.position[1],self.time
        for satellite in self.all_satellitelist:
            old_value = satellite.value
            # 如果观测到的亮度太低，那么即使卫星在区域内，望远镜也观测不到
            if telescope.caliber * satellite.bright < 0.0000001:
                break
            iss = ephem.readtle(satellite.tle['line1'],satellite.tle['line2'],satellite.tle['line3'])
            iss.compute(Telescope)
            if abs(degrees(iss.az - telescope.sita)) <= abs(degrees(telescope.field)) \
                    and abs(degrees(iss.alt - telescope.fai)) <= abs(degrees(telescope.field)) :
                if satellite in self.satellitelist:
                    satellite.be_observabed = True
                    telescope.observabing = True
                    telescope.observation_state = 1
                    # satellite.error *= 0.8
                    satellite.value = -1
                    # telescope.find_old = 0
                    # print("望远镜状态：%d，望远镜编号：%d，卫星编号：%d，观测前价值，%5f,观测后价值：%5f,价值采样数：%d"
                    #       % (telescope.observation_state, telescope.signal, satellite.signal, old_value,
                    #          satellite.value,satellite.value_sample))
                else:
                    satellite.be_observabed = True
                    telescope.observabing = True
                    telescope.observation_state = 10
                    satellite.value = -1
                    satellite.error = 0.05*1/telescope.caliber
                    self.satellitelist.append(satellite)
                    telescope.find_new = 0
                    # print("望远镜状态：%d，望远镜编号：%d，卫星编号：%d，观测前价值，%5f,观测后价值：%5f,价值采样数：%d"
                    #       % (telescope.observation_state, telescope.signal, satellite.signal, old_value,
                    #          satellite.value,satellite.value_sample))
                # 探索过程中找到不值得观测旧卫星不扣分
                if old_value < 0 :
                    old_value = 0
                self.reward += old_value * 2
                # self.reward += len(self.satellitelist) * 2
        if telescope.observation_state != 10:
            telescope.find_new += 1


    # 返回当前时间所有卫星和望远镜的情况
    def get_all_state(self):
        pass

    # 测试选取的卫星是否固定
    def test_s_random(self):
        telescope = self.all_telescope[0]
        Telescope = ephem.Observer()
        Telescope.lat = telescope.position[0]
        Telescope.lon = telescope.position[1]
        Telescope.date = self.time
        number = 0
        for satellite in self.all_satellitelist:
            iss = ephem.readtle(satellite.tle['line1'], satellite.tle['line2'], satellite.tle['line3'])
            iss.compute(Telescope)
            number += 1
            print(iss.name)
        print(number)

    # 测试单个卫星数的运行是否固定
    def test_single(self,number):
        self.time += self.step_time
        for telescope in self.all_telescope:
            Telescope = ephem.Observer()
            Telescope.lat = telescope.position[0]
            Telescope.lon = telescope.position[1]
            Telescope.date = self.time
            for satellite in self.all_satellitelist:
                # 如果观测到的亮度太低，那么即使卫星在区域内，望远镜也观测不到
                if satellite.signal == number :
                    if telescope.caliber * satellite.bright < 0.0000001:
                        break
                    iss = ephem.readtle(satellite.tle['line1'], satellite.tle['line2'], satellite.tle['line3'])
                    iss.compute(Telescope)
                    akk = False
                    if abs(degrees(iss.az - telescope.sita)) <= abs(degrees(telescope.field)) \
                            and abs(degrees(iss.alt - telescope.fai)) <= abs(degrees(telescope.field)):
                        akk = True
                    print(ephem.Date(self.time + 1))
                    print(iss.az,iss.alt,iss.a_ra,iss.a_dec,akk)
                    print(iss.alt)



    def monitor(self):

        no_need_see = 0
        for satellite in self.satellitelist:
            if satellite.value < -0.6:
                no_need_see += 1

        if len(self.satellitelist) == 0 or no_need_see == len(self.satellitelist):
            self.reward += -20
        else:
            max_value_satellite = self.satellitelist[0]
            max_value = max_value_satellite.value
            max_signal = max_value_satellite.signal
            for satellite in self.satellitelist :
                if satellite.value > max_value:
                    max_value_satellite = satellite
                    max_value = max_value_satellite.value
                    max_signal = max_value_satellite.signal
            # if random.random() < max_value_satellite.error:
            #     max_value_satellite.error = inf
            #     max_value_satellite.value = 10
            #     max_value_satellite.value_sample = 0
            #     max_value_satellite.be_observabed = False
            #     max_value_satellite.have_observabed = 0
            #     # 从列表里删除
            #     self.satellitelist.remove(max_value_satellite)
            # else:
            #     self.reward += max_value_satellite.value
            #     max_value_satellite.value = -1
            self.reward += max_value_satellite.value
            max_value_satellite.value = -1



    # 以下函数服务于强化学习
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def reset(self):
        self.time = self.start_time
        self.satellitelist = []     # 已探察到的卫星的列表，存储的是已知卫星的编号
        for satellite in self.all_satellitelist:
            satellite.be_observabed = False
            satellite.have_observabed = 0
            satellite.value = 10
            satellite.value_sample = 0
            satellite.error = inf
        for i,tele in enumerate(self.all_telescope):
            tele.sita = 0
            tele.fai = 0
            tele.find_new = 0
            # tele.find_old = 0
            tele.observation_state = 0
        return self._get_obs()

    def _get_obs(self):
        # s1 = self.all_telescope[0].find_new
        s2 = self.all_telescope[0].find_old
        s2 = 0
        for telescope in self.all_telescope:
            s2 += telescope.find_old

        need_see = 0
        for satellite in self.satellitelist:
            if satellite.value > 0.6:
                need_see += 1
        s3 = need_see

        s4 = len(self.satellitelist)

        return np.array([s2,s3,s4])

    def have_done(self):
        value = 0
        if len(self.all_satellitelist) * 0.8 < len(self.satellitelist):
            for satellite in self.satellitelist:
                value += satellite.value
        if len(self.all_satellitelist) * 0.9 < len(self.satellitelist) or value < 0:
            return True
        else:
            return False


    def step(self,a):
        self.reward = 0
        for i in range(int(len(self.all_telescope))):
            ta = (a >> i)&1
            if ta == 0 :
                self.monitor()
                self.time += self.step_time
                self.upgrade()
            if ta == 1:
                self.all_telescope[i].sita = random.uniform(-pi,pi)
                self.all_telescope[i].fai = random.uniform(0,pi)
                self.time += self.step_time
                self.tele_observation(self.all_telescope[i])
                # self.observation_state()
                self.upgrade()

        # 观测价值越低代表监测效果越好
        monitor_value = 0
        for satellite in self.satellitelist:
            monitor_value += satellite.value

        self.reward -= monitor_value

        return self._get_obs(),self.reward,self.have_done(),len(self.satellitelist)
