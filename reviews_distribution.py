import json
import matplotlib.pyplot as plt
import numpy


original_restaurant = []
query_result = []
with open('openrice_data.json') as f:
    original_restaurant = json.load(f)

for x in original_restaurant:
    if x['district'] == 'Tsim Sha Tsui':
        query_result.append(x)
    else:
        pass

review_result=[]
for x in query_result:
     review_result.append(int(x['reviews'][0] + x['reviews'][1] + x['reviews'][2]))


plt.title("Top-10 cuisine types in Tsim Sha Tsui")
plt.rcParams['font.size'] = 10.0

plt.hist(review_result, alpha=0.75,facecolor='blue',edgecolor='black', linewidth=1.2,bins=[0,100,200,300,400,500,600,700,800,900,1000,1100,1200])
plt.axis([0, 1200, 0, 110])
plt.title("The Distribution of the number of reviews in Tsim Sha Tsui")
plt.xlabel("Number of Reviews")
plt.ylabel("Number of Restaurant")
plt.show()