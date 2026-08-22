from datetime import date

import requests
import streamlit as st
import pandas as pd
import plotly.express as px


API_URL = "http://127.0.0.1:8000"


def parse_comma_separated_values(value):
    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]


st.set_page_config(
    page_title="GigRoute Europe",
    page_icon="🎵",
    layout="wide",
)


st.title("GigRoute Europe 🎵")

st.write(
    "Discover concerts based on your location, "
    "travel radius, dates, and music preferences."
)


st.subheader("Search Preferences")


col1, col2 = st.columns(2)


with col1:
    latitude = st.number_input(
        "Latitude",
        min_value=-90.0,
        max_value=90.0,
        value=52.5200,
        format="%.4f",
    )

    radius_km = st.slider(
        "Travel radius (km)",
        min_value=10,
        max_value=1000,
        value=300,
        step=10,
    )

    start_date = st.date_input(
        "Start date",
        value=date(2026, 8, 21),
    )


with col2:
    longitude = st.number_input(
        "Longitude",
        min_value=-180.0,
        max_value=180.0,
        value=13.4050,
        format="%.4f",
    )

    end_date = st.date_input(
        "End date",
        value=date(2027, 2, 28),
    )

    limit = st.slider(
        "Number of recommendations",
        min_value=5,
        max_value=100,
        value=20,
        step=5,
    )


preferred_artists_text = st.text_input(
    "Preferred artists",
    placeholder="Muse, Austria, Radiohead",
)

preferred_genres_text = st.text_input(
    "Preferred genres",
    placeholder="rock, electronic, pop",
)


if st.button(
    "Find Concerts",
    type="primary",
):
    if start_date > end_date:
        st.error(
            "Start date must be before end date."
        )
        st.stop()

    preferred_artists = (
        parse_comma_separated_values(
            preferred_artists_text
        )
    )

    preferred_genres = (
        parse_comma_separated_values(
            preferred_genres_text
        )
    )

    payload = {
        "user_latitude": latitude,
        "user_longitude": longitude,
        "radius_km": radius_km,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "preferred_artists": preferred_artists,
        "preferred_genres": preferred_genres,
        "limit": limit,
    }

    try:
        with st.spinner(
            "Finding concerts..."
        ):
            response = requests.post(
                f"{API_URL}/recommendations",
                json=payload,
                timeout=30,
            )

        response.raise_for_status()
        data = response.json()

    except requests.RequestException as error:
        st.error(
            f"Could not connect to the API: {error}"
        )
        st.stop()

    recommendations = data.get(
        "recommendations",
        [],
    )

    if not recommendations:
        st.warning(
            "No concerts found for these preferences."
        )
        st.stop()

    st.success(
        f"Found {len(recommendations)} recommendations."
    )

    map_df = pd.DataFrame(
        recommendations
    )

    map_df = map_df.dropna(
        subset=[
            "latitude",
            "longitude",
        ]
    )

    if not map_df.empty:
        st.subheader(
            "Concert Map"
        )

        fig = px.scatter_map(
            map_df,
            lat="latitude",
            lon="longitude",
            hover_name="event_name",
            hover_data={
                "artist_name": True,
                "city": True,
                "venue_name": True,
                "event_date": True,
                "distance_km": ":.1f",
                "ranking_score": ":.2f",
                "latitude": False,
                "longitude": False,
            },
            size="ranking_score",
            center={
                "lat": latitude,
                "lon": longitude,
            },
            zoom=4,
            height=550,
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )
    
    st.subheader(
        "Recommended Concerts"
    )

    for index, event in enumerate(
        recommendations,
        start=1,
    ):
        with st.container(
            border=True
        ):
            st.markdown(
                f"### {index}. "
                f"{event.get('event_name', 'Unknown Event')}"
            )

            st.write(
                f"**Artist:** "
                f"{event.get('artist_name') or 'Unknown'}"
            )

            city = (
                event.get("city")
                or "Unknown city"
            )

            country = (
                event.get("country")
                or "Unknown country"
            )

            st.write(
                f"**Location:** "
                f"{city}, {country}"
            )

            st.write(
                f"**Venue:** "
                f"{event.get('venue_name') or 'Unknown'}"
            )

            st.write(
                f"**Date:** "
                f"{event.get('event_date') or 'Unknown'}"
            )

            event_time = event.get(
                "event_time"
            )

            if (
                event_time
                and event_time != "None"
                and event_time != "NaT"
            ):
                st.write(
                    f"**Time:** {event_time}"
                )

            distance_km = event.get(
                "distance_km"
            )

            if distance_km is not None:
                st.write(
                    f"**Distance:** "
                    f"{distance_km:.1f} km"
                )

            genres = event.get(
                "genres",
                [],
            )

            if genres:
                st.write(
                    "**Genres:** "
                    + ", ".join(genres)
                )

            ranking_score = event.get(
                "ranking_score"
            )

            if ranking_score is not None:
                st.write(
                    f"**Match score:** "
                    f"{ranking_score:.2f}"
                )