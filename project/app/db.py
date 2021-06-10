import logging
import os

from fastapi import FastAPI
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise
from dotenv import load_dotenv

log = logging.getLogger("uvicorn")

load_dotenv()
database_url = "DATABASE_URL"

# called by FastAPI on startup, from 'main'
# 'generate_schemas' is False to avoid recreating schema whenever app restarts
async def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.database.models"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )


# called through CLI -> 'docker-compose exec web python app/db.py'
async def generate_schema() -> None:
    log.info("Initializing Tortoise...")

    await Tortoise.init(
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.database.models"]},
    )
    log.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(generate_schema())
