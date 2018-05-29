import matplotlib.pyplot as plt
import json

original_restaurant = []
query_result = []
review = []
money = []
with open('openrice_data.json') as f:
    original_restaurant = json.load(f)
# the result after filter/ranking
for x in original_restaurant:
    if x['district'].lower() in ['shatin', 'sha tin']:
        query_result.append(x)
for x in query_result:
    review.append(int(x['reviews'][0] + x['reviews'][1] + x['reviews'][2]))
    if x['price-range'] == 'Below $50':
        money.append(25)
    elif x['price-range'] == '$51-100':
        money.append(75.5)
    elif x['price-range'] == '$101-200':
        money.append(150.5)
    elif x['price-range'] == '$201-400':
        money.append(300.5)
    elif x['price-range'] == '$401-800':
        money.append(600.5)
    elif x['price-range'] == 'Above $801':
        money.append(900.5)

fig, ax = plt.subplots()
ax.scatter(money, review, color='b', s=30, alpha=0.1)
plt.axis([0, 1000, 0, 700])
plt.title("The relationship between price and popularity in Restaurants in Hong Kong")
plt.xlabel("Price")
plt.ylabel("Number of Reviews")
plt.show()