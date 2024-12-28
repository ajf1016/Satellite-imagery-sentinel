from datetime import datetime
import ee
from datetime import datetime, timedelta

# Authenticate with service account key file
service_account = 'waste-management@ee-talropajmal1016.iam.gserviceaccount.com'
key_file = './service-account-key.json'

ee.Initialize(ee.ServiceAccountCredentials(service_account, key_file))

# Define area of interest
# Replace with your coordinates
point = ee.Geometry.Point([75.89532712, 11.10155387])

end_date = datetime.utcnow()  # Today's date
start_date = end_date - timedelta(days=7)  # 7 days ago

# Format the dates as strings
start_date_str = start_date.strftime('2024-12-01')
end_date_str = end_date.strftime('2024-12-28')

image_collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
    .filterBounds(point) \
    .filterDate(start_date_str, end_date_str) \
    .sort('CLOUD_COVER')

# Get all available dates
dates = image_collection.aggregate_array('system:time_start').getInfo()
if dates:
    for date in dates:
        readable_date = datetime.utcfromtimestamp(
            date / 1000).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Available image date: {readable_date}")
else:
    print("No images found in the specified range.")
