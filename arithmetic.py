from py_ecc.bn128 import curve_order
from typing import List, Tuple


def field_sub(a: int, b: int) -> int:
    return (a - b) % curve_order


def modular_inverse(a: int) -> int:
    return pow(a, curve_order - 2, curve_order)


def field_div(a: int, b: int) -> int:
    return (a * modular_inverse(b)) % curve_order


def poly_div(a: List[int], b: List[int]) -> Tuple[List[int], List[int]]:
    r = array_of_zeroes(len(a) - len(b) + 1)
    rem = a
    while len(rem) >= len(b):
        l = field_div(rem[len(rem)-1], b[len(b)-1])
        pos = len(rem) - len(b)
        r[pos] = l
        aux = array_of_zeroes(pos)
        aux.append(l)
        aux2 = poly_sub(rem, poly_mul(b, aux))
        rem = aux2[:-1]

    return r, rem


def array_of_zeroes(length: int) -> List[int]:
    return [0] * length


def poly_sub(a: List[int], b: List[int]) -> List[int]:
    r = array_of_zeroes(max(len(a), len(b)))
    for i in range(len(a)):
        r[i] = a[i]
    for i in range(len(b)):
        r[i] = field_sub(r[i], b[i])
    return r


def poly_mul(a: List[int], b: List[int]) -> List[int]:

    r = array_of_zeroes(len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            r[i + j] = (r[i + j] + (a[i] * b[j])) % curve_order

    return r
