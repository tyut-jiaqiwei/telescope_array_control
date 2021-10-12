import random
import ephem

random.seed(1314)
def read_tle(flie_name):
    with open(flie_name,"r") as f :
        linenumber = 0
        star_tle = []
        the_tle = dict()
        for line in f.readlines():
            linenumber += 1
            if linenumber % 3 == 1:
                the_tle.update({'line1': line})
            if linenumber % 3 == 2:
                the_tle.update({'line2': line})
            if linenumber % 3 == 0:
                the_tle.update({'line3': line})
                star_tle.append(the_tle.copy())
                the_tle.clear()
    return star_tle

# Geosynchronous = read_tle('3le.txt')
#
# start_time = ephem.Date('2021/1/1 12:00:00')
# tle = Geosynchronous[0]
# line1 = tle['line1']
# line2 = tle['line2']
# line3 = tle['line3']
# iss = ephem.readtle(line1, line2, line3)
# Telescope = ephem.Observer()
# Telescope.lat,Telescope.lon = '42.37', '-71.03'
# Telescope.date = start_time
# hours = 1/24
# minutes = hours/60
# for k in range(8):
#     Telescope.date  += minutes
#     iss.compute()
#     print(iss.az,iss.alt)

