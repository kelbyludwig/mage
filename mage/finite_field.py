class GF():
    """
    Returns a finite field defined by a irreducible polynomial.
    """

    def __init__(self, modulus):
        self.modulus = modulus
        self.elem = lambda x: GFElem(x, self)

    def __eq__(a,b):
        return a.modulus == b.modulus

class GFElem():
    
    def __init__(self, n, field):
        """
        Return a instance of a element of a binary finite field.

        INPUT:
        - ``n`` -- the element in field represented by an integer

        - ``field`` -- a GF instance that this element belongs to

        OUTPUT:
        
        A binary finite field element.

        EXAMPLES:

        ::

            sage: from mage import finite_field as mf
            sage: G = mf.GF(0b101010101010101)
            sage: a = G.elem(0b10101)
            sage: b = G.elem(0b100011011)
            sage: a+b,b+a,b-a,a-b
            (270, 270, 270, 270)
            sage: H = mf.GF(0x11B)
            sage: c = H.elem(0x53)
            sage: d = H.elem(0xCA)
            sage: c*d,c*d
            (1, 1)

        ::

        """
        _, nr  = GFElem._divmod(n, field.modulus)
        self.n = nr
        self.field = field

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
            sage: mf.GFElem._divmod(a, m)
            (61, 251)

        ::

        """
        q, r = 0, a
        rd, bd = GFElem._deg(r), GFElem._deg(b)
        while rd >= bd:
            d = rd - bd
            q = q ^ (1 << d)
            r = r ^ (b << d)
            rd = GFElem._deg(r)
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
            sage: G = mf.GF(0b100011011)
            sage: a = G.elem(0b10011)
            sage: a.deg() 
            4
            sage: G.elem(0b1).deg()
            0
            sage: G.elem(0b0).deg()
            -1

        ::

        """

        return GFElem._deg(self.n)

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

    def __eq__(a, b):
        if type(a) != type(b):
            return False

        if a.field != b.field:
            raise Exception("different field moduli")

        return a.n == b.n

    def __xor__(a, b):
        return a.field.elem(a.n ^ b.n) 

    def __rshift__(a, b):
        return a.field.elem(a.n >> b)

    def __lshift__(a, b):
        return a.field.elem(a.n << b)

    __add__  = __xor__
    __sub__  = __xor__

    def __mul__(a, b):
        assert a.field == b.field
        m, p = a.field.modulus, b.field.elem(0)
        
        while a.n > 0:
            if a.n & 1:
                p = p ^ b
            a = a >> 1
            b = b << 1
            if b.deg() == GFElem._deg(m):
                b = b ^ m #"subtract" the most signficant bit
        return p
    
    def modinv(self):
        p = self.field.m
        one, zero = GF(1, p), GF(0, p)
        t, r, newt, newr = zero, p, one, self
        
        ps = lambda x: format(int(x), '08b')

        step = 1 
        while newr != zero:
            q, _ = GFElem._divmod(r.n, newr.n) 
            r, newr = newr, r.n - q*newr.n
            t, newt = newt, t.n - q*newt.n
            step += 1
        
        if r.deg() > 0:
            raise Exception("common factors")
