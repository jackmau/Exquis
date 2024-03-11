# Intuitive Instruments Exquis Quick Layout Programmer

Thanks to chatGPT handling of OOP, threading and UI stuff, I have a working python script with a very basic fronted for reprogramming lights and notes layouts.

## Requirements
- Exquis updated to firmare 1.1.
- Python 3.8+
- The following python libraries:
	- python-rtmidi
	- tkinter
	- Pillow

## User Guide

Currently the app is very limited, as my Python programming skills.
You can just select a layout (which is a preloaded picture) and then send it to the device by pressing the `start midi` button.
Once you press the `stop midi` button, you should see all the lights turned off.
 
Currently you need to define the name of your device in the application.
 
Intuitive Instruments is likely to come up with something slightly more sophisticated in the future, so don't get too excited about this, it is likely to become abandonware soon as I am only developing this for my personal needs.

## Sysex commands used in the script

There are 3 main sysex messages used in the script:

1. F0 00 21 7E F7, every 400 ms, to let the device know that we are holding onto it very dearly and we want to be in control
2. F0 00 21 7E 03 (keynum) (R) (G) (B) F7, for notes colours
3. F0 00 21 7E 04 (keynum) (NoteNumber) F7, for midi notes numbers

If you are curious to know, other sysex messages supported include:
- Input:
	- button colour : F0 00 21 7E 07 buttonId r g b F7
	- knob colour : F0 00 21 7E 09 knobId r g b F7
- Output:
	- button click : F0 00 21 7E 08 buttonId buttonState F7
	- knob left : F0 00 21 7E 10 knobId leftIncrement F7
	- knob right : F0 00 21 7E 11 knobId rightIncrement F7

List fetched by post by *Sergueï Bécoulet* on the official Intuitive Instruments Discord.

| **Important note**: the current messages are working in v 1.1, but are not officialy supported and may change in the future 

The keys are numbered from 0 at the lower left to 60 at the top right, running across the rows.
The standard scale colours are 00 00 00 (blank), 38 1D 41, and 7F 5F 3F.
From my experience (but it may be exquis) colours higher than 79 (in binary, which corresponds to 128) don't seem to get sent on G and B.
This is why I included an adjustment to rescale colours

## Acknowledgments

- [@bjglover](https://github.com/bjglover) for his original repo, which is where I became aware that there were sysex messages to control lights of the Exquis, and that I took inspiration (and some code from)
- Sergueï Bécoulet, which gently provided the sysex codes, in particular the one that allows to talk with the exquis
- the whole Intuitive Instruments team for creating such an excellent instrument

As a client of most French speaking expressive controller makers (Expressive E, Intuitive instruments, Embodme and La Voix du Luthier) a big thanks for the French government/IRCAM for feeding up this fantastic start-ups!
