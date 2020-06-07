#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 12:35:19 2020

@author: root
"""

import requests,datetime,time,copy,json,ssl,socket
import matplotlib.pyplot as plt
import numpy as np


def funcionAPIrequest(url='https://api.tidex.com/api/3/ticker/eth_btc',*args,**kwargs):
    response = requests.get(url)
    json_response = response.json()
    apiTiempo = (json_response['eth_btc']['updated'])
    apiBuy = json_response['eth_btc']['buy']
    apiSell = json_response['eth_btc']['sell']
    apiAverage=0.5*(apiBuy+apiSell)
    return [apiTiempo,apiAverage]

def funcionSocket(*args,**kwargs):
    socketHandler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketWraped = ssl.create_default_context().wrap_socket(socketHandler, server_hostname='api.tidex.com')
    socketWraped.connect(('api.tidex.com', 443))
    socketWraped.sendall(b"GET /api/3/ticker/eth_btc HTTP/1.1\r\nHost: api.tidex.com\r\nConnection: close\r\n\r\n")
    data = socketWraped.recv(1024)
    ere=(str(copy.copy(data)).split('\\r\\n\\r\\n')[1])[:-1]
    bodysocket_response=json.loads(ere) 
    socketTiempo = (bodysocket_response['eth_btc']['updated'])
    socketBuy = bodysocket_response['eth_btc']['buy']
    socketSell = bodysocket_response['eth_btc']['sell']
    socketAverage=0.5*(socketBuy+socketSell)
    return [socketTiempo,socketAverage]


lista_requestAPI,lista_apiTiempos,lista_apiAVGvalues=list(),list(),list()
lista_socketTiempos,lista_socketAVGvalues=list(),list()
dictpersonalizado={}
url='https://api.tidex.com/api/3/ticker/eth_btc'

for i in range(10):
    
    offsetTiempo=(time.mktime(datetime.datetime.now().timetuple()))
    
    
    parAPI=funcionAPIrequest()
    parSocket=funcionSocket()
    
    
    lista_apiTiempos.append(datetime.datetime.fromtimestamp(parAPI[0]))
    lista_apiAVGvalues.append(parAPI[1])
    lista_socketTiempos.append(datetime.datetime.fromtimestamp(parSocket[0]))
    lista_socketAVGvalues.append(parSocket[1])
    
#    dictpersonalizado['api']={'apiTiempo':apiTiempo}
#    dictpersonalizado['api']['apiAVGvalue']=apiAverage
#    dicti=None
#    dicti=copy.copy(dictpersonalizado)
#    print(dicti)
#    lista_requestAPI.append(dicti)
    time.sleep(2)

#

#dates = matplotlib.dates.date2num(lista_apiTiempos)

#plt.plot(dates, lista_apiAVGvalues,'r*-',0.00007+dates, range(10),'b*-');
#matplotlib.pyplot.plot_date(dates, range(10),fmt='r*-')
#
#matplotlib.pyplot.plot_date(dates, range(10),'r*-',dates, range(10,20),'b*-')
plt.plot(lista_apiTiempos, lista_apiAVGvalues,'r*-',lista_socketTiempos, lista_socketAVGvalues,'b*-');
plt.show()

print('fin')




