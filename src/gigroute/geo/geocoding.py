from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError


geolocator = Nominatim(
    user_agent="gigroute-europe"
)


def geocode_city(city):
    if not city or not city.strip():
        raise ValueError(
            "City must not be empty"
        )

    try:
        location = geolocator.geocode(
            city.strip(),
            exactly_one=True,
            language="en",
        )

    except GeocoderServiceError as error:
        raise RuntimeError(
            "Geocoding service is unavailable"
        ) from error

    if location is None:
        return None

    return {
        "name": location.address,
        "latitude": location.latitude,
        "longitude": location.longitude,
    }