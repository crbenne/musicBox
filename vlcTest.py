#!/usr/bin/python3

import vlc
import time

songs = ["/home/pi/musicBox/pno-cs.mp3",
         "/home/pi/musicBox/file_example_MP3_1MG.mp3"]
		 
player = vlc.Instance()
mediaList = player.media_list_new()

for s in songs:
	mediaList.add_media(player.media_new(s))
	
listPlayer = player.media_list_player_new()
listPlayer.set_media_list(mediaList)

# print("List has " + str(mediaList.count()) + " songs")

for playlistPosition in range(mediaList.count()):
	try:
		print("Playing: " + str(mediaList.item_at_index(playlistPosition).get_mrl()))
	except:
		print("No more songs")
	else:
		listPlayer.play_item_at_index(playlistPosition)
		time.sleep(3)