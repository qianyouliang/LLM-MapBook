# utils.py
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

class GeocodeUtils:
    def __init__(self, user_agent="geoapiExercises"):
        self.geolocator = Nominatim(user_agent=user_agent)

    def geocode(self, address):
        """
        Geocode an address to get latitude and longitude.
        
        Parameters:
        address (str): The address to geocode.
        
        Returns:
        dict: A dictionary containing latitude, longitude, and the full address.
        """
        try:
            location = self.geolocator.geocode(address)
            if location:
                return {
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'address': location.address
                }
            else:
                return {'error': 'Address not found'}
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            return {'error': str(e)}

    def reverse_geocode(self, latitude, longitude):
        """
        Reverse geocode latitude and longitude to get an address.
        
        Parameters:
        latitude (float): The latitude to reverse geocode.
        longitude (float): The longitude to reverse geocode.
        
        Returns:
        dict: A dictionary containing the full address, latitude, and longitude.
        """
        try:
            location = self.geolocator.reverse((latitude, longitude), exactly_one=True)
            if location:
                return {
                    'address': location.address,
                    'latitude': location.latitude,
                    'longitude': location.longitude
                }
            else:
                return {'error': 'Location not found'}
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            return {'error': str(e)}

# 使用案例
if __name__ == "__main__":
    geocode_utils = GeocodeUtils()

    # 示例1: 地理编码
    address = "华沙"
    geocode_result = geocode_utils.geocode(address)
    print(f"Geocode result for '{address}': {geocode_result}")

    # 示例2: 逆地理编码
    latitude = 37.4223096
    longitude = -122.0846244
    reverse_geocode_result = geocode_utils.reverse_geocode(latitude, longitude)
    print(f"Reverse geocode result for ({latitude}, {longitude}): {reverse_geocode_result}")
