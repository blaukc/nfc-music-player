from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from vlc import Instance
import random
import time
import os


class VLC:
    def __init__(self):
        self.Player = Instance('--loop')

    def addPlaylist(self, path, shuffle):
        self.mediaList = self.Player.media_list_new()
        songs = os.listdir(path)
        playlist = []
        for s in songs:
            song_path = os.path.join(path,s)
            if 'mp3' in s[-3:]:
                mp3_specs = MP3(song_path)
                playlist.append([song_path, int(mp3_specs['TRCK'][0]), mp3_specs.info.length])
            elif 'flac' in s[-4]:
                flac_specs = FLAC(song_path)
                playlist.append([song_path, int(flac_specs['TRCK'][0]), flac_specs.info.length])

        if shuffle:
            playlist = self.shuffle_playlist(playlist)
        else:
            playlist = self.album_playlist(playlist)

        for song in playlist:
            self.mediaList.add_media(self.Player.media_new(song[0]))
        self.listPlayer = self.Player.media_list_player_new()
        self.listPlayer.set_media_list(self.mediaList)
        # print(self.mediaList.count())
        # print(self.listPlayer.get_state())

    def shuffle_playlist(self, playlist):
        random.shuffle(playlist)
        return playlist

    def album_playlist(self, playlist):
        sorted = []
        numbers = []
        for song in playlist:
            numbers.append(song[1])
        numbers.sort()
        for i in numbers:
            for song in playlist:
                if i == song[1]:
                    sorted.append(song)
                    break
        return sorted

    def play(self):
        self.listPlayer.play()

    def next(self):
        self.listPlayer.next()

    def pause(self):
        self.listPlayer.pause()

    def previous(self):
        self.listPlayer.previous()

    def stop(self):
        self.listPlayer.stop()

# player = VLC()
# player.addPlaylist("/home/pi/Music/211/", True)
# player.play()
# time.sleep(10)
# player.stop()
# player.addPlaylist("/home/pi/Music/212/", True)
# player.play()
# time.sleep(10)

# player = VLC("/home/pi/Music/MOTS/", False)
# player.play()
# pause = False
# while True:
#     time.sleep(2)
#     x = input('1234: ')
#     if x == '1':
#         if pause:
#             player.play()
#             pause = False
#         else:
#             player.pause()
#             pause = True
#
#     elif x == '2':
#         player.next()
#
#     elif x == '3':
#         player.previous()
#
#     elif x == '4':
#         player.stop()

# time.sleep(10)
# player.next()
# time.sleep(10)
# player.next()
# time.sleep(10)
# player.next()
# time.sleep(10)
# player.next()
# time.sleep(10)

# p = vlc.MediaPlayer("/home/pi/Music/212/Jeremy Zucker - i-70.mp3")
# playsong(p)
# time.sleep(5)
# print('hi')
# p.pause()

# x = threading.Thread(target=listen)
# x.start()
#
# y = threading.Thread(target=playsong)
# y.start()
