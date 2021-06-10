from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.music.spotify import Spotify


router = APIRouter()


@router.get(
    "/spotify/song",
    summary="Retrieves summary Song data from Spotify",
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
    summary="Retrieves summary Artist data from Spotify",
    description=(
        (
            "Takes Artist name as a query parameter and returns "
            "Spotify artist data as a dictionary"
        )
    ),
)
def get_artist_data(artist_name: str):
    pass
