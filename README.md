# etternaOverlay
an attempt on showing how osu would look if it used ms-based scoring

gui mode (default cause its an overlay haha)
---
![](https://i.imgur.com/TkUolzu.png)  
yes it looks like garbage, i'm trash with guis.

requirements ~~.txt~~ 
---
well. this thing is a python thing. as with all python things you need [python](https://www.python.org/downloads/).  
if you don't have python this is nothing but a collection of text files.

this thing uses [streamcompanion]() to get all the data it needs cause i couldn't be bothered doing it myself and  
if you're going to use **this** overlay, you're likely going to have it. basically all of the osu streaming community uses  
streamcompanion, and if you dont this script wont work.

**make sure to have streamcompanion opened. it `will` just crash saying it can't connect to the websocket.  
thats what it means, if you get that just** ***__open stream companion__.***

if you want to do it ye olde windows way, just [click here](https://github.com/roridev/etternaOverlay/archive/refs/heads/beta.zip) to download a zip file with the latest version on `beta`.  
this is beta software by now, which means it should work, but could just crash in 2 hours from now.

if you have git already clone this repo. 

installation
---
you can unzip or whatever, just get into the folder until you see `main.py`, it should be just one click.

go to the `resources` folder and install the font. tkinter likelly will crash the program if you dont.  
then go back to the main folder (the one that looks like the image below).

eitherway once you are that. open a command prompt on that folder.
![](https://i.imgur.com/bt1QNUK.png)  
then run the following commands
```
pip install -r requirements.txt
python main.py
```
the first one needs to be run only once.  
the next times you want to open it, just right click on `main.py` and choose `open`. 

notes
---
dont get scared if the window is **not responding**. thats part of it.  
it will update per note/miss cause thats how i got it to work.
