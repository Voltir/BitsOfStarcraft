#!/usr/bin/env python
import shelve
import sc2reader
import sys
import os
from process import process

def inner(data1,data2):
	total = 0
	for k in data1:
		if k in data2:
			total += data1[k]*data2[k]
	return total

def distance(v1,v2):
	kxx = inner(v1,v1)
	kxz = inner(v1,v2)
	kzz = inner(v2,v2)

	if None in (kxx,kxz,kzz):
		return None

	return (kxx -2*kxz + kzz)

def playerGameDistance(input_race,input_v,game_data):
	total = 0

	if len(game_data) != 2:
		return None
	
	[(race1,v1),(race2,v2)] = game_data

	if input_race == race1 and input_race == race2:
		return min(distance(input_v,v1),distance(input_v,v2))
	elif input_race == race1:
		return distance(input_v,v1)
	elif input_race == race2:
		return distance(input_v,v2)
	else:
		return None

	

def search(search_game,feature_file):
	result = None
	sc2 = sc2reader.SC2Reader()
	sg = sc2.load_replay(search_game)
	
	search_data = process(sg)	
	if len(search_data) != 2:
		return None

	[(race1,v1),(race2,v2)] = search_data
	
	best = float('inf')
	for f,data in shelve.open(feature_file).iteritems():
		p1_dist = playerGameDistance(race1,v1,data)
		p2_dist = playerGameDistance(race2,v2,data)

		if p1_dist == None or p2_dist == None:
			continue

		#d = p1_dist + p2_dist
		d = p2_dist

		if d < best:
			best = d
			result = f
			print "Best: %s --" % result,best
	print "Wooot!",result

"""
def innerzz(r1,r2):
	total = 0

	data1 = process(r1)
	data2 = process(r2)

	if len(data1) != 2 or len(data2) != 2:
		return None

	[(race1_1,v1_1),(race2_1,v2_1)] = data1
	[(race1_2,v1_2),(race2_2,v2_2)] = data2

	compare_1 = None
	compare_2 = None

	if race1_1 != race2_1:
		if race1_1 == race1_2 and race2_1 == race2_2:
			compare_1 = v1_2
			compare_2 = v2_2
		elif race1_1 == race2_2 and race2_1 == race1_2:
			compare_1 = v2_2
			compare_2 = v1_2
		else:
			return None
	else:
		compare_1 = v1_2
		compare_2 = v2_2
	
	for k in v1_1:
		if k in compare_1:
			total += v1_1[k]*compare_1[k]

	for k in v2_1:
		if k in compare_2:
			total += v2_1[k]*compare_2[k]

	return total
"""

search(sys.argv[1],sys.argv[2])
