from collections import namedtuple
import os

import spotipy
import spotipy.util
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

redirect = os.getenv("SPOTIFY_REDIRECT_URI")
client = os.getenv("SPOTIFY_CLIENT_ID")
secret = os.getenv("SPOTIFY_SECRET")
account = os.getenv("SPOTIFY_ACCOUNT")
scope = os.getenv("SPOTIFY_SCOPE")

MARKET, LIMIT = "US", 1
Song = namedtuple("Song", ("spid artist name tempo energy " "danceability uri url"))
Features = namedtuple("Features", "energy danceability tempo")
Artist = namedtuple("Artist", "spid name uri url")


class SongNotFoundException(Exception):
    pass


class ArtistNotFoundException(Exception):
    pass


class Spotify:
    def __init__(self):
        self.sp = self._spotify_auth()

    def _spotify_auth(self):
        creds = SpotifyClientCredentials(client_id=client, client_secret=secret)
        return spotipy.Spotify(client_credentials_manager=creds)

    def _parse_features(self, spid: str):
        res = self.sp.audio_features(spid)
        fparsed = res[0]
        energy = fparsed["energy"]
        danceability = fparsed["danceability"]
        tempo = fparsed["tempo"]
        return Features(energy, danceability, tempo)

    def get_song(self, artist, name):
        search = f"{artist}+{name}"
        result = self.sp.search(search, limit=LIMIT, market=MARKET)
        if not result["tracks"]["items"]:
            raise SongNotFoundException("Song not found")

        parsed = result["tracks"]["items"][0]
        spid = parsed["id"]
        artist = parsed["artists"][0]["name"]
        name = parsed["name"]
        uri = parsed["uri"]
        url = parsed["external_urls"]["spotify"]
        features = self._parse_features(spid)
        return Song(
            spid,
            artist,
            name,
            features.tempo,
            features.energy,
            features.danceability,
            uri,
            url,
        )

    def get_artist(self, artist):
        search = f"{artist}"
        result = self.sp.search(search)
        if not result["tracks"]["items"][0]["artists"]:
            raise ArtistNotFoundException("Artist not found")

        parsed = result["tracks"]["items"][0]["artists"][0]
        spid = parsed["id"]
        name = parsed["name"]
        uri = parsed["uri"]
        url = parsed["external_urls"]["spotify"]
        return Artist(
            spid,
            name,
            uri,
            url,
        )
