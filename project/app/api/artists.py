from typing import List

from fastapi import APIRouter, HTTPException, Path, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError
from app.database.models import Artist, ArtistPydantic, ArtistInPydantic, Status
from app.api.auth import get_current_user

router = APIRouter()


@router.get("/artists", response_model=List[ArtistPydantic], summary="Get list of all songs in the database")
async def get_artists():
    return await ArtistPydantic.from_queryset(Artist.all())


@router.post("/artists", response_model=ArtistPydantic, status_code=201,  summary="Create a new song")
async def create_artist(
    artist: ArtistInPydantic):
    artist_obj = await Artist.create(**artist.dict(exclude_unset=True))
    return await ArtistPydantic.from_tortoise_orm(artist_obj)


@router.get(
    "/artists/{id}",
    response_model=ArtistPydantic,
    status_code=200,
    responses={404: {"model": HTTPNotFoundError}}, summary="Get a specific song by id",
)
async def get_artist(id: int = Path(..., gt=0)):
    return await ArtistPydantic.from_queryset_single(Artist.get(id=id))


@router.put("/artists/{id}", response_model=ArtistPydantic, status_code=200, summary="Update a specific song by id")
async def update_artist(
    artist: ArtistInPydantic,
    id: int = Path(..., gt=0)):
    await Artist.filter(id=id).update(**artist.dict(exclude_unset=True))
    artist = await ArtistPydantic.from_queryset_single(Artist.get(id=id))
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    return artist


@router.delete("/artists/{id}", response_model=Status, status_code=200, summary="Delete a specific song by id")
async def delete_artist(
    id: int = Path(..., gt=0)):
    deleted_count = await Artist.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Artist not found")
    return Status(message=f"Deleted artist {id}")
