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
##        'https://www.google.com/',
    )

    
##    def __init__(self):
##        self.setting_options()

    def setting_options(self):
        try:        
##            options = webdriver.ChromeOptions()
##            options.add_argument("--start-maximized")
##            options.add_argument("--disable-javascript")
##            options.add_argument("--disable-java")
##            options.add_argument("--disable-plugins")
##            options.add_argument("--disable-popup-blocking")        
##            options.add_argument("--disable-images")      
##            self.driver = webdriver.Chrome('c://chromedriver.exe',chrome_options = options)
            self.driver = webdriver.Firefox()
        except Exception as e:
            #driver.refresh()
            print e

    def read_csv(self, file='outputdatafinal.csv'):
        # with open(file,'rb') as mf:
        mf = open(file,'rb')
        reader = csv.reader(mf)
        return reader

    def read_text(self, file='locations.txt'):
        f = open(file,'rb')
        lines = f.readlines()
        return lines


    def get_counties(self, file= 'counties.json'):
        with open(file,'rb') as cf:
            return json.loads(cf.read())
        
    def parse(self, response):
        print "here in parse"
        locations = self.read_text()
        search_terms = self.read_text('search_terms.txt')
        pause = 4        
        driver = webdriver.Firefox()
##        driver = webdriver.Chrome('c://chromedriver.exe')
        while True:
            for search_term in search_terms:
                for location in locations:
                    if search_term.strip() and location.strip():
                        print '{0}, {1}'.format(search_term.strip('\r\n'), location.strip('\r\n'))
                        try:
                            driver.get(response.url)        
                            search_elem = driver.find_element_by_name("q")
                            search_elem.clear()
                            search_elem.send_keys('{0}, {1}'.format(search_term.strip('\r\n'), location.strip('\r\n'))) #search term putted into the search field.                    
                            time.sleep(4)
                            search_btn_elem = driver.find_elements_by_class_name('searchbox-searchbutton')
                            search_btn_elem[0].click()
                            time.sleep(6)
                        except Exception as e:
                            print e.message                            

                            
                        for x in range(4):
                            properties_xpaths = driver.find_elements_by_xpath('//div[@class="widget-pane-section-result"]')
                            for ctr,elem in enumerate(properties_xpaths):
                                properties_list = driver.find_elements_by_xpath('//div[@class="widget-pane-section-result"]')
                                print len(properties_list)
                                try:
                                    properties_list[ctr].click()
                                    time.sleep(3)
                                except Exception as e:
                                    print e.message
                                    
                                    
        ##                            driver.get(response.url)
                                    
        ##                        elem.click()
                                

                                """Gathering info from detail page"""
                                html = driver.page_source
                                hxs = lxml.html.fromstring(html)

                                item = GooglepropertyItem()
                                
                                company = hxs.xpath('//div[@class="widget-pane-section-header-title"]/h1[1]/text()')
                                print company
                                if company:
                                    item['Company'] = company
                                    item['SearchTerm'] = '{0}, {1}'.format(search_term.strip('\r\n'), location.strip('\r\n'))

                                category = hxs.xpath('//button[@jsaction="pane.rating.category"]/text()')
                                print category
                                if category:
                                    item['Category'] = category

                                address = hxs.xpath('//span[@class="widget-pane-section-info-text"]/span/span/text()')
                                print address
                                if address:
                                    address = address[0].split(',')
                                    street = address[0]                            
                                    city = address[1]
                                    item['Address'] = address
                                    item['Street'] = street
                                    item['City'] = city
                                    
                                    if len(address) >= 3:
                                        state_and_zip = address[2].split()
                                        state = state_and_zip[0]
                                        zip_code = state_and_zip[1]                                
                                        item['State'] = state
                                        item['Zipcode'] = zip_code                                                        
                                
                                phone = hxs.xpath('//span[@class="widget-pane-section-info-icon maps-sprite-pane-info-phone"]/following-sibling::span//a/text()')
                                if phone:
                                    item['Phone'] = phone
                                    print phone

                                website = hxs.xpath('//a[contains(@data-attribution-url,"http:")]/@href')
                                if website:
                                    item['Website'] = website
                                    print website


                                print item
                                yield item
    ##                            driver.execute_script("window.history.go(-1)")
    ##                            time.sleep(3)

                                try:
                                    """Moving back to the original listing page"""
                                    back_to_results = driver.find_element_by_xpath('//button[@class="widget-pane-section-back-to-list-button blue-link noprint"]')
                                    back_to_results.click()
                                    time.sleep(2)
                                    print "after clicking back"
                                except Exception as e:
                                    print e.message
                                    
                                    
                            #clicking next arrow
                            try:
                                next_btn = driver.find_element_by_xpath('//button[@id="widget-pane-section-pagination-button-next"]')
                                print next_btn
                                if next_btn:
                                    next_btn.click()
                                    time.sleep(3)
                            except Exception as e:
                                break
                                
                                print e.message
                                

##                    driver.refresh()
                        
                    


##                        try:
##                            """Moving back to the original listing page"""
##                            back_to_results = driver.find_element_by_xpath('//button[@class="widget-pane-section-back-to-list-button blue-link noprint"]')
##                            back_to_results.click()
##                            time.sleep(2)
##                            print "after clicking back"
##                        except Exception as e:
##                            print e.message
##
##                    driver.get(response.url)
