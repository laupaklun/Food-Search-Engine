import gmplot
import requests
import json
import gmplot

#load the data and initialize the values
original_restaurant = []
query_result = []
latitudes = []
longitudes = []
gmap = gmplot.GoogleMapPlotter(22.395607,114.1963153, 13)

with open('openrice_data.json') as f:
    original_restaurant = json.load(f)

## Getting data and filtering
for x in original_restaurant:
    if x['district'].lower() in ['sha tin','shatin']:
        query_result.append(x)
    else:
        pass


## Please register your key and design the correct query
key = '&key=AIzaSyDfO1YKH8DATONpi_y2fSR-sVYR0kFCsug'
urllist = []
for x in query_result:
    dest_lat = x['address'][0]
    dest_lng = x['address'][1]
    query = 'origins=22.4179252,114.2027235&destinations={0},{1}&departure_time=1512045300&mode=transit&language=en-EN{2}'.format(str(dest_lat),str(dest_lng),str(key))
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?" + query
    res = requests.get(url).json()
    try:
        x['distance-martix'] = res['rows'][0]['elements'][0]['duration']['value']
    except KeyError:
        query = 'origins=22.4179252,114.2027235&destinations={0},{1}&departure_time=1512045300&mode=walking&language=en-EN{2}'.format(
            str(dest_lat), str(dest_lng), str(key))
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?" + query
        res = requests.get(url).json()
        x['distance-martix'] = res['rows'][0]['elements'][0]['duration']['value']
# you might want a for loop to send and receive the query


#plotting using gmplot
for x in query_result:
    try:
        dest_lat = x['address'][0]
        dest_lng = x['address'][1]
        if 2100 >= x['distance-martix'] >= 0:
            gmap.circle(x['address'][0], x['address'][1], 100, color="0000FF")
        elif 3600 >= x['distance-martix'] > 2100:
            gmap.circle(x['address'][0], x['address'][1], 100, color="FF0000")
        else:
            pass
    except KeyError:
        pass

gmap.draw("mymap_time.html")
