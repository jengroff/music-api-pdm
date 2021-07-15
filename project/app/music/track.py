from collections import namedtuple
import os
from pydantic import BaseModel
from typing import Optional

import spotipy
import spotipy.util
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

redirect = os.getenv("SPOTIFY_REDIRECT_URI")
client = os.getenv("SPOTIFY_CLIENT_ID")
secret = os.getenv("SPOTIFY_SECRET")

MARKET, LIMIT = "US", 1
Track = namedtuple("Track", ("id name artist uri acousticness danceability energy instrumentalness liveness loudness speechiness tempo valence"))
Features = namedtuple("Features", ("acousticness danceability energy instrumentalness liveness loudness speechiness tempo valence"))


class TrackNotFoundException(Exception):
    pass


class SongFeatures:
    def __init__(self):
        self.sp = self._spotify_auth()

    def _spotify_auth(self):
        creds = SpotifyClientCredentials(client_id=client, client_secret=secret)
        return spotipy.Spotify(client_credentials_manager=creds)

    def _parse_features(self, id: str):
        res = self.sp.audio_features(id)
        fparsed = res[0]
        acousticness = fparsed["acousticness"]
        danceability = fparsed["danceability"]
        energy = fparsed["energy"]
        instrumentalness = fparsed["instrumentalness"]
        liveness = fparsed["liveness"]
        loudness = fparsed["loudness"]
        speechiness = fparsed["speechiness"]
        tempo = fparsed["tempo"]
        valence = fparsed["valence"]

        return Features(
            acousticness,
            danceability,
            energy,
            instrumentalness,
            liveness,
            loudness,
            speechiness,
            tempo,
            valence
        )

    def get_song(self, artist, name):
        search = f"{artist}+{name}"
        result = self.sp.search(search, limit=LIMIT, market=MARKET)
        if not result["tracks"]["items"]:
            raise TrackNotFoundException("Song not found")

        parsed = result["tracks"]["items"][0]
        id = parsed["id"]
        artist = parsed["artists"][0]["name"]
        name = parsed["name"]
        uri = parsed["uri"]
        features = self._parse_features(id)
        return Track(
            id,
            artist,
            name,
            uri,
            features.acousticness,
            features.danceability,
            features.energy,
            features.instrumentalness,
            features.liveness,
            features.loudness,
            features.speechiness,
            features.tempo,
            features.valence
        )
