# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GooglepropertyItem(scrapy.Item):
    # define the fields for your item here like:    
   	row = scrapy.Field()
   	CompanyName = scrapy.Field()
   	Address = scrapy.Field()
	City = scrapy.Field()
	State = scrapy.Field()
	Zipcode = scrapy.Field()
	URL = scrapy.Field()
	Phone = scrapy.Field()
	NoOfReviews = scrapy.Field()
	AverageReview = scrapy.Field()
