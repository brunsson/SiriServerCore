#!/usr/bin/python
# -*- coding: utf-8 -*-


from plugin import *
import struct, socket
import ping

class WakeOnLan(Plugin):

    @register("fr-FR", u"((Allumer)|(Démarrer)).* (PC|ordinateur)$")
    def Allumer(self, speech, language, regex):
        ethernet_address = 'F4:6D:04:1A:25:6F'
        # Construct a six-byte hardware address

        addr_byte = ethernet_address.split(':')
        hw_addr = struct.pack('BBBBBB', int(addr_byte[0], 16),
          int(addr_byte[1], 16),
          int(addr_byte[2], 16),
          int(addr_byte[3], 16),
          int(addr_byte[4], 16),
          int(addr_byte[5], 16))

        # Build the Wake-On-LAN "Magic Packet"...

        msg = '\xff' * 6 + hw_addr * 16

        # ...and send it to the broadcast address using UDP

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(msg, ('<broadcast>', 9))
        s.close()
        self.say("Le pc demarre :) ")
        self.complete_request()

    @register("fr-FR",u"(Ping pc)")
    def Ping_Pc(self, speech, language):
        Retour_Ping = ping.verbose_ping("192.168.0.29",2,1)
        self.say(Retour_Ping)
        self.complete_request()
