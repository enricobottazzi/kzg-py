from py_ecc.fields import FQ, FQ2
from py_ecc.bn128 import G1, G2, multiply, curve_order, add
from typing import List, Tuple, Optional, TypeAlias
import random
import numpy as np

TrustedSetup: TypeAlias = Tuple[List[Tuple[FQ, FQ]], List[Tuple[FQ2, FQ2]]]

# Generate a trusted setup for the KZG scheme. Secret should be generated as part of a MPC ceremony.
def trusted_setup (length: int) -> TrustedSetup:

    # generate a random 256-bit integer
    bit_string = ''.join(str(random.randint(0, 1)) for _ in range(256))
    s = int(bit_string, 2)

    # s must be a field element
    s_mod: int = s % curve_order

    tau_g1: List[Tuple[FQ, FQ]]= []
    tau_g2: List[Tuple[FQ2, FQ2]]= []

    for i in range(length):
        s_pow: int = pow(s_mod, i, curve_order)

        point_g1: Optional[Tuple[FQ, FQ]] = multiply(G1, s_pow)
        point_g2: Optional[Tuple[FQ2, FQ2]] = multiply(G2, s_pow)

        if point_g1 is None or point_g2 is None:
            raise ValueError("Scalar multiplication failed.")

        tau_g1.append(point_g1)
        tau_g2.append(point_g2)

    return tau_g1, tau_g2

# Generate KZG commtiment for a polynomial. The coefficients of the polynomial are given as a list of field elements ordered from lowest to highest degree.
def commit(ts: TrustedSetup, poly: List[int]) -> Tuple[FQ, FQ]:

    tau_g1, _ = ts

    if len(tau_g1) != len(poly):
        raise ValueError("Polynomial length does not match trusted setup.")
    
    # Evaluate polynomial at tau points
    c : Optional[Tuple[FQ, FQ]] = multiply(tau_g1[0], poly[0])

    if c is None :
        raise ValueError("Scalar multiplication failed.")

    for i in range(1, len(poly)):

        to_add: Optional[Tuple[FQ, FQ]] = multiply(tau_g1[i], poly[i])        
        c: Optional[Tuple[FQ, FQ]] = add(c, to_add)

    return c

