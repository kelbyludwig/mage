from sage.all import Integer as _Integer
from sage.rings.integer import Integer as _RInteger
from itertools import izip_longest

class RingPolynomial():

    def __init__(self, ring, coefficients):
        """
        Initializes a polynomial with coefficients in the base ring `ring`.

        INPUT:
        - ``ring`` -- the base ring

        - ``coefficients`` -- a list representing polynomials in the base ring.
          coefficient[0] is the most significant coefficient.

        EXAMPLES:

        ::

            sage: from mage import finite_field as mf
            sage: Z2 = Zmod(2)
            sage: f = mf.RingPolynomial(Z2, [1,1,0,1])
            sage: g = mf.RingPolynomial(Z2, [0,1,1])
            sage: f+g
            [1, 0, 1, 1]
            sage: (f + g).to_string()
            '1*x^3 + 1*x^2 + 1*x^0'
            sage: (f * g).to_string()
            '1*x^5 + 1*x^4 + 1*x^3 + 1*x^1'
            sage: g = mf.RingPolynomial(Z2, [1,1,1,1,0,1,1])
            sage: g.to_string()
            '1*x^6 + 1*x^5 + 1*x^3 + 1*x^2 + 1*x^1 + 1*x^0'
            sage: h = mf.RingPolynomial(Z2, [1,0,0,1,1])
            sage: h.to_string()
            '1*x^4 + 1*x^3 + 1*x^0'
            sage: q,r = divmod(g, h)
            sage: (q.to_string(), r.to_string())
            ('1*x^2', '1*x^3 + 1*x^1 + 1*x^0')
            sage: q*h+r == g
            True
            sage: (g-g).is_zero()
            True
            sage: g.degree()
            6
            sage: g = mf.RingPolynomial(Z2, [1,0,0,0,1,1,1,0,1,1,1])
            sage: g.to_string()
            '1*x^10 + 1*x^9 + 1*x^8 + 1*x^6 + 1*x^5 + 1*x^4 + 1*x^0'
            sage: h = mf.RingPolynomial(Z2, [1,0,1,1,0,1,1,0,0,1])
            sage: h.to_string()
            '1*x^9 + 1*x^6 + 1*x^5 + 1*x^3 + 1*x^2 + 1*x^0'
            sage: Z5 = Zmod(5)
            sage: g = mf.RingPolynomial(Z5, [1,0,2])
            sage: g.monic().to_string()
            '1*x^2 + 3*x^0'
            sage: g.to_string()
            '2*x^2 + 1*x^0'
            sage: g.derivative().to_string()
            '4*x^1'
            sage: g.derivative().derivative().to_string()
            '4*x^0'
            sage: g.derivative().derivative().derivative().to_string()
            '0'
            sage: g = mf.RingPolynomial(Z5, [0, 0, 0, 1, 1, 2, 2, 1, 1])
            sage: g.to_string()
            '1*x^8 + 1*x^7 + 2*x^6 + 2*x^5 + 1*x^4 + 1*x^3'
            sage: h = mf.RingPolynomial(Z5, [0, 0, 3, 4, 0, 2, 2, 3])
            sage: d = g.gcd(h)
            sage: d.to_string()
            '1*x^4 + 1*x^2'
            sage: g = mf.RingPolynomial(Z5,[0, 0, 0, 0, 3, 3, 3, 1, 2, 3, 2, 0, 0, 0, 3, 3, 3, 1, 2, 4, 3, 1, 2, 4, 0, 3, 4, 3, 1, 3, 0, 4, 3, 1, 4, 1]) 
            sage: g.squarefree_decomposition()
            [([0, 2, 1], 4), ([3, 1], 7), ([1, 1], 5), ([4, 1], 15)]
            sage: g = mf.RingPolynomial(Z5, [4, 2, 4, 4, 2, 0, 1])
            sage: g.ddf()
            [([2, 3, 1], 1), ([2, 3, 4, 2, 1], 2)]
            sage: g = mf.RingPolynomial(Z5, [2, 1, 1, 3, 3, 2, 4, 2, 0, 0, 2, 1, 3, 2, 2, 3, 1, 4, 4, 3, 1])
            sage: # this next test takes forever
            sage: #g.ddf() => [([3, 2, 1], 2), ([2, 0, 4, 0, 1], 4), ([1, 1, 4, 0, 4, 3, 1], 6), ([2, 1, 2, 0, 1, 1, 2, 3, 1], 8)]

        ::

        """
        ring_coefficients = map(lambda x: ring(x), coefficients)
        trunc = len(ring_coefficients)
        for rc in reversed(ring_coefficients):
            if rc.is_zero():
                trunc -= 1
                continue
            break
        self.coefficients = ring_coefficients[:trunc]
        self.ring = ring 

    def __repr__(self):
        return str(self.coefficients)

    def to_string(self):
        st = ""
        n = len(self.coefficients)
        if n == 0:
            return '0'
        for i,d in enumerate(reversed(self.coefficients)):
            if d != self.ring(0):
                st += "%d*x^%d + " % (d, n-i-1)
        return st[:-3]

    def __eq__(a, b):
        return a.ring == b.ring and a.coefficients == b.coefficients

    def __ne__(a, b):
        return not (a == b)

    def __add__(a, b):
        new_coef = [ia+ib for (ia,ib) in izip_longest(a.coefficients, b.coefficients, fillvalue=a.ring.zero())]
        return RingPolynomial(a.ring, new_coef)

    def __sub__(a, b):
        new_coef = [ia-ib for (ia,ib) in izip_longest(a.coefficients, b.coefficients, fillvalue=a.ring.zero())]
        return RingPolynomial(a.ring, new_coef)

    def __mul__(a, b):
        if a.is_zero() or b.is_zero():
            return RingPolynomial(a.ring, [])
        new_coef = [a.ring.zero() for _ in range(len(a.coefficients) + len(b.coefficients) - 1)]
        for i, ac in enumerate(a.coefficients):
            for j, bc in enumerate(b.coefficients):
                new_coef[i+j] += ac*bc
        return RingPolynomial(a.ring, new_coef)

    def __neg__(self):
        return RingPolynomial(self.ring, [-c for c in self.coefficients])

    def __getitem__(self, i):
        return self.coefficients[i]

    def __div__(a, b):
        q,_ = divmod(a, b)
        return RingPolynomial(q.ring, q.coefficients)

    def __mod__(a, b):
        _,r = divmod(a, b)
        return RingPolynomial(r.ring, r.coefficients)

    def __divmod__(a, b):
        if b.degree() < 0:
            raise Exception("polydiv by zero")
        q, r = RingPolynomial(a.ring, []), a
        if a.degree() < b.degree():
            return q, a
        bdeg = b.degree()
        lc = b[-1]
        while r.degree() >= bdeg:
            e = r.degree() - bdeg
            z = [a.ring.zero()] * e
            d = RingPolynomial(a.ring, z + [r[-1] / lc])
            q += d
            r -= d * b
        return q, r

    def is_zero(self):
        s = RingPolynomial(self.ring, self.coefficients)
        return len(s.coefficients) == 0 

    def degree(self):
        if self.is_zero():
            return -1
        return len(self.coefficients)-1

    def monic(self):
        cs = self.coefficients[:]
        d = cs[-1]
        for i,x in enumerate(cs):
            cs[i] = x / d 
        return RingPolynomial(self.ring, cs)

    def derivative(self):
        cs = self.coefficients[:]
        nm = len(cs)
        if nm == 0:
            return RingPolynomial(self.ring, [])
        cs = cs[1:] # drop the constant
        for i,c in enumerate(cs):
            cs[i] = cs[i]*self.ring(i+1)
        return RingPolynomial(self.ring, cs)

    def squarefree_decomposition(A, pmult=0):
        p = A.ring.characteristic()
        one = RingPolynomial(A.ring, [A.ring(1)])
        T = A.gcd(A.derivative())
        factors = []
        k = 1
        Tk = T
        Vk = A/T
        while Vk.degree() > 0:
            if not (k % p).is_zero():
                Vkplus1 = Tk.gcd(Vk)
                if (Vk/Vkplus1) != one:
                    factors.append((Vk/Vkplus1, p**(pmult)*k))
            else:
                Vkplus1 = Vk
            Tkplus1 = Tk/Vkplus1
            k = k+1
            Vk = Vkplus1
            Tk = Tkplus1
        if Tk.degree() == 0:
            return factors
        newACofs = []
        for i in range(Tk.degree()/p + 1):
            newACofs.append(Tk.coefficients[p*i])
        newA = RingPolynomial(A.ring, newACofs)
        return factors + newA.squarefree_decomposition(pmult=pmult+1)

    def ddf(f):
        i, s, fp, q = 0, [], RingPolynomial(f.ring, f.coefficients), f.ring.characteristic()
        cgen = lambda i: [0, -1] + [0]*(q**i-2) + [1]
        one = RingPolynomial(f.ring, [f.ring(1)])
        while fp.degree() >= 2*i:
            cs = cgen(i)
            print("1")
            np = RingPolynomial(f.ring, cs)
            print("2 np %d fp %d" % (np.degree(), fp.degree()))
            #np = np % fp
            _, np = divmod(np, fp)
            print("3")
            g = fp.gcd(np)
            print("4")
            if g != one:
                s.append((g, i))
                fp = fp / g
            i += 1
        if fp != one:
            s.append((fp, fp.degree()))
        if len(s) == 0:
            return [(f, 1)]
        else:
            return s

    def gcd(g, h):
        gc, hc = RingPolynomial(g.ring, g.coefficients), RingPolynomial(h.ring, h.coefficients)
        while not hc.is_zero():
            _, r = divmod(gc, hc)
            gc = hc
            hc = r
        return gc.monic()

    # TODO(kkl): This mostly works but g is not always monic?
    #def egcd(g, h):
    #    zero = RingPolynomial(g.ring, [])
    #    one = RingPolynomial(g.ring, [1])
    #    if h.is_zero():
    #        return g, one, zero

    #    s2, s1 = one, zero
    #    t2, t1 = zero, one
    #    while not h.is_zero():
    #        q, r = divmod(g, h)
    #        s, t = s2 - q*s1, t2 - q*t1
    #        g, h = h, r
    #        s2, s1 = s1, s
    #        t2, t1 = t1, t
    #    return g, s2, t2

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
            sage: H = mf.GF(0xE1000000000000000000000000000000)
            sage: c = H.elem(0x5e2ec746917062882c85b0685353de37)
            sage: d = H.elem(0x66e94bd4ef8a2c3b884cfa59ca342b2e)
            sage: c*d
            323733119472864005843474405660461955205

        ::

        """
        self.n = n
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

    def __divmod__(a, b):
        q, r = GFElem._divmod(a.n, b.n)
        return a.field.elem(q), a.field.elem(r)

    def __mul__(a, b):
        assert a.field == b.field
        assert a.n < (1 << 128) and b.n < (1 << 128)
        x, y, r = a.n, b.n, a.field.modulus
        z, v, d = 0, x, (1 << 127)
        for i in range(128):
            if y & (d >> i):
                z = z ^ v
            if not v & 1:
                v = v >> 1
            else:
                v = (v >> 1) ^ r
        return a.field.elem(z)

    
    #TODO(kkl): This is broken!
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
            sage: # a.inverse(); 202
            sage: # a.inverse()*a; 1

        ::

        """

        #zero, one = self.field.elem(0), self.field.elem(1)
        #t, newt, r, newr = zero, one, self.field.modelem, self
        #while newr.n != 0:
        #    quotient = r / newr
        #    t, newt = newt, t - quotient * newt
        #    r, newr = newr, r - quotient * newr
        #if GFElem._deg(r) > 0: raise Exception("not invertible")
