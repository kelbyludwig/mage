from . import ecdsa 

def proj(u, v):
    """
    proj takes two vectors as input and returns the vector corresponding to the
    projection of v onto u.

    INPUT:
    - `u` - the vector to project onto
    - `v` - the vector being projected

    OUTPUT:
    The vector representing the projection of v onto u. 
    """
    assert len(u) == len(v)
    zv = zero_vector(len(u))
    if u == zv:
        return zv
    return ((v*u) / (u*u)) * u

def gram_schmidt(basis):
    """
    gram_schmidt takes an basis as input and returns an orthonogonal basis
    which spans the same subspace. If the input basis vectors are not linearly
    indepedent the output matrix will have zero vectors.
    TODO(kkl): Unit Tests - various rings, assertions that match sage's builtin results

    INPUT:
    - `basis` - a matrix representing a lattice basis

    OUTPUT:
    A matrix representing the orthonormalized input basis.

    EXAMPLES:

    ::
        sage: A = Matrix(QQ, [[1,2,3],[74,61,2],[3,3,3]])
        sage: oA1 = gram_schmidt(A) 
        sage: oA2, _ = A.gram_schmidt() #sage's built in gram_schmidt for testing
        sage: oA1 == oA2
        True
    ::
    """
    Q = []
    for i, v in enumerate(basis):
        Q.append(v - sum(proj(u,v) for u in Q[:i]))
    return Matrix(basis.base_ring(), Q)

def LLL(basis, delta=.99):
    """
    LLL takes an input basis and returns a reduced basis with short, nearly
    orthogonal vectors.

    INPUT:
    - `basis` - a matrix representing a lattice basis
    - `delta` - (default: .99) a reduction parameter TODO(kkl): come up with an intuitive description of the delta param

    OUTPUT:
    A LLL-reduced basis represented by a matrix

    EXAMPLES:
    ::
        sage: B = Matrix(QQ, [[-2,0,2,0],[1/2,-1,0,0],[-1,0,-2,1/2],[-1,1,1,2]])
        sage: LLL(B)
        [ 1/2   -1    0    0]
        [  -1    0   -2  1/2]
        [-1/2    0    1    2]
        [-3/2   -1    2    0]
    ::
    """
    assert delta > .25 and delta <= 1
    B = copy(basis)
    Q = gram_schmidt(B)
    
    def mu(i, j):
        v = B[i]
        u = Q[j]
        return (v*u) / (u*u)
    
    n = B.nrows()
    k = 1

    while k < n:
        for j in reversed(range(k)):
            if abs(mu(k, j)) > 1/2:
                B[k] = B[k] - round(mu(k,j))*B[j]
                Q = gram_schmidt(B)
        if (Q[k]*Q[k]) >= (delta - mu(k, k-1)^2) * (Q[k-1]*Q[k-1]):
            k += 1
        else:
            B[k], B[k-1] = B[k-1], B[k]
            Q = gram_schmidt(B)
            k = max(k-1, 1)
    return B

def attack(oracle, lbits=8):
    signatures = []
    for x in range(50): 
        signatures.append(oracle(str(x)))
    #tuf = lambda (r,s): (r / (s*2^lbits), 

def test():
    F = FiniteField(233970423115425145524320034830162017933)
    E = EllipticCurve(F, [-95051,11279326])
    g = E(182, 85518893674295321206118380980485522083)
    kp = ecdsa.ECDSAKeyPair(E, g)   
    def oracle(message):
        return kp.bias_sign(message)
    r,s = kp.sign("allo")
    assert kp.verify("allo", r,s)
    assert not kp.verify("hello", r,s)
