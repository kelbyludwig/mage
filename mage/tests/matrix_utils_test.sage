import unittest
from sage.all import Matrix, random_matrix, QQ
from mage import matrix_utils

class TestMatrixUtils(unittest.TestCase):
   
    def test_gram_schmidt(self): 
        for i in range(20):
            dim = i
            A = random_matrix(QQ, i, algorithm='unimodular')
            oA1 = matrix_utils.gram_schmidt(A)
            oA2, _ = A.gram_schmidt() # compare results with sage's built in gram_schmidt
            assert oA1 == oA2

    def test_lll(self):
        # do a quick verification of the basis from cryptopals
        B  = Matrix(QQ, [[-2,0,2,0],[1/2,-1,0,0],[-1,0,-2,1/2],[-1,1,1,2]])
        ex = Matrix(QQ, [[1/2,-1,0,0],[-1,0,-2,1/2],[-1/2,0,1,2],[-3/2,-1,2,0]])
        re = matrix_utils.LLL(B) 
        assert re == ex
        #for _ in range(20):
        #    A = random_matrix(QQ, randint(1,20), randint(1,20), density=1)
        #    exp = A.LLL()
        #    assert utils.LLL(A) == exp


if __name__ == "__main__":
    unittest.main()
