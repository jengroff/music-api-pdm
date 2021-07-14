# Music API

API for managing music playlists and related assets; makes use of Spotify API but does not require it.

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
