from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pprint import pprint as pp

from app.music.track import SongFeatures
from app.music.spotify import Spotify


def get_track_features(artist: str, name: str):
    sf = SongFeatures()
    song = sf.get_song(artist, name)._asdict()
    json_compatible_item_data = jsonable_encoder(song)
    return JSONResponse(content=json_compatible_item_data)


def get_song_data(artist: str, name: str):
    sp = Spotify()
    song = sp.get_song(artist, name)._asdict()
    json_compatible_item_data = jsonable_encoder(song)
    return JSONResponse(content=json_compatible_item_data)
    # adding comment


