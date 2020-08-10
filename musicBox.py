#!/usr/bin/python3

import tkinter
import tkinter.font
import sqlite3
import vlc
import time
from pathlib import Path

# set some of the main window properties
playerWindow = tkinter.Tk()
playerWindow.geometry("480x320")
playerWindow.title("Music Box")
myFont = tkinter.font.Font(family='Helvetica', size=12, weight="bold")
playlistFont = tkinter.font.Font(family='Helvetica', size=9)

# the root directory where music will be stored
rootMusicPath = Path("/music/")

# persistent playlist variable
playlist = []

# create the VLC objects we need -- a player, a media list, and a media list player
player = vlc.Instance()
mediaList = player.media_list_new()
listPlayer = player.media_list_player_new()

def prevTrack():
	playerWindow.quit()

def pauseTrack():
	playerWindow.quit()

def stopTrack():
	playerWindow.quit()

def nextTrack():
	playerWindow.quit()

def exitProgram():
	playerWindow.quit()
	
def scanHandler(event=None):
	fetchAlbum(barcodeEntry.get())
	
def fetchAlbum(barcode):

	barcodeEntry.delete(0, tkinter.END)

	# set up connection to SQLite3 database
	conn = sqlite3.connect("/home/pi/musicBox/music.db")
	curs = conn.cursor()

	# find the path to the files using the barcode
	query = "SELECT albumPath FROM albums WHERE albumID = " + str(barcode)
	curs.execute(query)
	result = curs.fetchall()

	# if we find a match in the database
	if result:
		for x in result:
			albumPath = rootMusicPath / x[0]
			fileList = sorted(albumPath.glob('*.mp3'))
			# if there are already entries in the playlist, we want to insert the new songs at the end
			# and not interrupt playback of the current list
			# get the number of items currently in the list
			mediaListCount = mediaList.count()
			for y in fileList:
				# write a 'nicer' string with just the filename in the player window
				playlistBox.insert(tkinter.CURRENT, str(y.stem) + "\n")
				# append the media to the persistent playlist
				playlist.append(y)
				mediaList.insert_media(vlc.Media(str(y)), mediaListCount)
				# if you want to see the MRL for the media in the window (debug)
				# playlistBox.insert(tkinter.CURRENT, mediaList.item_at_index(mediaListCount).get_mrl() + "\n")
				mediaListCount += 1

		listPlayer.set_media_list(mediaList)

	# no matching album ID in the database, print a helpful error message
	else:
		barcodeEntry.insert(0, "No match!")
		# time.sleep(3)
		# barcodeEntry.delete(0, tkinter.END)
		# playlistBox.insert(tkinter.CURRENT, "No matching album found!\n")

	conn.close()
	
def clearTracks():
	# clear everything displayed in the playlist window
	playlistBox.delete("1.0", tkinter.END)
	# clear the playlist list
	playlist.clear()
	# clear the media list
	mediaListCount = mediaList.count()
	i = 0
	while i < mediaListCount:
		mediaList.remove_index(0)
		i += 1

# frame for playlist
playlistFrame = tkinter.Frame(playerWindow)
playlistFrame.pack()

# playlist widget
playlistBox = tkinter.Text(playlistFrame, width=60, height=12, font=playlistFont)
playlistBox.pack()

# frame for now playing label
npFrame = tkinter.Frame()
npFrame.pack(fill=tkinter.X)

# add a "Now Playing:" label in the controlFrame
npLabel = tkinter.Label(npFrame, text="Now playing:", font=myFont)
npLabel.pack(anchor=tkinter.W, padx=10)

# frame for control buttons 
controlFrame = tkinter.Frame()
controlFrame.pack()

# pack the control buttons into controlFrame
prevButton = tkinter.Button(controlFrame, text="<<", font=myFont, command=prevTrack)
prevButton.pack(side=tkinter.LEFT)
stopButton = tkinter.Button(controlFrame, text="[]", font=myFont, command=stopTrack)
stopButton.pack(side=tkinter.LEFT)
pauseButton = tkinter.Button(controlFrame, text=">", font=myFont, command=pauseTrack)
pauseButton.pack(side=tkinter.LEFT)
nextButton = tkinter.Button(controlFrame, text=">>", font=myFont, command=nextTrack)
nextButton.pack(side=tkinter.LEFT)

# frame for extra buttons
extraFrame = tkinter.Frame()
extraFrame.pack()

# pack the extra widgets into extraFrame
barcodeLabel = tkinter.Label(extraFrame, text="UPC Code", font=myFont)
barcodeLabel.pack(side=tkinter.LEFT)
barcodeEntry = tkinter.Entry(extraFrame, font=myFont, width=20)
barcodeEntry.pack(side=tkinter.LEFT)
barcodeEntry.bind('<Return>', scanHandler)
clearButton = tkinter.Button(extraFrame, text='Clear list', font=myFont, command=clearTracks)
clearButton.pack(side=tkinter.LEFT)

playerWindow.mainloop()
