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
playlistFont = tkinter.font.Font(family='Helvetica', size=10)

# the root directory where music will be stored
rootMusicPath = Path("/music/")

# persistent playlist variable
playlist = []
playlistPos = 0

# create the VLC objects we need -- a player, a media list, a media list player, and an event manager for the media player in the media list player
player = vlc.Instance()
mediaList = player.media_list_new()
listPlayer = player.media_list_player_new()
events = listPlayer.get_media_player().event_manager()

def prevTrack():
	global playlistPos
	
	if playlistPos > 0:
		playlistPos -= 1
		listPlayer.previous()
		npLabel.config(text="Now playing: " + str(playlist[playlistPos].stem))

def pauseTrack():
	global playlistPos
	
	if listPlayer.is_playing():
		listPlayer.pause()
		pauseButton.config(text=">")
		npLabel.config(text="Now playing: Paused")
	else:
		listPlayer.play()
		pauseButton.config(text="||")
		npLabel.config(text="Now playing: " + str(playlist[playlistPos].stem))

def stopTrack():
	if listPlayer.is_playing():
		listPlayer.stop()
		pauseButton.config(text=">")
		npLabel.config(text="Now playing: Stopped")

def nextTrack():
	global playlistPos
	
	if playlistPos < (len(playlist) - 1):
		playlistPos += 1
		listPlayer.next()
		npLabel.config(text="Now playing: " + str(playlist[playlistPos].stem))

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
			# append the path from the match in the database to the root music path
			albumPath = rootMusicPath / x[0]
			# get a list of mp3 files from the path, alphanumerically sorted (assuming they have track numbers at the start)
			fileList = sorted(albumPath.glob('*.mp3'))
			# find out how many items are currently in the media list so we can insert any new items at the correct position
			mediaListCount = mediaList.count()
			# loop through each mp3 file found in the path
			for y in fileList:
				# write a 'nicer' string with just the filename with no extension (the stem) in the player window
				playlistBox.insert(tkinter.CURRENT, str(y.stem) + "\n")
				# append the media to the internal playlist
				playlist.append(y)
				# add the media to the media list
				mediaList.insert_media(vlc.Media(str(y)), mediaListCount)
				mediaListCount += 1

		# if the player is already playing something, we don't want to interrupt this -- so only do these if it's not playing
		if not listPlayer.is_playing():
			listPlayer.set_media_list(mediaList)
			listPlayer.play_item_at_index(0)
			pauseButton.config(text="||")
			npLabel.config(text="Now playing: " + str(playlist[playlistPos].stem))

	# no matching album ID in the database, probably good to display an error but right now just blanks the entry box
	else:
		# barcodeEntry.insert(0, "No match!")
		# time.sleep(3)
		barcodeEntry.delete(0, tkinter.END)
		# playlistBox.insert(tkinter.CURRENT, "No matching album found!\n")

	conn.close()
	
def clearTracks():
	global playlistPos

	# stop the player
	listPlayer.stop()
	# clear everything displayed in the playlist window and the Now Playing label
	playlistBox.delete("1.0", tkinter.END)
	npLabel.config(text="Now playing: Stopped")
	# clear the playlist and reset playlist position
	playlist.clear()
	playlistPos = 0
	# clear the media list
	mediaListCount = mediaList.count()
	i = 0
	while i < mediaListCount:
		mediaList.remove_index(0)
		i += 1
		
def songEnd(event):
	global playlistPos
	
	if playlistPos < (len(playlist) - 1):
		playlistPos += 1
		npLabel.config(text="Now playing: " + str(playlist[playlistPos].stem))

# frame for playlist
playlistFrame = tkinter.Frame(playerWindow)
playlistFrame.pack()

# playlist widget
playlistBox = tkinter.Text(playlistFrame, width=60, height=11, font=playlistFont)
playlistBox.pack()

# frame for now playing label
npFrame = tkinter.Frame()
npFrame.pack(fill=tkinter.X)

# add a "Now Playing:" label in the controlFrame
npLabel = tkinter.Label(npFrame, text="Now playing: Stopped", font=myFont)
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

# set event handlers
events.event_attach(vlc.EventType.MediaPlayerEndReached, songEnd)

playerWindow.mainloop()
