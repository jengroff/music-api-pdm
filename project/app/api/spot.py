from fastapi import APIRouter
from pprint import pprint as pp

from app.music.spotify import SpotifySong, SpotifySongResponse


router = APIRouter()


@router.get("/spotify/song", response_model=SpotifySong,
            summary="Retrieves summary Song data from Spotify",
            description="Takes both Artist and Song name in query parameter and returns Spotify song data as a "
                        "dictionary")
def get_song_data(artist: str, name: str):
    song_object = SpotifySong(artist, name)
    return song_object


@router.get("/spotify/artist",
            summary="Retrieves summary Artist data from Spotify",
            description="Takes Artist name as a query parameter and returns Spotify artist data as a dictionary")
def get_artist_data(artist_name: str):
    pass
