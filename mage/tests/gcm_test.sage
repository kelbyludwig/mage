import unittest
from mage import gcm as g

class TestGCM(unittest.TestCase):
   
    def test_pad(self): 
        C = g.GCM("yellow submarine") 
        i1,r1 = "yellow submarine", "yellow submarine"
        i2,r2 = "yellow subma", "yellow subma\x00\x00\x00\x00"
        i3,r3 = "", "\x00"*16
        assert C._bspad(i1) == r1
        assert C._bspad(i2) == r2
        assert C._bspad(i3) == r3

    def test_elem_unelem(self):
        C = g.GCM("yellow submarine") 
        ins = ["\x00"*15+"\x01", "\x00"*7+"\x01"+"\x00"*7+"\x01"]
        for i in ins:
            e = C._elem(i)
            r = C._unelem(e)
            assert r == i

    def test_gcm_vector(self): 
        print("\n")
        k = "\x00" * 16
        C = g.GCM(k)
        assert C.hash_key == "\x66\xe9\x4b\xd4\xef\x8a\x2c\x3b\x88\x4c\xfa\x59\xca\x34\x2b\x2e"
        pt = "\x00" * 16
        obs = C._prep_input(pt, "")
        import binascii
        print("obs %s" % binascii.hexlify(obs))
        gbs = C._ghash(obs)
        print("gbs %s" % binascii.hexlify(gbs))

if __name__ == "__main__":
    unittest.main()
