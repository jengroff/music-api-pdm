import os
import time
from collections import namedtuple
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import pandas as pd
import sqlite3
import json
from dotenv import load_dotenv
from pprint import pprint as pp


load_dotenv()
client = os.getenv("CLIENT")
secret = os.getenv("SECRET")
database_url = os.getenv("DATABASE_URL")


class SongNotFoundException(Exception):
    pass


class Features:
    def __init__(self, name):
        self.sp = self._spotify_auth()
        self.name = name

    def _spotify_auth(self):
        creds = SpotifyClientCredentials(client_id=client, client_secret=secret)
        return spotipy.Spotify(client_credentials_manager=creds)

    def get_song_features(self):
        result = self.sp.search(self.name)
        artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
        sp_albums = self.sp.artist_albums(artist_uri, album_type='album')
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
            tracks = self.sp.album_tracks(album)
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

            track_count = 0
            for track in spotify_albums[album]['uri']:
                features = self.sp.audio_features(track)

                spotify_albums[album]['acousticness'].append(features[0]['acousticness'])
                spotify_albums[album]['danceability'].append(features[0]['danceability'])
                spotify_albums[album]['energy'].append(features[0]['energy'])
                spotify_albums[album]['instrumentalness'].append(features[0]['instrumentalness'])
                spotify_albums[album]['liveness'].append(features[0]['liveness'])
                spotify_albums[album]['loudness'].append(features[0]['loudness'])
                spotify_albums[album]['speechiness'].append(features[0]['speechiness'])
                spotify_albums[album]['tempo'].append(features[0]['tempo'])
                spotify_albums[album]['valence'].append(features[0]['valence'])

                pop = self.sp.track(track)
                spotify_albums[album]['popularity'].append(pop['popularity'])
                track_count += 1

        sleep_min = 2
        sleep_max = 5
        start_time = time.time()
        request_count = 0
        for i in spotify_albums:
            audio_features(i)
            request_count += 1
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
        df['artist'] = self.name

        return df.to_dict(orient='records')
