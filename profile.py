#!/usr/bin/env python
import sc2reader
import sys
import urllib2
from BeautifulSoup import BeautifulSoup

sc2 = sc2reader.SC2Reader()
replay = sc2.load_replay(sys.argv[1])
print replay.__dict__.keys()
print replay.people[0],type(replay.people[0])
print replay.winner.__dict__

for person in replay.people:
	uid = person.uid
	name = person.name
	region = person.region
	print "##########",name,"##############"

	url = "http://%s.battle.net/sc2/en/profile/%s/1/%s/" % (region,uid,name)
	site = BeautifulSoup(urllib2.urlopen(url))
	best1v1 = site.find(id="best-team-1")
	badge_data = best1v1.parent.a.span["class"]
	rank = badge_data.split()[1][6:]
	print "RANK:",rank
