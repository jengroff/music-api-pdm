from typing import List

from fastapi import APIRouter, HTTPException, Path
from tortoise.contrib.fastapi import HTTPNotFoundError

from app.database.models import Song, SongSchema, SongPayloadSchema
from app.database.models import Status


router = APIRouter()


@router.get("/songs", response_model=List[SongSchema])
async def get_songs():
    return await SongSchema.from_queryset(Song.all())


@router.post("/songs", response_model=SongSchema, status_code=201)
async def create_song(song: SongPayloadSchema):
    song_obj = await Song.create(**song.dict(exclude_unset=True))
    return await SongSchema.from_tortoise_orm(song_obj)



@router.get(
    "/songs/{id}",
    response_model=SongSchema,
    status_code=200)
async def get_song(id: int = Path(..., gt=0)):
    song = await SongSchema.from_queryset_single(Song.get(id=id))
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    return song


@router.put(
    "/songs/{id}",
    response_model=SongSchema,
    status_code=200,
    responses={404: {"model": HTTPNotFoundError}}
)
async def update_song(song: SongPayloadSchema, id: int = Path(..., gt=0)):
    await Song.filter(id=id).update(**song.dict(exclude_unset=True))
    song = await SongSchema.from_queryset_single(Song.get(id=id))
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    return song


@router.delete(
    "/songs/{id}",
    response_model=Status,
    status_code=200
)
async def delete_song(id: int = Path(..., gt=0)):
    deleted_count = await Song.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Song not found")
    return Status(message=f"Deleted song {id}")



