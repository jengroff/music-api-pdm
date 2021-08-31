from bson.objectid import ObjectId
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.music.track import SongFeatures
from app.music.spotify import Spotify
from app.music.tasks import (
    retrieve_and_cache_song_features,
    app as celery_app)
from app.mongo_db import retrieve_song_features

router = APIRouter()


@router.get(
    "/spotify/song",
    summary=("Fetch song data from Spotify "
             "(using artist and song name as parameters)"),
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
    description=(("Takes both Artist and Song name in query parameter")),
)
def get_track_features(artist: str, name: str):
    sf = SongFeatures()
    song = sf.get_song(artist, name)._asdict()
    json_compatible_item_data = jsonable_encoder(song)
    return JSONResponse(content=json_compatible_item_data)


def _serialize(song):
    """Rip out the _id: ObjectId (k, v) pair because
       it's not serializable
    """
    return {k: v for k, v in song.items()
            if not isinstance(v, ObjectId)}


@router.get(
    "/spotify/artist/all",
    summary="Returns acoustic features for every song of a given artist..",
    description="Takes Artist name as a query parameter"
)
def get_artist_songs(artist: str):
    """If songs are already in DB, retrieve them,
       otherwise start the retrieval / caching
       asynchronously.
    """
    artist = artist.lower()

    # TODO: how to prevent we kick off two download tasks?
    # so far we just check the DB for songs from artist
    # as a criteria of "job done"
    songs = retrieve_song_features(artist)

    if songs.count() > 0:
        return {
            "data": [_serialize(song) for song in songs]
        }

    job = retrieve_and_cache_song_features.delay(artist)
    return {"task_id": job.task_id}


@router.get(
    "/spotify/artist/all/download/status",
    summary="Returns status of async download",
    description="Takes task id as a query parameter"
)
def get_task_status(task_id: str):
    """This is useful for the front-end to show if the
       features download is still in progress.
    """
    result = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "ready": result.status.lower() == "success"
    }
