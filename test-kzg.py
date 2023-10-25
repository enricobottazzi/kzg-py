import time
import unittest
from kzg import trusted_setup, commit, generate_evaluation_proof, verify_proof


class TestKZG(unittest.TestCase):

    def test_kzg(self):

        # Perform trusted setup. The setup is parameterized by the degree of the polynomial that will be committed to.
        deg = 3
        ts = trusted_setup(deg)

        # p(x) = x^3 + x + 5
        # p(x) is the polynomial of the prover
        # prover commits to the polynomial and sends the commitment to the verifier
        p = [5, 1, 0, 1]
        assert len(p) == deg + 1
        c = commit(ts, p)

        # The verifier wants to check that the evaluation p(3) = 35 is correct
        # Prover generates a proof that p(3) = 35 and sends it to the verifier
        start = time.time()
        proof = generate_evaluation_proof(ts, p, 3, 35)
        end = time.time()
        print("Time to generate the proof ", end - start)

        # verify proof
        start = time.time()
        bool = verify_proof(ts, c, proof, 3, 35)
        end = time.time()
        print("Time to verify the proof ", end - start)


        # assert that the proof is valid
        assert bool == True


if __name__ == "__main__":
    unittest.main()
