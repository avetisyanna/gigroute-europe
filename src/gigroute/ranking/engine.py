from gigroute.enrichment.artists import enrich_events_with_artists
from gigroute.geo.events import get_nearby_events
from gigroute.ranking.scoring import (
    calculate_artist_score,
    calculate_distance_score,
    calculate_genre_score,
    calculate_ranking_score,
)


def rank_concerts(
    user_latitude,
    user_longitude,
    radius_km,
    start_date,
    end_date,
    preferred_artists=None,
    preferred_genres=None,
):
    preferred_artists = preferred_artists or []
    preferred_genres = preferred_genres or []

    events_df = get_nearby_events(
        user_latitude=user_latitude,
        user_longitude=user_longitude,
        radius_km=radius_km,
        start_date=start_date,
        end_date=end_date,
    )

    events_df = enrich_events_with_artists(
        events_df
    )

    events_df["artist_score"] = (
        events_df["artist_name"]
        .apply(
            lambda artist_name:
            calculate_artist_score(
                artist_name,
                preferred_artists,
            )
        )
    )

    events_df["genre_score"] = (
        events_df["genres"]
        .apply(
            lambda genres:
            calculate_genre_score(
                genres,
                preferred_genres,
            )
        )
    )

    events_df["distance_score"] = (
        events_df["distance_km"]
        .apply(
            lambda distance_km:
            calculate_distance_score(
                distance_km,
                radius_km,
            )
        )
    )

    events_df["ranking_score"] = (
        events_df.apply(
            lambda row:
            calculate_ranking_score(
                artist_score=row["artist_score"],
                genre_score=row["genre_score"],
                distance_score=row["distance_score"],
            ),
            axis=1,
        )
    )

    ranked_events = (
        events_df
        .sort_values(
            ["ranking_score", "event_date"],
            ascending=[False, True],
        )
        .reset_index(drop=True)
    )

    return ranked_events