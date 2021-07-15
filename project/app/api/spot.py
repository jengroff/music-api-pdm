from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.music.track import SongFeatures
from app.music.spotify import Spotify


router = APIRouter()


@router.get(
    "/spotify/song",
    summary="Fetch song data from Spotify (using artist and song name as parameters)",
    description=(
        "Takes both Artist and Song name in query parameter "
        "and returns Spotify song data as a dictionary"
    ),
)
def get_song_data(artist: str, name: str):
    sp = Spotify()
    song = sp.get_song(artist, name)._asdict()
    json_compatible_item_data = jsonable_encoder(song)
    return JSONResponse(content=json_compatible_item_data)

@router.get(
    "/spotify/artist",
    summary="Fetch artist data from Spotify (using artist name as parameter)",
    description=(
        (
            "Takes Artist name as a query parameter and returns "
            "Spotify artist data as a dictionary"
        )
    ),
)
def get_artist_data(artist: str):
    sp = Spotify()
    artist = sp.get_artist(artist)._asdict()
    json_compatible_item_data = jsonable_encoder(artist)
    return JSONResponse(content=json_compatible_item_data)


@router.get(
    "/spotify/song/features",
    summary="Fetch the acoustic features for one song from Spotify",
    description=(
        (
            "Takes both Artist and Song name in query parameter"
        )
    ),
)
def get_track_features(artist: str, name: str):
    sf = SongFeatures()
    song = sf.get_song(artist, name)._asdict()
    json_compatible_item_data = jsonable_encoder(song)
    return JSONResponse(content=json_compatible_item_data)


@router.get(
    "/spotify/artist/all",
    summary="Returns acoustic features for every song of a given artist. USE WITH CARE.",
    description=(
        (
            "Takes Artist name as a query parameter"
        )
    ),
)
def get_artist_songs(artist: str):
    sf = Features(artist)
    artist_songs = sf.get_song_features()
    return artist_songs
