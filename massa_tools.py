#massa_tools.py
"""This file contains the simple tools that will come together to process the massa data and turn it into water depth data"""

#import neccesary packages and modules
import pandas as pd
import geopandas as gpd
import shapely.geometry
import rasterio

class MassaTools:
    """This class contains the tools that will come together to process the massa data"""

    def __init__(self):
        print("initialized")

    def load_massa_file(self, filepath, epsg):
        """take massa file and turn it into a geopandas dataframe"""

        #print filepath
        print(filepath)

        # Load the CSV file into a pandas DataFrame
        # Skip the first 28 rows and the line immediately after the header
        df = pd.read_csv(filepath, skiprows=29, header=0)

        # Skip the line immediately after the header by reloading the file and skipping necessary lines
        df = pd.read_csv(filepath, skiprows=list(range(28)) + [29])

        # Assuming your CSV has 'latitude' and 'longitude' columns
        # Create a 'geometry' column using the 'longitude' and 'latitude' columns
        geometry = [shapely.geometry.Point(xy) for xy in zip(df['X'], df['Y'])]

        # Convert the DataFrame to a GeoDataFrame
        gdf = gpd.GeoDataFrame(df, geometry=geometry)

        # Set the coordinate reference system (CRS) if known, e.g., WGS84
        gdf.set_crs(epsg = epsg, inplace=True)

        # Now you have a GeoDataFrame ready for spatial operations
        return gdf

    def get_water_depth(self, water_elev, fp_elev, offset = 0):
        """take the loaded massa file (geodataframe) and add a column for floodplain elevation by extracting the nearest elevation point from a geotiff"""
        with rasterio.open(fp_elev) as src:
            # Ensure the CRS of the GeoTIFF and the GeoDataFrame match
            assert src.crs.to_string() == water_elev.crs.to_string(), "CRS mismatch between GeoTIFF and GeoDataFrame"

            # Sample the raster values at the point locations
            coords = [(x,y) for x, y in zip(water_elev.geometry.x, water_elev.geometry.y)]
            floodplain_elevation = [val[0] for val in src.sample(coords)]


            # Append the raster values to the GeoDataFrame
            water_elev["fp_elev"] = floodplain_elevation

            water_elev["Massa Target"] = water_elev["Massa Target"].replace("OutOfRange", -9999)
            water_elev["Massa Target"] = water_elev["Massa Target"].astype(float)

            print("Massa: ", water_elev["Massa Target"].dtype)
            print("Massa: ", water_elev["Massa Target"])
            print("fp: ", water_elev["fp_elev"].dtype)
            print("fp: ", water_elev["fp_elev"])


        #differene the floodplain and water elevations to find the water depths
        water_elev["water_depth"] = water_elev["Massa Target"] - water_elev["fp_elev"] + offset

        return water_elev

    def extract_aoi(self, gdf, shp, polygon):
        """take a geodataframe and extract points from and area of interest"""

        # Load the shapefile containing the polygons
        polygons = gpd.read_file(shp)

        # Select the polygons based on an attribute value
        selected_polygons = polygons[polygons['id'] == polygon]

        # Combine the geometries of the selected polygons into a single geometry
        combined_geometry = selected_polygons.unary_union

        # Subset the points to those within the combined geometry
        subset_gdf = gdf[gdf.within(combined_geometry)]

        return subset_gdf
