from typing import List

from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError

from app.database.models import (
    Playlist,
    PlaylistSchema,
    PlaylistPayloadSchema,
    Status,
)


router = APIRouter()


@router.get("/playlists", response_model=List[PlaylistSchema])
async def get_playlists():
    return await PlaylistSchema.from_queryset(Playlist.all())


@router.post("/playlists", response_model=PlaylistSchema, status_code=201)
async def create_playlist(playlist: PlaylistPayloadSchema):
    playlist_obj = await Playlist.create(**playlist.dict(exclude_unset=True))
    return await PlaylistSchema.from_tortoise_orm(playlist_obj)


@router.get(
    "/playlists/{id}",
    response_model=PlaylistSchema,
    status_code=200,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_playlist(id: int):
    return await PlaylistSchema.from_queryset_single(Playlist.get(id=id))


@router.put(
    "/playlists/{id}",
    response_model=PlaylistSchema,
    status_code=200,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_playlist(id: int, playlist: PlaylistPayloadSchema):
    await Playlist.filter(id=id).update(**playlist.dict(exclude_unset=True))
    return await PlaylistSchema.from_queryset_single(Playlist.get(id=id))


@router.delete(
    "/playlists/{id}",
    response_model=Status,
    status_code=200,
    responses={404: {"model": HTTPNotFoundError}},
)
async def delete_playlist(id: int):
    deleted_count = await Playlist.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Playlist {id} not found")
    return Status(message=f"Deleted playlist {id}")
