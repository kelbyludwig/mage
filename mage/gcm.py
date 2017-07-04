import mage.finite_field as _ff
from Crypto.Cipher import AES

class GCM():

    def __init__(self, key):
        assert len(key) == 16
        self.cipher = AES.AESCipher(key)
        self.field  = _ff.GF(0xE1000000000000000000000000000000)
    
    def _elem(self, bytes):
        #TODO(kkl): Not sure of endianness
        e1, e2 = struct.unpack(">QQ", bytes)
        en = (e1 << 64) + e2
        return self.field.elem(en)

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

    def _gmac(pt, ad):
        h = self._encrypt('\x00'*self.cipher.block_size)
        he = self._elem(h)
        pass

    def seal(pt):
        pass

    def unseal(ct, tag):
        pass
