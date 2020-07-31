#!/usr/bin/python3

import sqlite3
import tkinter
import tkinter.font
import vlc

def parseInput(event=None):
	playAlbum(albumIDEntry.get())
	
def playAlbum(searchID):
	
	# find the path to the files using the album ID
	query = "SELECT albumPath FROM albums WHERE albumID = " + str(searchID)
	curs.execute(query)
	result = curs.fetchall()

	# if we find a match in the database
	if result:
		for x in result:
			# filePath = x[0] + "*.mp3"
			filePath = "/music/Led Zeppelin - Led Zeppelin II/07 Ramble On.mp3"
			# print(filePath)
			# awful prototype hack using a system call to mpg123
			# os.system('mpg123 ' + filePath)
			
			# much better using VLC to play the files
			player = vlc.MediaPlayer(filePath)
			player.play()


	# no matching album ID in the database, print a helpful error message
	else:
		error = tkinter.Label(text="No matching album found", font=myFont)
		error.grid(row=3)
		
def exitProgram():
	scanWindow.quit()

# set up connection to SQLite3 database
conn = sqlite3.connect("/home/pi/music.db")
curs = conn.cursor()

# set up initial window parameters
scanWindow = tkinter.Tk()
scanWindow.title("Music Box")
myFont = tkinter.font.Font(family='Helvetica', size=12, weight="bold")

# define and place all our UI elements in the window
instructions = tkinter.Label(scanWindow, text="Scan the album barcode to play", font=myFont)
instructions.grid(row=1)
albumIDEntry = tkinter.Entry(scanWindow, font=myFont, width=20)
albumIDEntry.grid(row=2)
albumIDEntry.bind('<Return>', parseInput)
exitButton=tkinter.Button(scanWindow, text='Exit', font=myFont, command=exitProgram, bg='cyan', height=1, width=6)
exitButton.grid(row=4)

scanWindow.mainloop()

# show the scan window
# look for the album in the database
  # add the files to a playlist
  # open the player window
  # play the playlist