import mage.vector_utils as _vu
from sage.all import Matrix as _Matrix, copy as _copy, plot as _plot, points as _points

def gram_schmidt(basis):
    """
    gram_schmidt takes an basis as input and returns an orthonogonal basis
    which spans the same subspace. 

    INPUT:

    - ``basis`` -- a matrix representing a lattice basis.

    OUTPUT:

    A matrix representing the orthonormalized input basis.

    .. SEEALSO::

        :meth:`sage.matrix.matrix2.Matrix.gram_schmidt`

    .. NOTE::

        this function will not fail if given a invalid basis.

    EXAMPLES:

    ::

        sage: A = Matrix(QQ, [[1,2,3],[74,61,2],[3,3,3]])
        sage: from mage import matrix_utils as mu
        sage: oA1 = mu.gram_schmidt(A) 
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

    - ``basis`` -- a matrix representing a lattice basis

    - ``delta`` -- (default: .99) a reduction parameter 

    OUTPUT:

    A LLL-reduced basis represented by a matrix

    .. SEEALSO::
    
        :meth:`sage.matrix.matrix_dense.Matrix_dense.LLL`

    EXAMPLES:

        ::

            sage: B = Matrix(QQ, [[-2,0,2,0],[1/2,-1,0,0],[-1,0,-2,1/2],[-1,1,1,2]])
            sage: from mage import matrix_utils as mu
            sage: mu.LLL(B)
            [ 1/2   -1    0    0]
            [  -1    0   -2  1/2]
            [-1/2    0    1    2]
            [-3/2   -1    2    0]

        ::

    .. TODO:: 

        come up with an intuitive description of the ``delta`` param

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
            k = max(k-1, 1)
    return B


def plot_2d_lattice(v1, v2, xmin=-10, xmax=10, ymin=-10, ymax=10, show_basis_vectors=True):
    """
    sage plot of a lattice with v1 and v2 as basis vectors.

    INPUT:

    - ``v1`` -- one of the basis vectors

    - ``v2`` -- one of the basis vectors

    - ``xmin`` -- (default: -10) the minimum x-coordinate scalar that will be used when plotting lattice points

    - ``xmax`` -- (default: 10) the maximum x-coordinate scalar that will be used when plotting lattice points

    - ``ymin`` -- (default: -10) the minimum y-coordinate scalar that will be used when plotting lattice points

    - ``ymax`` -- (default: 10) the maximum y-coordinate scalar that will be used when plotting lattice points

    - ``show_basis_vectors`` -- (default: True) if True, the two basis vectors will also be plotted

    OUTPUT:

    A sage plot of the lattice produced by the basis vectors.

    EXAMPLES:

    ::

            sage: from mage import matrix_utils as mu
            sage: b1 = vector(ZZ, [3,4])
            sage: b2 = vector(ZZ, [4,5])
            sage: mu.plot_2d_lattice(b1,b2) # this will open a graphics viewer
            Graphics object consisting of 3 graphics primitives
            sage: mu.plot_2d_lattice(b1,b2,show_basis_vectors=False)
            Graphics object consisting of 1 graphics primitive

    ::

    """

    pts = []
    # plot all integer multiples of the basis so long as the x and y coordinates
    # are within (x|y)(min|max).
    for i in range(xmin, xmax):
        for j in range(ymin, ymax):
            pt = i*v1 + j*v2
            x,y = pt[0], pt[1]
            if x < xmin or x > xmax or y < ymin or y > ymax:
                continue
            pts.append(pt)
    the_plot = _plot(_points(pts))
    if show_basis_vectors:
        the_plot += _plot(v1) + _plot(v2)
    return the_plot
