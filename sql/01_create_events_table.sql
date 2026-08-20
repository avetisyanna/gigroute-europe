CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    artist_name TEXT,
    event_date DATE NOT NULL,
    event_time TIME,
    venue_name TEXT,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    event_url TEXT,
    location GEOGRAPHY(POINT, 4326),
    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE events
ADD COLUMN IF NOT EXISTS location GEOGRAPHY(POINT, 4326);

CREATE INDEX IF NOT EXISTS idx_events_location
ON events
USING GIST (location);