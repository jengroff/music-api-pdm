from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from tortoise import run_async
from app.music.spotify import Spotify
from app.database.models import Artist, ArtistPydantic, Song, SongPydantic

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
    "/spotify/artist/db",
    summary="Fetch artist data from Spotify AND save to database (= time saver)",
    description=(
            (
                    "Takes Artist name as a query parameter and"
                    "stores result in the database"
            )
    ),
)
async def create_artist_db(artist):

    """
    Fetches artist data from Spotify then automatically
    adds it to the artists table in the db, saving a step
    """

    sp = Spotify()
    artist = sp.get_artist(artist)._asdict()
    artist_obj = await Artist.create(**artist)
    return await ArtistPydantic.from_tortoise_orm(artist_obj)


@router.get(
    "/spotify/song/db",
    summary="Fetch artist data from Spotify AND save to database (= time saver)",
    description=(
            (
                    "Takes Song name as a query parameter and"
                    "stores result in the database"
            )
    ),
)
async def create_song_db(artist: str, name: str):
    """
     Fetches song data from Spotify then automatically
     adds it to the songs table in the db, saving a step
     """

    sp = Spotify()
    song = sp.get_song(artist, name)._asdict()
    song_obj = await Song.create(**song)
    return await SongPydantic.from_tortoise_orm(song_obj)

