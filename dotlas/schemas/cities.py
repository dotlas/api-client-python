from pydantic import BaseModel, validator
from typing import List, Union, Dict


class ReverseGeocodeEndpointResponse(BaseModel):
    class ReverseGeocodeRequest(BaseModel):
        latitude: float
        longitude: float

        @validator("latitude")
        def latitude_validation(cls, latitude):
            if not -90 <= latitude <= 90:
                raise ValueError("Invalid Coordinate Inputs")
            return latitude

        @validator("longitude")
        def longitude_validation(cls, longitude):
            if not -180 <= longitude <= 180:
                raise ValueError("Invalid Coordinate Inputs")
            return longitude

    class ReverseGeocodeResponse(BaseModel):
        nbd_name: str = None
        place_code: str = None
        place_name: str = None
        place_name_complete: str = None
        urban_area_name: str = None
        urban_area_name_complete: str = None
        county_geo_id: str
        county_name: str
        county_name_complete: str
        state_code: str
        state_name: str
        state_postcode: str
        county_code: str

    request: ReverseGeocodeRequest
    response: ReverseGeocodeResponse
