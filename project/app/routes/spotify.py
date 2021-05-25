import spotipy
import spotipy.util
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from app.utils.const import SPOTIFY_SECRET, SPOTIFY_CLIENT_ID, SPOTIFY_REDIRECT_URI
from fastapi import APIRouter


router = APIRouter()


def spotify_auth():
    auth_manager = SpotifyOAuth('joshengroff',
                                'playlist-read-collaborative',
                                redirect_uri=SPOTIFY_REDIRECT_URI)

    sp = spotipy.Spotify(auth_manager=auth_manager)
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                          client_secret=SPOTIFY_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp


def get_track_acoustic_features(spid: str):
    sp = spotify_auth()
    response = sp.audio_features(spid)
    energy = response[0]['energy']
    danceability = response[0]['danceability']
    tempo = response[0]['tempo']
    features_dict = {
        "spenergy": energy,
        "spanceability": danceability,
        "spempo": int(tempo)
    }
    return features_dict


@router.get("/spotify/song",
            summary="Retrieves summary Song data from Spotify",
            description="Takes both Artist and Song name in query parameter and returns Spotify song data as a dictionary")
def get_song_data(artist: str, track: str):
    sp = spotify_auth()
    result = sp.search(f"{artist}+{track}", limit=1, market="US")
    uri = result['tracks']['items'][0]['uri']
    spid = result['tracks']['items'][0]['id']
    name = result['tracks']['items'][0]['name']
    artist = result['tracks']['items'][0]['artists'][0]['name']
    url = result['tracks']['items'][0]['external_urls']['spotify']

    song_dict = {
        "spid": spid,
        "name": name,
        "artist": artist,
        "uri": uri,
        "url": url
    }
    features = get_track_acoustic_features(spid)
    song_dict.update(features)
    return song_dict


@router.get("/spotify/artist",
            summary="Retrieves summary Artist data from Spotify",
            description="Takes Artist name as a query parameter and returns Spotify artist data as a dictionary")
def get_artist_data(artist_name: str):
    sp = spotify_auth()
    name = artist_name
    result = sp.search(name)
    artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
    artist_id = result['tracks']['items'][0]['artists'][0]['id']
    artist_name = result['tracks']['items'][0]['artists'][0]['name']
    artist_url = result['tracks']['items'][0]['artists'][0]['external_urls']['spotify']
    artist_dict = {
        "spid": artist_id,
        "name": artist_name,
        "uri": artist_uri,
        "url": artist_url
    }
    return artist_dict
