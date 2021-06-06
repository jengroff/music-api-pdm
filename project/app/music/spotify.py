from collections import namedtuple
from dataclasses import dataclass
import os
from typing import Optional

from pydantic import BaseModel
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


# TODO: change design to have Spotify class that generates Song objects
# you basically split the behavior from the data
# Spotify.create_playlist(list[Song])
# Spotify is kind of the manager of Song, Playlist, etc. objects
Song = namedtuple("Song", ("spid track artist tempo energy " "danceability uri url"))


def spotify_auth():
    auth_manager = SpotifyOAuth(
        account, "playlist-read-collaborative", redirect_uri=redirect
    )

    sp = spotipy.Spotify(auth_manager=auth_manager)
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client, client_secret=secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp


def get_track_acoustic_features(spid: str):
    sp = spotify_auth()
    response = sp.audio_features(spid)
    energy = response[0]["energy"]
    danceability = response[0]["danceability"]
    tempo = response[0]["tempo"]
    features_dict = {
        "spenergy": energy,
        "spanceability": danceability,
        "spempo": int(tempo),
    }
    return features_dict


@dataclass
class SpotifySong:
    """Represents the Spotify song data we want to store.

    Attributes:
        spid: Spotify's unique ID for the song, as a string.
        track: The human-readable song track, as a string.
        artist: The human-readable artist track, as a string.
        tempo: Spotify-assigned acoustic feature 'tempo'.
        energy: Spotify-assigned acoustic feature 'energy'.
        danceability: Spotify-assigned acoustic feature 'danceability'.
        uri: Spotify's uniform resource identifier.
        url: Spotify-assigned url for the track.
        sp: spotipy.Spotify auth object
    """

    artist: str
    name: str
    tempo = Optional[int]
    energy = Optional[int]
    danceability = Optional[int]
    uri = Optional[str]
    url = Optional[str]
    sp = Optional[str]

    def __post_init__(self):
        self.sp = self._spotify_auth()
        self._make_song()

    def _spotify_auth(self):
        auth_manager = SpotifyOAuth(account, scope, redirect_uri=redirect)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client, client_secret=secret
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        return sp

    def _get_features(self, spid: str):
        res = self.sp.audio_features(spid)
        fparsed = res[0]
        energy = fparsed["energy"]
        danceability = fparsed["danceability"]
        tempo = fparsed["tempo"]

        features_dict = {
            "energy": energy,
            "danceability": danceability,
            "tempo": int(tempo),
        }
        return features_dict

    def _make_song(self):
        result = self.sp.search(f"{self.artist}+{self.name}", limit=1, market="US")
        if not result["tracks"]["items"]:
            return

        parsed = result["tracks"]["items"][0]
        uri = parsed["uri"]
        spid = parsed["id"]
        name = parsed["name"]
        artist = parsed["artists"][0]["name"]
        url = parsed["external_urls"]["spotify"]

        song_dict = {
            "spid": spid,
            "name": name,
            "artist": artist,
            "uri": uri,
            "url": url,
        }
        features = self._get_features(spid)
        song_dict.update(features)
        from pprint import pprint as pp

        pp(song_dict)
        return song_dict


class SpotifySongResponse(BaseModel):
    artist: str
    name: str
    tempo: Optional[int]
    energy: Optional[int]
    danceability: Optional[int]
    uri: Optional[str]
    url: Optional[str]
    sp: Optional[str]
