#!/usr/bin/python3

import tkinter
import tkinter.font

playerWindow = tkinter.Tk()
playerWindow.title("Playlist")
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

# define and place all our UI elements in the window
instructions = tkinter.Label(playerWindow, text="Use the buttons below to control playback", font=myFont)
instructions.pack()

# frame for playlist
playlistFrame = tkinter.Frame(playerWindow)
playlistFrame.pack()
playlistBox = tkinter.Text(playlistFrame, width=40, height=8)
playlistBox.pack()

# frame for transport controls
controlFrame = tkinter.Frame()
controlFrame.pack()

# pack the control buttons into the frame
prevButton = tkinter.Button(controlFrame, text="<<", font=myFont, command=prevTrack)
prevButton.pack(side=tkinter.LEFT)
stopButton = tkinter.Button(controlFrame, text="[]", font=myFont, command=stopTrack)
stopButton.pack(side=tkinter.LEFT)
pauseButton = tkinter.Button(controlFrame, text=">", font=myFont, command=pauseTrack)
pauseButton.pack(side=tkinter.LEFT)
nextButton = tkinter.Button(controlFrame, text=">>", font=myFont, command=nextTrack)
nextButton.pack(side=tkinter.LEFT)
exitButton = tkinter.Button(playerWindow, text='Exit', font=myFont, command=exitProgram)
exitButton.pack()


playerWindow.mainloop()