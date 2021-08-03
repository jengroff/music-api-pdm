import logging

from fastapi import FastAPI

from app.api import playlists, songs, artists, spot, ping, auth
from app.db import init_db

"""
The create_application() function loads each of the endpoint "groups"
(playlists, artists, songs, spotify) as separate routers, each in their
own module inside the app.api directory.
"""

log = logging.getLogger("uvicorn")


# mount the routes here
def create_application() -> FastAPI:
    application = FastAPI(
        title="Spring Music API",
        description="REST API for extracting, transforming, and storing playlists, artists, songs, and related "
                    "metadata.",
        version="1.0.0",
    )
    application.include_router(ping.router, tags=["Application"])
    application.include_router(playlists.router, tags=["Playlists"])
    application.include_router(songs.router, tags=["Songs"])
    application.include_router(artists.router, tags=["Artists"])
    application.include_router(auth.router, tags=["Users"])
    application.include_router(spot.router, tags=["Spotify"])

    return application


app = create_application()

# setup
@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    await init_db(app)

# tear down
@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
