class GF():
    
    def __init__(self, n, modulus=None):
        """
        Return a instance of a element of a Galois Field.
        NOTE: This is kinda an akward interface as it implicitly creates a
        finite field but returns a element of the field.

        INPUT:
        - ``n`` -- the element in field represented by an integer

        - ``modulus`` -- the monic irreducible polynomial modulus represented by an integer

        OUTPUT:
        
        A finite field element.

        """
        if modulus is not None:
            _, nr  = GF._divmod(n, modulus)
            if n != nr:
                raise Exception("non-reducing integer used")
            self.n = nr
            self.m = GF(modulus)
        else:
            self.n = n
            self.m = None

    @staticmethod
    def _divmod(a, b):
        q, r = 0, a
        rd, bd = GF._deg(r), GF._deg(b)
        while rd >= bd:
            d = rd - bd
            q = q ^ (1 << d)
            r = r ^ (b << d)
        return q, r

    def deg(self):
        """
        Returns the degree of the field element's polynomial 

        OUTPUT:
        
        The degree of the corresponding polynomial. Returns -1 for 
        a zero element.

        EXAMPLES:

        ::

            sage: from mage import finite_field as mf
            sage: a = mf.GF(0b10011, 0b100011011)
            sage: a.deg() 
            4
            sage: mf.GF(0b1, 0b100011011).deg()
            0
            sage: mf.GF(0b0, 0b100011011).deg()
            -1

        ::

        """

        return GF._deg(self.n)

    @staticmethod
    def _deg(n):
        if n == 1:
            return 0
        if n == 0:
            return -1

        deg = 0
        while n > 0:
            n >>= 1
            deg += 1
        return deg-1

    def __eq__(self, x):
        if self.m is None and x.m is None:
            return self.n == x.n
        
        if self.m != x.m:
            raise Exception("different field moduli")

        if self.n == self.x:
            return True
        else:
            return False

    def __and__(self, x):
        return GF(self.n & x, self.m)

    def __xor__(self, x):
        return GF(self.n ^ x.n, self.m)

    def __rshift__(self, b):
        return GF(self.n >> b, self.m)

    def __lshift__(self, b):
        return GF(self.n << b, self.m)

    def __add__(self, x):
        return self ^ x

    __sub__ = __add__
    __radd__ = __add__

    def __mul__(self, x):
        a, b, m, p = self, x, self.m, zero
        
        while a > 0:
            if a & 1 == one:
                p = p ^ b
            a = a >> 1
            b = b << 1
            if b.deg() == m.deg():
                b = b ^ m         #"subtract" the most signficant bit
        return p
    
    __rmul__ = __mul__

    def modinv(self):
        a, p = self.n, self.m
        one, zero = GF(1, self.m), GF(0, self.m)
        t, r, newt, newr = zero, p, one, a
        
        def ps(x):
            print("x:   %s" % x)
            print("x.n: %s" % x.n)
            return format(x.n, '08b')
        print("(step, r, newr) = (pre, %s, %s)" % (ps(r), ps(newr)))
        print("(step, t, newt) = (pre, %s, %s)" % (ps(t), ps(newt)))
        step = 1 
        while newr != zero:
            q, _ = r.divmod(newr) 
            r, newr = newr, r - q*newr 
            t, newt = newt, t - q*newt
            print("(step, r, newr) = (%d, %s, %s)" % (step, ps(r.n), ps(newr.n)))
            print("(step, t, newt) = (%d, %s, %s)" % (step, ps(t.n), ps(newt.n)))
            step += 1
        
        if r.deg() > 0:
            raise Exception("common factors")
        print("(step, r, t) = (fin, %s, %s)" % (ps(r.n), ps(t.n)))

