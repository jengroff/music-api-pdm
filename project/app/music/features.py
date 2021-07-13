
import time
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint as pp
import numpy as np
import pandas as pd
import sqlite3
from dotenv import load_dotenv


"""
The code in this module is experimental, as is the sqlite database
in the same directory
"""


load_dotenv()
client = "CLIENT"
secret = "SECRET"


def spotify_auth():
    creds = SpotifyClientCredentials(client_id=client, client_secret=secret)
    return spotipy.Spotify(client_credentials_manager=creds)


sp = spotify_auth()

name = "Beck"
result = sp.search(name)
artist_uri = result['tracks']['items'][0]['artists'][0]['uri']

sp_albums = sp.artist_albums(artist_uri, album_type='album')
album_names = []
album_uris = []
for i in range(len(sp_albums['items'])):
    album_names.append(sp_albums['items'][i]['name'])
    album_uris.append(sp_albums['items'][i]['uri'])

spotify_albums = {}
album_count = 0


def albumSongs(uri):
    album = uri
    spotify_albums[album] = {}
    spotify_albums[album]['album'] = []
    spotify_albums[album]['track_number'] = []
    spotify_albums[album]['id'] = []
    spotify_albums[album]['name'] = []
    spotify_albums[album]['uri'] = []
    tracks = sp.album_tracks(album)
    for n in range(len(tracks['items'])):
        spotify_albums[album]['album'].append(album_names[album_count])
        spotify_albums[album]['track_number'].append(tracks['items'][n]['track_number'])
        spotify_albums[album]['id'].append(tracks['items'][n]['id'])
        spotify_albums[album]['name'].append(tracks['items'][n]['name'])
        spotify_albums[album]['uri'].append(tracks['items'][n]['uri'])


for i in album_uris:
    albumSongs(i)
    print("Album " + str(album_names[album_count]) + " songs has been added to spotify_albums dictionary")
    album_count += 1


def audio_features(album):
    # Add new key-values to store audio features
    spotify_albums[album]['acousticness'] = []
    spotify_albums[album]['danceability'] = []
    spotify_albums[album]['energy'] = []
    spotify_albums[album]['instrumentalness'] = []
    spotify_albums[album]['liveness'] = []
    spotify_albums[album]['loudness'] = []
    spotify_albums[album]['speechiness'] = []
    spotify_albums[album]['tempo'] = []
    spotify_albums[album]['valence'] = []
    spotify_albums[album]['popularity'] = []
    # create a track counter
    track_count = 0
    for track in spotify_albums[album]['uri']:
        # pull audio features per track
        features = sp.audio_features(track)

        # Append to relevant key-value
        spotify_albums[album]['acousticness'].append(features[0]['acousticness'])
        spotify_albums[album]['danceability'].append(features[0]['danceability'])
        spotify_albums[album]['energy'].append(features[0]['energy'])
        spotify_albums[album]['instrumentalness'].append(features[0]['instrumentalness'])
        spotify_albums[album]['liveness'].append(features[0]['liveness'])
        spotify_albums[album]['loudness'].append(features[0]['loudness'])
        spotify_albums[album]['speechiness'].append(features[0]['speechiness'])
        spotify_albums[album]['tempo'].append(features[0]['tempo'])
        spotify_albums[album]['valence'].append(features[0]['valence'])
        # popularity is stored elsewhere
        pop = sp.track(track)
        spotify_albums[album]['popularity'].append(pop['popularity'])
        track_count += 1


sleep_min = 2
sleep_max = 5
start_time = time.time()
request_count = 0
for i in spotify_albums:
    audio_features(i)
    request_count+=1
    if request_count % 5 == 0:
        print(str(request_count) + " playlists completed")
        time.sleep(np.random.uniform(sleep_min, sleep_max))
        print('Loop #: {request_count}')
        print('Elapsed Time: {} seconds'.format(time.time() - start_time))


dic_df = {'album': [], 'track_number': [], 'id': [], 'name': [], 'uri': [], 'acousticness': [], 'danceability': [],
          'energy': [], 'instrumentalness': [], 'liveness': [], 'loudness': [], 'speechiness': [], 'tempo': [],
          'valence': [], 'popularity': []}
for album in spotify_albums:
    for feature in spotify_albums[album]:
        dic_df[feature].extend(spotify_albums[album][feature])

df = pd.DataFrame.from_dict(dic_df)
df['artist'] = name

db = 'artist.sqlite'
conn = sqlite3.connect(db)

df.to_csv(f'{name}_artist_features.csv')
df.to_sql('Features', con=conn, if_exists='append', index=False)

