import unittest
from kzg import trusted_setup

class TestKZG(unittest.TestCase):

    def test_setup(self):

        deg : int = 4
        ts = trusted_setup(deg)

        ptau_g1, ptau_g2 = ts

        self.assertEqual(len(ptau_g1), deg)
        self.assertEqual(len(ptau_g2), deg)

if __name__ == "__main__":
    unittest.main()
