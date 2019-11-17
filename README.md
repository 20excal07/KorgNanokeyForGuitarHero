# Korg nanoKEY/nanoKEY2 [FreePIE](https://andersmalmgren.github.io/FreePIE/) script for Guitar Hero
FreePIE script for Korg nanoKEY/nanoKEY2 usage with Guitar Hero-esque rhythm games.

[**Requires vJoy to be installed first.**](http://vjoystick.sourceforge.net/site/)

You don't have to configure anything on the vJoy side of things, its default setup will work just fine. Just make sure at least one vJoy controller is active.

### Intended/Default control scheme:

![alt text](https://github.com/20excal07/KorgNanokeyForGuitarHero/raw/master/NanokeyGH.png)

## **How do I play with this?**
Hold the keyboard such that it faces away from you. The right end of the keyboard should be resting on your left hand, with your fingers fretting on the keys like you would a regular Guitar Hero controller. Reach for the strum keys with your right index and middle fingers with your right hand hovering slightly above the keyboard (kinda like playing a real bass guitar), and place your ring finger on the MOD button for star power/overdrive. Make sure you are sitting down for this so that the left end of the keyboard has something to rest on while you are playing.

[This video of someone playing GH3 with a PC keyboard held upside-down should give you a good picture.](https://www.youtube.com/watch?v=CrDsT99ml9Y)

## **The fret buttons are too close to the edge of the keyboard, it's uncomfy!**
Increment the `offset` variable in the script to shift the frets further down (to the left of) the keyboard.

## "Guitar on Keys mode"? What's that?
This mode is intended specifically for use with Keys charts in [_Phase Shift_](http://www.dwsk.co.uk/index_phase_shift.html).

When you press this button, the script switches to a mode where it essentially emulates the ability to play Keys charts with a guitar controller, like in _Rock Band 3_. The downside to this mode is that you won't be able to see visual feedback of frets being held down, and you will still need to strum every single note, even if they're like an eighth note apart from each other where they would normally be converted to HOPOs in Rock Band. You also won't be able to hold sustain notes, at least not without holding down on the strum button.

Press the other mode button to exit this mode.

## Can I use this with the original nanoKEY?
Yes you can, however I strongly recommend against it due to how cheaply the keyboard was built. You will likely be tapping hard on the keys to strum, and the keys will eventually fall off once enough wear has built up on the mechanical springs. Save up for a nanoKEY2 if you can... or just buy a Guitar Hero/Rock Band guitar controller like a normal person. :p

## Anything else?
Yes. Get the KORG Kontrol Editor software ([for Win7/8.1](https://www.korg.com/us/support/download/driver/1/133/1356/) | [for Win10](https://www.korg.com/us/support/download/driver/1/133/3541/)) and make sure to do the following. It'll make sure all the buttons being used here are "digital" and will overall just be much much more reliable to use. To apply the settings, click "Communications" > "Write Scene Data". Confirm when asked. 

![alt text](https://github.com/20excal07/KorgNanokeyForGuitarHero/raw/master/korgkontrol.png)
