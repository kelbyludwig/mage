import struct
import mage.finite_field as _ff
from Crypto.Cipher import AES

class GCM():

    def __init__(self, key):
        assert len(key) == 16
        self.cipher = AES.AESCipher(key)
        self.field  = _ff.GF(0xE1000000000000000000000000000000)
        hash_key = self._encrypt('\x00'*self.cipher.block_size)
        self.he = self._elem(hash_key)
    
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

    def _ghash(bs):
        assert len(bs) % 16 == 0
        g = self.field.elem(0)
        for b in bs:
            g = g + self.field.elem(b)
            g = g * self.he
        return 

    def _gmac(pt, ad):
        pass

    def seal(iv, pt, ad):
        ptp = self._bspad(pt)
        adp = self._bspad(ad)
        bitlen = lambda x: struct.pack(">Q", len(x)*8)
        pass

    def unseal(iv, ct, tag):
        pass
