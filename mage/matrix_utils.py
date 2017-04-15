import mage.vector_utils as _vu
from sage.all import Matrix as _Matrix, copy as _copy

def gram_schmidt(basis):
    """
    gram_schmidt takes an basis as input and returns an orthonogonal basis
    which spans the same subspace. If the input basis vectors are not linearly
    indepedent the output matrix will have zero vectors.

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
        Q.append(v - sum(_vu.proj(u,v) for u in Q[:i]))
    return _Matrix(basis.base_ring(), Q)


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
    B = _copy(basis)
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
        if (Q[k]*Q[k]) >= (delta - mu(k, k-1)**2) * (Q[k-1]*Q[k-1]):
            k += 1
        else:
            B[k], B[k-1] = B[k-1], B[k]
            Q = gram_schmidt(B)
            k = max(k-1, 1)
    return B
