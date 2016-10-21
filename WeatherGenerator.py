##################################################################################
# Local weather information generator
# Ver:	0.1
# Date:	17 June 2016
# Author:
# Func:	1. Consider local climate condition.
#	2. Randomly generate reasonable weather information based on location.
# 	3. Write generated info into a file using standard format.
# Usage: python WeatherGenerator.py [Location]
# List of locations: Adelaide, Peking, London, LosAngeles, Melbourne, Miami, Moscow, NewYork, Ottawa, Paris, Seoul, Shanghai, Shenzhen, Singapore, Sydney, Tokyo
##################################################################################
import sys
import os
import random
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import geocoder
import datetime
import time
from random import choice
import random
from time import sleep
import pytz
import string

'''
Function: Based on city name to generator lantitude & longtitude
'''
def do_geocode(geolocator,address):
	try:
		if "_" in address:
			address = string.replace(address,'_',' ')
		sleep(1)
		return geolocator.geocode(address,timeout=None)
	except GeocoderTimedOut:
		print ("GeoPy API policy restriction on query frequency. Wait 1s to re-try.")
		return do_geocode(geolocator,address)
	except:
		print ("Error: geocode failed on input %s with message %s" %(address, sys.exc_info()[0]))
		exit(3)

'''
Main. Start Point.
'''
if __name__=="__main__":
	# Verify the arguments
	if len(sys.argv) != 2:
		print ("The no. of arguments are not correct. Please verify.")
		print ("Usage: python WeatherGenerator.py [Location]")
		print ("List of locations: Adelaide, Peking, London, Los_Angeles, Melbourne, Miami, Moscow, New_York, Ottawa, Paris, Seoul, Shanghai, Shenzhen, Singapore, Sydney, Tokyo")
		exit(1)

	# List of locations, which can generate weather report
	list_of_loc=['Adelaide', 'Peking', 'London', 'Los_Angeles', 'Melbourne', 'Miami', 'Moscow', 'New_York', 'Ottawa', 'Paris', 'Seoul', 'Shanghai', 'Shenzhen', 'Singapore', 'Sydney', 'Tokyo']
	# Verify the city, which user input
	city=sys.argv[1]
	if not city in list_of_loc:
		print ("%s is not recognized. Please choose from list of locations." %city)
		print ("Usage: python WeatherGenerator.py [Location]")
		print ("List of locations: Adelaide, Peking, London, Los_Angeles, Melbourne, Miami, Moscow, New_York, Ottawa, Paris, Seoul, Shanghai, Shenzhen, Singapore, Sydney, Tokyo")
		exit(2)

	# Get this python program full path to let use can program anywhere.
	abs_dir =  os.path.dirname(os.path.abspath(sys.argv[0]))

	'''
	The following part is designed for randomly generating the elements of weather
	for the city of input. In real situation, program must measure by some sensors
	or take actual data from weather API.
	''' 
	# List of conditions
	conditions=['Rain','Snow','Sunny','Cloudy','Windy']
	# Range of temperature, simulate cold, warm and hot areas temperature ranges. Using dictionary.
	range_tem={}
	range_tem['cold']="-10,24"
	range_tem['warm']="10,30"
	range_tem['hot']="15,40"
	# Type of locations. Classify locations areas by cold, warm & hot. Using dictionary.
	tem_loc={}
	tem_loc['Adelaide']="hot"
	tem_loc['Peking']="cold"
	tem_loc['London']="cold"
	tem_loc['Los_Angeles']="warm"
	tem_loc['Melbourne']="cold"
	tem_loc['Miami']="hot"
	tem_loc['Moscow']="cold"
	tem_loc['New_York']="cold"
	tem_loc['Ottawa']="cold"
	tem_loc['Paris']="warm"
	tem_loc['Seoul']="cold"
	tem_loc['Shanghai']="warm"
	tem_loc['Shenzhen']="warm"
	tem_loc['Singapore']="hot"
	tem_loc['Sydney']="cold"
	tem_loc['Tokyo']="cold"
	# Range of humidity, simulate seaside & non-seaside areas humidity. Using dictionary.
	range_hum={}
	range_hum['seaside']="50,100"
	range_hum['notseaside']="30,80"
	# Type of locations. Classify locations areas by seaside & non-seaside. Using dictionary.
	hum_loc={}
	hum_loc['Adelaide']="seaside"
	hum_loc['Peking']="notseaside"
	hum_loc['London']="notseaside"
	hum_loc['Los_Angeles']="seaside"
	hum_loc['Melbourne']="notseaside"
	hum_loc['Miami']="seaside"
	hum_loc['Moscow']="notseaside"
	hum_loc['New_York']="notseaside"
	hum_loc['Ottawa']="notseaside"
	hum_loc['Paris']="notseaside"
	hum_loc['Seoul']="notseaside"
	hum_loc['Shanghai']="seaside"
	hum_loc['Shenzhen']="seaside"
	hum_loc['Singapore']="seaside"
	hum_loc['Sydney']="seaside"
	hum_loc['Tokyo']="seaside"
	# Range of pressure, high & low as int.
	high=1200
	low=800

	'''
	IATA Codes
	'''
	iata_loc={}
	iata_loc['Adelaide']="ADL"
	iata_loc['Peking']="BJS"
	iata_loc['London']="LCY"
	iata_loc['Los_Angeles']="LAX"
	iata_loc['Melbourne']="MEL"
	iata_loc['Miami']="MIA"
	iata_loc['Moscow']="MOW"
	iata_loc['New_York']="NYC"
	iata_loc['Ottawa']="YOW"
	iata_loc['Paris']="PAR"
	iata_loc['Seoul']="SEL"
	iata_loc['Shanghai']="SHA"
	iata_loc['Shenzhen']="SZX"
	iata_loc['Singapore']="SIN"
	iata_loc['Sydney']="SYD"
	iata_loc['Tokyo']="TYO"

	'''
	TimeZone
	'''
	tz_loc={}
	tz_loc['Adelaide']="Australia/Adelaide"
	tz_loc['Peking']="Etc/GMT+8"
	tz_loc['London']="Etc/GMT+1"
	tz_loc['Los_Angeles']="America/Los_Angeles"
	tz_loc['Melbourne']="Australia/Melbourne"
	tz_loc['Miami']="Etc/GMT-4"
	tz_loc['Moscow']="Etc/GMT+3"
	tz_loc['New_York']="America/New_York"
	tz_loc['Ottawa']="Etc/GMT-4"
	tz_loc['Paris']="Etc/GMT+2"
	tz_loc['Seoul']="Etc/GMT+9"
	tz_loc['Shanghai']="Asia/Shanghai"
	tz_loc['Shenzhen']="Etc/GMT+8"
	tz_loc['Singapore']="Asia/Singapore"
	tz_loc['Sydney']="Australia/Sydney"
	tz_loc['Tokyo']="Etc/GMT+9"

	'''
	Start to prepare the string data
	'''
	str_data=iata_loc.get(city) + "|"

	'''
	The following part generate city's lantitude and longtitude.
	GeoPy package required. GeoPy use policy is quite strict. Avoid to 
	use it frequently, we will write location into a file. In the next
	query, the program will read the data from the file directly.
	Format in the file: [city],[lantitude],[longtitude]
	'''
	geolocations_file = abs_dir + "/city_locations.txt"
	# Initial geolocation dictionary to store written data.
	geolocaiton = {}
	# Judge whether the file exist or not
	if os.path.isfile(geolocations_file):
		frlocation = open(geolocations_file,'r')
		for line in frlocation:
			temp = line.strip().split(',')
			geolocaiton[temp[0]] = temp[1] + "," + temp[2]
		frlocation.close()
	# Judge whether the input city exists in the location file.
	if not geolocaiton.has_key(city):
		fwlocation = open(geolocations_file,'a')
		geolocator = Nominatim()
		location = do_geocode(geolocator,city.lower())
		lan = location.latitude
		lon = location.longitude
		fwlocation.write(city + "," + str(round(float(lan),2)) + "," + str(round(float(lon),2)) + "\n")
		fwlocation.close()
	else:
		location = geolocaiton.get(city)
		lan = location.split(',')[0]
		lon = location.split(',')[1]
	# Write into the string data
	str_data = str_data + str(round(float(lan),2)) + "," + str(round(float(lon),2)) + ","

	'''
	The following part generate city's altitude.
	geocoder package required.
	'''
	g = geocoder.elevation([lan,lon])
	alt = g.meters
	# Write into the string data
	str_data = str_data + str(int(alt)) + "|"

	'''
	Get current time using standard format
	'''
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts,pytz.timezone(tz_loc.get(city))).strftime('%Y-%m-%dT%H:%M:%SZ')
	# Write into the string data
	str_data = str_data + st + "|"

	'''
	Randomly get conditions
	'''
	str_data = str_data + choice(conditions) + "|"

	'''
	Randomly get temperature
	'''
	range_temperature = range_tem.get(tem_loc.get(city))
	low_temp = int(range_temperature.split(',')[0])
	high_temp = int(range_temperature.split(',')[1])
	str_data = str_data + str(round(random.uniform(low_temp,high_temp),1)) + "|"

	'''
	Randomly get pressure
	'''
	str_data = str_data + str(round(random.uniform(low,high),1)) + "|"

	'''
	Randomly get humidity
	'''
	range_humidity = range_hum.get(hum_loc.get(city))
	low_hum = float(range_humidity.split(',')[0])
	high_hum = float(range_humidity.split(',')[1])
	str_data = str_data + str(int(random.uniform(low_hum,high_hum)))

	''''
	Writing/Updating city weather data into a file. In future, may use them for plotting a map etc.
	'''
	# Specify the file name and path
	fpath = abs_dir + "/city_weather_info.txt"
	weather_info = {}
	if os.path.isfile(fpath):
		fr = open(fpath,'r')
		'''
		Check whether there is historic city weather information data.
		'''
		for line in fr:
			temp =  line.split('|')
			weather_info[temp[0]] = line.strip()
		# Update the latest info
		weather_info[iata_loc.get(city)] = str_data
		fr.close()
	# Writing data into table
	fw = open(fpath,'w')
	if len(weather_info.keys()) == 0:
		fw.write(str_data + "\n")
	else:
		for key in weather_info:
			fw.write(weather_info[key] + "\n")
	fw.close()
