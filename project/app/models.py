from pydantic import BaseModel
from typing import Optional, List, Union, Type, Any
import json
from tortoise.fields.base import Field
from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


"""
This module defines the Tortoise and Pydantic classes used for all endpoints.
For each Tortoise class definition, a Pydantic equivalent is generated 
using the pydantic_model_creator function. 

"""

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


class Songs(Model):
    """
    This references a song and all its attributes as stored in the database
    """
    spid = fields.CharField(pk=True)
    name = fields.CharField()
    artist = fields.CharField(null=True)
    oridur = fields.CharField(null=True)
    imark = fields.CharField(null=True)
    omark = fields.CharField(null=True)
    revidur = fields.CharField(null=True)
    uri = fields.CharField(null=True)
    url = fields.CharField(null=True)
    tempo: fields.IntField(null=True)
    energy: fields.IntField(null=True)
    danceability: fields.IntField(null=True)
    popularity: fields.IntField(null=True)
    spm: fields.IntField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class SongInsertSchema(BaseModel):
    """
    This references the user-defined attributes of a song
    """
    spid: str
    name: str
    artist: Optional[str] = None
    oridur: Optional[str] = None
    imark: Optional[str] = None
    omark: Optional[str] = None
    revidur: Optional[str] = None
    uri: Optional[str] = None
    url: Optional[str] = None
    sp_tempo: Optional[int] = None
    sp_energy: Optional[int] = None
    sp_danceability: Optional[int] = None
    sp_popularity: Optional[int] = None
    spm: Optional[int] = None


Song_Pydantic = pydantic_model_creator(Songs)


class Playlists(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField()
    songs = StrArrayField(null=True)
    spm_min = fields.IntField(null=True)
    spm_max = fields.IntField(null=True)
    spm_avg = fields.IntField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class PlaylistInsertSchema(BaseModel):
    name: str
    songs: Optional[List[str]]
    spm_min: Optional[int] = None
    spm_max: Optional[int] = None
    spm_avg: Optional[int] = None


Playlist_Pydantic = pydantic_model_creator(Playlists, name="Playlist")


class Artists(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField()
    spid = fields.CharField()
    uri = fields.CharField(null=True)
    url = fields.CharField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class ArtistInsertSchema(BaseModel):
    name: str
    spid: str
    uri: Optional[str] = None
    url: Optional[str] = None


Artist_Pydantic = pydantic_model_creator(Artists)
