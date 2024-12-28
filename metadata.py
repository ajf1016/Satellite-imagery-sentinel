from datetime import datetime
import ee
from datetime import datetime, timedelta

# Authenticate with service account key file
service_account = 'waste-management@ee-talropajmal1016.iam.gserviceaccount.com'
key_file = './service-account-key.json'

ee.Initialize(ee.ServiceAccountCredentials(service_account, key_file))

# Define area of interest
point = ee.Geometry.Point([77.5946, 12.9716])  # Replace with your coordinates

end_date = datetime.utcnow()  # Today's date
start_date = end_date - timedelta(days=7)  # 7 days ago

# Format the dates as strings
start_date_str = start_date.strftime('2024-12-01')
end_date_str = end_date.strftime('2024-12-10')

# Use the date range in your query
image = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
    .filterBounds(point) \
    .filterDate(start_date_str, end_date_str) \
    .sort('CLOUD_COVER') \
    .first()


capture_date = image.get('system:time_start').getInfo()

# Convert timestamp to human-readable date
if capture_date:
    readable_date = datetime.utcfromtimestamp(
        capture_date / 1000).strftime('%Y-%m-%d %H:%M:%S')
    print(f"The image was captured on: {readable_date}")
else:
    print("No image metadata found.")
