"""Some useful general functions
"""

from random import randint

from Crypto.Util.number import getPrime


def solve_crt(remainders, moduli):
    """Solve the Chinese Remainder Theorem problem
    """
    # print(f"In solve_crt() with {remainders} and {moduli}")
    if len(remainders) != len(moduli):
        print("Error in solve_crt(). Arguments must be two lists with the" +
              f"same lengths: {len(remainders)} {len(moduli)}")
        raise ValueError
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


def main():
    """Try calculating discrete logs using some small examples."""
    m1 = getPrime(10)
    m2 = getPrime(11)
    m3 = getPrime(12)

    x1 = randint(1, m1)
    x2 = randint(1, m2)
    x3 = randint(1, m3)

    x = solve_crt([x1, x2, x3], [m1, m2, m3])

    print(x)


if __name__ == "__main__":
    main()
