import ephem
from ephem import degrees
from  satellite import satellite
from telescope import telescope
from read_tle import read_tle
import random
import time


hours = 1/24
minutes = hours/60
star_tle = read_tle("3le.txt")
# select_tle = random.sample(star_tle, 5000)

class env:
    def __init__(self,object_number,start_time,end_time):

        self.all_satellitelist = []   # 环境中构建出来的所有卫星存储在该列表中
        self.satellitelist = []       # 已探察到的卫星的列表，存储的是已知卫星的编号
        self.start_time = ephem.Date(start_time)
        self.end_time = ephem.Date(end_time)
        self.time = self.start_time
        self.obs_orbit = {}           # 已知卫星的编号和轨道，轨道用列表存储，列表长度为周期（min）
        self.all_tle = random.sample(star_tle, object_number)  # 从全部tle数据中挑选固定数目做测试

        self.all_telescope = []      # 已望远镜列表，存储的是望远镜的编号

    def create_satellite(self,satellite_number):
        self.all_satellite = random.sample(star_tle, satellite_number)
        signal = 0
        for tle in self.all_satellite:
            signal += 1
            scale = random.uniform(0,1)
            satellite_i = satellite(signal,self.satellitelist,tle,scale)
            self.all_satellitelist.append(satellite_i)


    def create_telescope(self,position, caliber, field):
        signal = len(self.all_telescope)+1
        telescope_i = telescope(signal, position, caliber, self.satellitelist, field)
        self.all_telescope.append(telescope_i)

    def telescope_factory(self,number,position):
        for signal in range(len(env.all_telescope), len(env.all_telescope)+number):
            signal += 1
            caliber = 5.
            field = '1.'
            env.create_telescope(position, caliber, field)

    def change_telescope(self,signal,position, caliber, field):
        for telescope in self.all_telescope:
            if telescope.signal == signal:
                telescope.position = position
                telescope.caliber = caliber
                telescope.field = field

    def upgrade(self):
        for satellite in self.all_satellitelist:
            # satellite.a_ra, satellite.a_dec =satellite.get_current_postion(self.time)    # 更新每颗卫星的当前价值
            satellite.value_upgrade()  # 更新每颗卫星的观测价值
            # if satellite.signal == 5 :
            #     print(satellite.a_ra, satellite.a_dec)
            #     print(self.time)
        return self


    def observation_state(self):
        for telescope in self.all_telescope:
            telescope.observation_state = 0
            Telescope = ephem.Observer()
            Telescope.lat = telescope.position[0]
            Telescope.lon = telescope.position[1]
            Telescope.date = self.time
            for satellite in self.all_satellitelist:
                # 如果观测到的亮度太低，那么即使卫星在区域内，望远镜也观测不到
                if telescope.caliber * satellite.bright < 0.0000001:
                    break
                iss = ephem.readtle(satellite.tle['line1'],satellite.tle['line2'],satellite.tle['line3'])
                iss.compute(Telescope)
                if abs(degrees(iss.az - telescope.sita)) <= abs(degrees(telescope.field)) \
                        and abs(degrees(iss.alt - telescope.fai)) <= abs(degrees(telescope.field)) :
                    if satellite.signal in self.satellitelist:
                        satellite.be_observabed = True
                        telescope.observabing = True
                        telescope.observation_state = 1
                        old_value = satellite.value
                        satellite.value = 0.01
                        print(ephem.Date(self.time + 1))
                        print("望远镜状态：%d，望远镜编号：%d，卫星编号：%d，观测前价值，%5f,观测后价值：%5f,价值采样数：%d"
                              % (telescope.observation_state, telescope.signal, satellite.signal, old_value,
                                 satellite.value,satellite.value_sample))
                    else:
                        satellite.be_observabed = True
                        telescope.observabing = True
                        telescope.observation_state = 2
                        # satellite_orbit = self.cal_obs_orbit(telescope, satellite)
                        # self.obs_orbit.update({satellite.signal: satellite_orbit})
                        old_value = satellite.value
                        satellite.value = 0.01
                        self.satellitelist.append(satellite.signal)
                        print(ephem.Date(self.time+1))
                        print("望远镜状态：%d，望远镜编号：%d，卫星编号：%d，观测前价值，%5f,观测后价值：%5f,价值采样数：%d"
                              % (telescope.observation_state, telescope.signal, satellite.signal, old_value,
                                 satellite.value,satellite.value_sample))



    def test_single(self,number):
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


if __name__ == '__main__':
    env = env(500,'2021/10/1 12:00:00','2021/12/1 12:00:00')
    env.create_satellite(500)
    env.telescope_factory(5,['42.37', '-71.03'])
    for tele in env.all_telescope:
        print(degrees(tele.sita),degrees(tele.fai))
    start_time = time.time()
    while True:
        env.time += minutes * 5
        env.upgrade()
        env.observation_state()
        # env.test_single(348)

        if env.time > env.end_time :
            break
    end_time = time.time()
    print("观测到的总卫星一共有%d个" %len(env.satellitelist))

    print("模拟两个月用时"+str(end_time - start_time))

