from pydantic import BaseModel, validator


class PriceBins(BaseModel):
    price_1: int = None
    price_2: int = None
    price_3: int = None
    price_4: int = None


class OperatingHours(BaseModel):
    sunday: list[int]
    monday: list[int]
    tuesday: list[int]
    wednesday: list[int]
    thursday: list[int]
    friday: list[int]
    saturday: list[int]


class CompetitionEndpointResponse(BaseModel):
    class CompetitionRequest(BaseModel):
        latitude: float
        longitude: float
        city: str
        commercial_type: str
        radius_meters: int
        brands: list[str] = None
        categories: list[str] = None

        radius_meters_valid = (
            lambda radius_meters: True if 1 <= radius_meters <= 10000 else False
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

        @validator("radius_meters")
        def radius_meters_validation(cls, radius_meters):
            if not cls.radius_meters_valid(radius_meters):
                raise ValueError("Radius Meters not in range of 1 mile")
            return radius_meters

    class CompetitionResponse(BaseModel):
        class CompetitionInsights(BaseModel):
            nearby_outlet_count: int = None
            rating_percentile: float = None
            price_range_percentile: float = None
            orders_percentile: float = None
            price_bins: PriceBins

        class CompetitionData(BaseModel):
            class TopOutlets(BaseModel):
                brand_name: str
                address: str
                category_tags: list[str]
                rating: float
                number_of_reviews: int = None
                rating_percentile: float
                orders_percentile: float
                latitude: float
                longitude: float

            top_occurring_categories: list[str] = None
            top_nearby_outlets: list[TopOutlets] = None
            operating_hours_outlet_count: int
            operating_hours: OperatingHours

        insights: CompetitionInsights
        data: CompetitionData

    request: CompetitionRequest
    response: CompetitionResponse


class CompetitionCityEndpointResponse(BaseModel):
    class CompetitionCityRequest(BaseModel):
        city: str
        commercial_type: str
        brands: list[str] = None
        categories: list[str] = None

    class CompetitionCityResponse(BaseModel):
        class CompetitionCity(BaseModel):
            brand_name: str
            address: str
            latitude: float
            longitude: float
            category_tags: list[str]
            rating: float = None
            number_of_reviews: int = None
            indices_price_range: float = None
            indices_order_proxy: float = None

        competitors: list[CompetitionCity]

    request: CompetitionCityRequest = None
    response: CompetitionCityResponse = None


class CompetitionDiscoveryRequest(BaseModel):
    city: str
    commercial_type: str


class CompetitionDiscoveryBrandsEndpointResponse(BaseModel):
    class CompetitionDiscoveryBrandsResponse(BaseModel):
        brands: list[str] = None

    request: CompetitionDiscoveryRequest = None
    response: CompetitionDiscoveryBrandsResponse = None


class CompetitionDiscoveryCategoriesEndpointResponse(BaseModel):
    class CompetitionDiscoveryCategoriesResponse(BaseModel):
        categories: list[str] = None

    request: CompetitionDiscoveryRequest = None
    response: CompetitionDiscoveryCategoriesResponse = None


class GenericInsightsRequests(BaseModel):
    city: str
    commercial_type: str
    categories: list[str] = None
    price_range: int = None

    @validator("price_range")
    def price_range_validation(cls, price_range):
        if price_range and price_range < 1:
            raise ValueError("Invalid Price Range")
        return price_range


class GenericInsights(BaseModel):
    max_outlets: str
    max_avg_rating: str
    max_avg_reviews: str


class CategoryInsightsEndpointResponse(BaseModel):
    class CategoryInsights(GenericInsights):
        class CategoryStat(BaseModel):
            category_tag: str
            avg_rating: float
            avg_number_of_reviews: float
            outlet_count: int
            price_bins: PriceBins

        class CategoryPairwiseOccurrence(BaseModel):
            category_1: str
            category_2: str
            pair_occurrences: int

        min_avg_rating: str
        category_stats: list[CategoryStat]
        category_by_pairwise_occurrence: list[CategoryPairwiseOccurrence]

    request: GenericInsightsRequests
    response: CategoryInsights


class BrandInsightsEndpointResponse(BaseModel):
    class BrandInsights(GenericInsights):
        class BrandStat(BaseModel):
            brand_name: str
            avg_rating: float
            avg_number_of_reviews: float
            outlet_count: int
            category_tags: list[str]
            price_bins: PriceBins

        outlet_count: int
        brand_stats_by_outlet_count: list[BrandStat]
        brand_stats_by_avg_rating: list[BrandStat]
        brand_stats_by_avg_number_of_reviews: list[BrandStat]
        outlet_counts_by_price: PriceBins
        operating_hours_outlet_count: int
        operating_hours: OperatingHours

    request: GenericInsightsRequests
    response: BrandInsights


class AreaInsightsEndpointResponse(BaseModel):
    class AreaInsights(BaseModel):
        class StreetStat(BaseModel):
            street: str
            avg_rating: float
            avg_number_of_reviews: float
            brand_count: int

        class NeighborhoodStat(BaseModel):
            neighborhood: str
            avg_rating: float
            avg_number_of_reviews: float
            brand_count: int

        class PostcodeStat(BaseModel):
            postcode: str
            avg_rating: float
            avg_number_of_reviews: float
            brand_count: int

        street_stats: list[StreetStat]
        neighborhood_stats: list[NeighborhoodStat]
        postcode_stats: list[PostcodeStat]

    request: GenericInsightsRequests
    response: AreaInsights
