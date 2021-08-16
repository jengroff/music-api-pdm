from typing import List

from fastapi import APIRouter, HTTPException, Path, Depends

from app.database.models import Song, SongPydantic, SongInPydantic, Status

router = APIRouter()


@router.get(
    "/songs",
    response_model=List[SongPydantic],
    summary="Get list of all songs in the database",
)
async def get_songs():
    return await SongPydantic.from_queryset(Song.all())


@router.post(
    "/songs", response_model=SongPydantic, status_code=201, summary="Create a new song"
)
async def create_song(song: SongInPydantic):
    song_obj = await Song.create(**song.dict(exclude_unset=True))
    return await SongPydantic.from_tortoise_orm(song_obj)


@router.get(
    "/songs/{id}",
    response_model=SongPydantic,
    status_code=200,
    summary="Get a specific song by id",
)
async def get_song(id: int = Path(..., gt=0)):
    song = await SongPydantic.from_queryset_single(Song.get(id=id))
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    return song


@router.put(
    "/songs/{id}",
    response_model=SongPydantic,
    status_code=200,
    summary="Update a specific song by id",
)
async def update_song(song: SongInPydantic, id: int = Path(..., gt=0)):
    await Song.filter(id=id).update(**song.dict(exclude_unset=True))
    song = await SongPydantic.from_queryset_single(Song.get(id=id))
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    return song


@router.delete(
    "/songs/{id}",
    response_model=Status,
    status_code=200,
    summary="Delete a specific song by id",
)
async def delete_song(
    id: int = Path(..., gt=0),
):
    deleted_count = await Song.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Song not found")
    return Status(message=f"Deleted song {id}")
