# Music API

API for managing music playlists and related assets. 
To make use of the Spotify endpoints (and related classes & methods) you need to supply your own `SPOTIFY_CLIENT_ID` and `SPOTIFY_SECRET`. 
You can obtain them here if you're not already registered as a Spotify developer:  https://developer.spotify.com/

## Features 

- API endpoints to manage Artists, Songs, and Playlists, including POST, GET, PUT, PATCH, DELETE methods
- API endpoints for managing Users, including password encryption (bcrypt) and OAuth (JWTs)
- API endpoints for retrieving Artist and Song data from Spotify (requires Spotify API credentials)
- one API endpoint in particular deserves its own bullet -> `/spotify/artist/all ` returns a giant dictionary containing all song features for all songs of a specified artist

## Moving parts

- Python, YAML, and a couple of shell scripts
- FastAPI, Pydantic, Tortoise-ORM, and Postgres
- Docker, GitHub Actions, and Heroku
- Pytest fixtures and tests
- Black code formatting
- The included `env.sample` shows the environment variables you need to set  

# Run the app ->

## Docker (recommended):
#### Use docker-compose to build the image and run the container:
```
docker-compose up -d --build
```

## Create the database schema:
```
docker-compose exec web python app/db.py
```
    
## Run Pytest and Black: 
```
docker-compose exec web python -m pytest
```

```
docker-compose exec web black .
```

## To view the Postgres DB from the CLI:
```
docker-compose exec web-db psql -U postgres
```

## _To run the app without Docker:_

```
cd project && uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
```
## API Documentation

#### This is what your documentation should look like in Swagger / OpenAPI:

<img width="654" alt="screengrab 2021-07-19 at 3 28 31 PM" src="https://user-images.githubusercontent.com/30704684/126216181-cd06758f-6aba-438c-827b-fbb2adf2b2fc.png">
