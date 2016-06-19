# WeatherGenerator
Generate weather info for certain cities

# Prerequisite (python packages):
1. GeoPy
2. Geocoder
3. pytz

# Files description:
1. WeatherGenerator.py
Des: Main python program.
2. all_cities_weather.sh
Des: Bash program is to generate all cities weather information in one time.

# Usage:
python WeatherGenerator.py [Location]

# List of locations: 
Adelaide, Peking, London, LosAngeles, Melbourne, Miami, Moscow, NewYork, Ottawa, Paris, Seoul, Shanghai, Shenzhen, Singapore, Sydney, Tokyo

# Expected generated files description:
1. city_locations.txt
Des: Python program generates lantitude and longitude information for cities. The purpose is to avoid to use GeoPy function much frequent and comply with the policy of GeoPy.
2. city_weather_info.txt
Des: The expected result which contains the latest weather information generated by program.
