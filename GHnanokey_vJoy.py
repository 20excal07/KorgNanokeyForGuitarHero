def update():	
	channel	= midi[midiPort].data.channel
	status	= midi[midiPort].data.status
	note	= midi[midiPort].data.buffer[0]
	vel		= midi[midiPort].data.buffer[1]
	
	#reset a few things when nothing pressed
	if joystick[joyId].getDown(b_starPwr): vJoy[joyId].setButton(b_starPwr, False)
	if joystick[joyId].getDown(b_start): vJoy[joyId].setButton(b_start, False)
	
	if '48' in pressed:		#dpad guard Y axis
		lastStrum = '48'
	elif '49' in pressed:
		lastStrum = '49'
	
	if '66' in pressed:		#dpad guard X axis
		lastNav = '66'
	elif '70' in pressed:
		lastNav = '70'

	# listening for MIDI inputs & stores/removes the button inputs to/from the array as appropriate
	if status.Equals(MidiStatus.NoteOn) and str(note) not in pressed:
		pressed.append(str(note))	
	elif status.Equals(MidiStatus.NoteOff) and str(note) in pressed:
		pressed.remove(str(note))

	if status.Equals(MidiStatus.Control) and vel != 0 and ('cc' + str(note)) not in pressed:
		pressed.append('cc' + str(note))	
	elif status.Equals(MidiStatus.Control) and vel == 0 and ('cc' + str(note)) in pressed:
		pressed.remove('cc' + str(note))
	
	#whammy
	if status.Equals(MidiStatus.PitchBendChange) and vel != 64:
		if vel > 64: vJoy[joyId].z = filters.mapRange(vel,64,127,0x4001,0x8000)
		else: vJoy[joyId].z = filters.mapRange(vel,63,0,0x4001,0x8000)
	elif status.Equals(MidiStatus.PitchBendChange) and vel == 64:
		vJoy[joyId].z = 0x4000
	
	#dpad guard
	if '48' in pressed and '49' in pressed: pressed.remove(lastStrum)
	if '66' in pressed and '70' in pressed: pressed.remove(lastNav)
	
	# switch between button modes	
	if '52' in pressed and 'mode1' not in inputmode:
		inputmode.append('mode1')
		inputmode.remove('mode2')
	elif '53' in pressed and 'mode2' not in inputmode:
		inputmode.append('mode2')
		inputmode.remove('mode1')
	
	#guitar on keys mode (only register held frets on strum)
	execute = True;
	if 'mode2' in inputmode: execute = '48' in pressed or '49' in pressed;
	
	# mapping MIDI inputs to vJoy
	# optimised so we don't send vJoy too many repeat button inputs while frets are held down
	if execute:
		if G in pressed:	#green
			if not joystick[joyId].getDown(b_GRN): vJoy[joyId].setButton(b_GRN, True)
		else:
			if joystick[joyId].getDown(b_GRN): vJoy[joyId].setButton(b_GRN, False)
			
		if R in pressed:	#red
			if not joystick[joyId].getDown(b_RED): vJoy[joyId].setButton(b_RED, True)
		else:
			if joystick[joyId].getDown(b_RED): vJoy[joyId].setButton(b_RED, False)
			
		if Y in pressed:	#yellow
			if not joystick[joyId].getDown(b_YLW): vJoy[joyId].setButton(b_YLW, True)
		else:
			if joystick[joyId].getDown(b_YLW): vJoy[joyId].setButton(b_YLW, False)
			
		if B in pressed:	#blue
			if not joystick[joyId].getDown(b_BLU): vJoy[joyId].setButton(b_BLU, True)
		else:
			if joystick[joyId].getDown(b_BLU): vJoy[joyId].setButton(b_BLU, False)
			
		if O in pressed:	#orange
			if not joystick[joyId].getDown(b_ORN): vJoy[joyId].setButton(b_ORN, True)
		else:
			if joystick[joyId].getDown(b_ORN): vJoy[joyId].setButton(b_ORN, False)

	if 'cc1' in pressed: vJoy[joyId].setButton(b_starPwr, True)		#star power/overdrive
	
	#this if/else chain seems to work as a debouncer too
	if '49' in pressed: vJoy[joyId].setAnalogPov(0, 0)				#strum up
	elif '48' in pressed: vJoy[joyId].setAnalogPov(0, 18000)		#strum down	
	elif '66' in pressed: vJoy[joyId].setAnalogPov(0, 9000)			#navigate right
	elif '70' in pressed: vJoy[joyId].setAnalogPov(0, 27000)		#navigate left
	elif joystick[joyId].pov[0] != -1: vJoy[joyId].setAnalogPov(0, -1)
	
	if '68' in pressed: vJoy[joyId].setButton(b_start, True)		#start
	
	if 'mode1' in inputmode and 'mode2' not in inputmode:
		mode = "1: Normal guitar mode"
	elif 'mode2' in inputmode and 'mode1' not in inputmode:
		mode = "2: Guitar on Keys mode"
		
	diagnostics.watch(mode)
	
	# debug stuff
	if debug:
		nanoKey = ""
		controller = ""
	
		for x in pressed:
			nanoKey += "[" + x + "]"
			
		for y in range(7):
			if joystick[joyId].getDown(y):
				controller += "█│"
			else:
				controller += "░│"		
		
		if joystick[joyId].pov[0] == 0: controller += "▲"
		elif joystick[joyId].pov[0] == 18000: controller += "▼"
			
		diagnostics.watch(channel)
		diagnostics.watch(status)
		diagnostics.watch(note)
		diagnostics.watch(vel)	
		diagnostics.watch(nanoKey)
		diagnostics.watch(controller)
	
if starting:
	#script settings
	pollingRate = 120	#Hz; default is 120
	fretOffset = 0		#increase the offset to shift the fret buttons further down the keyboard; default is 0
	debug = 0			#turn this on to show the script working (may introduce a tiny bit of latency)
	midiPort = 0		#MIDI port number
	joyId = 0			#vjoy controller ID
	
	#vJoy button assignments
	b_GRN = 0
	b_RED = 1
	b_YLW = 2
	b_BLU = 3
	b_ORN = 4
	b_start = 5
	b_starPwr = 6

	system.setThreadTiming(TimingTypes.HighresSystemTimer)
	system.threadExecutionInterval = 1000 / pollingRate

	#white keys mapping; thanks clipsey! <3
	def GenKeys(octaves, rootoctave):
		keys = [None] * (7*(octaves)+1)
		matcher = [0,2,4,5,7,9,11]
		index = 0
		for i in range(0,octaves):
			for m in matcher:
				keys[index] = str((12*(i+rootoctave))+m)
				index += 1				
		keys[index] = str((12*(i+rootoctave))+12)		
		return keys[::-1]

	keys = GenKeys(2,4)
	G = keys[0+fretOffset]
	R = keys[1+fretOffset]
	Y = keys[2+fretOffset]
	B = keys[3+fretOffset]
	O = keys[4+fretOffset]
	
	whiteKeys = ""
	for f in keys:
		whiteKeys += '[' + str(f) + ']'
		
	mode = "(press any key)"
	diagnostics.watch(whiteKeys)
	diagnostics.watch(mode)
	
	lastStrum = lastNav = ''
	pressed = []
	inputmode = ['mode1']
	midi[midiPort].update += update
