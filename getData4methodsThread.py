#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 14:14:13 2020

@author: root
"""

import json,copy
import time
import urllib.request as getBy_urllib
import requests,ssl,socket
import http.client as getBy_httpclient
import threading, queue
global listaURLLIB,listaHTTPCLIENT,listaAPI,listaSOCKET
listaURLLIB=list()
listaAPI=list()
listaHTTPCLIENT=list()
listaSOCKET=list()

class Fetch4MethodGET():
    def __init__(self):
        self.HOSTNAME='api.tidex.com'
        self.URL='https://api.tidex.com/api/3/ticker/eth_btc'
        self.dominio='.com'
        self.__diccionatioAPI=dict()
        self.__diccionatioURLLIB=dict()
        self.__diccionatioHTTPCLIENT=dict()
        self.__diccionatioSOCKET=dict()
        
        
    def funcionURLlibrequest(self):
        global listaURLLIB
        req = getBy_urllib.Request(url=self.URL,method='GET')                           
        f= getBy_urllib.urlopen(req)
        response_urllib=f.read().decode('utf-8')
        json_urllib=json.loads(response_urllib) 
#        return json_urllib
        listaURLLIB.append(json_urllib)
        
    
    def funcionHTTPclient(self):
        global listaHTTPCLIENT
        g = getBy_httpclient.HTTPSConnection(self.HOSTNAME)
        g.request("GET", self.URL.split(self.dominio)[1])
        response_httpclient = g.getresponse().read().decode('utf-8')
        json_urlhttpclient=json.loads(response_httpclient)
#        return json_urlhttpclient
        listaHTTPCLIENT.append(json_urlhttpclient)
    
    def funcionAPIrequest(self):
        global listaAPI
        response = requests.get(self.URL)
        json_response = response.json()
#        print(json_response)
        listaAPI.append(json_response)
#        return json_response
    
    def funcionSocket(self):
        global listaSOCKET
        socketHandler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketWraped = ssl.create_default_context().wrap_socket(socketHandler, server_hostname=self.HOSTNAME)
        socketWraped.connect((self.HOSTNAME, 443))
        HEADER="GET "+self.URL.split(self.dominio)[1]+" HTTP/1.1\r\nHost: "+self.HOSTNAME+"\r\nConnection: close\r\n\r\n"
        socketWraped.sendall(bytes(HEADER,'utf-8'))
        data = socketWraped.recv(1024)
        ere=(str(copy.copy(data)).split('\\r\\n\\r\\n')[1])[:-1]
        bodysocket_response=json.loads(ere) 
        listaSOCKET.append(bodysocket_response)
#        print(bodysocket_response)
#        return bodysocket_response
    

instancia=Fetch4MethodGET()    

#q = queue.Queue()
a=threading.Thread(target=instancia.funcionAPIrequest ,args=())
b=threading.Thread(target=instancia.funcionSocket ,args=())
c=threading.Thread(target=instancia.funcionURLlibrequest ,args=())
d=threading.Thread(target=instancia.funcionHTTPclient ,args=())
a.start()
b.start()
c.start()
d.start()
d.join()
c.join()
b.join()
a.join()
#result=[instancia.funcionAPIrequest(),instancia.funcionHTTPclient(),instancia.funcionSocket(),instancia.funcionURLlibrequest()]

#print(result)

#apiTiempo = (json_response['eth_btc']['updated'])
#    apiBuy = json_response['eth_btc']['buy']
#    apiSell = json_response['eth_btc']['sell']
#    apiAverage=0.5*(apiBuy+apiSell)