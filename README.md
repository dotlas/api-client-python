<h1 align="center" style="border-bottom: none">
    <b>
        <a href="https://www.dotlas.com">Dotlas Python Client</a><br>
    </b>
</h1>

<p align="center">
<strong>The Dotlas REST API enables you to:</strong>

<ul><p align="center">Integrate data & insights with your own web or mobile apps 📲</p></ul>
<ul><p align="center">Consume information that supplements in-house data analysis and visualization 📊</p></ul>
<ul><p align="center">Enhance the functionality of your tech stack 🖥</p></ul>
<ul><p align="center">Leverage alternative data in your data pipeline 🏗</p></ul>

</p>


<div align="center">
 
[![License](https://img.shields.io/badge/license-MIT-green)](https://img.shields.io/badge/license-MIT-green) 
[![Python version](https://img.shields.io/badge/python-v3.8-blue)](https://img.shields.io/badge/python-v3.8-blue)

</div>

<p align="center">
    <a href="https://www.dotlas.com"><b>Website</b></a> •
    <a href="https://api.dotlas.com/docs"><b>API Documentation</b></a> •
    <a href="mailto:info@dotlas.com"><b>Email</b></a> •
    <a href="https://www.linkedin.com/company/76513297"><b>LinkedIn</b></a>
</p>  

## Setup

### Pip
To install Dotlas from [PyPi](https://pypi.org/) run the following command:
```bash
$ pip install dotlas
```

### Local
To setup dotlas from GitHub:

<p align="center"><img src="https://raw.githubusercontent.com/dotlas/api-client-python/main/assets/local_install.png" height=150></img></p>

## Usage

### Basic Calls

```python
import dotlas

dot = dotlas.App(api_key="<YOUR API KEY>")

cities = dot.list_cities()
houston_city_stats = dot.city_stats(city="Houston")

restaurants_near_empire_state_bldg = dot.nearby_competition(
    latitude=40.74861114520377,
    longitude=-73.98560002111566,
    city="New York",
    commercial_type="Restaurant",
)

esb_insights = restaurants_near_empire_state_bldg.response.insights
esb_data = restaurants_near_empire_state_bldg.response.data
```
### Mapping

> `pip install folium` if you don't have it already. `MAPBOX_ACCESS_TOKEN` can be obtained from [mapbox.com](https://www.mapbox.com/account/access-tokens/)

```python
import folium
MAPBOX_MAP: str = "https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/{z}/{x}/{y}?access_token={MAPBOX_ACCESS_TOKEN}"


empire_state_building_profile = dot.sales_territory(
    latitude=40.74861114520377,
    longitude=-73.98560002111566,
    city="New York",
    time_minutes=10,
    mode_of_mobility="driving"
)

folMap: folium.Map = folium.Map(
    location=[
        empire_state_building_stats.request.latitude, 
        empire_state_building_stats.request.longitude, 
    ],
    tiles=MAPBOX_MAP,
    attr='mapbox',
    zoom_start=12
)

folium.GeoJson(
    empire_state_building_stats.response.geometry.dict()
).add_to(folMap)
```

<p align="center"><img src="https://raw.githubusercontent.com/dotlas/api-client-python/main/assets/folium_mapbox_map.png" height=200></img></p>
