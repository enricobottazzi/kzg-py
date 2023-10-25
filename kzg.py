from py_ecc.fields import FQ, FQ2
from py_ecc.bn128 import G1, G2, multiply, curve_order, add
from py_ecc.bn128.bn128_pairing import pairing
from typing import List, Tuple, Optional, TypeAlias
from arithmetic import *
import random

TrustedSetup: TypeAlias = Tuple[List[Tuple[FQ, FQ]], List[Tuple[FQ2, FQ2]]]
PointG1: TypeAlias = Tuple[FQ, FQ]
PointG2: TypeAlias = Tuple[FQ2, FQ2]

# Generate a trusted setup for the KZG scheme. Secret should be generated as part of a MPC ceremony.
# Degree is the degree of the polynomial that will be committed to.


def trusted_setup(degree: int) -> TrustedSetup:

    # generate a random 256-bit integer secret tau
    bit_string = ''.join(str(random.randint(0, 1)) for _ in range(256))
    tau = int(bit_string, 2)

    # tau must be a field element
    tau_mod: int = tau % curve_order

    powers_of_tau_g1: List[PointG1] = []
    powers_of_tau_g2: List[PointG2] = []

    for i in range(degree + 1):
        s_pow: int = pow(tau_mod, i, curve_order)

        point_g1: Optional[PointG1] = multiply(G1, s_pow)
        point_g2: Optional[PointG2] = multiply(G2, s_pow)

        if point_g1 is None or point_g2 is None:
            raise ValueError("Scalar multiplication failed.")

        powers_of_tau_g1.append(point_g1)
        powers_of_tau_g2.append(point_g2)

    return powers_of_tau_g1, powers_of_tau_g2

# Generate KZG commtiment for a polynomial. 
# The coefficients of the polynomial are given as a list of field elements ordered from lowest to highest degree.


def commit(ts: TrustedSetup, poly: List[int]) -> PointG1:

    tau_g1, _ = ts

    if len(tau_g1) != len(poly):
        raise ValueError("Polynomial length does not match trusted setup.")

    # commitment = g * poly(tau)
    c: PointG1 = evaluate_poly_at_tau(poly, ts[0])

    return c

# Generate evalaution proof for a polynomial. p(z) = y
# The coefficients of the polynomial are given as a list of field elements ordered from lowest to highest degree.


def generate_evaluation_proof(ts: TrustedSetup, poly: List[int], z: int, y: int) -> PointG1:

    # numerator is poly - y
    poly[0] = field_sub(poly[0], y)
    num: List[int] = poly

    # denominator is x - z
    den: List[int] = [field_sub(0, z), 1]

    # perform polynomial division
    quotient, remainder = poly_div(num, den)

    # assert that remainder is 0
    if remainder != [0]:
        raise ValueError("Remainder is not 0.")

    # π = g*q(tau)
    proof: PointG1 = evaluate_poly_at_tau(quotient, ts[0])

    return proof

# Verify evaluation proof π for a polynomial p(z) = y, given the commitment c = g * p(tau)
# Verification is performed via a pairing check.


def verify_proof(ts: TrustedSetup, c: PointG1, proof: PointG1, z: int, y: int) -> bool :
    s2: PointG2 = ts[1][1]

    z_g2_neg: Optional[PointG2] = multiply(G2, field_sub(0, z))

    if z_g2_neg is None:
        raise ValueError("Scalar multiplication failed.")

    sz: Optional[PointG2] = add(s2, z_g2_neg)

    if sz is None:
        raise ValueError("Scalar multiplication failed.")

    y_g1_neg: Optional[PointG1] = multiply(G1, field_sub(0, y))

    if y_g1_neg is None:
        raise ValueError("Scalar multiplication failed.")

    cy: Optional[PointG1] = add(c, y_g1_neg)

    if cy is None:
        raise ValueError("Scalar multiplication failed.")

    h: Optional[PointG2] = multiply(G2, 1)
    
    if h is None:
        raise ValueError("Scalar multiplication failed.")

    # e(proof, [s]₂ - [z]₂) == e(c - [y]₁, H)
    return pairing(sz, proof) == pairing(h, cy)


# Evaluate a polynomial at tau using the powers of tau from the trusted setup.


def evaluate_poly_at_tau(poly: List[int], powers_of_tau_g1: List[PointG1]) -> PointG1:
    r: Optional[PointG1] = multiply(powers_of_tau_g1[0], poly[0])

    if r is None:
        raise ValueError("Scalar multiplication failed.")

    for i in range(1, len(poly)):
        to_add: Optional[PointG1] = multiply(powers_of_tau_g1[i], poly[i])

        r = add(r, to_add)

        if r is None:
            raise ValueError("Addition failed.")

    return r