def update():	
	channel	= midi[0].data.channel
	status	= midi[0].data.status
	note	= midi[0].data.buffer[0]
	vel		= midi[0].data.buffer[1]
	
	#reset the POV hat when nothing pressed
	vJoy[0].setAnalogPov(0, -1)
	
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

	if status.Equals(MidiStatus.PitchBendChange) and vel != 64 and 'bend' not in pressed:
		pressed.append('bend')
	elif status.Equals(MidiStatus.PitchBendChange) and vel == 64 and 'bend' in pressed:
		pressed.remove('bend')

	# switch between button modes	
	if '52' in pressed and 'mode1' not in inputmode:
		inputmode.append('mode1')
		inputmode.remove('mode2')
	elif '53' in pressed and 'mode2' not in inputmode:
		inputmode.append('mode2')
		inputmode.remove('mode1')

	# mapping MIDI inputs to vJoy
	if 'mode1' in inputmode:
		vJoy[0].setButton(b_GRN,G in pressed)	#green
		vJoy[0].setButton(b_RED,R in pressed)	#red
		vJoy[0].setButton(b_YLW,Y in pressed)	#yellow
		vJoy[0].setButton(b_BLU,B in pressed)	#blue
		vJoy[0].setButton(b_ORN,O in pressed)	#orange

	# guitar on keys mode
	if 'mode2' in inputmode:
		if '48' in pressed or '49' in pressed:
			vJoy[0].setButton(b_GRN,G in pressed)
			vJoy[0].setButton(b_RED,R in pressed)
			vJoy[0].setButton(b_YLW,Y in pressed)
			vJoy[0].setButton(b_BLU,B in pressed)
			vJoy[0].setButton(b_ORN,O in pressed)

	#dpad guard
	if '48' in pressed and '49' in pressed: pressed.remove(lastStrum)
	if '66' in pressed and '70' in pressed: pressed.remove(lastNav)

	vJoy[0].setButton(b_start,'68' in pressed)		#start button
	if '49' in pressed: vJoy[0].setAnalogPov(0, 0)		#strum up
	if '48' in pressed: vJoy[0].setAnalogPov(0, 18000)	#strum down
	vJoy[0].setButton(b_starPwr,'cc1' in pressed)		#overdrive/star power
	if '66' in pressed: vJoy[0].setAnalogPov(0, 9000)	#navigate right
	if '70' in pressed: vJoy[0].setAnalogPov(0, 27000)	#navigate left
	
	#whammy
	vJoy[0].z = filters.mapRange(vel,0,127,0x0001,0x8000) if 'bend' in pressed else 0x4000
	
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
			if joystick[0].getDown(y):
				controller += "█│"
			else:
				controller += "░│"		
		
		if joystick[0].pov[0] == 0: controller += "▲"
		elif joystick[0].pov[0] == 18000: controller += "▼"
			
		diagnostics.watch(channel)
		diagnostics.watch(status)
		diagnostics.watch(note)
		diagnostics.watch(vel)	
		diagnostics.watch(nanoKey)
		diagnostics.watch(controller)
	
if starting:
	#script settings
	pollingRate = 60	#Hz; default is 60
	fretOffset = 0		#increase the offset to shift the fret buttons further down the keyboard; default is 0
	debug = 1			#turn this on to show the script working (may introduce a tiny bit of latency)
	
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
	midi[0].update += update
