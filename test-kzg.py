import unittest
from kzg import trusted_setup, commit

class TestKZG(unittest.TestCase):

    def test_kzg(self):

        poly = [5, 1, 0, 1]
        deg : int = len(poly)
        ts = trusted_setup(deg)

        ptau_g1, ptau_g2 = ts

        print("Tau G1: ", ptau_g1)
        print("Tau G2: ", ptau_g2)

        self.assertEqual(len(ptau_g1), deg)
        self.assertEqual(len(ptau_g2), deg)

        # Commit to polynomial
        c = commit(ts, poly)

        self.assertIsNotNone(c)

        

if __name__ == "__main__":
    unittest.main()
