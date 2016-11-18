# -*- coding:utf-8 -*-

import binascii

class dc_tools:
    def MyAHex(self, str):
        return binascii.a2b_hex(str.replace(' ',''))

    def MyHexA(self, str):
        return binascii.b2a_hex(str).upper()

    def dataProcess(self, str):
        return binascii.a2b_hex(str.replace(' ',''))[10:]

    def xor(self, data):
        lrc = int(0)
        for c in data:
            lrc = lrc ^ c
        return self.MyAHex("%02x" % lrc)

    def SeriportPack(self, sdata):
        sdata = b"\x02" + self.MyAHex("%08x"%(len(sdata))) + sdata
        lrc = self.xor(sdata)
        result=sdata+lrc + b"\x03"
        return result
