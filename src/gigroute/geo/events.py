import pandas as pd
from sqlalchemy import text

from gigroute.database.connection import get_database_engine


def get_nearby_events(
    user_latitude,
    user_longitude,
    radius_km,
    start_date,
    end_date,
):
    if radius_km <= 0:
        raise ValueError("radius_km must be greater than 0")

    engine = get_database_engine()

    query = text("""
        SELECT
            event_id,
            event_name,
            artist_name,
            event_date,
            event_time,
            venue_name,
            city,
            country,
            latitude,
            longitude,
            ST_Distance(
                location,
                ST_SetSRID(
                    ST_MakePoint(
                        :user_longitude,
                        :user_latitude
                    ),
                    4326
                )::geography
            ) / 1000 AS distance_km
        FROM events
        WHERE event_date BETWEEN :start_date AND :end_date
          AND ST_DWithin(
                location,
                ST_SetSRID(
                    ST_MakePoint(
                        :user_longitude,
                        :user_latitude
                    ),
                    4326
                )::geography,
                :radius_meters
          )
        ORDER BY event_date;
    """)

    events_df = pd.read_sql(
        query,
        engine,
        params={
            "user_latitude": user_latitude,
            "user_longitude": user_longitude,
            "radius_meters": radius_km * 1000,
            "start_date": start_date,
            "end_date": end_date,
        },
    )

    return events_df