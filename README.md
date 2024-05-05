# Intuitive Instruments Exquis Isomorphic Layout Programmer

Thanks to chatGPT handling of OOP, threading and UI stuff, I have a working python script with a very basic fronted for reprogramming lights and notes layouts.

## Requirements
- Exquis updated to firmare 1.1.
- Python 3.8+
- The following python libraries:
	- python-rtmidi
	- tkinter
	- matplotlib
	- numpy

## User Guide

Currently the app is very limited, as my Python programming skills. Its main aim is to create custom isomorphic layout for the Exquis.
App has been tested in Arch Linux and Windows 10.
As far as I have seen it is still possible to use the device as a MIDI controller in DAWs while this tool is running.

> Intuitive Instruments is likely to come up with something slightly more sophisticated in the future, so don't get too excited about this, it is likely to become abandonware soon as I am only developing this for my personal need

### Connection

The first step is to connect to an Exquis, by selecting a midi device via the first dropdomn menu next to the `Select MIDI Device` text.  If connection is successful you will receive a message prompt that indicates that the port has been successfully open.

### Basic Layout

When creating the layout, it is useful to tilt your Exquis horizontally as such that the function buttons and the strip are on the left and the knobs are on the right. I will be describing the logic with which you can create custom templates on the `Main Layer` tab, going through each of the options in the order of appearance:
-`Start Note`, this would be the midi note that will be assigned to the Top-Left note in the layout with the Exquis placed as said before. In the normal layout, it is the hexagon just above the octave buttons.
-`Start Octave`, completes the note before with the octave
-`X semitone intervals`, this would be the step in semitones between each hexagon and the next one next to it on the X axis, i.e. on its right, looking at the Exquis horizontally, as indicated before.
-`Y semitone intervals`, as above but for the Y-axis, which corresponds to the semitones in the Exquis normal layout.
-`Z semitone intervals`, this would be the step in semitones between each hexagon and the one in the next column (if seen horizontally) or row.

Once we have made our selection by pressing the `Generate Template` the template will be generated and we can regenerate it as many time as we want to try different intervals.
In order to send the generated template to the Exquis we can press the `Send Template` Button.
 
> You can use the template generating capabilities of the app to visualise layout even without an Exquis connected

#### Example - Horizontal Harmonic table
If we take the same template that the Exquis ships with but we want to transpose it horizontally, ignoring the initial note we can set the following:
- `X` will have to be a semitone, 1
- `Y` would need to be a descending fourth (-5), because we are starting from the top and going down.
- `Z` would need to be a minor third (i.e. -4 semitones). 


### Advanced Layouts
The real reason I developed this tool was to create templates for two handed usage with split layout. Those are accessible selecting the `Split Layer` tab. Note that there are two types of split, whose names have been attributed by looking at the Exquis in his *natural* vertical state :
- `Horizontal`,  i.e. by rows vertically or columns horizontally, it is possible to split the Exquis starting from the 3rd,5th,7th or 9th column/row by selecting the required interval in the `Column Split` combobox. The option on the main layer are going to be applied to the left/bottom later, the ones on the split layer to the top/right one. The options are the same as for the main layout.
- `Vertical`, i.e. trying to split the Exquis Vertically, which means that each column/row of length 6 is split evenly between the two layer, but the user has the option to select how to split the rows/columns of length 5. There are 3 options to deal with such split:
	- `32`, assigns 3 hexagons to the left/top layer and 2  to the right/bottom one,
	-  `23` does exactly the opposite
	- `22` assigns 2 tho two leftmost/top notes to the main layer and the two rightmost/bottom to the split layer. The remaining note is blanked out.

#### Example Vertical Split - Diagonal Symmetric Harmonic Table
This layout is a slight variation on the default Exquis layout where the chromatic notes are to be found diagonally in rows of 5 notes without any duplicate. It features a couple of missing notes on the top and on the bottom and it dosen't use 5 keys. It is particularly ergonomic when playing the Exquis vertically on your lap. You can decide the starting notes as you please but the important intervals are the following:
- `X`, 5 for both the main and the split layer
- `Y`, 3 for the main layer and -3 for the split one, as the the mirror each other
- `Z`, 4 for the main layer and 1 for the 
- `Column Split` set to 22.
Here is the resulting layout, with its main characteristics highlighted:
#### Example Horizontal Split - Mixed  Diagonal-Horizontal Harmonic Table
Conceptually this is similar to the previous, but asymmetric and with the left/bottom/main layout diagonal and the other horizontal. Here are the main parameters:
- `X`, 2 for the main layer (the diagonal one), 1 for the split one (the horizontal one)
- `Y`, 4 for the main layer (notes increasing descending), -7 for the split one (notes increasing as normally going up)
- `Z`, 3 for the main layer, and -3 for the split one
- `Column Split` will be set as 5, the first 4 columns/rows are used by the main layer, the other by the secondary one
Here is the resulting layout, with its main characteristics highlighted:

### Exiting the application

Pressing the `Close Application` button in the top right corner will:
 1. Free the Exquis from the application control, all the lights would turn dark
 2. Close the application itself
 3. Close Python

Note that, from what I have seen, it seems the notes assignment do not disappear after the application has been stored, you would need to restart the Exquis.

## Technical Notes

### In development

- possibility to save and load templates
- default templates 
- creating colour schemes
- saving and loading colour schemes
- default colour schemes

### Sysex commands used in the script

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

As a client of most French speaking expressive controller makers (Expressive E, Intuitive instruments, Embodme, Aodyo and La Voix du Luthier) a big thanks for the French government/IRCAM for feeding up this fantastic start-ups!
