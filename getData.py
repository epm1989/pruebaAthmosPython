#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 14:02:09 2020

@author: root





"""
import ssl
import socket
import os, requests,time
from time import sleep
import matplotlib.pyplot as plt



f = open("getElapse_scrapy.txt", "w")
f.write("")
f.close()

f = open("getElapse_requestAPI.txt", "w")
f.write("")
f.close()

f = open("getElapse_WEBsocket.txt", "w")
f.write("")
f.close()

lista_alapsed_requestAPI=list()
url='https://api.tidex.com/api/3/ticker/eth_btc'

for i in range(10):
    
    ##opcion SCRAPY
    os.system('python3.6 scrapy2.py --nolog')
    
    ##opcion request API
    response = requests.get(url)
    json_response = response.json()
    delay1=response.elapsed.total_seconds()
    lista_alapsed_requestAPI.append(delay1)
    eldict = json_response['eth_btc']
    f = open("getElapse_requestAPI.txt", "a")
    f.write(str(delay1)+'\n')
    f.close()
    
    
    ##opcion socket
    
    socketHandler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketWraped = ssl.create_default_context().wrap_socket(socketHandler, server_hostname='api.tidex.com')
    starttimeSocket = time.perf_counter()
    socketWraped.connect(('api.tidex.com', 443))
    socketWraped.sendall(b"GET /api/3/ticker/eth_btc HTTP/1.1\r\nHost: api.tidex.com\r\nConnection: close\r\n\r\n")
    elapsed_time_socket=time.perf_counter()-starttimeSocket
    data = socketWraped.recv(1024)
    
    print(elapsed_time_socket)
    f = open("getElapse_WEBsocket.txt", "a")
    f.write(str(elapsed_time_socket)+'\n')
    f.close()
###################################################
#leer archivos
for i in range(10,0,-1):
    print('...'+str(i)+'...')
    sleep(0.5)
    
    
file1 = open("getElapse_scrapy.txt", "r")
listafile1=list()
for x in file1:
    delay1=float(x)
#    print(delay1)
    listafile1.append(delay1)


file2 = open("getElapse_requestAPI.txt", "r")
listafile2=list()
for y in file2:
    delay2=float(y)
#    print(delay2)
    listafile2.append(delay2)


file3 = open("getElapse_WEBsocket.txt", "r")
listafile3=list()
for z in file3:
    delay3=float(z)
#    print(delay2)
    listafile3.append(delay3)


plt.plot(range(len(listafile1)), listafile1, 'r--',range(len(listafile2)), listafile2, 'b--',range(len(listafile3)), listafile3, 'g--')
plt.xlabel('Muestras')
plt.ylabel('Delay en segundos')
plt.suptitle('(scrapy Rojo) Vs (API requests Azul) Vs  (WEB socket Verde)')
plt.show()


