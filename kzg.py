from py_ecc import bn128
from py_ecc.fields import FQ, FQ2
from py_ecc.bn128 import G1, G2, multiply, curve_order
from typing import List, Tuple, Optional, TypeAlias
import random

TrustedSetup: TypeAlias = Tuple[List[Tuple[FQ, FQ]], List[Tuple[FQ2, FQ2]]]

def trusted_setup (length: int) -> TrustedSetup:

    # generate a random 256-bit integer
    bit_string = ''.join(str(random.randint(0, 1)) for _ in range(256))
    s = int(bit_string, 2)

    # s must be a field element
    s: int = s % curve_order

    tau_g1: List[Tuple[FQ, FQ]]= []
    tau_g2: List[Tuple[FQ2, FQ2]]= []

    for i in range(length):
        s_pow: int = pow(s, i, curve_order)

        point_g1: Optional[Tuple[FQ, FQ]] = multiply(G1, s_pow)
        point_g2: Optional[Tuple[FQ2, FQ2]] = multiply(G2, s_pow)

        if point_g1 is None or point_g2 is None:
            raise ValueError("Scalar multiplication failed.")

        tau_g1.append(point_g1)
        tau_g2.append(point_g2)

    return tau_g1, tau_g2
