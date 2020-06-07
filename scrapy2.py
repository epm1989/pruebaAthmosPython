#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 12:32:08 2020

@author: root
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from time import sleep
import matplotlib.pyplot as plt
from datetime import datetime , timedelta

class QuotesSpider(scrapy.Spider):
    name = "Bot"
    def __init__(self, stats):
        self.stats = stats
        self.lista_alapsed_scrapy=list()


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)
    def start_requests(self):
        urls = [
            'https://api.tidex.com/api/3/ticker/eth_btc'
        ]
        
        for url in urls:
            
            yield scrapy.Request(url=url, callback=self.parse)
            
           
#            el=self.stats.get_stats()
#            print(el['start_time'])
#            duracion=(datetime.now()+ timedelta(hours=5)) - el['start_time']
#            print(duracion)
#            print(str(duracion.seconds))
#            print(str(duracion.microseconds))
#            print(str(ffin))
#            print(str(finicio))
#            print(str((ffin-finicio).microseconds))
            
#            print('Work time:', duracion.time.strftime("%S"))
#            for llave,valor in el:
#                print(llave,valor)
#                
            print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
            
    def parse(self, response):
        #print(response.url.split("/")[-2])
        #self.stats.get_value('item_scraped_count')
        
        banner='''
  _| || |_ _| || |_ _| || |_ _| || |_ _| || |_  
 |_  __  _|_  __  _|_  __  _|_  __  _|_  __  _| 
  _| || |_ _| || |_ _| || |_ _| || |_ _| || |_  
 |_  __  _|_  __  _|_  __  _|_  __  _|_  __  _| 
   |_||_|   |_||_|   |_||_|  _|_||_|   |_||_|   
  _| || |_  |  _ \          | |        _| || |_ 
 |_  __  _| | |_) | ___   __| |_   _  |_  __  _|
  _| || |_  |  _ < / _ \ / _` | | | |  _| || |_ 
 |_  __  _| | |_) | (_) | (_| | |_| | |_  __  _|
   |_||_|   |____/ \___/ \__,_|\__, |   |_||_|  
                                __/ |           
    _  _     _  _     _  _     |___/    _  _    
  _| || |_ _| || |_ _| || |_ _| || |_ _| || |_  
 |_  __  _|_  __  _|_  __  _|_  __  _|_  __  _| 
  _| || |_ _| || |_ _| || |_ _| || |_ _| || |_  
 |_  __  _|_  __  _|_  __  _|_  __  _|_  __  _| 
   |_||_|   |_||_|   |_||_|   |_||_|   |_||_| 
        
        '''
        banner2='''
    _  _     _  _     _  _     _  _     _  _     _  _  
  _| || |_ _| || |_ _| || |_ _| || |_ _| || |_ _| || |_ 
 |_  __  _|_  __  _|_  __  _|_  __  _|_  __  _|_  __  _|
  _| || |_ _| || |_ _| || |_ _| || |_ _| || |_ _| || |_ 
 |_  __  _|_  __  _|_  __  _|_  __  _|_  __  _|_  __  _|
   |_||_|   |_||_|   |_||_|   |_||_|   |_||_|   |_||_| 
        '''
        print(banner)
        print(response.body)
        
        print('#############################################################')
        el=self.stats.get_stats()
        print(el['start_time'])
        duracion=(datetime.now()+ timedelta(hours=5)) - el['start_time']
        print(duracion)
        print('tiempo de duracione en SEG: '+str(duracion.microseconds/1000000))
        f = open("getElapse_scrapy.txt", "a")
        f.write(str(duracion.microseconds/1000000)+'\n')
        f.close()
        print('#############################################################')
        print(banner2)
        self.lista_alapsed_scrapy.append(duracion.microseconds/1000000)
        print(self.lista_alapsed_scrapy)

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
crawler = process.create_crawler(QuotesSpider)
process.crawl(crawler)
process.start()







