#!/usr/bin/env python
import sc2reader
import sys
import os
from process import process
import shelve

def generate(data_dir):
	sc2 = sc2reader.SC2Reader()
	d = shelve.open("features")
	for f in os.listdir(data_dir):
		if(len(f) > 9 and f[-9:].lower() == "sc2replay"):
			print "Generating",f
			replay = sc2.load_replay(os.path.join(data_dir,f))
			result = process(replay)
			d[f] = result
	d.close()


generate(sys.argv[1])
