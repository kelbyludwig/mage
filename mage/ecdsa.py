import hashlib as _hashlib
from sage.all import Mod as _Mod, randint as _randint

class ECDSAKeyPair:

    def __init__(self, E, g, hashfunc=_hashlib.sha1):
        # setup curve and field
        self.E = E
        self.F = E.base_field()
        self.G = g
        self.N = g.order() 
        
        # generate keypair
        d = _randint(1, self.N)
        q = d*self.G
        self.d = d
        self.Q = q
        self.H = hashfunc

    def sign(self, message, k=None):
        if k is None:
            k = _randint(1, self.N)
        r,_ = (k*self.G).xy(); r = _Mod(r, self.N) #sets r to the x coord of kG
        hashstr = self.H(message).hexdigest()
        hai = _Mod(int(hashstr, 16), self.N)
        kinv = _Mod(k, self.N)**-1
        s = ((hai + self.d * r) * kinv)
        return (r,s) 

    def verify(self, message, r, s):
        """
        Given a string and a signature (r,s), verify returns True if the
        signature is valid and False otherwise.
        """
        assert r > 0 and r == _Mod(r, self.N)
        assert s > 0 and s == _Mod(s, self.N)
        hashstr = self.H(message).hexdigest()
        hai = _Mod(int(hashstr, 16), self.N)
        w = _Mod(s, self.N)**-1
        u1 = hai * w
        u2 = r * w
        P1 = int(u1)*self.G
        P2 = int(u2)*self.Q 
        R,_ = (P1+P2).xy()
        return r == _Mod(R, self.N)
