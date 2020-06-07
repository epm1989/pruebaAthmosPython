#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 15:43:56 2020

@author: root
https://saralgyaan.com/posts/python-realtime-plotting-matplotlib-tutorial-chapter-9-35-36/
"""


import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import requests,datetime,copy,json,ssl,socket
import threading, queue
#

##########

def funcionAPIrequest(url,q):
#    url='https://api.tidex.com/api/3/ticker/eth_btc'
    response = requests.get(url)
    json_response = response.json()
    apiTiempo = (json_response['eth_btc']['updated'])
    apiBuy = json_response['eth_btc']['buy']
    apiSell = json_response['eth_btc']['sell']
    apiAverage=0.5*(apiBuy+apiSell)
#    return [apiTiempo,apiAverage]
    q.put([apiTiempo,apiAverage])

def funcionSocket(url,q):
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
#    return [socketTiempo,socketAverage]
    q.put([socketTiempo,socketAverage])


lista_requestAPI,lista_apiTiempos,lista_apiAVGvalues=list(),list(),list()
lista_socketTiempos,lista_socketAVGvalues=list(),list()
dictpersonalizado={}
url='https://api.tidex.com/api/3/ticker/eth_btc'

#plt.style.use('fivethirtyeight')



q = queue.Queue()
s = queue.Queue()


def animate(i):
    a=threading.Thread(target=funcionSocket, args=('https://api.tidex.com/api/3/ticker/eth_btc',q))
    b=threading.Thread(target=funcionAPIrequest, args=('https://api.tidex.com/api/3/ticker/eth_btc',s))
    a.start()
    b.start()
    parAPI = q.get()
    parSocket = s.get()
    a.join();b.join()
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
   
    
    plt.cla()

    plt.title('Winner is= '+winner+', ('+dataX+', '+dataY+')',color=colortitulo)
    red_dot, = plt.plot(lista_apiTiempos,lista_apiAVGvalues, "r--", markersize=15)
    white_cross, = plt.plot(lista_socketTiempos,lista_socketAVGvalues, "b--", markeredgewidth=3, markersize=15)
    
    plt.legend([red_dot, white_cross], ["API_Req", "SocketCall"])



ani = FuncAnimation(plt.gcf(), animate, 100)


plt.ylabel('average sell-buy')
plt.xlabel('Tiempo')
plt.tight_layout()
plt.show()


