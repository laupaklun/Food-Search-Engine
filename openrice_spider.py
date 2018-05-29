import scrapy
import json
import io
import os

class OpenriceSpider(scrapy.Spider):
	name = 'openrice'
	allowed_domains = ['www.openrice.com']

	def start_requests(self):
		headers = {
			'accept-encoding': 'gzip, deflate, sdch, br',
			'accept-language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
			'upgrade-insecure-requests': '1',
			'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'cache-control': 'max-age=0',
		}
		with open('openrice_urls.txt') as f:
			content = f.readlines()
		content = [x.strip() for x in content]
		output_filename = 'openrice_data.json'
		with open(output_filename, mode='w', encoding='utf-8') as f:
			json.dump([], f)
		for url in content:
			yield scrapy.Request(url=url, headers=headers, callback=self.parse)
		try:
			with open('openrice_data.json', 'r') as file:
				accounts = json.load(file)
		except (OSError, ValueError):  # file does not exist or is empty/invalid
			accounts = {}
		with open('openrice_data.json', 'w') as file:
			json.dump(accounts, file, indent=2)


	def parse(self, response):
		output_filename = 'openrice_data.json'
		open(output_filename)
		# name = 'div.smaller-font-name::text'
		# pricerange = 'div.header-poi-price.dot-separator a::text'
		# latitude = 'div#poi-mapview-container.mapview-container::attr(data-latitude)'
		# longitude = 'div#poi-mapview-container.mapview-container::attr(data-longitude)'
		cuisinelist = 'div.header-poi-categories.dot-separator'
		cuisine = 'a[href]::text'
		rating = 'div.header-score::text'
		emotion = 'div.score-div::text'
		dataselector = 'script[type="application/ld+json"]::text'
		data = json.loads(str(response.css(dataselector).extract_first()))
		rice = {}
		address = []
		reviews =[]

		rice["name"]=data["name"]
		rice["cuisine"]= response.css(cuisinelist).css(cuisine).extract()
		rice["price-range"]=data["priceRange"]
		address.append(data["geo"]["latitude"])
		address.append(data["geo"]["longitude"])
		rice["address"]=address
		rice["rating"]=float(response.css(rating).extract_first())
		reviews.append(int(response.css(emotion).extract()[0]))
		reviews.append(int(response.css(emotion).extract()[1]))
		reviews.append(int(response.css(emotion).extract()[2]))
		rice["reviews"]= reviews
		if data["address"]["addressLocality"]=="Sha Tin":
			rice["district"] = "Shatin"
		else:
			rice["district"]=data["address"]["addressLocality"]
		rice["url"]=response.url
		with open(output_filename, mode='r', encoding='utf-8') as feedsjson:
			feeds = json.load(feedsjson)
		with open(output_filename, mode='w', encoding='utf-8') as feedsjson:
			feeds.append(rice)
			json.dump(feeds, feedsjson)