from typing import List

from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError

from app.database.models import Artist_Pydantic, Artists, ArtistInsertSchema
from app.database.models import Status

router = APIRouter()


@router.get("/artists", response_model=List[Artist_Pydantic])
async def get_artists():
    return await Artist_Pydantic.from_queryset(Artists.all())


@router.post("/artists", response_model=Artist_Pydantic, status_code=201)
async def create_artist(artist: ArtistInsertSchema):
    artist_obj = await Artists.create(**artist.dict(exclude_unset=True))
    return await Artist_Pydantic.from_tortoise_orm(artist_obj)


@router.get(
    "/artists/{id}",
    response_model=Artist_Pydantic,
    status_code=200,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_artist(id: int):
    return await Artist_Pydantic.from_queryset_single(Artists.get(id=id))


@router.put(
    "/artists/{id}",
    response_model=Artist_Pydantic,
    status_code=200,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_artist(id: int, artist: ArtistInsertSchema):
    await Artists.filter(id=id).update(**artist.dict(exclude_unset=True))
    return await Artist_Pydantic.from_queryset_single(Artists.get(id=id))


@router.delete(
    "/artists/{id}",
    response_model=Status,
    status_code=200,
    responses={404: {"model": HTTPNotFoundError}},
)
async def delete_artist(id: int):
    deleted_count = await Artists.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Artist {id} not found")
    return Status(message=f"Deleted artist {id}")
