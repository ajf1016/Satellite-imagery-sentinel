import ee
import folium

# Authenticate with service account key file
service_account = 'waste-management@ee-talropajmal1016.iam.gserviceaccount.com'
key_file = './service-account-key.json'

ee.Initialize(ee.ServiceAccountCredentials(service_account, key_file))
print("Earth Engine Initialized successfully!")

# Define area of interest
# Replace with your coordinates
point = ee.Geometry.Point([75.89532712, 11.10155387])
image = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
    .filterBounds(point) \
    .filterDate('2024-12-20', '2024-12-28') \
    .sort('CLOUD_COVER') \
    .first()


# Visualization parameters
vis_params = {
    'min': 0,
    'max': 3000,
    'bands': ['B4', 'B3', 'B2'],  # RGB bands
}

# Center map on the area of interest
map = folium.Map(location=[12.9716, 77.5946], zoom_start=10)

# Define a function to add Earth Engine data to the map


def add_ee_layer(self, ee_object, vis_params, name):
    map_id_dict = ee.Image(ee_object).getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Google Earth Engine',
        name=name,
        overlay=True,
        control=True
    ).add_to(self)


# Add the Earth Engine layer to Folium map
folium.Map.add_ee_layer = add_ee_layer
map.add_ee_layer(image, vis_params, 'Sentinel-2 Image')

# Add layer control and display map
folium.LayerControl().add_to(map)
map.save('map.html')  # Save the map as an HTML file
print("Map saved as map.html. Open it in your browser to view.")
