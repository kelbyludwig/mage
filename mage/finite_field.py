class GF():
    
    def __init__(self, n, modulus=None):
        """
        Return a instance of a element of a binary Galois Field.
        NOTE: This is kinda an akward interface as it implicitly creates a
        finite field but returns a element of the field.

        INPUT:
        - ``n`` -- the element in field represented by an integer

        - ``modulus`` -- the monic irreducible polynomial modulus represented by an integer

        OUTPUT:
        
        A binary finite field element.

        EXAMPLES:

        ::
            sage: from mage import finite_field as mf
            sage: a = mf.GF(0b10101, 0b100011011)
            sage: b = mf.GF(0b1011, 0b100011011)
            sage: a+b,b+a,b-a,a-b
            (30, 30, 30, 30)
            sage: c = mf.GF(0x53, 0x11B)
            sage: d = mf.GF(0xCA, 0x11B)
            sage: c*d,c*d
            (1, 1)

        ::

        """
        if modulus is not None:
            _, nr  = GF._divmod(n, int(modulus))
            if n != nr:
                raise Exception("non-reducing integer used")
            self.n = nr
            self.m = GF(modulus)
        else:
            self.n = n
            self.m = None

    @staticmethod
    def _divmod(a, b):
        """
        Returns the quotient and remainder of a / b

        INPUT:

        - ``a`` -- the numerator 

        - ``b`` -- the denominator

        OUTPUT:

        Returns the quotient and remainder as a pair.

        EXAMPLES:

        ::

            sage: from mage import finite_field as mf
            sage: m = 0b100011011
            sage: a = 0b11111110000100
            sage: mf.GF._divmod(a, m)
            (61, 251)

        ::

        """
        q, r = 0, a
        rd, bd = GF._deg(r), GF._deg(b)
        while rd >= bd:
            d = rd - bd
            q = q ^ (1 << d)
            r = r ^ (b << d)

            rd = GF._deg(r)
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

    def __repr__(self):
        return str(self.n)

    def __trunc__(self):
        return self.n

    def __eq__(self, x):
        if type(self) != type(x):
            return False

        if self.m is None and x.m is None:
            return self.n == x.n
        
        if self.m != x.m:
            raise Exception("different field moduli")

        if self.n == self.x:
            return True
        else:
            return False

    def __xor__(self, x):
        nx = GF(self.n ^ x.n) 
        nx.m = self.m
        return nx

    def __rshift__(self, x):
        nx = GF(self.n >> x) 
        nx.m = self.m
        return nx

    def __lshift__(self, x):
        nx = GF(self.n << x)
        nx.m = self.m
        return nx

    __add__  = __xor__
    __sub__  = __xor__

    def __mul__(a, b):
        m, p = a.m, GF(0)
        
        while a.n > 0:
            if a.n & 1:
                p = p ^ b
            a = a >> 1
            b = b << 1
            if b.deg() == m.deg():
                b = b ^ m #"subtract" the most signficant bit
        return p
    
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

