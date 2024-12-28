from datetime import datetime, timedelta
import folium
import ee

# Authenticate with service account key file
service_account = 'waste-management@ee-talropajmal1016.iam.gserviceaccount.com'
key_file = './service-account-key.json'
ee.Initialize(ee.ServiceAccountCredentials(service_account, key_file))

# Define area of interest
point = ee.Geometry.Point([77.5946, 12.9716])  # Replace with valid coordinates

# Define dynamic date range
end_date = datetime.utcnow()  # Today's date
start_date = end_date - timedelta(days=30)  # 30 days ago
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

# Fetch the most recent image
image = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
    .filterBounds(point) \
    .filterDate(start_date_str, end_date_str) \
    .filter(ee.Filter.lt('CLOUD_COVER', 80)) \
    .sort('CLOUD_COVER') \
    .first()

# Check if an image was found
if image:
    print("Image found:", image.getInfo())
else:
    print("No matching image found. Adjust the query parameters.")
    exit()

# Visualization parameters
vis_params = {
    'min': 0,
    'max': 3000,
    'bands': ['B4', 'B3', 'B2'],  # True-color bands
}

# Create a Folium map
map = folium.Map(location=[12.9716, 77.5946], zoom_start=18)

# Define a function to add Earth Engine layers to the map


def add_ee_layer(self, ee_object, vis_params, name):
    map_id_dict = ee.Image(ee_object).getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Google Earth Engine',
        name=name,
        overlay=True,
        control=True
    ).add_to(self)


# Add the layer
folium.Map.add_ee_layer = add_ee_layer
map.add_ee_layer(image, vis_params, 'Sentinel-2 Image')

# Save and view the map
map.save('map.html')
print("Map saved as 'map.html'. Open it in your browser to view.")
