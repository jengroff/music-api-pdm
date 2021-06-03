import json
from typing import Optional, List, Union, Type, Any

from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields.base import Field
from pydantic import BaseModel


class StrArrayField(Field, list):
    """
    String Array field specifically for PostgreSQL.
    This field can store list of str values.
    """
    SQL_TYPE = "text[]"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_db_value(self, value: List[str], instance: "Union[Type[Model], Model]") -> Optional[List[str]]:
        return value

    def to_python_value(self, value: Any) -> Optional[List[str]]:
        if isinstance(value, str):
            array = json.loads(value.replace("'", '"'))
            return [str(x) for x in array]
        return value


class Status(BaseModel):
    message: str


class Artists(Model):
    id = fields.IntField(pk=True, auto_now_add=True)
    name = fields.CharField(max_length=255)
    spid = fields.CharField(max_length=255)
    uri = fields.CharField(null=True, max_length=255)
    url = fields.CharField(null=True, max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)


class ArtistInsertSchema(BaseModel):
    name: str
    spid: str
    uri: Optional[str] = None
    url: Optional[str] = None


Artist_Pydantic = pydantic_model_creator(Artists)


class Playlists(Model):
    id = fields.IntField(pk=True, auto_now_add=True)
    name = fields.CharField(max_length=255)
    songs = StrArrayField(null=True)
    spm_min = fields.IntField(null=True)
    spm_max = fields.IntField(null=True)
    spm_avg = fields.IntField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class PlaylistInsertSchema(BaseModel):
    name: str
    songs = str
    spm_min: Optional[int] = None
    spm_max: Optional[int] = None
    spm_avg: Optional[int] = None


Playlist_Pydantic = pydantic_model_creator(Playlists, name="Playlist")


class Songs(Model):
    """
    This references a song and all its attributes as stored in the database
    """
    spid = fields.CharField(pk=True, max_length=255)
    name = fields.CharField(max_length=255)
    artist = fields.CharField(null=True, max_length=255)
    oridur = fields.CharField(null=True, max_length=255)
    imark = fields.CharField(null=True, max_length=255)
    omark = fields.CharField(null=True, max_length=255)
    revidur = fields.CharField(null=True, max_length=255)
    uri = fields.CharField(null=True, max_length=255)
    url = fields.CharField(null=True, max_length=255)
    spempo: fields.IntField(null=True)
    spenergy: fields.IntField(null=True)
    spanceability: fields.IntField(null=True)
    spopularity: fields.IntField(null=True)
    spm: fields.IntField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class SongInsertSchema(BaseModel):
    spid: str
    name: str
    artist: Optional[str] = None
    oridur: Optional[str] = None
    imark: Optional[str] = None
    omark: Optional[str] = None
    revidur: Optional[str] = None
    uri: Optional[str] = None
    url: Optional[str] = None
    spempo: Optional[int] = None
    spenergy: Optional[int] = None
    spanceability: Optional[int] = None
    spopularity: Optional[int] = None
    spm: Optional[int] = None


Song_Pydantic = pydantic_model_creator(Songs)
