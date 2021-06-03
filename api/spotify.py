import os

from fastapi import APIRouter

router = APIRouter()


@router.get("/spotify/song",
            summary="Retrieves summary Song data from Spotify",
            description="Takes both Artist and Song name in query parameter and returns Spotify song data as a "
                        "dictionary")
def get_song_data(artist: str, track: str):
    # TODO should call spotify method defined on the class
    pass


@router.get("/spotify/artist",
            summary="Retrieves summary Artist data from Spotify",
            description="Takes Artist name as a query parameter and returns Spotify artist data as a dictionary")
def get_artist_data(artist_name: str):
    pass
