from typing import List

from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError

from app.database.models import Playlist_Pydantic, Playlists, PlaylistInsertSchema, Status


router = APIRouter()

@router.get("/playlists", response_model=List[Playlist_Pydantic])
async def get_playlists():
    return await Playlist_Pydantic.from_queryset(Playlists.all())


@router.post("/playlists", response_model=Playlist_Pydantic, status_code=201)
async def create_playlist(playlist: PlaylistInsertSchema):
    playlist_obj = await Playlists.create(**playlist.dict(exclude_unset=True))
    return await Playlist_Pydantic.from_tortoise_orm(playlist_obj)


@router.get("/playlists/{id}", response_model=Playlist_Pydantic, status_code=200,
            responses={404: {"model": HTTPNotFoundError}})
async def get_playlist(id: int):
    return await Playlist_Pydantic.from_queryset_single(Playlists.get(id=id))


@router.put("/playlists/{id}", response_model=Playlist_Pydantic, status_code=200,
            responses={404: {"model": HTTPNotFoundError}})
async def update_playlist(id: int, playlist: PlaylistInsertSchema):
    await Playlists.filter(id=id).update(**playlist.dict(exclude_unset=True))
    return await Playlist_Pydantic.from_queryset_single(Playlists.get(id=id))


@router.delete("/playlists/{id}", response_model=Status, status_code=200,
               responses={404: {"model": HTTPNotFoundError}})
async def delete_playlist(id: int):
    deleted_count = await Playlists.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Playlist {id} not found")
    return Status(message=f"Deleted playlist {id}")
