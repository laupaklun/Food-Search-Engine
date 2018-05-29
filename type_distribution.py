import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

original_restaurant = []
query_result =[]
cuisine_result = []
with open('openrice_data.json') as f:
    original_restaurant = json.load(f)
# the result after filter/ranking

for x in original_restaurant:
    if x['district'].lower() in ['mongkok', 'mong kok','mk']:
        query_result.append(x)
for x in query_result:
    cuisine_result.append(x['cuisine'][0])

list = Counter(cuisine_result).most_common(10)

cuisine_name =[]
cuisine_number =[]
others= 0
for x in list:
    cuisine_name.append(x[0])
    others += int(x[1])*100/len(cuisine_result)
    cuisine_number.append(float(str.format('{0:.2f}', int(x[1])*100/len(cuisine_result))))
others = str.format('{0:.2f}',100 - others)
cuisine_number.append(float(others))
cuisine_name.append('Others')
plt.title("Top-10 cuisine types in Mong Kok")
plt.rcParams['font.size'] = 10.0
plt.pie(cuisine_number,
        labels=cuisine_name,
        autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
plt.show()