import json
import re
import math

class Food_Search_Engine:
    # original data from crawled json file
    original_data = []
    # the result after filter/ranking
    query_result = []

    def __init__(self, json_file_name):
        self.load_data(json_file_name)
        self.reset()

    def load_data(self, json_file_name):
        with open(json_file_name) as json_data:
            self.original_data = json.load(json_data)

    def reset(self):
        self.query_result = list(self.original_data)

    def filter(self, filter_cond):
        self.query_result = self.original_data

        try:
            filter_condition = filter_cond
            try:
                self.query_result =[x for x in self.query_result if x['name'].lower() in filter_condition['name']]
            except AttributeError:
                self.query_result =[x for x in self.query_result if x['name'].lower() in [item.lower() for item in filter_condition['name']]]
            except KeyError:
                pass
            try:
                self.query_result =[x for x in self.query_result if filter_condition['name_contains'].lower() in x['name'].lower()]
            except AttributeError:
                self.query_result =[x for x in self.query_result if True in [item.lower()in x['name'].lower() for item in filter_condition['name_contains']]]
            except KeyError:
                pass
            try:
                self.query_result = [x for x in self.query_result if [item.lower() for item in x['cuisine']] in filter_condition['cuisine'].lower()]
            except AttributeError:
                self.query_result =[x for x in self.query_result if True in [item.lower()in [dish.lower() for dish in x['cuisine']] for item in filter_condition['cuisine']]]
            except KeyError:
                pass
            try:
                if filter_condition['district'].lower() == 'sha tin':
                    self.query_result = [x for x in self.query_result if
                                         x['district'].lower() == 'shatin']
                else:
                    self.query_result = [x for x in self.query_result if x['district'].lower() in filter_condition['district'].lower()]
            except AttributeError:
                if 'sha tin' in [item.lower() for item in filter_condition['district']]:
                    self.query_result = [x for x in self.query_result if
                                         x['district'].lower() == 'shatin']
                else:
                    self.query_result = [x for x in self.query_result if
                                         x['district'].lower() in filter_condition['district'].lower()]
            except KeyError:
                pass
            try:
                range_price = re.split('-',filter_condition['price-range'].replace("$", ""))
                range_price = [float(x) for x in range_price]
                price = []
                if range_price[0] <= 50 and 0 <= range_price[1]:
                    price.append('Below $50')
                if range_price[0] <= 100 and 51 <= range_price[1]:
                    price.append('$51-100')
                if range_price[0] <= 200 and 101 <= range_price[1]:
                    price.append('$101-200')
                if range_price[0] <= 400 and 201 <= range_price[1]:
                    price.append('$201-400')
                if 801 <= range_price[1]:
                    price.append('Above $801')
                filter_condition['pricerange'] = price
                self.query_result = [x for x in self.query_result if x['price-range'] in filter_condition['pricerange']]
            except KeyError:
                pass
            try:
                self.query_result = [x for x in self.query_result if float(x['rating']) >= float(filter_condition['rating'])]
            except KeyError:
                pass
        except FileNotFoundError:
            pass

    def rank(self, ranking_weight):
        try:
            for x in self.query_result:
                v1= float(x['rating'])
                v2= float(math.sqrt((x['address'][0]-22.417875) ** (2) + (x['address'][1]-114.207263)** (2)))
                if x['price-range'] == 'Below $50':
                    v3 = 25
                elif x['price-range'] == '$51-100':
                    v3 = 75.5
                elif x['price-range'] == '$101-200':
                    v3 = 150.5
                elif x['price-range'] == '$201-400':
                    v3 = 300.5
                elif x['price-range'] == '$401-800':
                    v3 = 600.5
                elif x['price-range'] == 'Above $801':
                    v3 = 900.5
                v4=x['reviews'][2]/(x['reviews'][0]+x['reviews'][1]+x['reviews'][2])
                x['rank'] = ranking_weight[0]*v1 + ranking_weight[1]*v2 +ranking_weight[2]*v3 +ranking_weight[3]*v4
            self.query_result = sorted(self.query_result, key=lambda x : x['rank'], reverse=True)
            for x in self.query_result:
                x.pop('rank',None)
        except KeyError:
            pass

    def find_similar(self, restaurant, similiarity_weight, k):
        similiarlist = self.original_data
        u1 = float(restaurant['rating'])
        u2 = float(math.sqrt((restaurant['address'][0] - 22.417875) ** (2) + (restaurant['address'][1] - 114.207263) ** (2)))
        if restaurant['price-range'] == 'Below $50':
            u3 = 25
        elif restaurant['price-range'] == '$51-100':
            u3 = 75.5
        elif restaurant['price-range'] == '$101-200':
            u3 = 150.5
        elif restaurant['price-range'] == '$201-400':
            u3 = 300.5
        elif restaurant['price-range'] == '$401-800':
            u3 = 600.5
        elif restaurant['price-range'] == 'Above $801':
            u3 = 900.5
        u4 = restaurant['reviews'][2] / (restaurant['reviews'][0] + restaurant['reviews'][1] + restaurant['reviews'][2])
        for otherrestaurant in similiarlist:
                v1 = float(otherrestaurant['rating'])
                v2 = float(math.sqrt((otherrestaurant['address'][0] - 22.417875) ** (2) + (otherrestaurant['address'][1] - 114.207263) ** (2)))
                if otherrestaurant['price-range'] == 'Below $50':
                    v3 = 25
                elif otherrestaurant['price-range'] == '$51-100':
                    v3 = 75.5
                elif otherrestaurant['price-range'] == '$101-200':
                    v3 = 150.5
                elif otherrestaurant['price-range'] == '$201-400':
                    v3 = 300.5
                elif otherrestaurant['price-range'] == '$401-800':
                    v3 = 600.5
                elif otherrestaurant['price-range'] == 'Above $801':
                    v3 = 900.5
                v4 = otherrestaurant['reviews'][2] / (otherrestaurant['reviews'][0] + otherrestaurant['reviews'][1] + otherrestaurant['reviews'][2])
                otherrestaurant['similar'] = similiarity_weight[0]* abs(u1-v1) + similiarity_weight[1]* abs(u2-v2) + similiarity_weight[2]* abs(u3-v3)+ similiarity_weight[3]* abs(u4-v4)
        similiarlist.remove(restaurant)
        similiarlist= sorted(similiarlist, key=lambda x : x['similar'], reverse=False)
        if len(similiarlist) != k:
            if similiarlist[k-1] == similiarlist[k]:
                newsimiliarlist = similiarlist[:(k+1)]
            else:
                newsimiliarlist = similiarlist[:k]
        for x in newsimiliarlist:
            x.pop('similar', None)
        print("Top-10 similar restaurants:")
        for x in newsimiliarlist:
            print(x)

    def print_query_result(self):
        print('Overall number of query_result: %d' % len(self.query_result))
        for restaurant in self.query_result:
            print(restaurant)
