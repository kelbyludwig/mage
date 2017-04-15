from sage.all import zero_vector as _zero_vector

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
    zv = _zero_vector(len(u))
    if u == zv:
        return zv
    return ((v*u) / (u*u)) * u

