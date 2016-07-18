import os
import urllib2
import json
import time
import sys

perc_ponds = (37.2687140272739, -121.952868728497) # perc ponds
home = (37.2706395341357, -121.968670287041) # home
santana_row = (37.321999710354, -121.948474833221) # santana row
moffet = (37.4188916849005, -122.050083924735) # moffett field
start = home
finish = santana_row
steps= 9000
step = ((finish[0]-start[0])/steps, (finish[1]-start[1])/steps)
walk_time = 10.0*60.0
sleep_time = 1.0/(steps/walk_time)

def checkConnected():
    try:
        response = urllib2.urlopen("http://192.168.33.33/", timeout = 1)
        return json.load(response)
    except urllib2.URLError as e:
        print e.reason


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


def walk():
    current = list(start)
    for ii in xrange(steps):
        write_gpx(current)
        clickAction(sleep_time, ii)
        current[0] += step[0]
        current[1] += step[1]


def do_auto():
    while True:
        if checkConnected() != None:
            clickAction()

if len(sys.argv) > 1:
    walk()
else:
    do_auto()