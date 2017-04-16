import hashlib as _hashlib
from sage.all import Mod as _Mod, randint as _randint

class ECDSAKeyPair:

    def __init__(self, E, g, hashfunc=_hashlib.sha1):
        """
        Initializes a ECDSAKeyPair with the over the supplied parameters. 

        INPUT:

        - ``E`` -- An EllipticCurve defined over a finite field.
    
        - ``g`` -- A base element for the given curve.

        - ``hashfunc`` -- (default: hashlib.sha1) a hashlib hash function used for message digests.

        OUTPUT:

        An ECDSAKeyPair that can be used to sign and verify signatures on messages.

        EXAMPLES:

        ::

            sage: F = FiniteField(233970423115425145524320034830162017933)
            sage: E = EllipticCurve(F, [-95051,11279326])
            sage: g = E(182, 85518893674295321206118380980485522083)
            sage: from mage import ecdsa
            sage: kp = ecdsa.ECDSAKeyPair(E, g)
            sage: mes = "mage rulez"
            sage: r,s = kp.sign(mes)
            sage: kp.verify(mes, r, s)
            True

        ::

        """
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
        """
        Sign the supplied message using ECDSA.

        INPUT:

        - ``message`` -- a string representing the message to sign.

        - ``k`` -- (default: None) if provided, the nonce used for the signature.

        OUTPUT:
        
        A pair of numbers that represent the signature of the message.


        """
        if k is None:
            k = _randint(1, self.N)
        r,_ = (k*self.G).xy(); r = _Mod(r, self.N) #sets r to the x coord of kG
        hai = self._message_hash_as_integer(message)
        kinv = _Mod(k, self.N)**-1
        s = ((hai + self.d * r) * kinv)
        return (r,s) 

    def verify(self, message, r, s):
        """
        Verifies an ECDSA signature using the supplied public key.

        INPUT:

        - ``message`` -- a string representing the message to sign.

        - ``r`` -- one of the numbers that makes up the ECDSA signature.

        - ``s`` -- one of the numbers that makes up the ECDSA signature.

        OUTPUT:

        True if the signature is valid and False otherwise.

        """
        assert r > 0 and r == _Mod(r, self.N)
        assert s > 0 and s == _Mod(s, self.N)
        hai = self._message_hash_as_integer(message)
        w = _Mod(s, self.N)**-1
        u1 = hai * w
        u2 = r * w
        P1 = int(u1)*self.G
        P2 = int(u2)*self.Q 
        R,_ = (P1+P2).xy()
        return r == _Mod(R, self.N)

    def _message_hash_as_integer(self, message):
        hashstr = self.H(message).hexdigest()
        return _Mod(int(hashstr, 16), self.N)
