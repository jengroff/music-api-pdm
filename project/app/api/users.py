from typing import List

from fastapi import APIRouter, HTTPException, Path
from tortoise.contrib.fastapi import HTTPNotFoundError
from app.database.models import User, UserPayloadSchema, Status, UserSchema

router = APIRouter()


@router.get("/users", response_model=List[UserSchema])
async def get_users():
    return await UserSchema.from_queryset(User.all())


@router.post("/users", response_model=UserSchema, status_code=201)
async def create_user(user: UserPayloadSchema):
    user_obj = await User.create(**user.dict(exclude_unset=True))
    return await UserSchema.from_tortoise_orm(user_obj)


@router.get(
    "/users/{id}",
    response_model=UserSchema,
    status_code=200,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_user(id: int = Path(..., gt=0)):
    return await UserSchema.from_queryset_single(User.get(id=id))


@router.put("/users/{id}", response_model=UserSchema, status_code=200)
async def update_user(user: UserPayloadSchema, id: int = Path(..., gt=0)):
    await User.filter(id=id).update(**user.dict(exclude_unset=True))
    user = await UserSchema.from_queryset_single(User.get(id=id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.delete("/users/{id}", response_model=Status, status_code=200)
async def delete_user(id: int = Path(..., gt=0)):
    deleted_count = await User.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User not found")
    return Status(message=f"Deleted user {id}")
