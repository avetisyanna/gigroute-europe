from pathlib import Path

import pandas as pd


project_path = Path(__file__).resolve().parents[3]

musicbrainz_path = (
    project_path
    / "data"
    / "processed"
    / "musicbrainz"
)


def load_artist_mapping():
    mapping_file = (
        musicbrainz_path
        / "artist_mapping.csv"
    )

    return pd.read_csv(mapping_file)


def load_artist_genres():
    genres_file = (
        musicbrainz_path
        / "artist_genres.csv"
    )

    return pd.read_csv(genres_file)

def get_genres_by_mbid():
    artist_genres = load_artist_genres()

    return (
        artist_genres
        .groupby("mbid")["genre"]
        .apply(set)
        .to_dict()
    )

def enrich_events_with_artists(events_df):
    artist_mapping = load_artist_mapping()

    mapping_columns = artist_mapping[
        [
            "ticketmaster_artist_name",
            "mbid",
            "match_status",
        ]
    ].copy()

    enriched_df = events_df.merge(
        mapping_columns,
        left_on="artist_name",
        right_on="ticketmaster_artist_name",
        how="left",
    )

    genres_by_mbid = get_genres_by_mbid()

    enriched_df["genres"] = (
        enriched_df["mbid"]
        .map(genres_by_mbid)
        .apply(
            lambda genres:
            genres
            if isinstance(genres, set)
            else set()
        )
    )

    return enriched_df