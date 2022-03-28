import requests

from typing import List, Dict, Union

from dotlas.schemas.cities import ReverseGeocodeEndpointResponse
from dotlas.schemas.sociodemographics import (
    AreaResponse,
    GeojsonSpec,
    SalesTerritoryRequest,
    SocioDemographicsCityResponse,
    SalesTerritoryEndpointResponse,
)
from dotlas.schemas.competition import (
    AreaInsightsEndpointResponse,
    BrandInsightsEndpointResponse,
    CategoryInsightsEndpointResponse,
    CompetitionEndpointResponse,
    GenericInsightsRequests,
)


class App:
    def __init__(self, api_key: str):
        """Create a Dotlas App with integration to the API using the provided API key.
        API Docs: https://api.dotlas.com/docs

        Args:
            api_key (str): The API Key to use for all requests. To get an API Key, visit dotlas.com or email us at info@dotlas.com
        """
        self.api_key: str = api_key

        self.__base_url: str = "https://api.dotlas.com"
        self.__sociodemographics_url: str = f"{self.__base_url}/socio-demographics"
        self.__competition_url: str = f"{self.__base_url}/competition"
        self.__cities_url: str = f"{self.__base_url}/cities"

        self.__params = {"api_key": self.api_key}
        self.__headers: Dict[str, str] = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": self.api_key,
        }

    def __generic_fetch(
        self, url: str, params: dict, request_type: str = "GET"
    ) -> dict:
        """A generic requests client to fetch data from API

        Args:
            url (str): The URL to fetch data from. Endpoints.
            params (dict): The parameters to pass to the endpoint.
            request_type (str, optional): The type of HTTP request (GET/POST/PUT). Defaults to "GET".

        Raises:
            ValueError: (HTTP Exception) If the request type is not a valid HTTP request type.
            ValueError: (404) If the data required is missing
            ValueError: (422) If the request data is invalid
            ValueError: (403) If the API key is invalid

        Returns:
            dict: The response from the endpoint in JSON format
        """
        try:
            response = requests.request(
                request_type, url, params=params, headers=self.__headers
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                raise ValueError(f"{response.status_code}: {response.json()}")
            elif response.status_code == 422:
                raise ValueError("Validation Error - Check params or body")
            elif response.status_code == 403:
                raise ValueError("Invalid API Key")

            response.raise_for_status()

        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            requests.exceptions.RequestException,
        ) as e:
            raise ValueError(f"Unable to fetch response: {e}")

    def list_commercial_types(self) -> List[str]:
        """List all available commercial types.
        A commercial type is a type of industry, such as retail, restaurants, gyms etc.

        Returns:
            List[str]: A list of commercial types acceptable by the API.
        """
        url = f"{self.__competition_url}/types"
        return self.__generic_fetch(url=url, params=self.__params)

    def list_cities(self) -> List[str]:
        """List all cities supported by the API.

        Returns:
            List[str]: A list of cities supported by the API.
        """
        url = self.__cities_url
        return self.__generic_fetch(url=url, params=self.__params)

    def list_places_in_city(self, city: str) -> List[str]:
        """Takes in a city and returns the list of places (sub-areas) within a city.
        Ex: Burbank, Beverly Hills are example of `places` in the city / urban area of Los Angeles.
        These don't qualify as areas or neighborhoods.

        Args:
            city (str): The city to list places in.

        Returns:
            List[str]: A list of places in the city.
        """
        url: str = f"{self.__cities_url}/places/{city}"
        return self.__generic_fetch(url=url, params=self.__params)

    def list_areas_in_city(self, city: str) -> List[str]:
        """Takes in a city and returns the list of areas (neighborhoods) within a city.
        Ex: Financial District, Upper West Side are example of `areas` in the city / urban area of New York.

        Args:
            city (str): The city to list areas in.

        Returns:
            List[str]: A list of areas in the city.
        """
        url: str = f"{self.__cities_url}/areas/{city}"
        return self.__generic_fetch(url=url, params=self.__params)

    def list_commercial_brands(self, city: str, commercial_type: str) -> List[str]:
        """Takes in a `city` and a `commercial_type` returns a set of all brands of `commercial_type` within the city.
        A brand is a chain / group of businesses that are part of the same industry. Ex: Pizza Hut / Starbucks

        Args:
            city (str): The city to list brands in.
            commercial_type (str): The commercial type to list brands in.

        Returns:
            List[str]: A list of distinct brands in the city.
        """
        url = f"{self.__competition_url}/brands/{city}/{commercial_type}"
        return self.__generic_fetch(url=url, params=self.__params)

    def list_commercial_categories(self, city: str, commercial_type: str) -> List[str]:
        """Takes in a `city` and a `commercial_type` returns a set of all categories of `commercial_type`
        within the city ordered by most number of locations. A category is a class tag assigned to a location.
        Examples for Restaurants: Italian / American / Fast Food / Pizza / Chinese / Japanese / Thai / Indian

        Args:
            city (str): The city to list categories in.
            commercial_type (str): The commercial type to list categories in.

        Returns:
            List[str]: A list of distinct categories in the city.
        """
        url = f"{self.__competition_url}/categories/{city}/{commercial_type}"
        return self.__generic_fetch(url=url, params=self.__params)

    def city_stats(self, city: str) -> SocioDemographicsCityResponse:
        """Takes in a city and returns the summarized (and averaged) statistics on
        demographics, income, household composition, and racial information.
        Can be used to summarize the overall population profile of a city.

        Args:
            city (str): The city to get stats for.

        Returns:
            SocioDemographicsCityResponse: A SocioDemographicsCityResponse object containing the city stats.
        """
        url = f"{self.__sociodemographics_url}/stats/{city}"
        return SocioDemographicsCityResponse(
            self.__generic_fetch(url=url, params=self.__params)
        )

    def area_stats(self, city: str, area: str) -> AreaResponse:
        """Takes in a city and area and returns the summarized (and averaged) statistics on
        demographics, income, household composition, and racial information for the area.
        Useful for qualifying population profiles within specific neighborhoods or administrative areas.

        Args:
            city (str): The city to get area level stats for.
            area (str): The area in the city to get area level stats for.

        Returns:
            AreaResponse: AreaResponse object containing the area stats.
        """
        url = f"{self.__sociodemographics_url}/stats/{city}/{area}"
        area_stats_response = self.__generic_fetch(url=url, params=self.__params)
        return AreaResponse(
            sociodemographic=area_stats_response["sociodemographic"],
            areas_covered=area_stats_response["areas_covered"],
            geometry=area_stats_response["geometry"],
        )

    def sales_territory(
        self,
        latitude: float,
        longitude: float,
        city: str,
        mode_of_mobility: str = "driving",
        time_minutes: int = None,
        distance_meters: int = None,
    ) -> SalesTerritoryEndpointResponse:
        """Takes in a coordinate point, the city where the point is located and the
        [isochrone](https://en.wikipedia.org/wiki/Isochrone_map) parameters.
        Either one of `time_minutes` or `distance_meters` must be specified.
        The `mode_of_mobility` parameter is optional for `distance_meters` and defaults to `driving`.
        If `mode_of_mobility` is set to NULL with `distance_meters`, the sales territory will be a circular radius.
        Returns the isochrone populated with the relevant sales territory statistics valid within the isochrone area.

        Args:
            latitude (float): The latitude of the coordinate point.
            longitude (float): The longitude of the coordinate point.
            city (str): The city where the coordinate point is located.
            mode_of_mobility (str, optional): The mode of mobility used to derive sales territory Can be walking / driving. Defaults to driving.
            time_minutes (int, optional): The time in minutes within `mode_of_mobility` to traverse. Defaults to None.
            distance_meters (int, optional): The distance in meters to consider for radius / `mode_of_mobility` traversal. Defaults to None.

        Raises:
            ValueError: `mode_of_mobility`: Required for `time_minutes`
            ValueError: `isochrone`: Must be one of either optional parameters `time_minutes` or `distance_meters`

        Returns:
            SalesTerritoryEndpointResponse: SalesTerritoryEndpointResponse object containing the sales territory stats.
        """

        if not any([time_minutes, distance_meters]):
            raise ValueError(
                "Either time_minutes or distance_meters parameters must be specified"
            )

        SalesTerritoryRequest(
            latitude=latitude,
            longitude=longitude,
            city=city,
            mode_of_mobility=mode_of_mobility,
            time_minutes=time_minutes,
            distance_meters=distance_meters,
        )
        url: str = None
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "city": city,
            "mode_of_mobility": mode_of_mobility,
        }

        if time_minutes:
            if not mode_of_mobility:
                raise ValueError(
                    "`Mode of Mobility` parameter must be provided for time-based \
                    sales territory derivation"
                )
            url = f"{self.__sociodemographics_url}/sales_territory/time"
            params["time_minutes"] = time_minutes

        elif distance_meters:
            url = f"{self.__sociodemographics_url}/sales_territory/distance"
            params["distance_meters"] = distance_meters

        sales_territory_response = self.__generic_fetch(url=url, params=params)
        return SalesTerritoryEndpointResponse(
            request=sales_territory_response["request"],
            response=sales_territory_response["response"],
        )

    def nearby_competition(
        self,
        latitude: float,
        longitude: float,
        city: str,
        commercial_type: str,
        radius_meters: int = 500,
        brand_filters: List[str] = None,
        category_filters: List[str] = None,
    ) -> CompetitionEndpointResponse:
        """Takes in a coordinate point, the city where the point is located, the search radius and filters (brands and categories).
        Returns a set of statistics and data for all locations within the search radius that satisfy the `commercial_type`.

        Args:
            latitude (float): The latitude of the coordinate point.
            longitude (float): The longitude of the coordinate point.
            city (str): The city where the coordinate point is located.
            commercial_type (str): The commercial type to search for.
            radius_meters (int): The circular radius distance (in meters) to take from the coordinates. Defaults to 500.
            brand_filters (List[str], optional): Filter for locations of specific brands in the radius. Defaults to None.
            category_filters (List[str], optional): Filter for locations with specific category tags in the radius. Defaults to None.

        Returns:
            CompetitionEndpointResponse: CompetitionEndpointResponse object containing the competition stats.
        """

        CompetitionEndpointResponse.CompetitionRequest(
            latitude=latitude,
            longitude=longitude,
            city=city,
            commercial_type=commercial_type,
            radius_meters=radius_meters,
            brand_filters=brand_filters,
            category_filters=category_filters,
        )
        url: str = f"{self.__competition_url}/nearby/{commercial_type}"
        params: dict = {
            "latitude": latitude,
            "longitude": longitude,
            "city": city,
            "radius_meters": radius_meters,
            "brand_filters": brand_filters,
            "category_filters": category_filters,
        }
        nearby_competition_response = self.__generic_fetch(url=url, params=params)
        return CompetitionEndpointResponse(
            request=nearby_competition_response["request"],
            response=nearby_competition_response["response"],
        )

    def category_insights(
        self,
        city: str,
        commercial_type: str,
        categories: List[str] = None,
        price_range: int = None,
    ) -> CategoryInsightsEndpointResponse:
        """A function that returns a set of aggregated insights on the locations in a city at a categorical level.
        Takes in a `city` parameter along with optional filters for `categories` and `price range`.
        Returns a comprehensive list of insights for the city for `commercial_type` taking categories as the threshold.

        Args:
            city (str): The city to retrieve category insights for.
            commercial_type (str): The commercial type to search for.
            categories (List[str], optional): Filter for locations with specific category tags in the radius. Defaults to None.
            price_range (int, optional): Filter for locations with specific set of price ranges. Defaults to None.

        Returns:
            CategoryInsightsEndpointResponse: CategoryInsightsEndpointResponse object containing the category insights.
        """
        GenericInsightsRequests(
            city=city,
            commercial_type=commercial_type,
            categories=categories,
            price_range=price_range,
        )
        url: str = (
            f"{self.__competition_url}/insights/categories/{city}/{commercial_type}"
        )
        params: dict = {}
        if categories:
            params["categories"] = categories
        if price_range:
            params["price_range"] = price_range

        category_insights_response = self.__generic_fetch(
            url=url, params=params if params else self.__params
        )
        return CategoryInsightsEndpointResponse(
            request=category_insights_response["request"],
            response=category_insights_response["response"],
        )

    def brand_insights(
        self,
        city: str,
        commercial_type: str,
        categories: List[str] = None,
        price_range: int = None,
    ) -> BrandInsightsEndpointResponse:
        """A function that returns a set of aggregated insights on the locations in a city at a brand level.
        Takes in a `city` parameter along with optional filters for `categories` and `price range`.
        Returns a comprehensive list of insights for the city for `commercial_type` taking brands of locations as the threshold.

        Args:
            city (str): The city to retrieve category insights for.
            commercial_type (str): The commercial type to search for.
            categories (List[str], optional): Filter for locations with specific category tags in the radius. Defaults to None.
            price_range (int, optional): Filter for locations with specific set of price ranges. Defaults to None.

        Returns:
            BrandInsightsEndpointResponse: BrandInsightsEndpointResponse object containing the category insights.
        """
        GenericInsightsRequests(
            city=city,
            commercial_type=commercial_type,
            categories=categories,
            price_range=price_range,
        )
        url: str = f"{self.__competition_url}/insights/brands/{city}/{commercial_type}"
        params: dict = {}
        if categories:
            params["categories"] = categories
        if price_range:
            params["price_range"] = price_range

        brand_insights_response: dict = self.__generic_fetch(
            url=url, params=params if params else self.__params
        )
        return BrandInsightsEndpointResponse(
            request=brand_insights_response["request"],
            response=brand_insights_response["response"],
        )

    def area_insights(
        self,
        city: str,
        commercial_type: str,
        categories: List[str] = None,
        price_range: int = None,
    ) -> AreaInsightsEndpointResponse:
        """A function that returns a set of aggregated insights on the locations in a city at an area level.
        Areas could be streets, neighbourhoods or postcodes.
        Takes in a `city` parameter along with optional filters for `categories` and `price range`.
        Returns a comprehensive list of insights for the city for `commercial_type` taking brands of areas as the threshold.

        Args:
            city (str): The city to retrieve category insights for.
            commercial_type (str): The commercial type to search for.
            categories (List[str], optional): Filter for locations with specific category tags in the radius. Defaults to None.
            price_range (int, optional): Filter for locations with specific set of price ranges. Defaults to None.

        Returns:
            AreaInsightsEndpointResponse: AreaInsightsEndpointResponse object containing the category insights.
        """
        GenericInsightsRequests(
            city=city,
            commercial_type=commercial_type,
            categories=categories,
            price_range=price_range,
        )
        url: str = f"{self.__competition_url}/insights/areas/{city}/{commercial_type}"
        params: dict = {}
        if categories:
            params["categories"] = categories
        if price_range:
            params["price_range"] = price_range

        area_insights_response: dict = self.__generic_fetch(
            url=url, params=params if params else self.__params
        )
        return AreaInsightsEndpointResponse(
            request=area_insights_response["request"],
            response=area_insights_response["response"],
        )

    def reverse_geocode(
        self, latitude: float, longitude: float
    ) -> ReverseGeocodeEndpointResponse:
        ReverseGeocodeEndpointResponse.ReverseGeocodeRequest(
            latitude=latitude, longitude=longitude
        )
        url: str = f"{self.__cities_url}/reverse_geocode"
        params: dict = {"latitude": latitude, "longitude": longitude}

        reverse_geocode_response: dict = self.__generic_fetch(url=url, params=params)
        return ReverseGeocodeEndpointResponse(
            request=reverse_geocode_response["request"],
            response=reverse_geocode_response["response"],
        )

    def city_boundary(self, city: str) -> GeojsonSpec:
        """A function that returns the boundary of a city in GeoJSON format.

        Args:
            city (str): The city to retrieve the boundary for.

        Returns:
            GeojsonSpec: GeoJSON object containing the boundary of the city.
        """
        url: str = f"{self.__cities_url}/boundary/{city}"
        return GeojsonSpec(self.__generic_fetch(url=url, params=self.__params))

    def place_boundary(self, city: str, place: str) -> GeojsonSpec:
        """A function that returns the boundary of a place in GeoJSON format.

        Args:
            city (str): The city containing the place.
            place (str): The place in the city to retrieve the boundary for.

        Returns:
            GeojsonSpec: GeoJSON object containing the boundary of the place.
        """
        url: str = f"{self.__cities_url}/places/boundary/{city}/{place}"
        return GeojsonSpec(self.__generic_fetch(url=url, params=self.__params))

    def area_boundary(self, city: str, area: str) -> GeojsonSpec:
        """A function that returns the boundary of an area in GeoJSON format.

        Args:
            city (str): The city containing the area.
            area (str): The area in the city to retrieve the boundary for.

        Returns:
            GeojsonSpec: _description_
        """
        url: str = f"{self.__cities_url}/areas/boundary/{city}/{area}"
        return GeojsonSpec(self.__generic_fetch(url=url, params=self.__params))
