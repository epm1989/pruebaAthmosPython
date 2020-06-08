#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 14:14:13 2020

@author: root
"""

import json,copy
import time
import urllib.request as getBy_urllib
import requests,ssl,socket,subprocess
import http.client as getBy_httpclient


class Fetch4MethodGET():
    def __init__(self):
        self.HOSTNAME='api.tidex.com'
        self.URL='https://api.tidex.com/api/3/ticker/eth_btc'
        self.dominio='.com'
        
        
    def funcionURLlibrequest(self):
        req = getBy_urllib.Request(url=self.URL,method='GET')                           
        f= getBy_urllib.urlopen(req)
        response_urllib=f.read().decode('utf-8')
        json_urllib=json.loads(response_urllib) 
        return json_urllib
        
    
    def funcionHTTPclient(self):
        g = getBy_httpclient.HTTPSConnection(self.HOSTNAME)
        g.request("GET", self.URL.split(self.dominio)[1])
        response_httpclient = g.getresponse().read().decode('utf-8')
        json_urlhttpclient=json.loads(response_httpclient)
        return json_urlhttpclient
    
    
    def funcionAPIrequest(self):
        response = requests.get(self.URL)
        json_response = response.json()
        return json_response
    
    def funcionSocket(self):
        socketHandler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketWraped = ssl.create_default_context().wrap_socket(socketHandler, server_hostname=self.HOSTNAME)
        socketWraped.connect((self.HOSTNAME, 443))
        HEADER="GET "+self.URL.split(self.dominio)[1]+" HTTP/1.1\r\nHost: "+self.HOSTNAME+"\r\nConnection: close\r\n\r\n"
        socketWraped.sendall(bytes(HEADER,'utf-8'))
        data = socketWraped.recv(1024)
        ere=(str(copy.copy(data)).split('\\r\\n\\r\\n')[1])[:-1]
        bodysocket_response=json.loads(ere) 
        return bodysocket_response
    
    def funcionScapy(self):
        #python scapyTLS1_2_final_python2_7.py api.tidex.com /api/3/ticker/eth_btc 2>/dev/null
        out=subprocess.Popen(['python', 'scapyTLS1_2_final_python2_7.py', 'api.tidex.com','/api/3/ticker/eth_btc','2>/dev/null'], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        stdout,stderr = out.communicate()
        salidascapy=str(stdout, 'utf-8')
        response_Scapy=salidascapy.split('why)')[1]
        json_scapy=json.loads(response_Scapy) 
        return json_scapy


instancia=Fetch4MethodGET()    

result=[instancia.funcionAPIrequest(),instancia.funcionHTTPclient(),instancia.funcionSocket(),instancia.funcionURLlibrequest(),instancia.funcionScapy()]

print(result)

#apiTiempo = (json_response['eth_btc']['updated'])
#    apiBuy = json_response['eth_btc']['buy']
#    apiSell = json_response['eth_btc']['sell']
#    apiAverage=0.5*(apiBuy+apiSell)