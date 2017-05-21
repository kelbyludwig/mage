import unittest
from sage.all import Matrix, random_matrix, QQ, random, randint, random_vector
from mage import matrix_utils

class TestMatrixUtils(unittest.TestCase):
   
    def test_gram_schmidt(self): 
        for i in range(5, 20):
            dim = i
            A = random_matrix(QQ, i, algorithm='unimodular')
            oA1 = matrix_utils.gram_schmidt(A)
            oA2, _ = A.gram_schmidt() # compare results with sage's built in gram_schmidt
            assert oA1 == oA2
        
        for i in range(5, 20):
            dim = i 
            A = random_matrix(QQ, i, i, algorithm='unimodular')
            Q,_ = A.gram_schmidt()
            r = randint(0, dim-1)
            A[r] = random_vector(QQ, dim)
            oA1 = matrix_utils.gram_schmidt(A, r, Q) 
            oA2, _ = A.gram_schmidt() # compare results with sage's built in gram_schmidt
            assert oA1 == oA2

    def test_lll(self):

        B = Matrix(QQ, [[1,-1,3],[1,0,5],[1,2,6]])
        ex = Matrix(QQ, [[1,-1,0],[-1,0,1],[1,1,1]])
        re = matrix_utils.LLL(B)
        assert re == ex

        # do a quick verification of the basis from cryptopals
        B  = Matrix(QQ, [[-2,0,2,0],[1/2,-1,0,0],[-1,0,-2,1/2],[-1,1,1,2]])
        ex = Matrix(QQ, [[1/2,-1,0,0],[-1,0,-2,1/2],[-1/2,0,1,2],[-3/2,-1,2,0]])
        assert ex == B.LLL()
        re = matrix_utils.LLL(B) 
        assert re == B.LLL()

    #    bad = 0
    #    for _ in range(200):
    #        n = randint(1,10)
    #        A = random_matrix(QQ, n, n)
    #        d = .25 + (random() * .74)
    #        ex = A.LLL(delta=d)
    #        try:
    #            re = matrix_utils.LLL(A, delta=d)
    #        except ZeroDivisionError as e:
    #            continue
    #        if ex != re:
    #            bad += 1 
    #    assert bad < 10


if __name__ == "__main__":
    unittest.main()
