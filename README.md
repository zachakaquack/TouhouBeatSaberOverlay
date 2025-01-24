# TouhouBeatSaberOverlay
An overlay for Beat Saber that is themed around Touhou Project. All credit to ZUN for Touhou stuff.

# QUICK WARNING!!!
As of Jan 24th, 2025, the miss counter is fucked up. The websocket always returns the wrong number of misses, for some reason, so I had to make a jank hacky solution, so unfortunately, you will have to let the map play out to get an accurate count of the misses. I am trying to contact the author of the mod to fix this.

# What it actually looks like!
![Screenshot of the OBS overlay](/imgs/OBSExample.PNG)

# How it gets managed!
![Screenshot of the program that manages everything](/imgs/GUIExample.PNG)

# HOW TO INSTALL!!!!!
Follow [this guide](https://www.youtube.com/watch?v=XIMB5_kUxTs) to install. Make sure you follow exactly.
DM me on discord @zachakaquack if you have any questions, and I can help you with installation if needed.

## Prereqs:
Make sure your OBS is up to date enough to where you have websockets. To check, go to Tools -> Websocket Settings.
You will also need python (I used version 3.11 for this), pip, a library installer for python, and at least a text editor to change the password.
### Libraries Needed:
- customtkinter (pip install customtkinter)
- obswebsocket (pip install obs-websocket-py)
- asyncio (Included with python)
- json (Included with python)
- websockets (Included with python)
- threading (Included with python)

# How to use

## Starting up the overlay:
Literally just click the start button, and as long as your overlay is good, this should work.

## Creating the overlay in obs:
Make sure **ALL** the boxes are ticked, and click "Set OBS". You can customize the name of the scene in the bottom right. Just don't set it to like emojis or some dumb shit please

# WHAT NOT TO DO
DO NOT CHANGE THE NAMES OF THE TEXT IN THE SOURCE! IT WILL BREAK. I will fix this eventually maybe.
Don't set the name of the scene to emojis when making it or some dumb shit like that
