import datetime
import json
from typing import Optional, List, Union, Type, Any
import enum

from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields.base import Field
from pydantic import BaseModel, AnyHttpUrl


class Status(BaseModel):
    message: str


class Artist(Model):
    id = fields.IntField(pk=True, auto_now_add=True)
    name = fields.CharField(max_length=128)
    spid = fields.CharField(max_length=128)
    uri = fields.CharField(null=True, max_length=128)
    url = fields.CharField(null=True, max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)


ArtistSchema = pydantic_model_creator(Artist)


class ArtistPayloadSchema(BaseModel):
    name: str
    spid: str
    uri: Optional[str]
    url: Optional[AnyHttpUrl]


class ArtistResponseSchema(ArtistPayloadSchema):
    id: int


class Song(Model):
    """
    This references a song and all its attributes as stored in the database
    """

    id = fields.IntField(pk=True, auto_now_add=True)
    spid = fields.CharField(max_length=255)
    name = fields.CharField(max_length=255)
    artist = fields.CharField(null=True, max_length=255)
    oridur = fields.CharField(null=True, max_length=255)
    imark = fields.CharField(null=True, max_length=255)
    omark = fields.CharField(null=True, max_length=255)
    revidur = fields.CharField(null=True, max_length=255)
    uri = fields.CharField(null=True, max_length=255)
    url = fields.CharField(null=True, max_length=255)
    spm: fields.CharField(null=True, max_length=255)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)


SongSchema = pydantic_model_creator(Song)


class SongPayloadSchema(BaseModel):
    spid: str
    name: str
    artist: Optional[str]
    oridur: Optional[str]
    imark: Optional[str]
    omark: Optional[str]
    revidur: Optional[str]
    uri: Optional[str]
    url: Optional[AnyHttpUrl]
    spm: Optional[str]


class SongResponseSchema(SongPayloadSchema):
    id: int


class StrArrayField(Field, list):
    """
    String Array field specifically for PostgreSQL.
    This field can store list of str values.
    """

    SQL_TYPE = "text[]"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_db_value(
        self, value: List[str], instance: "Union[Type[Model], Model]"
    ) -> Optional[List[str]]:
        return value

    def to_python_value(self, value: Any) -> Optional[List[str]]:
        if isinstance(value, str):
            array = json.loads(value.replace("'", '"'))
            return [str(x) for x in array]
        return value


class Playlist(Model):
    id = fields.IntField(pk=True, auto_now_add=True)
    name = fields.CharField(max_length=255)
    songs = StrArrayField(null=True)
    spm_min = fields.IntField(null=True)
    spm_max = fields.IntField(null=True)
    spm_avg = fields.IntField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)


PlaylistSchema = pydantic_model_creator(Playlist)


class PlaylistPayloadSchema(BaseModel):
    name: str
    songs: Optional[List[str]]
    spm_min: Optional[int]
    spm_max: Optional[int]
    spm_avg: Optional[int]


class PlaylistResponseSchema(PlaylistPayloadSchema):
    id: int


class Role(str, enum.Enum):
    admin: str = "Admin"
    consumer: str = "Consumer"


class User(Model):
    id = fields.IntField(pk=True, auto_now_add=True)
    name = fields.CharField(max_length=255, null=True)
    email = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    role = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)


UserSchema = pydantic_model_creator(User)


class UserPayloadSchema(BaseModel):
    name: Optional[str]
    email: str
    password: str
    role: Optional[Role]


class UserResponseSchema(UserPayloadSchema):
    id: int
