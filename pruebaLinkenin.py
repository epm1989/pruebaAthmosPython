#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 12:31:57 2020

@author: epm1989
"""

import requests,subprocess 
from time import sleep
import matplotlib.pyplot as plt

NumMuestras=10
frecuencia=1

url='https://api.tidex.com/api/3/ticker/eth_btc'

counter=0
lista1=list()
lista2=list()
while True:
    #####
    response = requests.get(url)
    json_response = response.json()
    delay1=response.elapsed.total_seconds()
    lista1.append(delay1)
    eldict = json_response['eth_btc']
    #####
    out=subprocess.Popen(['curl', '-so', '/dev/null','-w','%{time_total}\n','https://api.tidex.com/api/3/ticker/eth_btc'], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    delay2=float((str(stdout, 'utf-8')[:-1]).replace(',','.'))
    lista2.append(delay2)
    #####
    sleep(frecuencia)
    counter +=1
    print(counter,delay1)
    print(counter,delay2)
    if counter >= NumMuestras:
        break



range(len(lista1))
# red dashes, blue squares and green triangles
plt.plot(range(len(lista1)), lista1, 'r--',range(len(lista2)), lista2,'b--')
plt.xlabel('Muestras')
plt.ylabel('Delay en segundos')
plt.suptitle('(Get request RED) Vs (curl by subprocess BLUE)')
plt.show()




