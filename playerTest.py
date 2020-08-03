#!/usr/bin/python3

import tkinter
import tkinter.font
import sqlite3
import vlc

playerWindow = tkinter.Tk()
playerWindow.geometry("480x320")
playerWindow.title("Music Box")
myFont = tkinter.font.Font(family='Helvetica', size=12, weight="bold")

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
	
def scanHandler():
	fetchAlbum(barcodeEntry.get())
	
def fetchAlbum():

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
			# filePath = x[0] + "*.mp3"
			filePath = "/music/Led Zeppelin - Led Zeppelin II/07 Ramble On.mp3"
			playlistBox.insert("1.0", str(filePath))
			# print(filePath)
			# awful prototype hack using a system call to mpg123
			# os.system('mpg123 ' + filePath)
			
			# much better using VLC to play the files
			# player = vlc.MediaPlayer(filePath)
			# player.play()


	# no matching album ID in the database, print a helpful error message
	else:
		error = tkinter.Label(text="No matching album found", font=myFont)
		error.grid(row=3)
		
def addAlbum():
	scanWindow = tkinter.Tk()
	scanWindow.title("Scan barcode")
	
	barcodeEntry = tkinter.Entry(scanWindow, font=myFont, width=20)
	barcodeEntry.grid(row=1)
	barcodeEntry.bind('<Return>', scanHandler)

	cancelButton = tkinter.Button(scanWindow, text='Cancel', font=myFont)
	cancelButton.grid(row=2)

	scanWindow.mainloop()
	
def clearTracks():
	playlistBox.delete("1.0", tkinter.END)

# frame for playlist
playlistFrame = tkinter.Frame(playerWindow)
playlistFrame.pack()
playlistBox = tkinter.Text(playlistFrame, width=50, height=11)
playlistBox.pack()

# frame for control buttons 
controlFrame = tkinter.Frame()
controlFrame.pack()

# frame for extra buttons
extraFrame = tkinter.Frame()
extraFrame.pack()

# pack the control buttons into controlFrame
prevButton = tkinter.Button(controlFrame, text="<<", font=myFont, command=prevTrack)
prevButton.pack(side=tkinter.LEFT)
stopButton = tkinter.Button(controlFrame, text="[]", font=myFont, command=stopTrack)
stopButton.pack(side=tkinter.LEFT)
pauseButton = tkinter.Button(controlFrame, text=">", font=myFont, command=pauseTrack)
pauseButton.pack(side=tkinter.LEFT)
nextButton = tkinter.Button(controlFrame, text=">>", font=myFont, command=nextTrack)
nextButton.pack(side=tkinter.LEFT)

# pack the extra buttons into extraFrame
addButton = tkinter.Button(extraFrame, text='Add', font=myFont, command=addAlbum)
addButton.pack(side=tkinter.LEFT)
clearButton = tkinter.Button(extraFrame, text='Clear', font=myFont, command=clearTracks)
clearButton.pack(side=tkinter.LEFT)

playerWindow.mainloop()