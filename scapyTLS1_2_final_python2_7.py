#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 12:33:40 2020

@author: epm1989
"""
import logging,sys
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

if(len(sys.argv) == 3):
    HOSTNAME = str(sys.argv[1])
    URL = str(sys.argv[2])
else:
    HOSTNAME='api.tidex.com'
    URL='/api/3/ticker/eth_btc'
    
#print(HOSTNAME,URL)
try:
    # This import works from the project directory
    from scapy_ssl_tls.ssl_tls import *
except ImportError:
    # If you installed this package via pip, you just need to execute this
    from scapy.layers.ssl_tls import *
#HOSTNAME='api.macvendors.com'
#URL='/000c00'
#HOSTNAME='github.com'
#URL='/public-apis/public-apis'
#HOSTNAME='worldtimeapi.org'
#URL='/api/ip'


tls_version = TLSVersion.TLS_1_2
ciphers = [TLSCipherSuite.ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,49196,49195,49200,159,52392,52394.49195,49199,52393,49161,4866,TLSCipherSuite.DHE_RSA_WITH_AES_256_GCM_SHA384]  #159

extensions = [
              TLSExtension() / TLSExtECPointsFormat(),
              TLSExtension() / TLSExtSupportedGroups(),
              TLSExtension() / TLSExtPSKKeyExchangeModes(),
              TLSExtension() / TLSExtServerNameIndication(server_names=TLSServerName(data=HOSTNAME))
              ]
#              TLSExtension() / TLSExtHeartbeat(),
#              TLSExtension() / TLSExtSessionTicketTLS(),
#              TLSExtension() / TLSExtRenegotiationInfo(),
#              TLSExtension() / TLSExtSignatureAlgorithms(),
#              TLSExtension() / TLSExtSupportedVersions(),
#              TLSExtension() / TLSExtKeyShare(),
#              TLSExtension() / TLSExtPadding(),
#              TLSExtension() / TLSExtPSKKeyExchangeModes(),
#              TLSExtension() / TLSExtCertificateStatusRequest(),
#              TLSExtension() / TLSExtMaxFragmentLength(),
#              TLSExtension() / TLSExtCertificateURL(),
#              ]
              
compression_methods=[0]

ip = (HOSTNAME, 443)
with TLSSocket(client=True) as tls_socket:
    try:
        tls_socket.connect(ip)
#            print("Connected to server: %s" % (ip,))
    except socket.timeout:
        pass
#            print("Failed to open connection to server: %s" % (ip,), file=sys.stderr)
    else:
        try:
            server_hello, server_kex = tls_socket.do_handshake(tls_version, ciphers,extensions)
#                server_hello.show()
#                print(type(server_hello))
            pass
        except TLSProtocolError as tpe:
#            print("Got TLS error: %s" % tpe, file=sys.stderr)
#            tpe.response.show()
            pass
        else:
            resp = tls_socket.do_round_trip(TLSPlaintext(data="GET {0} HTTP/1.1\r\nHOST: {1}\r\n\r\n".format(URL,HOSTNAME)))
#            print("Got response from server")
#            print('..................................................--------------------')
#            resp.show()
#            print(dir(resp),(type(resp)))
#            print('..................................................')
        finally:
#                print(tls_socket.tls_ctx)
            pass


print(repr(resp).split('\\r\\n\\r\\n')[1].split('explicit_iv')[0][:-2])
