# The Hidden Number Problem

## What Is the Hidden Number Problem?

HNP is a mathematical problem with interesting cryptographic applications. If
you are familiar with the discrete log and Diffie-Hellman problems, HNP is
similar. The HNP is as follows:

* `p` = prime number
* `n` = bit length of p
* `MSB_k(x)` = Approximately the most significant k bits of x
    * NOTE: `z = MSB_k(x)` where `z` satisfies `abs(x - z) < p/2^(k+1)`
* `O_alpha,g(x) = MSB_k(alpha*g^x mod p)` = The oracle used in HNP

# The Matrix

```
b1 = [  q  0  0  0  0  0 ...  0 ]
b2 = [  0  q  0  0  0  0 ...  0 ]
b3 = [  0  0  q  0  0  0 ...  0 ]
b4 = [  0  0  0  q  0  0 ...  0 ]
b5 = [  0  0  0  0  q  0 ...  0 ]
b6 = [  0  0  0  0  0  q ...  0 ]
        ...              ...
bn = [  0  0  0  0  0  0 ...  q ]
bt = [ t0 t1 t2 t3 t4 t5 ... tn ]
```

HNP can be depicted using row linear combinations of these basis vectors.

`alpha*t0 (mod q)` (an example input to the HNP oracle) can be written as
`alpha*t0 - X*q` (just by the def of modulus). This is (part of) linear comb of
the basis vectors: `alpha*bt - X*b1`

## MSB_k impl


```
def MSB_k(k,p):
    """
    MSB_k(k,p)(x) ≈ k most significant bits of x. However this definition is more
    flexible. In particular, k need not be an integer.
    (Def. from: http://www.isg.rhul.ac.uk/~sdg/igor-slides.pdf) 
    """
    def MSB(x):
        t = 1
        while True:
            if x >= (t-1)*(p/2^k) and x < t*(p/2^k):
                return t
            t += 1
    return MSB
```

## Representing High/Low Bits as a Number

This was annoying until I remember a silly fact: Multiplication/Division by
powers of two is the same a left/right shifts.

Say `k` is the number we want, and we know the `l` least significant bits of `k`.
The `l` LSBs of `k` can be represented by a number between 0 and (2^l)-1. Call
this LSB number `a`. The claim that tripped me up for a bit was `k-a=(2^l)*b` for
some `b`. Is this always true? Yup! Here is how I puzzled it out.

```
k-a=(2^l)*b
k = (2^l)*b + a 
# here (2^l)*b is the high order bits, and a is the low order bits
# multiplication by (2^l) is just a left shift by l.
```

## Notation From the Nyugen Paper

DSA Signing:

`r(k) = (g^k (mod p)) (mod q)`
`s(k,u) = k^-1 * (h(u) + alpha*r(k)) (mod q)` where `alpha` is the private key
`r(k), s(k,u)` is the signature pair with key `k` and message `u`

Page 5 Congruence:

`alpha*r(k) = s(k,u)*k - h(u) (mod q)`
if you sub `s(k,u)` with its def:
`alpha*r(k) = (k^-1 * (h(u)+alpha*r(k)))*k - h(u) (mod q)`
`           = h(u) + alpha*r(k) - h(u) (mod q)`
`           = alpha*r(k) (mod q)`

Page 5 Congruence 2:
`alpha*r(k) = s(k,u)*k - h(u) (mod q)`
is morphed into (on the LHS)
`alpha * r(k) * 2^-l * s(k,u)^-1 # aka just multiplying by 2^-l*s(k,u)^-1` 
and morphed into (on the RHS)
`(a - s(k,u)^-1)*h(u)*2^-l + b (mod q) # a and b are derived from the high/low bits of k`

How did RHS happen?
`s(k,u)*k - h(u)`
`#replace k with (2^l)*b+a`
`s(k,u)* ((2^l)*b + a) - h(u)`
`#distribute s(k,u)`
`s(k,u)*(2^l)*b + s(k,u)*a - h(u)`
`#multiply by 2^-l*s(k,u)^-1`
`2^-l*s(k,u)^-1 * (s(k,u)*(2^l)*b + s(k,u)*a - h(u))`
`#distribute`
`b + 2^-l*a - 2^-l*s(k,u)^-1*h(u)`
`#NOT SURE BUT I THINK THAT CAN BE RE-ARRANGED :)`

## Some Algebra From CryptoPals
```
Focus on the s calculation. Observe that if the low l bits of k are
biased to some constant c, we can rewrite k as b*2^l + c. In our case,
c = 0, so we'll instead rewrite k as b*2^l. This means we can relate
the public r and s values like this:

    s = (H(m) + d*r) * (b*2^l)^-1

Some straightforward algebra gets us from there to here:

    d*r / (s*2^l) = (H(m) / (-s*2^l)) + b
```

Whats that algebra? There are two equations. The first:

```
s = (H(m) + d*r) * (b*2^l)^-1
# recall:
r = kG
s = (H(m) + d*r) * k^-1
# the equation there only replaces k with b*2^l (some b shifted l times, or the HOB of k)
```

The second:
```
d*r / (s*2^l) = (H(m) / (-s*2^l)) + b
# start with 
s = (H(m) + d*r) * (b*2^l)^-1
s*b*2^l = H(m) + d*r
# divide by s*2^l
b = (H(m) + d*r)/s*2^l
b = H(m)/s*2^l + d*r/s*2^l
b - H(m)/s*2^l = d*r/s*2^l
# which can be moved around
d*r / (s*2^l) = (H(m)/(-s*2^l)) + b

```

## Cryptopals Clarification of `m`

```
In other words, u is an approximation for d*t mod q. Let's massage the
numbers some more. Since this is mod q, we can instead say this:

    d*t ~ u + m*q
      0 ~ u + m*q - d*t
```

This is annoying, but at this point, `m` is not the message but
some multiple of `q` to demonstrated that `d*t` is congruent to `u mod q`.

## Generating A Lattice Vector Space in Sage

```
q = 11
dim = 3
ZZ_q = IntegerModRing(q)
V = VectorSpace(ZZ_q, dim)
S = V.subspace([random_vector(ZZ_q, dim)])
basis(S)
```
This is kinda useless though because a basis in Sage does
not have a lot of useful methods defined for it.

## References
[Hidden Number Problem and It's Applications](http://www.isg.rhul.ac.uk/~sdg/igor-slides.pdf)
