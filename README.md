Here's a few simple Python programs to control lights on the Exquis.

They're controlled by MIDI sysex commands of the form:

F0 00 21 7E 03 (keynum) (R) (G) (B) F7

The keys are numbered from 0 at the lower left to 60 at the top right, running across the rows.

Install Python from here:
https://www.python.org/downloads/

Open a command prompt and enter "pip install python-rtmidi"
   
Download Python scripts above (eg click on the "raw" button).

Navigate to the relevant folder in the command window and run eg "py blank.py".

This turns all lights off. Other scripts turn all lights green, and animate rows and columns.

If this doesn't work, try running "py listports.py" to find the name of the device for your Exquis and edit the script in Notepad to change it from "Exquis 1" to whatever the value is. (Eg perhaps "Exquis 2".)

Demo:

https://youtu.be/MVPomWVR_68

(The method for discovering this was to install a virtual MIDI port, loopMIDI, on Windows, point the App at it, and use utilities like Bome/MidiOx to display the sysex messages when changing scales while passing them onto the Exquis.)


(Disclaimer: I only dabble in programming/github.)
