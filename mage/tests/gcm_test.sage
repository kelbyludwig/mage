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


if __name__ == "__main__":
    unittest.main()
