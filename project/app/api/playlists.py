from typing import List

from fastapi import APIRouter, HTTPException, Path, Depends, Body


from app.database.models import (
    Playlist,
    PlaylistPydantic,
    PlaylistInPydantic,
    Status,
    PlaylistNamePatch,
    PlaylistSongPatch,
)


router = APIRouter()


@router.get(
    "/playlists",
    response_model=List[PlaylistPydantic],
    summary="Get list of all playlists in the database",
)
async def get_playlists():
    return await PlaylistPydantic.from_queryset(Playlist.all())


@router.post(
    "/playlists",
    response_model=PlaylistPydantic,
    status_code=201,
    summary="Create a new playlist",
)
async def create_playlist(playlist: PlaylistInPydantic):
    playlist_obj = await Playlist.create(**playlist.dict(exclude_unset=True))
    return await PlaylistPydantic.from_tortoise_orm(playlist_obj)


@router.get(
    "/playlists/{id}",
    response_model=PlaylistPydantic,
    status_code=200,
    summary="Get a specific playlist by id",
)
async def get_playlist(id: int = Path(..., gt=0)):
    playlist = await PlaylistPydantic.from_queryset_single(Playlist.get(id=id))
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    return playlist


@router.put(
    "/playlists/{id}",
    response_model=PlaylistPydantic,
    status_code=200,
    summary="Update a specific playlist by id",
)
async def update_playlist(playlist: PlaylistInPydantic, id: int = Path(..., gt=0)):
    await Playlist.filter(id=id).update(**playlist.dict(exclude_unset=True))
    playlist = await PlaylistPydantic.from_queryset_single(Playlist.get(id=id))
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    return playlist


@router.patch(
    "/playlists/{id}/name",
    response_model=PlaylistPydantic,
    status_code=200,
    summary="Update a playlist's name",
)
async def patch_playlist_name(playlist: PlaylistNamePatch, id: int = Path(..., gt=0)):
    await Playlist.filter(id=id).update(**playlist.dict(exclude_unset=True))
    playlist = await PlaylistPydantic.from_queryset_single(Playlist.get(id=id))
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    return playlist


@router.patch(
    "/playlists/{id}/songs",
    response_model=PlaylistPydantic,
    status_code=200,
    summary="Update a playlist's songs",
)
async def patch_playlist_name(playlist: PlaylistSongPatch, id: int = Path(..., gt=0)):
    await Playlist.filter(id=id).update(**playlist.dict(exclude_unset=True))
    playlist = await PlaylistPydantic.from_queryset_single(Playlist.get(id=id))
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    return playlist


@router.delete(
    "/playlists/{id}",
    response_model=Status,
    status_code=200,
    summary="Delete a specific playlist by id",
)
async def delete_playlist(
    id: int = Path(..., gt=0),
):
    deleted_count = await Playlist.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Playlist not found")
    return Status(message=f"Deleted playlist {id}")
