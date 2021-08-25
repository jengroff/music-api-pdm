-- upgrade --
CREATE TABLE IF NOT EXISTS "artist" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(128) NOT NULL,
    "spid" VARCHAR(128) NOT NULL,
    "uri" VARCHAR(128),
    "url" VARCHAR(128),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "playlist" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "spm_min" INT,
    "spm_max" INT,
    "spm_avg" INT,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "song" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "spid" VARCHAR(255) NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "artist" VARCHAR(255),
    "uri" VARCHAR(255),
    "tempo" DOUBLE PRECISION,
    "energy" DOUBLE PRECISION,
    "danceability" DOUBLE PRECISION,
    "acousticness" DOUBLE PRECISION,
    "instrumentalness" DOUBLE PRECISION,
    "liveness" DOUBLE PRECISION,
    "loudness" DOUBLE PRECISION,
    "speechiness" DOUBLE PRECISION,
    "valence" DOUBLE PRECISION,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(64) NOT NULL UNIQUE,
    "password_hash" VARCHAR(128) NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "playlist_song" (
    "playlist_id" INT NOT NULL REFERENCES "playlist" ("id") ON DELETE CASCADE,
    "song_id" INT NOT NULL REFERENCES "song" ("id") ON DELETE CASCADE
);
