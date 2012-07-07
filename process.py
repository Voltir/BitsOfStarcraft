#!/usr/bin/env python

import sc2reader
import sys

def __update(data,key,value):
	if key in data:
		data[key] += value
	else:
		data[key] = value
#Camera
def processCameraMovement(camera_event,context,output):
	#print "Sadly, I need to figure out how to add in camera data"
	#__update(output,"CameraEvent",1)
	pass

#SelfAbility
def processSelfAbility(ability_event,context,output):
	__update(output,"SelfAbility_%s"%ability_event.ability,1)

#LocationAbility
def processLocationAbility(ability_event,context,output):
	if ability_event.ability != "Right click":
		__update(output,"LocationAbility_%s" % ability_event.ability,1)

#AddToHotkey
def setupAddToHotkey(context,output):
	for i in xrange(10):
		context["Hotkey%s"%i] = set()

def finalizeAddToHotkey(context,output):
	pass
	#for i in xrange(10):
	#	print "~~~~WOOOT",context["Hotkey%s"%i]
	
def processAddToHotkey(hotkey_event,context,output):
	selection = context["CurrentSelection"]
	current = context["Hotkey%s" % hotkey_event.hotkey]
	for obj in selection.objects:
		current.add(obj)

#GetFromHotkey
def processGetFromHotkey(hotkey_event,context,output):
	current = context["Hotkey%s" % hotkey_event.hotkey]
	__update(output,"GetHotkey%s"%hotkey_event.hotkey,1)
	for obj in current:
		__update(output,"GotFromHotkey%s_%s"%(hotkey_event.hotkey,obj.name),1)

#Selection
def setupSelectionEvent(context,output):
	context["SelectEvents"] = {}

def finalizeSelectionEvent(context,output):
	unique_count = context["SelectEvents"]
	for obj_name,id_set in unique_count.iteritems():
		__update(output,"SelectUnique%s"%obj_name,len(id_set))
	
def processSelectionEvent(selection_event,context,output):
	context["CurrentSelection"] = selection_event
	unique_count = context["SelectEvents"]
	for obj in selection_event.objects:
		#__update(output,"Select%s"%obj.name,1)
		if obj.name not in unique_count:
			unique_count[obj.name] = set()
		unique_count[obj.name].add(obj.id)

startup = [
	setupSelectionEvent,
	#setupAddToHotkey,
]

finalize = [
	finalizeSelectionEvent,
	#finalizeAddToHotkey,
]

event_map = {
	#'CameraMovementEvent' : processCameraMovement,
	'SelectionEvent': processSelectionEvent,
	#'GetFromHotkeyEvent' : processGetFromHotkey,
	#'AddToHotkeyEvent' : processAddToHotkey,
	'SelfAbilityEvent' : processSelfAbility,
	'LocationAbilityEvent' : processLocationAbility,
}


def process(replay):
	output = []
	for person in replay.players:
		context = {}
		output.append((person.play_race,{}))
		for f in startup:
			f(context,output[-1][1])

		for e in person.events:
			if e.name in event_map:
				event_map[e.name](e,context,output[-1][1])

		for f in finalize:
			f(context,output[-1][1])

	
	return output

if __name__ == "__main__":
	sc2 = sc2reader.SC2Reader()
	replay = sc2.load_replay(sys.argv[1])
	print replay.people
	#print replay.__dict__.keys()
	#print replay.people[0],type(replay.people[0])
	#print replay.winner.__dict__
	print process(replay)
