import gmplot
import json

original_restaurant = []
query_result =[]
latitudes = []
longitudes = []
with open('openrice_data.json') as f:
    original_restaurant = json.load(f)
# the result after filter/ranking
gmap = gmplot.GoogleMapPlotter(22.325222,114.1664163, 12.5)
for x in original_restaurant:
    if "japanese" in [dish.lower() for dish in x['cuisine']]:
        query_result.append(x)

for x in query_result:
    latitudes.append(x['address'][0])
    longitudes.append(x['address'][1])
    gmap.circle(x['address'][0],x['address'][1],200,color="0000FF")
    #gmap.marker(x['address'][0],x['address'][1], color='#FF0000', c=None, title="no implementation")

#gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=2)
#gmap.scatter(latitudes, longitudes, '#3B0B39', size=200, marker=False)
#gmap.heatmap(latitudes, longitudes)
#gmap.polygon(latitudes, longitudes)
gmap.draw("mymap_.html")