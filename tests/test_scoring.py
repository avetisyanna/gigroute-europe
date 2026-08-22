import pytest

from gigroute.ranking.scoring import (
    calculate_artist_score,
    calculate_distance_score,
    calculate_genre_score,
    calculate_ranking_score,
)


def test_distance_score_half_radius():
    score = calculate_distance_score(
        distance_km=150,
        radius_km=300,
    )

    assert score == 0.5


def test_distance_score_at_radius():
    score = calculate_distance_score(
        distance_km=300,
        radius_km=300,
    )

    assert score == 0.0


def test_distance_score_invalid_radius():
    with pytest.raises(ValueError):
        calculate_distance_score(
            distance_km=100,
            radius_km=0,
        )


def test_artist_score_match():
    score = calculate_artist_score(
        artist_name="Muse",
        preferred_artists=[
            "Radiohead",
            "Muse",
        ],
    )

    assert score == 1.0


def test_artist_score_missing_artist():
    score = calculate_artist_score(
        artist_name=None,
        preferred_artists=["Muse"],
    )

    assert score == 0.0


def test_genre_score_partial_match():
    score = calculate_genre_score(
        event_genres={
            "rock",
            "pop",
        },
        preferred_genres={
            "rock",
            "jazz",
        },
    )

    assert score == 0.5


def test_ranking_score():
    score = calculate_ranking_score(
        artist_score=1.0,
        genre_score=0.5,
        distance_score=0.5,
    )

    assert score == 0.75