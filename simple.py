#!/usr/bin/env python

import sc2reader
import sys

sc2 = sc2reader.SC2Reader()
replay = sc2.load_replay(sys.argv[1])
print replay.__dict__.keys()
print replay.people[0],type(replay.people[0])
print replay.winner.__dict__

def __update(data,key,value):
	if key in data:
		data[key] += value
	else:
		data[key] = value
#Camera
def processCameraMovement(camera_event,context,output):
	__update(output,"CameraEvent",1)

#SelfAbility
def processSelfAbility(ability_event,context,output):
	__update(output,"SelfAbility",1)

#LocationAbility
def processLocationAbility(ability_event,context,output):
	__update(output,"LocationAbility",1)

#AddToHotkey
def processAddToHotkey(hotkey_event,context,output):
	__update(output,"AddToHotkey",1)

#GetFromHotkey
def processGetFromHotkey(hotkey_event,context,output):
	__update(output,"GetFromHotkey",1)

#Selection
def processSelectionEvent(selection_event,context,output):
	__update(output,"Selection",1)

event_map = {
	'CameraMovementEvent' : processCameraMovement,
	'SelectionEvent': processSelectionEvent,
	'GetFromHotkeyEvent' : processGetFromHotkey,
	'AddToHotkeyEvent' : processAddToHotkey,
	'SelfAbilityEvent' : processSelfAbility,
	'LocationAbilityEvent' : processLocationAbility,
}


for person in replay.people:
	print "################"
	output = {}
	context = {}

	print person.name
	print person.pid
	print person.region
	print person.uid
	print person.play_race
	print person.__dict__.keys()
	for e in person.events:
		#print "###############"
		#print e.__dict__.keys()
		#print e
		#print e.name
		if e.name in event_map:
			event_map[e.name](e,context,output)


	print output
