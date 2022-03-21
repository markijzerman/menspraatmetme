# Humans, talk to me / Mens, praat met me
’Humans, Talk to Me’ / ‘Mens, Praat met Me’ is a speculative installation in which you get to talk to the North Sea. By using a machine learning model trained on a vast collection of Dutch texts about the North Sea, we approximate a "voice of the North Sea". Through this process, we hope to rewild the still mostly technocratic language with which we talk about the North Sea and its inhabitants.

When you address the North Sea with "Hey, North Sea" / "Hey Noordzee", like you would with Siri, the Sea asks you "What would you like to tell me". She will listen, and respond appropriately- in a Sea-ish language which seems like Dutch, but is riddled with new words and grammar, a result of the AI process.

Created together with Arita Baaijens, Axel Coumans and Eeke Brussee for the exhibition at Museum de Lakenhal, "If Things Grow Wrong".

https://www.markijzerman.com/works/humans-talk-to-me/

### LAKENHAL STARTUP
https://superuser.com/questions/954950/run-a-script-on-start-up-on-windows-10

Manage stuff in scheduler
https://www.addictivetips.com/windows-tips/terminate-close-an-app-on-schedule-on-windows-10/


### BAT FILE STARTUP

@ ECHO OFF
: This batch file starts up the Python and Touchdesigner
: script for the Lakenhal installation
: Mark IJzerman, 2021

TITLE LAKENHAL STARTUP

ECHO FIRST MAKE SURE THEYRE NOT RUNNING
TASKKILL /F /IM TouchDesigner.exe
TASKKILL /F /IM python3.9.exe

ECHO STARTING UP TOUCHDESIGNER
start "%programfiles%\derivative\touchdesigner099\bin\touchdesigner099.exe" "C:\Users\lakenhal\Desktop\LAKENHAL\LAKENHAL.toe"


ECHO STARTING UP PYTHON SCRIPT
start python "C:\Users\lakenhal\Desktop\LAKENHAL\live_recognizer.py"

### BAT FILE SHUTDOWN

@ ECHO OFF
: This batch file quits the Python and Touchdesigner
: script for the Lakenhal installation
: Mark IJzerman, 2021

TITLE LAKENHAL STOP

ECHO STOPPING TOUCH
TASKKILL /F /IM TouchDesigner.exe


ECHO STOPPING PYTHON SCRIPT
TASKKILL /F /IM python3.9.exe