from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel
from typing import Optional, List, Union, Type, Any
import json
from tortoise.fields.base import Field



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


Artist_Pydantic = pydantic_model_creator(Artists)


class Playlists(Model):
    id = fields.IntField(pk=True, auto_now_add=True)
    name = fields.CharField(max_length=255)
    songs = StrArrayField(null=True)
    spm_min = fields.IntField(null=True)
    spm_max = fields.IntField(null=True)
    spm_avg = fields.IntField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)


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
    tempo: fields.IntField(null=True)
    energy: fields.IntField(null=True)
    danceability: fields.IntField(null=True)
    popularity: fields.IntField(null=True)
    spm: fields.IntField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)


Song_Pydantic = pydantic_model_creator(Songs)