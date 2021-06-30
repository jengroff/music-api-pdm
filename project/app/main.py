import logging

from fastapi import FastAPI

from app.api import playlists, songs, artists, spot, ping, auth
from app.db import init_db

"""

The create_application() function loads each of the endpoint "groups"
(playlists, artists, songs, spotify) as separate routers, each in their
own module inside the "api" directory.

"""

log = logging.getLogger("uvicorn")

# mouunt the routes here 
def create_application() -> FastAPI:
    application = FastAPI(
        title="Everyton / Spring Music API",
        description="Built for a handsome Swedish bastard, this API "
                    "is used for creating, storing, and retrieving playlists, "
                    "songs, and artists in a PostgresQL database.",
        version = "1.0.0",
    )
    application.include_router(ping.router, tags=["Application"])
    application.include_router(playlists.router, tags=["Playlists"])
    application.include_router(songs.router, tags=["Songs"])
    application.include_router(artists.router, tags=["Artists"])
    application.include_router(auth.router, tags=["Users"])
    application.include_router(spot.router, tags=["Spotify"])

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    await init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
