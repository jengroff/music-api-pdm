from typing import List

from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError

from app.database.models import Song_Pydantic, Songs, SongInsertSchema
from app.database.models import Status


router = APIRouter()


@router.get("/songs", response_model=List[Song_Pydantic])
async def get_songs():
    return await Song_Pydantic.from_queryset(Songs.all())


@router.post("/songs", response_model=Song_Pydantic, status_code=201)
async def create_song(song: SongInsertSchema):
    song_obj = await Songs.create(**song.dict())
    return await Song_Pydantic.from_tortoise_orm(song_obj)


@router.get("/songs/{id}", response_model=Song_Pydantic, status_code=200,
            responses={404: {"model": HTTPNotFoundError}})
async def get_song(id: int):
    return await Song_Pydantic.from_queryset_single(Songs.get(id=id))


@router.put("/songs/{id}", response_model=Song_Pydantic, status_code=200,
            responses={404: {"model": HTTPNotFoundError}})
async def update_song(id: int, song: SongInsertSchema):
    await Songs.filter(id=id).update(**song.dict(exclude_unset=True))
    return await Song_Pydantic.from_queryset_single(Songs.get(id=id))


@router.delete("/songs/{id}", response_model=Status, status_code=200,
               responses={404: {"model": HTTPNotFoundError}})
async def delete_song(id: int):
    deleted_count = await Songs.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Song {id} not found")
    return Status(message=f"Deleted song {id}")