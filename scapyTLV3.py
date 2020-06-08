##CKIENT HELLO
from __future__ import print_function
import sys
try:
    import scapy.all as scapy
except ImportError:
    import scapy

try:
    # This import works from the project directory
    from scapy_ssl_tls.ssl_tls import *
except ImportError:
    # If you installed this package via pip, you just need to execute this
    from scapy.layers.ssl_tls import *

import socket

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print ("USAGE: <host> <port>")
#        exit(1)
#https://macvendors.co/api
    target = ('scapy.readthedocs.io', 443)
    target = ('macvendors.com', 443)
#    target = ('api.tidex.com', 443)
    # create tcp socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(target)

    # create TLS Handhsake / Client Hello packet
    p = TLSRecord(version="TLS_1_2") / TLSHandshakes(handshakes=[TLSHandshake() /
                                                TLSClientHello(version="TLS_1_2",compression_methods=list(range(0xff)),cipher_suites=list(range(0xff)))])
#    ciphers = [TLSCipherSuite.TLS_AES_256_GCM_SHA384, TLSCipherSuite.TLS_AES_128_GCM_SHA256]
#    TLSCipherSuite.RSA_WITH_AES_128_CBC_SHA
#    =x1301 -> 4865
#    aes128 gcm  sha256
    p.show()
    print ("sending TLS payload")
    s.sendall(str(p))
    resp = s.recv(1024 * 8)
    print ("received, %d --  %s" % (len(resp), repr(resp)))
    SSL(resp).show()
    s.close()