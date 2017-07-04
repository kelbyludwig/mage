from sage.all import Integer as _Integer
from sage.rings.integer import Integer as _RInteger

class GF():
    """
    Returns a finite field defined by a irreducible polynomial.
    """

    def __init__(self, modulus):
        self.modulus = modulus
        self.modelem = GFElem(modulus, self)
        self.modelem.n = modulus
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
        #if n > field.modulus:
        #    raise Exception("non-reduced value supplied")
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
            sage: mf.GFElem._divmod(0, m)
            (0, 0)

        ::

        """
        if not isinstance(a, _RInteger) and not isinstance(a, _Integer) and not isinstance(a, int) and not isinstance(a, long): 
            raise Exception("divmod does not accept %s as input" % type(a))
        if a == 0:
            return 0, 0
        if b == 0:
            raise Exception("divmod by zero")

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

    def __neq__(a, b):
        if type(a) != type(b):
            raise Exception("cannot compare different types")

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

    def __div__(a, b):
        q, _ = GFElem._divmod(a.n, b.n)
        return a.field.elem(q)

    def __mod__(a, b):
        _, r = GFElem._divmod(a.n, b.n)
        return a.field.elem(r)

    def __mul__(a, b):
        m, p = a.field.modelem, b.field.elem(0)
        
        while a.n > 0:
            if a.n & 1:
                p = p ^ b
            a = a >> 1
            b = b << 1
            if b.deg() == m.deg():
                b = b ^ m
        return p
    
    def inverse(self):
        """
        Returns the inverse of the field element.

        OUTPUT:
        
        The inverse of the element.

        EXAMPLES:

        ::

            sage: from mage import finite_field as mf
            sage: G = mf.GF(0b100011011)
            sage: a = G.elem(0b1010011)
            sage: a.inverse()
            202
            sage: a.inverse()*a 
            1

        ::

        """

        zero, one = self.field.elem(0), self.field.elem(1)
        t, newt, r, newr = zero, one, self.field.modelem, self
        while newr.n != 0:
            quotient = r / newr
            t, newt = newt, t - quotient * newt
            r, newr = newr, r - quotient * newr
        if GFElem._deg(r) > 0: raise Exception("not invertible")
        return t
