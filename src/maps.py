import warnings
from typing import List

import ee
import ipyleaflet as ipyl
from shapely.geometry import Polygon


class LeafletMap(ipyl.Map):
    """
    A custom Map class that extends the ipyleaflet Map class.

    Attributes:
        geometry (dict): A dictionary containing the GeoJSON data of the selected area.
        center (list): A list containing the latitude and longitude of the map center.
        zoom (int): The zoom level of the map.

    Methods:
        add_draw_control():
            Adds a draw control to the map to allow the user to select an area.

        add_gee_layer(dataset, year='2018'):
            Adds a Google Earth Engine layer to the map.

    Properties:
        region: The GeoJSON geometry of the selected area.
        coordinates: The coordinates of the selected area.
        polygon: The Shapely Polygon object of the selected area.
        bbox: The bounding box of the selected area.
        centroid: The centroid of the selected area.

    Usage:
        map = LeafletMap(geometry=geojson_data, center=[28.4, -16.4], zoom=10)
        map.add_gee_layer(dataset)
    """

    def __init__(self, geometry: dict = None, center: List[float] = [28.4, -16.4], zoom: int = 10, **kwargs):
        """
        Constructor for LeafletMap class.

        Parameters:
        geometry (dict, optional): A dictionary containing the GeoJSON data of the selected area. Defaults to None.
        center (list, optional): A list containing the latitude and longitude of the map center. Defaults to [28.4, -16.4].
        zoom (int, optional): The zoom level of the map. Defaults to 10.
        **kwargs: Additional arguments that are passed to the parent constructor.
        """
        self.geometry = geometry
        self.center = self.centroid if geometry else center
        self.zoom = zoom
        
        super().__init__(
            basemap=ipyl.basemap_to_tiles(ipyl.basemaps.Esri.WorldImagery),
            center=tuple(self.center), zoom=self.zoom, **kwargs)

        self.add_draw_control()

    def add_draw_control(self):
        """
        Adds a draw control to the map to allow the user to select an area.
        """
        control = ipyl.LayersControl(position='topright')
        self.add_control(control)

        print('Draw a rectangle on map to select and area.')

        draw_control = ipyl.DrawControl()

        draw_control.rectangle = {
            "shapeOptions": {
                "color": "#2BA4A0",
                "fillOpacity": 0,
                "opacity": 1
            }
        }

        if self.geometry:
                self.geometry['features'][0]['properties'] = {'style': {'color': "#2BA4A0", 'opacity': 1, 'fillOpacity': 0}}
                geo_json = ipyl.GeoJSON(
                    data=self.geometry
                )
                self.add_layer(geo_json)

        else:
            feature_collection = {
                'type': 'FeatureCollection',
                'features': []
            }

            def handle_draw(self, action, geo_json):
                """Do something with the GeoJSON when it's drawn on the map"""    
                #feature_collection['features'].append(geo_json)
                if 'pane' in list(geo_json['properties']['style'].keys()):
                    feature_collection['features'] = []
                else:
                    feature_collection['features'] = [geo_json]

            draw_control.on_draw(handle_draw)

            self.add_control(draw_control)

            self.geometry = feature_collection

    def add_gee_layer(self, dataset, year='2018'):
        """
        Adds a Google Earth Engine layer to the map.

        Parameters:
        dataset (GEEData): A GEEData object containing the land cover data
        year (str, optional): The year of the image to display. Defaults to '2018'.
        """
        image = dataset.ee_image(year)
        sld_interval = dataset.sld_interval
        name = dataset.layer_name(year)

        ee_tiles = '{tile_fetcher.url_format}'

        image = image.sldStyle(sld_interval)
        mapid = image.getMapId()
        tiles_url = ee_tiles.format(**mapid)

        layer = ipyl.TileLayer(url=tiles_url, name=name)
        self.add_layer(layer)

    @property
    def region(self):
        """
        The GeoJSON geometry of the selected area.
        """
        if not self.geometry['features']:
            warnings.warn("Rectangle hasn't been drawn yet. Polygon is not available.")
            return None

        return self.geometry['features'][0]['geometry']

    @property
    def coordinates(self):
        """
        The coordinates of the selected area.
        """
        if not self.geometry['features']:
            warnings.warn("Rectangle hasn't been drawn yet. Polygon is not available.")
            return None

        return self.region['coordinates']

    @property
    def polygon(self):
        """
        The Shapely Polygon object of the selected area.
        """
        if not self.geometry['features']:
            warnings.warn("Rectangle hasn't been drawn yet. Polygon is not available.")
            return None

        return Polygon(self.coordinates)

    @property
    def bbox(self):
        """
        The bounding box of the selected area.
        """
        if not self.polygon:
            warnings.warn("Rectangle hasn't been drawn yet. Bounding box is not available.")
            return None
        
        return list(self.polygon.bounds)
    
    @property
    def centroid(self):
        """
        The centroid of the selected area.
        """
        if not self.geometry['features']:
            warnings.warn("Rectangle hasn't been drawn yet. Centroid is not available.")
            return None
        else:
            return [arr[0] for arr in self.polygon.centroid.xy][::-1]