#!/usr/bin/python3

import tkinter
import tkinter.font

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

def addAlbum():
	scanWindow = tkinter.Tk()
	scanWindow.title("Scan barcode")
	
	barcodeEntry = tkinter.Entry(scanWindow, font=myFont, width=20)
	barcodeEntry.grid(row=1)
	
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
