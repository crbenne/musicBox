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
	
def scanHandler(event=None):
	fetchAlbum(barcodeEntry.get())
	
def fetchAlbum(barcode):

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
			filePath = x[0] + "/*.mp3"
			# filePath = "/music/Led Zeppelin - Led Zeppelin II/07 Ramble On.mp3"
			if playlistBox.compare("end-1c", "==", "1.0"):
				playlistBox.insert(tkinter.CURRENT, str(filePath))
			else:
				playlistBox.insert(tkinter.CURRENT, "\n" + str(filePath))
			# print(filePath)
			# awful prototype hack using a system call to mpg123
			# os.system('mpg123 ' + filePath)
			
			# much better using VLC to play the files
			# player = vlc.MediaPlayer(filePath)
			# player.play()


	# no matching album ID in the database, print a helpful error message
	else:
		if playlistBox.compare("end-1c", "==", "1.0"):
			playlistBox.insert(tkinter.CURRENT, "No matching album found!")
		else:
			playlistBox.insert(tkinter.CURRENT, "\nNo matching album found!")
		
	
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

# pack the extra widgets into extraFrame
barcodeLabel = tkinter.Label(extraFrame, text="UPC Code", font=myFont)
barcodeLabel.pack(side=tkinter.LEFT)
barcodeEntry = tkinter.Entry(extraFrame, font=myFont, width=20)
barcodeEntry.pack(side=tkinter.LEFT)
barcodeEntry.bind('<Return>', scanHandler)
clearButton = tkinter.Button(extraFrame, text='Clear list', font=myFont, command=clearTracks)
clearButton.pack(side=tkinter.LEFT)

playerWindow.mainloop()