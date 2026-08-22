from datetime import date

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from gigroute.ranking.engine import rank_concerts
from gigroute.geo.geocoding import geocode_city


app = FastAPI(
    title="GigRoute Europe API",
    version="1.0.0",
)


class RecommendationRequest(BaseModel):
    city: str = Field(
        min_length=1,
        max_length=100,
    )

    radius_km: float = Field(
        gt=0,
        le=1000,
    )

    start_date: date
    end_date: date

    preferred_artists: list[str] = []
    preferred_genres: list[str] = []

    limit: int = Field(
        default=20,
        ge=1,
        le=100,
    )

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/recommendations")
def get_recommendations(
    request: RecommendationRequest,
):
    if request.start_date > request.end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date must be before end_date",
        )

    location = geocode_city(
        request.city
    )

    if location is None:
        raise HTTPException(
            status_code=404,
            detail="City could not be found",
        )

    ranked_events = rank_concerts(
        user_latitude=location["latitude"],
        user_longitude=location["longitude"],
        radius_km=request.radius_km,
        start_date=request.start_date,
        end_date=request.end_date,
        preferred_artists=request.preferred_artists,
        preferred_genres=request.preferred_genres,
    )

    results = ranked_events.head(
        request.limit
    ).copy()

    if results.empty:
        return {
            "count": 0,
            "recommendations": [],
        }

    results["genres"] = (
        results["genres"]
        .apply(
            lambda genres:
            sorted(genres)
            if isinstance(genres, set)
            else []
        )
    )

    output_columns = [
        "event_id",
        "event_name",
        "artist_name",
        "event_date",
        "event_time",
        "venue_name",
        "city",
        "country",
        "latitude",
        "longitude",
        "distance_km",
        "genres",
        "artist_score",
        "genre_score",
        "distance_score",
        "ranking_score",
    ]

    results = results[
        output_columns
    ].copy()

    results["event_date"] = (
        results["event_date"]
        .astype(str)
    )

    results["event_time"] = (
        results["event_time"]
        .astype(str)
    )

    results = results.astype(object).where(
        pd.notna(results),
        None,
    )

    records = results.to_dict(
        orient="records"
    )

    return {
        "location": {
            "name": location["name"],
            "latitude": location["latitude"],
            "longitude": location["longitude"],
        },
        "count": len(records),
        "recommendations": records,
    }