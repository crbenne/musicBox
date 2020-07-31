#!/usr/bin/python3

import time
import vlc

fileList = ["/music/Led Zeppelin - Led Zeppelin II/01 Whole Lotta Love.mp3", "/music/Led Zeppelin - Led Zeppelin II/02 What Is and What Should Never Be.mp3"]

vlcOpts = "-A alsa"

instance = vlc.Instance(vlcOpts)
mainPlayer = vlc.MediaListPlayer(instance)
mainPlayer.set_media_list(instance.media_list_new(fileList))