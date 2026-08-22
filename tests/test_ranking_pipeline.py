from gigroute.ranking.engine import rank_concerts


def test_ranking_pipeline():
    results = rank_concerts(
        user_latitude=52.5200,
        user_longitude=13.4050,
        radius_km=300,
        start_date="2026-08-21",
        end_date="2027-02-28",
        preferred_artists=["Austria"],
        preferred_genres=["electronic"],
    )

    assert not results.empty

    assert results["ranking_score"].notna().all()

    assert results["ranking_score"].between(
        0,
        1,
    ).all()

    assert results[
        "ranking_score"
    ].is_monotonic_decreasing

    assert (
        results["distance_km"] <= 300
    ).all()