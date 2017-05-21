import hashlib
from mage import ecdsa
from mage import matrix_utils as mu

# params!
F = FiniteField(233970423115425145524320034830162017933)
E = EllipticCurve(F, [-95051,11279326])
g = E(182, 85518893674295321206118380980485522083)

# the keypair!
kp = ecdsa.ECDSAKeyPair(E, g)

def create_biased_oracle(num_bits=8):

    def oracle(message):
        k = randint(1, kp.N)
        k = (k >> num_bits) << num_bits
        return kp.sign(message, k)

    return oracle

def collect_biased_signatures(oracle, num_bits=8, signatures_to_collect=50):

    from string import ascii_letters  
    collected = 0
    base_message = ""
    
    u_vec, t_vec = [], []
    while collected < signatures_to_collect:
        letter_ind = collected % len(ascii_letters) 
        if letter_ind == 0:
            base_message += "A"

        message = base_message + ascii_letters[letter_ind]
        #print('gathering signature on %s' % message)
        r,s = oracle(message)

        t = r / (s * 2**num_bits) 
        u = kp._message_hash_as_integer(message) / (-s * 2**num_bits)

        t_vec.append(t)
        u_vec.append(u)
        collected += 1

    u_vec = vector(QQ, u_vec)
    t_vec = vector(QQ, t_vec)
    return (u_vec, t_vec)

def construct_lattice(us, ts, num_bits=8):
    B = Matrix.identity(QQ, len(us))
    B = kp.N * B
    def insert_row(M, row):
        r = M.rows()
        r.append(row)
        return Matrix(QQ, r)
    B = insert_row(B, ts)
    B = insert_row(B, us)
        
    #TODO(kkl): Come up with a reasonable way to share the number of bits that are biased across all of these functions.
    ct = 1/2**num_bits
    cu = kp.N/2**num_bits
    
    ctv = vector(QQ, ([0] * len(ts)) + [ct] + [0])
    cuv = vector(QQ, ([0] * (len(ts)+1)) + [cu])
    B = B.augment(ctv)
    B = B.augment(cuv)
    return B 
    
if __name__ == '__main__':
    oracle = create_biased_oracle()
    us, ts = collect_biased_signatures(oracle, signatures_to_collect=20)
    B = construct_lattice(us, ts) 
    # NOTE(kkl): For effiency, `mu.LLL(B)` can be replaced with `B.LLL()`. This
    # would use sage's LLL code and not my (slow) code.
    RB = mu.LLL(B, delta=QQ(.99))
    print("private key: %d" % kp.d)
    print("looking for:   %d" % -(kp.d/2**8))
    for row in RB:
        if kp.N/2**8 == row[-1]:
            print("(%d ,%d)" % (row[-2], row[-1]))
