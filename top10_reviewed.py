import json
import matplotlib.pyplot as plt

original_restaurant = []
query_result = []
with open('openrice_data.json') as f:
    original_restaurant = json.load(f)
# the result after filter/ranking
for x in original_restaurant:
    if x['district'].lower() in ['shatin', 'sha tin']:
        query_result.append(x)
for x in query_result:
    x['totalreviews'] = x['reviews'][0] + x['reviews'][1] + x['reviews'][2]
query_result= sorted(query_result, key=lambda x : x['totalreviews'], reverse=True)
query_result = query_result[:10]
top10restaurant= []
total_reviews = []
for restaurant in query_result:
    if '&#39;s' in restaurant["name"]:
        restaurant["name"] = restaurant["name"].replace('&#39;s', 's')
    if 'Caf&#233;' in restaurant["name"]:
        restaurant["name"] = restaurant["name"].replace('Caf&#233;', 'Cafe')
    if '&amp;' in restaurant["name"]:
        restaurant["name"] = restaurant["name"].replace('&amp;', 'and')
    top10restaurant.append(restaurant['name'])
    total_reviews.append(restaurant['totalreviews'])
fig, ax = plt.subplots()
plt.tick_params(axis='both', which='major', labelsize=10)
y_pos = range(len(top10restaurant))
ax.barh(y_pos, total_reviews)
ax.set_yticks(y_pos)
ax.set_yticklabels(top10restaurant)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Number of reviews')
ax.set_title('Top-10 most reviewed restaurants in Sha Tin')

plt.show()

