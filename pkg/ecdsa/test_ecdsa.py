import unittest
from sage.all import FiniteField, EllipticCurve, randint
from . import ecdsa

F = FiniteField(233970423115425145524320034830162017933)
E = EllipticCurve(F, [-95051,11279326])
g = E(182, 85518893674295321206118380980485522083)

class TestECDSA(unittest.TestCase):

    def test_ecdsa(self):
        for i in range(100):
            kp = ecdsa.ECDSAKeyPair(E, g)
            mes = "allo"
            r,s = kp.sign(mes)
            assert kp.verify(mes, r,s)
            assert not kp.verify("hello", r,s)

    def test_ecdsa_with_nonce(self):
        for i in range(100):
            kp = ecdsa.ECDSAKeyPair(E, g)
            mes = "allo"
            r,s = kp.sign(mes, randint(1,kp.N))
            assert kp.verify(mes, r,s)
            assert not kp.verify("hello", r,s)


if __name__ == '__main__':
    unittest.main()
