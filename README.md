# kzg-py
 
Implementation of KZG polynomial commitments in Python. For study purposes only.

The implementation consists of 4 simple APIs:

- `trusted_setup` -> generates the trusted setup parameters
- `commit` -> generates a KZG commtiment for a polynomial
- `generate_proof` -> generates a proof for a polynomial evaluation
- `verify_proof` -> verifies a proof for a polynomial evaluation using a pairing check

### Resources 

- [Scroll - Blogpost](https://scroll.io/blog/kzg)
- [KZG Commitments Study - ArnauCube](https://github.com/arnaucube/kzg-commitments-study)
- [Dankrad Feist - KZG Commitments](https://dankradfeist.de/ethereum/2020/06/16/kate-polynomial-commitments.html)
