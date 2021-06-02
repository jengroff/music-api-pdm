from typing import List
from fastapi import APIRouter, HTTPException
from app.models import Playlist_Pydantic, Playlists
from app.models import Status
from tortoise.contrib.fastapi import HTTPNotFoundError


router = APIRouter()


@router.get("/playlists", response_model=List[Playlist_Pydantic])
async def get_playlists():
    return await Playlist_Pydantic.from_queryset(Playlists.all())


@router.post("/playlists", response_model=Playlist_Pydantic, status_code=201)
async def create_playlist(playlist: Playlist_Pydantic):
    playlist_obj = await Playlists.create(**playlist.dict(exclude_unset=True))
    return await Playlist_Pydantic.from_tortoise_orm(playlist_obj)


@router.get("/playlists/{id}", response_model=Playlist_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_playlist(id: int):
    return await Playlist_Pydantic.from_queryset_single(Playlists.get(id=id))


@router.put("/playlists/{id}", response_model=Playlist_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_playlist(id: int, playlist: Playlist_Pydantic):
    await Playlists.filter(id=id).update(**playlist.dict(exclude_unset=True))
    return await Playlist_Pydantic.from_queryset_single(Playlists.get(id=id))


@router.delete("/playlists/{id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_playlist(id: int):
    deleted_count = await Playlists.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Playlist {id} not found")
    return Status(message=f"Deleted playlist {id}")


