#!/bin/sh
#######################################################
#Author: Wang Cheng
#Date: 19 June 2016
#Des: Using WeatherGenerator.py python program generates
#all cities weather information. 
#######################################################
# List of locations
declare -a list_locations
list_locations=(Adelaide Peking London Los_Angeles Melbourne Miami Moscow New_York Ottawa Paris Seoul Shanghai Shenzhen Singapore Sydney Tokyo)

# Start
running_time=`date`
echo "Program starts... $running_time"

# Using WeatherGenerator.py
for city in ${list_locations[@]}
do
	echo Generating $city weather information
	python WeatherGenerator.py $city
done

# End
running_time=`date`
echo "Program ends... $running_time"
echo "Please check city_weather_info.txt"