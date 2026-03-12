"""This script contains functions used to calculate discrete logs
Pohlig-Hellman code is from:
https://github.com/christiankrug/pohlig_hellman/blob/master/main.py
"""

from math import ceil, sqrt
from random import randint

from Crypto.Util.number import getPrime
from sympy import isprime, mod_inverse

from factoring import Pollard_Rho_all


def baby_step_giant_step(beta, p, alpha, n):
    """Find discrete log of beta to base alpha mod p, alpha has order n
    p is not necessarily prime

    :param beta: Base of group
    :type beta: ``int``
    :param p: Modulus for all calculations
    :type p: ``int``
    :param alpha: Generator of the group
    :type alpha: ``int``
    :param n: Order of the group
    :type n: ``int``
    :raises ValueError: If alpha is not a generator
    :rtype: ``str``
    """
    # print(f"beta: {beta} p: {p} alpha: {alpha} n: {n}")
    if pow(alpha, n, p) != 1:
        print(f"{alpha} does not have order {n}")
        raise ValueError
    # Handle trivial cases
    if beta == 1:
        return 0
    if beta == alpha:
        return 1
    m = ceil(sqrt(n))
    # print(f"m: {m}")
    alpha_powers = {}
    count = 0
    checkpoint = 2
    for j in range(0, m+1):
        if count == checkpoint:
            # print(f"Baby steps. At checkpoint: {count}")
            checkpoint *= 2
        count += 1
        alpha_powers[pow(alpha, j, p)] = j
    # print(f"alpha_powers: {alpha_powers}")
    count = 0
    checkpoint = 2
    gamma = beta
    for i in range(0, m):
        if count == checkpoint:
            # print(f"Giant steps. At checkpoint: {count}")
            checkpoint *= 2
        count += 1
        # print(f"gamma is {gamma}")
        if gamma in alpha_powers:
            discrete_log = i * m + alpha_powers[gamma]
            if pow(alpha, discrete_log, p) != beta:
                print("baby_step_giant_step() calculated discrete log as " +
                      f"{discrete_log} but that value is not the correct " +
                      "discrete log.")
                raise ValueError
            return discrete_log
        gamma = gamma * pow(alpha, -m, p) % p
    print(f"Unable to find discrete log of {beta} to base {alpha} mod {p}")
    raise ValueError


def calculate_subgrp_congruences(alpha, beta, p, q, pi, power):
    """Find a value di such that gi**di = hi mod p
    """
    # print(f"In calculate_subgrp_congruences() with {alpha} {beta} " +
    #       f"{p} {q} {pi} {power}")
    if (q % pi**power) != 0:
        print("Error in calculate_subgrp_congruences()")
        print("q is not divisible by pi**power")
        raise ValueError

    gi = pow(alpha, q // (pi**power), p)
    hi = pow(beta, q // (pi**power), p)

    return baby_step_giant_step(hi, p, gi, pi)


def solve_crt(remainders, moduli):
    """Solve the Chinese Remainder Theorem problem
    """
    # print(f"In solve_crt() with {remainders} and {moduli}")
    n = 1
    for i in moduli:
        n *= i
    x = 0
    for i in range(len(remainders)):
        yi = n // moduli[i]
        zi = pow(yi, -1, moduli[i])
        x += remainders[i] * yi * zi
    for i in range(len(remainders)):
        if x % moduli[i] != remainders[i]:
            print("solve_crt() did not calculate the correct solution")
            print(f"Remainders: {remainders}")
            print(f"Moduli: {moduli}")
            print(f"Solution obtained: {x}")
            raise ValueError
    return x % n


def solve_dl(beta, p, alpha):
    """Solve the discrete log of beta to base alpha mod p, with p prime
    Uses the Pohlig-Hellman algorithm
    """
    print(f"Starting solve_dl(): {beta} {p} {alpha}")
    if not isprime(p):
        print("solve_dl() requires p prime: {p}")
        raise ValueError
    if pow(beta, p-1, p) != 1:
        print("Error, order of beta is not p-1")
        raise ValueError
    pr_output = Pollard_Rho_all(p-1)
    factors = pr_output.keys()
    dlogs = []
    print(f"The prime factors found are {factors}.")
    for factor in factors:
        dlogs.append(calculate_subgrp_congruences(alpha, beta, p, p-1,
                     factor, pr_output[factor]))
    print(f"The Discrete logs found are {dlogs}.")
    key = solve_crt(dlogs, list(factors))

    if pow(alpha, key, p) != beta:
        print("solve_dl() failed to find the correct discrete log!")
        print(f"{key} is not the discrete log of {beta} base {alpha} mod {p}")
        raise ValueError
    return (key, pr_output)


def main():
    """Try calculating discrete logs using some small examples."""
    p = getPrime(8)
    x = randint(2, p - 2)
    print(f"Discrete log is: {x}")
    alpha = 3
    beta = pow(alpha, x, p)
    output = baby_step_giant_step(beta, p, alpha, p-1)
    print(f"Output is: {output}")
    if (beta - pow(alpha, output, p)) == 0:
        print("baby_step_giant_step() calculated the correct discrete log!")
    else:
        print("baby_step_giant_step() did not correctly calculate the " +
              "discrete log")
        print(f"target: {beta} value: {pow(alpha, output, p)}")
        print(f"p: {p} x: {x} alpha: {alpha} output: {output}")
        raise ValueError

    # These are the values from RookieMistake/small/gen.py
    p = 0x8b0a0fb358935588ae54f5bd0677d4415600f2f793aad6f3b9b4dc377f94b51173f0dbf5a4999edf2fb8296296b1baf04c8b1ae3da0b90e57ed974f31454dcc7f4b088054f6301c0a422f5b2eacb9b58bfebf2641b046d7212b6bac7f1162a7b80f649daa25f80d2e58f9e20b75748679270ba6bafd52f31b4d4368162c553ee6aeb4797
    n = 0xdf216294fb0ca422699c093dc1ff7270bb6ef15bf3c2701e44805b093e7a563f6c32274e02eba0e791fe810f4a3e8f8453618065fd08f59646e872556ff8a587d566093345f728e0076874537f6ff076b799e23cfa86726c94b08ae6dc85eaf184c837ed114cd928aea3a68cee0bafccc37d73a4f8f0ed5f2cc46034096bb23f3a6c69e0121de9c3f1c6c9524dbbfe7abbdcce1ff9fb182aa56e7262c9ec799aa9a13b9c80109c7e0453c7da95605ac8dafced7a90e3e30fbb4391a35475b13efea48a30d08b808dae8e670a5950bf7d80c529fbaa66f2e262d98dd7f8cccd056ec1ac36c9d074479e26d126f540883fdcb6e5b7d37b98ea057e5000a0ce835f6e7a39d9e9a0f89
    q = n // p
    a = 0xa79c112d8ff8bac91df13e9a7a95a31bb6dcbcf03ad3218bbe86546480580d55ca86cedd879d4e0242e66fb4055993c60feb7fd4065e551c490889bed3a70228b85b14028f5d61ace897bf217b80f78fdee7d184a67ef6437f342d153c39721f20f638db59e1c49e6d348a775f4b5511f40a5db858d98ff462cddfbefa459903419f026fe3c0e2b4e5ced3bc52fc7c506faacedb1446cde65af996215f8366250430460a16cff0b2573e0de99750b7b2d630478d2172c7e7ce7c80748a81fa7d1b256ab9680a84d93b3d125de279ee9b4fc644aa534c3e8ef061d2e069457960760c4ae2578074f8f0f8b82ac9191cd81efc3ea04ea10fa9d6e3b1450acd74febbb167bb06f06a2
    print(f"p is {p} and q is {q} and n is {n}")
    gen = 0x69420
    print(f"Generator gen is {gen}")
    solve_dl(a % p, p, gen)
    solve_dl(a % q, q, gen)


if __name__ == "__main__":
    main()
