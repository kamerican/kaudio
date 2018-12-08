from kaudio.logic import Song, Manager

manager = Manager()
file_gen = manager.get_song_gen(manager.song_dir)

# for f in file_gen:
#     print(f)
filename = 'Taeyeon - Something New.mp3'
manager.get_vocals(filename)
