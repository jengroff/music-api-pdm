from models.spotify import SpotifySong



my_song = SpotifySong('U2', 'Bad')

print(my_song)

my_song.make_song('U2', 'Bad')

print(my_song.uri)