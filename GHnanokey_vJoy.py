def update():	
	channel	= midi[0].data.channel
	status	= midi[0].data.status
	note	= midi[0].data.buffer[0]
	vel		= midi[0].data.buffer[1]
	rvel	= round(filters.mapRange(vel,0,127,-1.2,1.2),0)

	velocity = str(vel) + ' (' + str(rvel) + ')'
	inputs = ""

	# listening for MIDI inputs & stores/removes the button inputs to/from the array as appropriate
	if status.Equals(MidiStatus.NoteOn):
		pressed.append(str(note))	
	elif status.Equals(MidiStatus.NoteOff) and str(note) in pressed:
		pressed.remove(str(note))

	if status.Equals(MidiStatus.Control) and vel != 0:
		pressed.append('cc' + str(note))	
	elif status.Equals(MidiStatus.Control) and vel == 0 and ('cc' + str(note)) in pressed:
		pressed.remove('cc' + str(note))

	if status.Equals(MidiStatus.PitchBendChange) and rvel != 0 and 'bend' not in pressed:
		pressed.append('bend')
	elif status.Equals(MidiStatus.PitchBendChange) and rvel == 0 and 'bend' in pressed:
		pressed.remove('bend')

	# switch between button modes	
	if '52' in pressed and 'mode1' not in inputmode:
		inputmode.append('mode1')
		inputmode.remove('mode2')
	elif '53' in pressed and 'mode2' not in inputmode:
		inputmode.append('mode2')
		inputmode.remove('mode1')

	# mapping MIDI inputs to PPJoy
	if 'mode1' in inputmode:
		vJoy[0].setButton(6,G in pressed)	#green
		vJoy[0].setButton(4,R in pressed)	#red
		vJoy[0].setButton(5,Y in pressed)	#yellow
		vJoy[0].setButton(7,B in pressed)	#blue
		vJoy[0].setButton(3,O in pressed)	#orange

	if 'mode2' in inputmode:
		if '48' in pressed or '49' in pressed:
			vJoy[0].setButton(6,G in pressed)
			vJoy[0].setButton(4,R in pressed)
			vJoy[0].setButton(5,Y in pressed)
			vJoy[0].setButton(7,B in pressed)
			vJoy[0].setButton(3,O in pressed)
		elif G in pressed or R in pressed or Y in pressed or B in pressed or O in pressed:
			vJoy[0].setButton(6,0)
			vJoy[0].setButton(4,0)
			vJoy[0].setButton(5,0)
			vJoy[0].setButton(7,0)
			vJoy[0].setButton(3,0)

	vJoy[0].setButton(9,'68' in pressed)		#start
	vJoy[0].setButton(12,'49' in pressed)		#strum up
	vJoy[0].setButton(13,'48' in pressed)		#strum down
	vJoy[0].setButton(8,'cc1' in pressed)		#overdrive
	vJoy[0].setButton(14,'70' in pressed)		#left
	vJoy[0].setButton(15,'66' in pressed)		#right
	vJoy[0].setButton(11,'bend' in pressed)		#whammy

	# debug stuff
	if 'mode1' in inputmode and 'mode2' not in inputmode:
		mode = "1: Normal guitar mode"
	elif 'mode2' in inputmode and 'mode1' not in inputmode:
		mode = "2: Guitar on Keys mode"

	diagnostics.watch(whiteKeys)	
	diagnostics.watch(channel)
	diagnostics.watch(status)
	diagnostics.watch(note)
	diagnostics.watch(velocity)
	diagnostics.watch(mode)

	for x in pressed:
		inputs += "[" + x + "]"

	diagnostics.watch(inputs)

if starting:
	#white keys mapping; thanks clipsey! <3
	def GenKeys(octaves, rootoctave):
		keys = [None] * (7*(octaves))
		matcher = [0,2,4,5,7,9,11]
		index = 0
		for i in range(0,octaves):
			for m in matcher:
				keys[index] = str((12*(i+rootoctave))+m)
				index += 1				
		return keys

	keys = GenKeys(3,4)
	offset = 0		#increase the offset to shift the fret buttons further down the keyboard
	G = keys[14-offset]
	R = keys[13-offset]
	Y = keys[12-offset]
	B = keys[11-offset]
	O = keys[10-offset]
	
	#debug stuff
	whiteKeys = ""
	for f in keys:
		whiteKeys += '[' + str(f) + ']'

	pressed = []	
	inputmode = ['mode1']
	midi[0].update += update
