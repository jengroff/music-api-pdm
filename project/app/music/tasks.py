import os

from celery import Celery
from dotenv import load_dotenv

from app.music.features import Features
from app.mongo_db import bulk_insert_songs

load_dotenv()

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")

app = Celery('tasks',
             backend='redis://localhost',
             broker=CELERY_BROKER_URL)



@app.task
def retrieve_and_cache_song_features(artist: str):
    sf = Features(artist)
    song_features = sf.get_song_features()
    # TODO: prevent double inserts
    insert_count = bulk_insert_songs(song_features)
    print(insert_count)
    return insert_count
