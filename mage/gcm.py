import struct
import binascii
import mage.finite_field as _ff
from Crypto.Cipher import AES

class GCM():

    def __init__(self, key):
        assert len(key) == 16
        self.cipher = AES.AESCipher(key)
        self.field  = _ff.GF(0xE1000000000000000000000000000000)
        self.hash_key = self._encrypt('\x00'*self.cipher.block_size)
        self.he = self._elem(self.hash_key)
    
    def _elem(self, bytes):
        #TODO(kkl): Not sure of endianness
        assert len(bytes) == 16
        e1, e2 = struct.unpack(">QQ", bytes)
        en = (e1 << 64) + e2
        return self.field.elem(en)

    def _unelem(_, elem):
        e1, e2 = (elem.n >> 64), (elem.n & 0xFFFFFFFFFFFFFFFF)
        bs = struct.pack(">QQ", e1, e2)
        return bs

    def _bspad(self, bytes):
        l = len(bytes)
        if l == 0:
            return '\x00' * self.cipher.block_size
        lm = self.cipher.block_size % l
        if lm == 0:
            return bytes
        else:
            return bytes + ('\x00' * lm)
    
    def _decrypt(self, ct):
        return self.cipher.decrypt(ct)

    def _encrypt(self, pt):
        return self.cipher.encrypt(pt)

    def _prep_input(self, pt, ad):
        ptp = self._bspad(pt)
        adp = self._bspad(ad)
        bitlen = lambda x: struct.pack(">Q", len(x)*8)
        return adp + ptp + bitlen(ad) + bitlen(pt)

    def _ghash(self, bs):
        assert len(bs) % 16 == 0
        g = self.field.elem(0)
        for i in range(len(bs)/16):
            be = self._elem(bs[16*i:(i+1)*16])
            print("g %s be %s" % (g, binascii.hexlify(bs[16*i:(i+1)*16])))
            g = g + be
            g = g * self.he
        return self._unelem(g)

    def seal(iv, pt, ad):
        bs = self._prep_input(pt, ad)
        pass

    def unseal(iv, ct, tag):
        pass
