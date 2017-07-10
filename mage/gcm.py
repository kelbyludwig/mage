import struct
import binascii
import mage.finite_field as _ff
from Crypto.Cipher import AES
from Crypto.Util import Counter

class GCM():

    def __init__(self, key):
        assert len(key) == 16
        self.key = key
        self.cipher = AES.AESCipher(key)
        self.field  = _ff.GF(0xE1000000000000000000000000000000)
        self.hash_key = self._block_encrypt('\x00'*self.cipher.block_size)
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
            return bytes + ('\x00' * (self.cipher.block_size - l % 16))
    
    def _block_decrypt(self, ct):
        assert len(pt) == self.cipher.block_size
        return self.cipher.decrypt(ct)

    def _block_encrypt(self, pt):
        assert len(pt) == self.cipher.block_size
        return self.cipher.encrypt(pt)

    def _ctr_encrypt(self, pt, iv):
        hi, lo = struct.unpack(">QQ", iv)
        iv = (hi<<64)+lo+1 #because its already been used
        ctr = Counter.new(128, initial_value=iv)
        a = AES.new(self.key, AES.MODE_CTR, counter=ctr)
        return a.encrypt(pt)

    def _ghash(self, ct, ad):
        ptp = self._bspad(ct)
        adp = self._bspad(ad)
        bitlen = lambda x: struct.pack(">Q", len(x)*8)
        bs = adp + ptp + bitlen(ad) + bitlen(ct)
        assert len(bs) % 16 == 0
        g = self.field.elem(0)
        for i in range(len(bs)/16):
            be = self._elem(bs[16*i:(i+1)*16])
            g = g + be
            g = g * self.he
        return self._unelem(g)

    def seal(self, nonce, pt, ad):
        assert len(nonce) == 12 # 96 bit nonce
        iv = nonce + struct.pack(">L", 1) 
        s = self._block_encrypt(iv)
        ct = self._ctr_encrypt(pt, iv)
        g = self._ghash(ct, ad)
        t = self._elem(s) + self._elem(g)
        return ct, self._unelem(t)

    def unseal(self, iv, ct, tag):
        pass
