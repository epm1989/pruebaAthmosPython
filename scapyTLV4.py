#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 11:00:23 2020

@author: root
"""

import sys
from scapy_ssl_tls.ssl_tls import *
import scapy_ssl_tls.ssl_tls_keystore as tlsk
import tinyec.ec as ec
import tinyec.registry as ec_reg

def main():
    err = 0
    server = ('api.tidex.com', 443)
    server = ('macvendors.com', 443)
    # TODO: encapsulate this into a nicer interface
    nist256 = ec_reg.get_curve(TLS_SUPPORTED_GROUPS[TLSSupportedGroup.SECP256R1])
    keypair = ec.make_keypair(nist256)
    ec_pub = tlsk.point_to_ansi_str(keypair.pub)
    
    draft_version = 18
    ciphers = [TLSCipherSuite.TLS_AES_256_GCM_SHA384, TLSCipherSuite.TLS_AES_128_GCM_SHA256]
    ciphers = list(range(0xff))
    
    key_share = TLSExtension() / TLSExtKeyShare() / TLSClientHelloKeyShare(client_shares=[TLSKeyShareEntry(named_group=TLSSupportedGroup.SECP256R1,
                                                                                                           key_exchange=ec_pub)])
    named_groups = TLSExtension() / TLSExtSupportedGroups(named_group_list=[TLSSupportedGroup.SECP256R1,
                                                                            TLSSupportedGroup.SECP384R1,
                                                                            TLSSupportedGroup.SECP521R1])
    extensions = [TLSExtension() / TLSExtServerNameIndication(server_names=TLSServerName(data=server[0])),
                  TLSExtension() / TLSExtRenegotiationInfo(),
                  named_groups,
                  TLSExtension() / TLSExtECPointsFormat(),
                  TLSExtension(type=TLSExtensionType.SESSIONTICKET_TLS),
                  TLSExtension() / TLSExtALPN(),
                  TLSExtension(type=TLSExtensionType.SIGNED_CERTIFICATE_TIMESTAMP),
                  key_share,
                  TLSExtension() / TLSExtSupportedVersions(versions=[tls_draft_version(draft_version)]),
                  TLSExtension() / TLSExtSignatureAlgorithms()]
    
    
    with TLSSocket(client=True) as tls_socket:
        tls_socket.tls_ctx.client_ctx.shares.append(tlsk.ECDHKeyStore.from_keypair(nist256, keypair))
        tls_socket.connect(server)
        try:
            pkt = TLSRecord() / TLSHandshakes(handshakes=[TLSHandshake() / TLSClientHello(cipher_suites=ciphers, extensions=extensions)])
            r = tls_socket.do_round_trip(pkt)
            r.show()
            r = tls_socket.do_round_trip(TLSHandshakes(handshakes=[TLSHandshake() / TLSFinished(data=tls_socket.tls_ctx.get_verify_data())]), recv=False)
            r = tls_socket.do_round_trip(TLSPlaintext("GET / HTTP/1.1\r\nHOST: macvendors.com\r\n\r\n"))
            r.show()
        except TLSProtocolError as tpe:
            print(tpe)
            tpe.response.show()
            err +=1
        finally:
            print(tls_socket.tls_ctx)
    return err

if __name__=='__main__':
   main()