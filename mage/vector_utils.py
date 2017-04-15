from sage.all import zero_vector as _zero_vector

def proj(u, v):
    """
    proj takes two vectors as input and returns the vector corresponding to the
    projection of v onto u.

    INPUT:

    - ``u`` -- the vector to project onto

    - ``v`` -- the vector being projected

    OUTPUT:

    The vector representing the projection of v onto u. 

    EXAMPLES:

    :: 

        sage: v = vector(ZZ, [4,1,4])
        sage: u = vector(ZZ, [-1,1,1])
        sage: from mage import vector_utils as vu
        sage: vu.proj(u,v)
        (-1/3, 1/3, 1/3)

    :: 

    """
    assert len(u) == len(v)
    zv = _zero_vector(len(u))
    if u == zv:
        return zv
    return ((v*u) / (u*u)) * u

