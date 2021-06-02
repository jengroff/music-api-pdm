import os
from dataclasses import dataclass
from typing import Optional

import spotipy
import spotipy.util
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

redirect = os.getenv("SPOTIFY_REDIRECT_URI")
client = os.getenv("SPOTIFY_CLIENT_ID")
secret = os.getenv("SPOTIFY_SECRET")
account = os.getenv("SPOTIFY_ACCOUNT")
scope = os.getenv("SPOTIFY_SCOPE")


@dataclass
class SpotifySong:
    """Represents the Spotify song data we want to store.

    Attributes:
        spid: Spotify's unique ID for the song, as a string.
        track: The human-readable song name, as a string.
        artist: The human-readable artist name, as a string.
        tempo: Spotify-assigned acoustic feature 'tempo'.
        energy: Spotify-assigned acoustic feature 'energy'.
        danceability: Spotify-assigned acoustic feature 'danceability'.
        uri: Spotify's uniform resource identifier.
        url: Spotify-assigned url for the track.
    """
    artist: str
    name: str
    tempo = Optional[int]
    energy = Optional[int]
    danceability = Optional[int]
    uri = Optional[str]
    url = Optional[str]

    def spotify_auth(self):
        auth_manager = SpotifyOAuth(account, scope, redirect_uri=redirect)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        client_credentials_manager = SpotifyClientCredentials(client_id=client, client_secret=secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        return sp

    def get_features(self, spid: str):
        sp = self.spotify_auth()
        res = sp.audio_features(spid)
        fparsed = res[0]
        energy = fparsed['energy']
        danceability = fparsed['danceability']
        tempo = fparsed['tempo']

        features_dict = {
            "energy": energy,
            "danceability": danceability,
            "tempo": int(tempo)
        }
        return features_dict

    def make_song(self, artist: str, name: str):
        sp = self.spotify_auth()
        result = sp.search(f"{artist}+{name}", limit=1, market="US")
        parsed = result['tracks']['items'][0]
        uri = parsed['uri']
        spid = parsed['id']
        name = parsed['name']
        artist = parsed['artists'][0]['name']
        url = parsed['external_urls']['spotify']

        song_dict = {
            "spid": spid,
            "name": name,
            "artist": artist,
            "uri": uri,
            "url": url
        }
        features = self.get_features(spid)
        song_dict.update(features)
        return song_dict
