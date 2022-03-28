from multiprocessing.sharedctypes import Value
from pydantic import BaseModel, ValidationError, validator
from typing import List, Union

coordinate_valid = (
    lambda latitude, longitude: True
    if -90 <= latitude <= 90 and -180 <= longitude <= 180
    else False
)


class SocioDemographicsCityResponse(BaseModel):
    average_individual_income: float = None
    median_household_income: float = None
    population_total: int = None
    population_youth: int = None
    population_middle_age: int = None
    population_senior: int = None
    work_transportation_self_mobility: int = None
    household_income_low: int = None
    household_income_medium: int = None
    household_income_high: int = None
    households_total: int = None
    households_family_total: int = None
    average_household_composition: float = None


class GeometryModel(BaseModel):
    type: str = "Polygon"
    coordinates: list


class GeojsonSpec(BaseModel):
    class GeometryFeature(BaseModel):
        type: str = "Polygon"
        properties: dict = None
        geometry: GeometryModel

    type: str = "FeatureCollection"
    features: List[GeometryFeature]


class GeneralStatisitcal(BaseModel):
    value: float = None
    city: float = None
    share: float = None


class SocioDemographicResponse(BaseModel):
    class Demographics(BaseModel):
        class PopulationAffluence(BaseModel):
            low_median_household_income: GeneralStatisitcal = None
            medium_median_household_income: GeneralStatisitcal = None
            high_median_household_income: GeneralStatisitcal = None

        total_population: GeneralStatisitcal = None
        youth_population: GeneralStatisitcal = None
        middle_aged_population: GeneralStatisitcal = None
        senior_population: GeneralStatisitcal = None
        self_mobilizing_population: GeneralStatisitcal = None
        population_affluence: PopulationAffluence = None

    class Income(BaseModel):
        class IncomeStatistical(BaseModel):
            avg: GeneralStatisitcal = None
            median: GeneralStatisitcal = None

        household: IncomeStatistical = None
        individual: IncomeStatistical = None

    class HouseholdComposition(BaseModel):
        household_count: GeneralStatisitcal = None
        households_with_family_count: GeneralStatisitcal = None
        avg_persons_per_household: GeneralStatisitcal = None

    demographics: Demographics = None
    income: Income = None
    household_composition: HouseholdComposition = None


class SalesTerritoryRequest(BaseModel):
    latitude: float
    longitude: float
    city: str
    mode_of_mobility: str = None
    time_minutes: int = None
    distance_meters: int = None

    time_minutes_valid = lambda time_minutes: True if 1 <= time_minutes <= 60 else False
    distance_meters_valid = (
        lambda distance_meters: True if 1 <= distance_meters <= 10_000 else False
    )
    mode_of_mobility_valid = lambda mode_of_mobility: mode_of_mobility in (
        "driving",
        "walking",
    )

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

    @validator("time_minutes")
    def time_minutes_validation(cls, time_minutes):
        if time_minutes and not cls.time_minutes_valid(time_minutes):
            raise ValueError("time_minutes parameter not in range 1-60")
        return time_minutes

    @validator("distance_meters")
    def distance_meters_validation(cls, distance_meters):
        if distance_meters and not cls.distance_meters_valid(distance_meters):
            raise ValueError("distance_meters parameter not in range 1-10,000")
        return distance_meters

    @validator("mode_of_mobility")
    def mode_of_mobility_validation(cls, mode_of_mobility):
        if mode_of_mobility and not cls.mode_of_mobility_valid(mode_of_mobility):
            raise ValueError(
                "mode_of_mobility parameter invalid. Must be one of driving, walking"
            )
        return mode_of_mobility


class SalesTerritoryResponse(BaseModel):
    sociodemographic: SocioDemographicResponse = None
    areas_covered: List[str] = None
    geometry: GeojsonSpec = None


class AreaResponse(SalesTerritoryResponse):
    pass


class SalesTerritoryEndpointResponse(BaseModel):
    request: SalesTerritoryRequest = None
    response: SalesTerritoryResponse = None


class SalesTerritoryCompareCandidatesEndpointResponse(BaseModel):
    class SalesTerritoryCompareCandidatesRequest(BaseModel):
        candidates: List[SalesTerritoryRequest]

    request: SalesTerritoryCompareCandidatesRequest
    response: SalesTerritoryResponse


class SalesTerritoryCompareGeojsonEndpointResponse(BaseModel):
    class SalesTerritoryCompareGeojsonRequest(BaseModel):
        geojson: GeojsonSpec
        city: str

    request: SalesTerritoryCompareGeojsonRequest
    response: SalesTerritoryResponse


class SalesTerritoryCompareGeometriesEndpointResponse(BaseModel):
    class SalesTerritoryCompareGeometriesRequest(BaseModel):
        geometries: List[GeometryModel]
        city: str

    request: SalesTerritoryCompareGeometriesRequest
    response: SalesTerritoryResponse
