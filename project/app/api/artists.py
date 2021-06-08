from fastapi import APIRouter

from app.database.models import Artist, ArtistSchema, ArtistPayloadSchema, AristResponseSchema

router = APIRouter()


# @router.get("/artists", response_model=List[Artist_Pydantic])
# async def get_artists():
#     return await Artist_Pydantic.from_queryset(Artists.all())


@router.post("/artists", response_model=ArtistSchema, status_code=201)
async def create_artist(payload: ArtistPayloadSchema) -> AristResponseSchema:
    artist_obj = await artist_post(payload)
    return artist_obj


async def artist_post(payload:ArtistPayloadSchema):
    artist = Artist(name=payload.name, spid=payload.spid, url=payload.url, uri=payload.uri)
    artist_obj = await artist.save()
    return artist_obj


    #     artist: ArtistInsertSchema):
    # artist_obj = await Artists.create(**artist.dict(exclude_unset=True))
    # return await Artist_Pydantic.from_tortoise_orm(artist_obj)


# @router.get(
#     "/artists/{id}",
#     response_model=Artist_Pydantic,
#     status_code=200,
#     responses={404: {"model": HTTPNotFoundError}},
# )
# async def get_artist(id: int):
#     return await Artist_Pydantic.from_queryset_single(Artists.get(id=id))
#
#
# @router.put(
#     "/artists/{id}",
#     response_model=Artist_Pydantic,
#     status_code=200,
#     responses={404: {"model": HTTPNotFoundError}},
# )
# async def update_artist(id: int, artist: ArtistInsertSchema):
#     await Artists.filter(id=id).update(**artist.dict(exclude_unset=True))
#     return await Artist_Pydantic.from_queryset_single(Artists.get(id=id))
#
#
# @router.delete(
#     "/artists/{id}",
#     response_model=Status,
#     status_code=200,
#     responses={404: {"model": HTTPNotFoundError}},
# )
# async def delete_artist(id: int):
#     deleted_count = await Artists.filter(id=id).delete()
#     if not deleted_count:
#         raise HTTPException(status_code=404, detail=f"Artist {id} not found")
#     return Status(message=f"Deleted artist {id}")
