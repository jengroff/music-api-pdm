import json
from typing import Optional, List, Union, Type, Any

from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields.base import Field
from pydantic import BaseModel, AnyHttpUrl
from passlib.hash import bcrypt


class Status(BaseModel):
    message: str


class Artist(Model):
    id = fields.IntField(pk=True, auto_now_add=True)
    name = fields.CharField(max_length=128)
    spid = fields.CharField(max_length=128)
    uri = fields.CharField(null=True, max_length=128)
    url = fields.CharField(null=True, max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)


ArtistPydantic = pydantic_model_creator(Artist, name="Artist")
ArtistInPydantic = pydantic_model_creator(Artist, name="ArtistIn", exclude_readonly=True)


class Song(Model):
    id = fields.IntField(pk=True, auto_now_add=True)
    spid = fields.CharField(max_length=255)
    name = fields.CharField(max_length=255)
    artist = fields.CharField(null=True, max_length=255)
    uri = fields.CharField(null=True, max_length=255)
    tempo = fields.FloatField(null=True)
    energy = fields.FloatField(null=True)
    danceability = fields.FloatField(null=True)
    acousticness = fields.FloatField(null=True)
    instrumentalness = fields.FloatField(null=True)
    liveness = fields.FloatField(null=True)
    loudness = fields.FloatField(null=True)
    speechiness = fields.FloatField(null=True)
    valence = fields.FloatField(null=True)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)


SongPydantic = pydantic_model_creator(Song, name="Song")
SongInPydantic = pydantic_model_creator(Song, name="SongIn", exclude_readonly=True)


class StrArrayField(Field, list):
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
    songs = fields.ManyToManyField('models.Song', related_name='songs')
    spm_min = fields.IntField(null=True)
    spm_max = fields.IntField(null=True)
    spm_avg = fields.IntField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)


PlaylistPydantic = pydantic_model_creator(Playlist, name="Playlist")
PlaylistInPydantic = pydantic_model_creator(Playlist, name="PlaylistIn", exclude_readonly=True)

class PlaylistNamePatch(BaseModel):
    name: str

class PlaylistSongPatch(BaseModel):
    songs: List[str]


class User(Model):
    id = fields.IntField(pk=True, auto_now_add=True)
    username = fields.CharField(max_length=64, unique=True)
    password_hash = fields.CharField(max_length=128)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)


UserPydantic = pydantic_model_creator(User, name="User")
UserInPydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
