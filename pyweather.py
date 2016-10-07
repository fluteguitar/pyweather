import httplib
from httplib import HTTPConnection
from json import loads, load
import codecs
from geopy.geocoders import GoogleV3


def gen_weather_api_link(location_name):
	
	site = 'api.weather.com'
	path = '/v2/turbo/vt1precipitation;vt1currentd'\
			'atetime;vt1pollenforecast;vt1dailyForecast;vt1observation?units'\
			'=m&language=en&geocode={},{}&format=json&apiKey=c1ea9f47f6a88b9'\
			'acb43aba7faf389d4'
	geolocator = GoogleV3()			
	location = geolocator.geocode(location_name)

	if location is None:
		return "No matching locations found"

	path = path.format(
		str(location.latitude), 
		str(location.longitude))
	return site, path

def process_json_data(json_data):
	"""Return desired weather information from given json source.
	"""
	dict = {}
	current_cond = json_data['vt1observation']
	return (current_cond['phrase'] + "\n" 
		+ "Humidity: " + str(current_cond['humidity']) + "%\n" 
		+ "Wind Speed: " + str(current_cond['windSpeed']) + "km/h\n"
		+ "Temperature: " + str(current_cond['temperature']) + "^C\n" 
		+ "UV: " + str(current_cond['uvIndex']) + "/10 " + current_cond['uvDescription'] + "\n")

def process_http_request(location_name):

	site, path = gen_weather_api_link(location_name)
	conn = HTTPConnection(site)
	conn.request("GET", path)
	res = conn.getresponse()
	if res.status != 200:
		return -1

	data = res.read()
	json_data = loads(data)

	return json_data

print process_json_data(process_http_request("cu chi thanh pho ho chi minh"))