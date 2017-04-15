
# This file was *autogenerated* from the file mage/tests/matrix_utils_test.sage
from sage.all_cmdline import *   # import sage library

_sage_const_3 = Integer(3); _sage_const_2 = Integer(2); _sage_const_20 = Integer(20); _sage_const_0 = Integer(0); _sage_const_1 = Integer(1)
import unittest
from sage.all import Matrix, random_matrix, QQ
from mage import matrix_utils

class TestMatrixUtils(unittest.TestCase):
   
    def test_gram_schmidt(self): 
        for i in range(_sage_const_20 ):
            dim = i
            A = random_matrix(QQ, i, algorithm='unimodular')
            oA1 = matrix_utils.gram_schmidt(A)
            oA2, _ = A.gram_schmidt() # compare results with sage's built in gram_schmidt
            assert oA1 == oA2

    def test_lll(self):
        # do a quick verification of the basis from cryptopals
        B  = Matrix(QQ, [[-_sage_const_2 ,_sage_const_0 ,_sage_const_2 ,_sage_const_0 ],[_sage_const_1 /_sage_const_2 ,-_sage_const_1 ,_sage_const_0 ,_sage_const_0 ],[-_sage_const_1 ,_sage_const_0 ,-_sage_const_2 ,_sage_const_1 /_sage_const_2 ],[-_sage_const_1 ,_sage_const_1 ,_sage_const_1 ,_sage_const_2 ]])
        ex = Matrix(QQ, [[_sage_const_1 /_sage_const_2 ,-_sage_const_1 ,_sage_const_0 ,_sage_const_0 ],[-_sage_const_1 ,_sage_const_0 ,-_sage_const_2 ,_sage_const_1 /_sage_const_2 ],[-_sage_const_1 /_sage_const_2 ,_sage_const_0 ,_sage_const_1 ,_sage_const_2 ],[-_sage_const_3 /_sage_const_2 ,-_sage_const_1 ,_sage_const_2 ,_sage_const_0 ]])
        re = matrix_utils.LLL(B) 
        assert re == ex
        #for _ in range(20):
        #    A = random_matrix(QQ, randint(1,20), randint(1,20), density=1)
        #    exp = A.LLL()
        #    assert utils.LLL(A) == exp


if __name__ == "__main__":
    unittest.main()

