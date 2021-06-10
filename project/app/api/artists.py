from typing import List

from fastapi import APIRouter, HTTPException, Path
from tortoise.contrib.fastapi import HTTPNotFoundError
from app.database.models import Artist, ArtistSchema, ArtistPayloadSchema, Status

router = APIRouter()


@router.get("/artists", response_model=List[ArtistSchema])
async def get_artists():
    return await ArtistSchema.from_queryset(Artist.all())


@router.post("/artists", response_model=ArtistSchema, status_code=201)
async def create_artist(artist: ArtistPayloadSchema):
    artist_obj = await Artist.create(**artist.dict(exclude_unset=True))
    return await ArtistSchema.from_tortoise_orm(artist_obj)


@router.get(
    "/artists/{id}",
    response_model=ArtistSchema,
    status_code=200,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_artist(id: int = Path(..., gt=0)):
    return await ArtistSchema.from_queryset_single(Artist.get(id=id))


@router.put("/artists/{id}", response_model=ArtistSchema, status_code=200)
async def update_artist(artist: ArtistPayloadSchema, id: int = Path(..., gt=0)):
    await Artist.filter(id=id).update(**artist.dict(exclude_unset=True))
    artist = await ArtistSchema.from_queryset_single(Artist.get(id=id))
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    return artist


@router.delete("/artists/{id}", response_model=Status, status_code=200)
async def delete_artist(id: int = Path(..., gt=0)):
    deleted_count = await Artist.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Artist not found")
    return Status(message=f"Deleted artist {id}")
