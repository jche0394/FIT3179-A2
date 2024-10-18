import pandas as pd
from geopy.geocoders import Nominatim
import ssl
import certifi
from time import sleep

# Load your CSV file
file_path = 'phone-seatbeat-locations.csv'  # Path to your CSV file
data = pd.read_csv(file_path)

# Clean the headers
data.columns = ['Road', 'Suburb', 'Reason Code', 'Effective Date', 'Unnamed']

# Create a new column combining Road and Suburb to form the address
data['Address'] = data['Road'] + ', ' + data['Suburb'] + ', Victoria, Australia'

# Create an SSL context using the certifi certificate file
ctx = ssl.create_default_context(cafile=certifi.where())

# Initialize the Nominatim geocoder with SSL context
geolocator = Nominatim(user_agent="geoapiExercises", ssl_context=ctx)

# Function to geocode addresses
def geocode_address(address):
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        return None, None
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
        return None, None

# Geocode each address with a delay between requests (to avoid being blocked)
latitudes = []
longitudes = []
for address in data['Address']:
    lat, lon = geocode_address(address)
    latitudes.append(lat)
    longitudes.append(lon)
    sleep(1)  # Sleep for 1 second to avoid overwhelming the API

# Add the latitude and longitude columns to the dataframe
data['Latitude'] = latitudes
data['Longitude'] = longitudes

# Save the updated data with geocoded coordinates
data.to_csv('geocoded_phone_seatbelt_locations.csv', index=False)

print("Geocoding complete! Data saved to 'geocoded_phone_seatbelt_locations.csv'")