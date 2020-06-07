#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 15:43:56 2020

@author: root
https://saralgyaan.com/posts/python-realtime-plotting-matplotlib-tutorial-chapter-9-35-36/
"""


import random,time
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import requests,datetime,copy,json,ssl,socket


##########

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

#plt.style.use('fivethirtyeight')

x_values = []
y_values = []
w_values = []
z_values = []

index = count()



def animate(i):
    
    parSocket=funcionSocket()
    parAPI=funcionAPIrequest()
    
    lista_apiTiempos.append(datetime.datetime.fromtimestamp(parAPI[0]))
    lista_apiAVGvalues.append(parAPI[1])
    lista_socketTiempos.append(datetime.datetime.fromtimestamp(parSocket[0]))
    lista_socketAVGvalues.append(parSocket[1])
    winner=None
    dataY=None
    dataX=None
    if parAPI[0] < parSocket[0]:
        winner='API'
        colortitulo='red'
        dataX=datetime.datetime.fromtimestamp(parAPI[0]).strftime("%H:%M:%S")
        dataY=str(parAPI[1])
    elif parAPI[0] > parSocket[0]:
        winner='Socket'
        colortitulo='blue'
        dataX=datetime.datetime.fromtimestamp(parSocket[0]).strftime("%H:%M:%S")
        dataY=str(parSocket[1])
    else:
        winner='EQuAL'
        colortitulo='black'
        dataX=datetime.datetime.fromtimestamp(parAPI[0]).strftime("%H:%M:%S")
        dataY=str(parAPI[1])
        
            
#    time.sleep(2)
    x_values.append(next(index))
    y_values.append(random.randint(0, 5))
    w_values.append(next(index))
    z_values.append(random.randint(0, 5)*2)
    
    plt.cla()
#    plt.plot(x_values, y_values,'r*-',w_values, z_values,'b*-')
#    plt.plot(lista_apiTiempos, lista_apiAVGvalues,'r*-',lista_socketTiempos, lista_socketAVGvalues,'b*-')
    #plt.suptitle('(requests Rojo) Vs (socket Azul) -> Winner is= '+winner,color='red')
    plt.title('Winner is= '+winner+', ('+dataX+', '+dataY+')',color=colortitulo)
    red_dot, = plt.plot(lista_apiTiempos,lista_apiAVGvalues, "r*-", markersize=15)
    # Put a white cross over some of the data.
    white_cross, = plt.plot(lista_socketTiempos,lista_socketAVGvalues, "bx-", markeredgewidth=3, markersize=15)
    
    plt.legend([red_dot, white_cross], ["API_Req", "SocketCall"])



ani = FuncAnimation(plt.gcf(), animate, 100)


plt.ylabel('average sell-buy')
plt.xlabel('Tiempo')
plt.tight_layout()
plt.show()