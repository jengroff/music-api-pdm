import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")

app = Celery('tasks', broker=CELERY_BROKER_URL)


@app.task
def add(x, y):
    print(x + y)
