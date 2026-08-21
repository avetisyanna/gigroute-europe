def calculate_distance_score(distance_km, radius_km):
    if radius_km <= 0:
        raise ValueError("radius_km must be greater than 0")

    score = 1 - (distance_km / radius_km)

    return max(0.0, min(1.0, score))

def calculate_genre_score(event_genres, preferred_genres):
    if not preferred_genres:
        return 0.0

    event_genres = {
        genre.casefold()
        for genre in event_genres
    }

    preferred_genres = {
        genre.casefold()
        for genre in preferred_genres
    }

    matching_genres = event_genres & preferred_genres

    return len(matching_genres) / len(preferred_genres)

def calculate_artist_score(artist_name, preferred_artists):
    if not artist_name:
        return 0.0

    preferred_artists = {
        artist.casefold()
        for artist in preferred_artists
    }

    return float(
        artist_name.casefold() in preferred_artists
    )

def calculate_ranking_score(
    artist_score,
    genre_score,
    distance_score,
    artist_weight=0.50,
    genre_weight=0.30,
    distance_weight=0.20,
):
    total_weight = (
        artist_weight
        + genre_weight
        + distance_weight
    )

    if abs(total_weight - 1.0) > 1e-9:
        raise ValueError("Ranking weights must sum to 1")

    return (
        artist_score * artist_weight
        + genre_score * genre_weight
        + distance_score * distance_weight
    )