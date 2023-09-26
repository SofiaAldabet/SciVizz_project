import subprocess

import pandas as pd
import matplotlib.pyplot as plt

import ee
from ipyleaflet import DrawControl, LayersControl, Map, TileLayer, basemaps
from IPython.display import display as ipydisplay


class LandcoverDataProcessor:
    def __init__(self, input_nc_files, output_tif_files):
        self.input_nc_files = input_nc_files
        self.output_tif_files = output_tif_files

    def convert_nc_to_tif(self):
        for input_nc, output_tif in zip(self.input_nc_files, self.output_tif_files):
            gdalwarp_command = [
                "gdalwarp",
                "-of",
                "Gtiff",
                "-co",
                "COMPRESS=LZW",
                "-co",
                "TILED=YES",
                "-ot",
                "Byte",
                "-te",
                "-180.0000000",
                "-90.0000000",
                "180.0000000",
                "90.0000000",
                "-tr",
                "0.002777777777778",
                "0.002777777777778",
                "-t_srs",
                "EPSG:4326",
                f"NETCDF:{input_nc}:lccs_class",
                output_tif,
            ]
            subprocess.run(gdalwarp_command, check=True)

    def upload_to_gee(self):
        for output_tif in self.output_tif_files:
            asset_id = "projects/ee-sofiaaldabet-training/assets/landcover"
            upload_command = [
                "earthengine",
                "upload",
                "image",
                "--asset_id=" + asset_id,
                "--nodata_value=0",
                "--pyramiding_policy=mean",
                "--bands=band1",
                output_tif,
            ]
            subprocess.run(upload_command, check=True)


class GEEImageLoader:
    def __init__(self, collection_name):
        self.collection = ee.ImageCollection(collection_name)

    def get_first_and_last_images(self):
        sorted_collection = self.collection.sort("system:time_start")
        first_image = sorted_collection.first()
        last_image = sorted_collection.sort("system:time_start", False).first()
        return first_image, last_image

    def select_image_by_date(self, start_date, end_date):
        selected_image = self.collection.filterDate(start_date, end_date)
        return selected_image


class MapRenderer:
    def __init__(self, center, zoom):
        self.map = Map(center=center, zoom=zoom)
        self.layer_control = LayersControl(position="topright")
        self.map.add_control(self.layer_control)
        self.map.add_layer(basemaps.OpenStreetMap)

    def add_tile_layer(self, ee_image, vis_params=None, sld_ramp=None, name="Layer"):
        if sld_ramp:
            tile_layer = TileLayer(
                url=ee_image.sldStyle(sld_ramp).getMapId()["tile_fetcher"].url_format,
                attribution="Google Earth Engine",
                name=name,
                opacity=1.0,
            )
        else:
            tile_layer = TileLayer(
                url=ee_image.getMapId(vis_params)["tile_fetcher"].url_format,
                attribution="Google Earth Engine",
                name=name,
                opacity=1.0,
            )
        self.map.add_layer(tile_layer)

    def display(self):
        # Display the map
        ipydisplay(self.map)


class GeometryDrawer:
    def __init__(self, map_renderer):
        self.map_renderer = map_renderer
        self.drawn_geometries = []
        self.setup_drawing_controls()

    def setup_drawing_controls(self):
        # Add a drawing control to the map with only polygon and rectangle options
        polygon_style = {"color": "black", "weight": 4, "fillOpacity": 0}
        rectangle_style = {"color": "red", "weight": 4, "fillOpacity": 0}
        draw_control = DrawControl(
            polygon={"shapeOptions": polygon_style},
            rectangle={"shapeOptions": rectangle_style},
            edit=False,
            remove=True,
            draw={"polygon": {"allowIntersection": False}},
        )
        draw_control.on_draw(self.handle_draw)
        self.map_renderer.map.add_control(draw_control)

    def handle_draw(self, event, action, geo_json):
        if action == "created":
            self.drawn_geometries.append(geo_json)
        elif action == "deleted":
            for drawn_geometry in self.drawn_geometries:
                if drawn_geometry["id"] == event["id"]:
                    self.drawn_geometries.remove(drawn_geometry)

    def get_drawn_geometries(self):
        return self.drawn_geometries


class LandcoverAnalyzer:
    def __init__(self, map_renderer):
        self.map_renderer = map_renderer

    def select_and_clip_image(self, image_collection, start_date, end_date, geometries):
        lc_image = ee.Image(
            ee.ImageCollection(image_collection).filterDate(start_date, end_date).first()
        )
        lc_image_clipped = lc_image.clip(self.convert_geojson_to_feature_collection(geometries))
        return lc_image_clipped

    def calculate_frequency_histogram(self, lc_image, geometry_collection):
        lc_histogram = lc_image.reduceRegion(
            reducer=ee.Reducer.frequencyHistogram(),
            geometry=geometry_collection.geometry(),
            scale=30,
        )
        return lc_histogram

    def analyze_landcover(self, image_collection, start_date, end_date, landcover_info, geometries):
        # Convert the drawn geometries to an Earth Engine FeatureCollection
        geometry_collection = ee.FeatureCollection(geometries)

        # Select and clip the LC image using the drawn geometries
        lc_clipped = self.select_and_clip_image(image_collection, start_date, end_date, geometries)

        # Calculate the frequency histogram of land cover classes in the clipped image
        lc_histogram = self.calculate_frequency_histogram(lc_clipped, geometry_collection)

        # Calculate land cover percentages
        lc_counts = lc_histogram.get("b1").getInfo()
        total_count = sum(lc_counts.values())

        percentage_landcover = {}
        for landcover, count in lc_counts.items():
            percentage = round((count / total_count) * 100, 1)
            label = landcover_info[landcover]["Landcover"]
            color = landcover_info[landcover]["Color"]
            percentage_landcover[label] = {
                "Value": landcover,
                "Landcover": label,
                "Color": color,
                "Percentage": percentage,
            }

        # Create a DataFrame from the percentage_landcover dictionary
        result_df = pd.DataFrame(list(percentage_landcover.values()))

        # Remove rows that have a percentage of 0
        result_df = result_df[result_df["Percentage"] != 0]

        return result_df

    def convert_geojson_to_feature_collection(self, geo_json):
        return ee.FeatureCollection(geo_json)

    def plot_landcover_pie_chart(self, result_df, threshold=2):
        fig, ax = plt.subplots(figsize=(10, 10))
        wedges, _, autotexts = ax.pie(
            result_df["Percentage"],
            labels=[""] * len(result_df["Landcover"]),
            colors=result_df["Color"],
            autopct=lambda pct: f"{pct:.1f}%" if pct > threshold else "",
            startangle=90,
            textprops={"color": "k"},
        )  # Set labels to empty
        ax.axis("equal")

        # Create the legend labels with both category name and percentage
        legend_labels = [
            f"{label}: {pct:.1f}%"
            for label, pct in zip(result_df["Landcover"], result_df["Percentage"])
        ]
        ax.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(1, 0.5))

        # Adjust the label font size for better readability
        for autotext in autotexts:
            autotext.set_fontsize(10)

        plt.show()
