import os
import urllib2
import json
import time
import sys
from math import cos, sin, atan2, sqrt, pi, radians


def calc_distance(w1, w2):
    earth_radius = 3959
    lat1, lat2, lon1, lon2 = map(radians, [w1[0], w2[0], w1[1], w2[1]])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = earth_radius * c
    return d

def checkConnected():
    try:
        response = urllib2.urlopen("http://192.168.33.33/", timeout = 1)
        return json.load(response)
    except urllib2.URLError as e:
        print e.reason
        raise


def clickAction(click_sleep_time=1, n=0):
    os.system("./autoClicker -x 500 -y 440")
    os.system("./autoClicker -x 500 -y 490")
    time.sleep(click_sleep_time)
    print "clicking(%d)!!" % n


def write_gpx(loc):
    f = open('pokemonLocation.gpx', 'wb')
    f.write('<gpx creator="Xcode" version="1.1"><wpt lat="%0.12f" lon="%0.12f"><name>PokemonLocation</name></wpt></gpx>' % tuple(loc))
    f.close()
    del f


perc_ponds = (37.2687140272739, -121.952868728497) # perc ponds
home = (37.2706395341357, -121.968670287041) # home
santana_row = (37.321999710354, -121.948474833221) # santana row
moffet = (37.4188916849005, -122.050083924735) # moffett field
start = home
finish = moffet
speed_mph = 11.5
steps_per_sec = 2.0
distance = calc_distance(start, finish)
steps = int(distance/speed_mph * 3600 * steps_per_sec)
sleep_time = 0.5
step = ((finish[0]-start[0])/steps, (finish[1]-start[1])/steps)

print "distance: %f" % distance
print "steps: %d" % steps
print "step size: (%f, %f)" % step

def walk():
    counter = 0
    current = list(start)
    for ii in xrange(steps):
        write_gpx(current)
        clickAction(sleep_time, ii)
        current[0] += step[0]
        current[1] += step[1]
        counter += 1
        #if not (counter % 10):
            #checkConnected()


def do_auto():
    while True:
        if checkConnected() != None:
            clickAction()

if len(sys.argv) > 1:
    walk()
else:
    do_auto()