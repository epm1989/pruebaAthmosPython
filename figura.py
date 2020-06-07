
import tkinter as tk
import time

import json,copy
import datetime
import urllib.request as getBy_urllib
import requests,ssl,socket
import http.client as getBy_httpclient
import threading
import matplotlib.pyplot as plt
global listaURLLIB,listaHTTPCLIENT,listaAPI,listaSOCKET,contadorgrafico
listaURLLIB=list()
listaAPI=list()
listaHTTPCLIENT=list()
listaSOCKET=list()
contadorgrafico=0

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
    


###########################################################

class APP():
    def __init__(self):
        self.root = tk.Tk()
        self.root.minsize(840, 500)
        self.root.title('ETH_BTC')
        self.root.columnconfigure(0, weight=0)
        self.root.rowconfigure(0, weight=0)
        self.label = tk.Label(text="", font=('Helvetica', 48), fg='red')
        self.label1 = tk.Label(text="Method module request", font=('Helvetica', 22), fg='blue')
        self.label2 = tk.Label(text="Method module socket ssl", font=('Helvetica', 22), fg='blue')
        self.label3 = tk.Label(text="Method module urllib", font=('Helvetica', 22), fg='blue')
        self.label4 = tk.Label(text="Method module http.client", font=('Helvetica', 22), fg='blue')
        self.labelAVG= tk.Label(text='AVG Sell & Buy', font=('Helvetica', 22), fg='black')
        self.labelUpdate= tk.Label(text='query Time', font=('Helvetica', 22), fg='black')
        self.lavg1 = tk.Label(text='')
        self.lavg2 = tk.Label(text='')
        self.lavg3 = tk.Label(text='')
        self.lavg4 = tk.Label(text='')
        self.ltime1 = tk.Label(text='')
        self.ltime2 = tk.Label(text='')
        self.ltime3 = tk.Label(text='')
        self.ltime4 = tk.Label(text='')
        
        self.lactualWin = tk.Label(text='Winnerxxxx',font=('Helvetica', 32), fg='green')
        
        
        self.label1.place(x=1,y=160)
        self.label2.place(x=1,y=200)
        self.label3.place(x=1,y=240)
        self.label4.place(x=1,y=280)
        self.label.place(x=3,y=2)
        self.labelAVG.place(x=400,y=120)
        self.labelUpdate.place(x=630,y=120)
        self.lavg1.place(x=400,y=160)
        self.lavg2.place(x=400,y=200)
        self.lavg3.place(x=400,y=240)
        self.lavg4.place(x=400,y=280)
        self.ltime1.place(x=630,y=160)
        self.ltime2.place(x=630,y=200)
        self.ltime3.place(x=630,y=240)
        self.ltime4.place(x=630,y=280)
        self.lactualWin.place(x=200,y=380)
        
        

        
        self.update_clock()
        self.root.mainloop()

    def fetchdata(self):
        global listaURLLIB,listaHTTPCLIENT,listaAPI,listaSOCKET,contadorgrafico
        now = 'Linux Local Time -> '+time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        
        instancia=Fetch4MethodGET()    
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
        
        ##revisar maximimo y minimo
        """values=[tiempoSocket,tiempourllib,tiempohttpclient,tiempoAPI]"""
        values=[float(listaSOCKET[-1]['eth_btc']['updated']),float(listaURLLIB[-1]['eth_btc']['updated']),float(listaHTTPCLIENT[-1]['eth_btc']['updated']),float(listaAPI[-1]['eth_btc']['updated'])]
     
        winner=values.index(min(values))
#        print(values)
        
        WIN='........'
        
        if(winner == 0):
            WIN = "ganador SocketTLS"
            self.ltime2.configure(font=('Helvetica', 22), fg='green')
            self.ltime1.configure(font=('Helvetica', 12), fg='black')
            self.ltime3.configure(font=('Helvetica', 12), fg='black')
            self.ltime4.configure(font=('Helvetica', 12), fg='black')
        if(winner == 1):
            WIN = "ganador URLlib";
            self.ltime3.configure(font=('Helvetica', 22), fg='green')
            self.ltime1.configure(font=('Helvetica', 12), fg='black')
            self.ltime2.configure(font=('Helvetica', 12), fg='black')
            self.ltime4.configure(font=('Helvetica', 12), fg='black')
        if(winner == 2):
            WIN = "ganador HTTP.CLIENT";
            self.ltime4.configure(font=('Helvetica', 22), fg='green')
            self.ltime1.configure(font=('Helvetica', 12), fg='black')
            self.ltime2.configure(font=('Helvetica', 12), fg='black')
            self.ltime3.configure(font=('Helvetica', 12), fg='black')
        if(winner == 3):                    
            WIN='ganador RequestAPI';
            self.ltime1.configure(font=('Helvetica', 22), fg='green')
            self.ltime2.configure(font=('Helvetica', 12), fg='black')
            self.ltime3.configure(font=('Helvetica', 12), fg='black')
            self.ltime4.configure(font=('Helvetica', 12), fg='black')
        if(values[0] == values[1] == values[2] == values[3]):
            WIN='Resultado EMPATE- EQUAL'
            self.ltime1.configure(font=('Helvetica', 12), fg='black')
            self.ltime2.configure(font=('Helvetica', 12), fg='black')
            self.ltime3.configure(font=('Helvetica', 12), fg='black')
            self.ltime4.configure(font=('Helvetica', 12), fg='black')
         
            
            if contadorgrafico >=20:
                contadorgrafico =0
#                plt.ion()
                plt.xlabel('Muestras')
                plt.ylabel('Delay en segundos')
                xx1=[apiss['eth_btc']['updated'] for apiss in listaAPI ]
                yy1=[apiss['eth_btc']['buy'] for apiss in listaAPI ]
                xx2=[apiss['eth_btc']['updated'] for apiss in listaSOCKET ]
                yy2=[apiss['eth_btc']['buy'] for apiss in listaSOCKET ]
                xx3=[apiss['eth_btc']['updated'] for apiss in listaURLLIB ]
                yy3=[apiss['eth_btc']['buy'] for apiss in listaURLLIB ]
                xx4=[apiss['eth_btc']['updated'] for apiss in listaHTTPCLIENT ]
                yy4=[apiss['eth_btc']['buy'] for apiss in listaHTTPCLIENT ]
#                plt.plot(xx, yy, 'r--',xx, yy,'b--')
                plt.suptitle('Cuendo finalice de ver la grafica cierre "X" para continuar la consulta')
                red_dot, = plt.plot([(datetime.datetime.fromtimestamp(xxx1)) for xxx1 in xx1],yy1, "r*-", markersize=5)
                black_cross, = plt.plot([(datetime.datetime.fromtimestamp(xxx2)) for xxx2 in xx2],yy2, "bx-", markeredgewidth=3, markersize=8)
                blue_cross, = plt.plot([(datetime.datetime.fromtimestamp(xxx3)) for xxx3 in xx3],yy3, "b*-", markeredgewidth=3, markersize=8)
                green_cross, = plt.plot([(datetime.datetime.fromtimestamp(xxx4)) for xxx4 in xx4],yy4, "g+-", markeredgewidth=3, markersize=8)
                plt.legend([red_dot, black_cross, blue_cross,green_cross], ["APIreq", "SocketCall","URLlib","http.client"])
                plt.show()
                
 
                    
        
        #actualizar datos en pantalla
        
        
        
        self.lactualWin.configure(text=WIN)
        self.ltime1.configure(text=datetime.datetime.fromtimestamp(listaAPI[-1]['eth_btc']['updated']).strftime("%H:%M:%S"))
        self.ltime2.configure(text=datetime.datetime.fromtimestamp(listaSOCKET[-1]['eth_btc']['updated']).strftime("%H:%M:%S"))
        self.ltime3.configure(text=datetime.datetime.fromtimestamp(listaURLLIB[-1]['eth_btc']['updated']).strftime("%H:%M:%S"))
        self.ltime4.configure(text=datetime.datetime.fromtimestamp(listaHTTPCLIENT[-1]['eth_btc']['updated']).strftime("%H:%M:%S"))
        
        self.lavg1.configure(text=str(0.5*(listaAPI[-1]['eth_btc']['buy']+listaAPI[-1]['eth_btc']['sell'])))
        self.lavg2.configure(text=str(0.5*(listaSOCKET[-1]['eth_btc']['buy']+listaSOCKET[-1]['eth_btc']['sell'])))
        self.lavg3.configure(text=str(0.5*(listaURLLIB[-1]['eth_btc']['buy']+listaURLLIB[-1]['eth_btc']['sell'])))
        self.lavg4.configure(text=str(0.5*(listaHTTPCLIENT[-1]['eth_btc']['buy']+listaHTTPCLIENT[-1]['eth_btc']['sell'])))
        
        
        
        
    def update_clock(self):
        global contadorgrafico
        contadorgrafico+=1
        self.fetchdata()
        self.root.after(2000, self.update_clock)

app=APP()



#range(len(lista1))
## red dashes, blue squares and green triangles
#plt.plot(range(len(lista1)), lista1, 'r--',range(len(lista2)), lista2,'b--')
#plt.xlabel('Muestras')
#plt.ylabel('Delay en segundos')
#plt.suptitle('(Get request RED) Vs (curl by subprocess BLUE)')
#plt.show()
#plt.clf()
#plt.cla()
#plt.close()
#red_dot, = plt.plot(lista_apiTiempos,lista_apiAVGvalues, "r--", markersize=15)
#    white_cross, = plt.plot(lista_socketTiempos,lista_socketAVGvalues, "b--", markeredgewidth=3, markersize=15)
#    
#    plt.legend([red_dot, white_cross], ["API_Req", "SocketCall"])