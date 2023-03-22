import os
from typing import Union

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"),
                     connectTimeoutMS=200,
                     retryWrites=True)
db = client.music_library
songs = db.songs

Song = dict[str, Union[float, str, int]]
ArtistSongs = list[Song]


def bulk_insert_songs(song_features: ArtistSongs) -> int:
    """Inserts a list of song features into the songs collection"""
    songs.insert_many(song_features)
    return songs.count_documents({})


def retrieve_song_features(artist: str) -> list[Song]:
    song_features = songs.find({"artist": artist})
    return song_features


if __name__ == "__main__":
    from app.music.features import Features
    sf = Features("Pharcyde")
    song_features = sf.get_song_features()
    insert_count = bulk_insert_songs(song_features)
    print(insert_count)
