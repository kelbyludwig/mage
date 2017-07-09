import unittest
from mage import gcm as g

class TestGCM(unittest.TestCase):
   
    def test_pad(self): 
        C = g.GCM("yellow submarine") 
        i1,r1 = "yellow submarine", "yellow submarine"
        i2,r2 = "yellow subma", "yellow subma\x00\x00\x00\x00"
        i3,r3 = "yellow submarineyellow subma", "yellow submarineyellow subma\x00\x00\x00\x00"
        i4,r4 = "", "\x00"*16
        assert C._bspad(i1) == r1
        assert C._bspad(i2) == r2
        assert C._bspad(i3) == r3
        assert C._bspad(i4) == r4

    def test_elem_unelem(self):
        C = g.GCM("yellow submarine") 
        ins = ["\x00"*15+"\x01", "\x00"*7+"\x01"+"\x00"*7+"\x01"]
        for i in ins:
            e = C._elem(i)
            r = C._unelem(e)
            assert r == i

    def test_ghash(self):
        C = g.GCM("\x00"*16) 
        pt = "\x00"*16
        obs = C._prep_input(pt, "")
        gbs = C._ghash(obs)
        # a test vector i created using a different lib
        assert gbs == "\xa6\x6e\x5c\x0a\x72\xa5\x70\xd9\x69\x20\x17\xee\x37\x5c\x24\xba"

if __name__ == "__main__":
    unittest.main()
