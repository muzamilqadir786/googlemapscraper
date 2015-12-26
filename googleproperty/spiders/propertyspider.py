# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
from scrapy.selector import Selector
from scrapy.http import Request
import lxml.html
from googleproperty.items import GooglepropertyItem
import xlrd
from xlrd import open_workbook
from xlutils.copy import copy
import csv
import json

import sys
# reload(sys)
# sys.setdefaultencodig('utf-8')

class Propertyspider(scrapy.Spider):
    name = "googleproperty"
    allowed_domains = ["google.com/spider"]
    start_urls = (
        'https://www.google.com/maps/',
    )

    def __init__(self):
        self.setting_options()

    def setting_options(self):
        try:        
            options = webdriver.ChromeOptions()
            options.add_extension("c://block.crx")
            # options.add_extension("c://browsec.crx") #To use proxy extension to avoid blocking.
            options.add_argument("--start-maximized")
            options.add_argument("--disable-javascript")
            options.add_argument("--disable-java")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-popup-blocking")        
            options.add_argument("--disable-images")      
            self.driver = webdriver.Chrome('c://chromedriver.exe',chrome_options = options) 
        except Exception as e:
            #driver.refresh()
            print e

    def read_csv(self, file='outputdatafinal.csv'):
        # with open(file,'rb') as mf:
        mf = open(file,'rb')
        reader = csv.reader(mf)
        return reader


    def get_counties(self, file= 'counties.json'):
        with open(file,'rb') as cf:
            return json.loads(cf.read())


    def parse(self, response):
        counties = self.get_counties()
        rows = self.read_csv()
        print rows
        cols = rows.next()
        pause = 4
        rows = list(rows)
        for ctr,row in enumerate(rows,start=1):
            if not row[-5]:
                row = rows[ctr]

                property_location = row[4]
                file_name_col = row[-1]
                file_name = file_name_col.replace('.csv','.zip')
                district = counties[file_name].values()[0]
                print ctr
                print file_name,district
                driver = self.driver
                driver.get(response.url)

                search_elem = driver.find_element_by_name("q")
                search_elem.clear()
                search_elem.send_keys('{0}, {1}, {2}'.format(property_location, district, 'NJ')) #search term putted into the search field.
                # search_elem.send_keys(Keys.RETURN)
                time.sleep(pause)
                search_btn_elem = driver.find_elements_by_class_name('searchbox-searchbutton')
                search_btn_elem[0].click()
                time.sleep(3)

                html = driver.page_source
                hxs = lxml.html.fromstring(html)

                # properties = hxs.xpath('//h3[@class="cards-categorical-list-item-info"]')
                # properties_xpath = driver.find_elements_by_xpath('//h3[@class="cards-categorical-list-item-info"]')
                # print properties

                item = GooglepropertyItem()
                item['row'] = ctr
                #address = hxs.xpath('//h1[@class="cards-entity-title cards-strong cards-text-truncate-and-wrap"]/span/text()')
                address = hxs.xpath('//h1[@id="widget-pane-section-header-title"]/text()')
                #city_state_zip = hxs.xpath('//div[@class="cards-entity-address cards-strong"]/div/span/text()')
                city_state_zip = hxs.xpath('//h2[@class="widget-pane-section-header-subtitle"]/text()')
                print address
                print city_state_zip

                item['Address'] = address
                if city_state_zip:
                    city_state_zip = city_state_zip[0].split(',')
                    try:
                        item['City'] = city_state_zip[0]
                        state_zip = city_state_zip[1]
                    except IndexError:
                        state_zip = ''
                    state_zip = state_zip.split()
                    if state_zip:
                        try:
                            item['State'] = state_zip[0]
                            item['Zipcode'] = state_zip[1]
                        except IndexError:
                            item['State'] = ''
                            item['Zipcode'] = ''

                yield item

            #     item['Zipcode'] = zipcode
            #     item['State'] = state


            # for ctr,propertyd in enumerate(properties):
            #     print propertyd
            #     title = propertyd.xpath('./div[@class="cards-categorical-list-item-title cards-strong"]/span/text()')
            #     print title
            #     rating_score = propertyd.xpath('.//span[@class="cards-rating-score"]/text()')
            #     number_of_ratings = propertyd.xpath('.//div[@class="cards-categorical-list-item-num-ratings"]/span/text()')
            #     address = propertyd.xpath('./div[@class="cards-categorical-list-item-address"]/span/text()')
            #     print address
            #     if address:
            #         address = address[0].split(',')
            #         state = address[-1]
            #         zipcode = address[-2]
            #         property_city = address[-3]
            #         saddress = ','.join(address[:2])
            #
            #     item['CompanyName'] = title
            #     item['Address'] = saddress
            #     item['City'] = property_city
            #     item['Zipcode'] = zipcode
            #     item['State'] = state
            #     item['NoOfReviews'] = number_of_ratings
            #     item['AverageReview'] = rating_score
            #
            #     try:
            #         print properties_xpath[ctr]
            #         properties_xpath[ctr].click()
            #         time.sleep(2)
            #         url_and_phone_html = driver.page_source
            #         url_and_phone_hxs = lxml.html.fromstring(url_and_phone_html)
            #         url = url_and_phone_hxs.xpath('//div[@class="cards-entity-url"]/a/span/text()')
            #         phone = url_and_phone_hxs.xpath('//div[@class="cards-entity-phone"]/span/text()')
            #         print url
            #         print phone
            #         item["URL"] = url
            #         item["Phone"] = phone
            #         yield item
            #
            #         list_all_records_link = driver.find_element_by_xpath('//div[@class="cards-categorical-list-context-card"]/a')
            #         if list_all_records_link:
            #             list_all_records_link.click()
            #             time.sleep(2)
            #     except Exception as e:
            #         print e



            """Click next arrow to get the new 10 properties """
            # try:
            #     elem = driver.find_elements_by_xpath('//span[@class="cards-categorical-pagination-button-right"]/..')
            #     if elem:
            #         elem[0].click()
            # except Exception as e:
            #     print e
            #     break

            # time.sleep(5)
            # driver.quit()
                
