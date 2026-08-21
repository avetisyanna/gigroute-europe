# GigRoute Europe 🎵

A geospatial concert discovery application for finding and ranking concerts across Europe based on music taste, location, dates, and travel preferences.

## V1

GigRoute Europe combines live concert data, artist metadata, and geospatial analysis to help users discover relevant concerts within a chosen travel radius.

### Current Features

- Ticketmaster concert data ingestion
- Data cleaning and validation
- PostgreSQL/PostGIS event storage
- Geographic radius and distance analysis
- MusicBrainz artist enrichment
- Artist entity matching
- Artist genre and tag metadata
- Explainable concert ranking based on:
  - artist preference
  - genre relevance
  - travel distance

### V1 App

The final V1 will allow users to:

- Choose a starting location
- Select a travel radius
- Set a date range
- Enter artist and genre preferences
- View ranked concert recommendations
- Explore concerts on an interactive European map

## Stack

Python · Pandas · PostgreSQL/PostGIS · Docker · SQLAlchemy · Ticketmaster API · MusicBrainz API · FastAPI · Streamlit · Plotly

## Project Workflow

Ticketmaster API  
→ Data Cleaning  
→ PostgreSQL/PostGIS  
→ Geoanalytics  
→ MusicBrainz Enrichment  
→ Artist Entity Matching  
→ Artist Metadata  
→ Concert Ranking  
→ FastAPI + Streamlit