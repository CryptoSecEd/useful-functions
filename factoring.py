# Python 3 program to find a prime factor of composite using
# Pollard's Rho algorithm
# This code is contributed by chitranayal 

import random
import math
from sympy import isprime

 
# method to return prime divisor for n
def Pollard_Rho_one(n):
    # print(f"In Pollard_Rho_one(): {n}")
    # no prime divisor for 1
    if (n == 1):
        return n
    # even number means one of the divisors is 2
    if (n % 2 == 0):
        return 2
    # we will pick from the range [2, N)
    x = (random.randint(0, 2) % (n - 2))
    y = x
    # the constant in f(x).
    # Algorithm can be re-run with a different c
    # if it throws failure for a composite.
    c = (random.randint(0, 1) % (n - 1))
    # Initialize candidate divisor (or result)
    d = 1
    # until the prime factor isn't obtained.
    # If n is prime, return n
    while (d == 1):
        # print(f"x is {x} y is {y} c is {c}")
        # Tortoise Move: x(i+1) = f(x(i))
        x = (pow(x, 2, n) + c + n)%n
        # Hare Move: y(i+1) = f(f(y(i)))
        y = (pow(y, 2, n) + c + n)%n
        y = (pow(y, 2, n) + c + n)%n
        # check gcd of |x-y| and n
        d = math.gcd(abs(x - y), n)
        # retry if the algorithm fails to find prime factor
        # with chosen x and c
        if (d == n):
            return -1
    return d

# method to return all prime divisors for number
def Pollard_Rho_all(number):
    n = number
    all_factors = {}
    while not isprime(n) and n != 1:
        # print(f"Trying with {n}")
        factor = -1
        while factor == -1:
            factor = Pollard_Rho_one(n)
        # Pollard_Rho_one may give a prime power so I'm just skipping 
        # this case. If I want to get a little bit more efficiency, I 
        # could add a check for a prime squared, cubed, etc.
        if not isprime(factor):
            continue
        if ((n % factor) == 0 and n > factor):
            # print("One of the divisors for", n , "is ",factor)
            while math.gcd(n, factor) > 1 and n != 1:
                if factor in all_factors:
                    all_factors[factor] = all_factors[factor] + 1
                else:
                    all_factors[factor] = 1
                n = n // factor
            # print(all_factors)
        else:
            print(f"Pollard_Rho_one() gave a false factor: {factor} {n}")
            raise ValueException
    # print("Exiting as only left with a prime number.")
    if n == 1:
        pass
    elif n in all_factors:
        all_factors[n] = all_factors[n] + 1
    else:
        all_factors[n] = 1
    only_primes = True
    check = 1
    for i in all_factors:
        check *= i**all_factors[i]
        if not isprime(i):
            only_primes = False
            print("Found a factor in Pollard_Rho_all that is not prime: {all}")
            raise ValueException
    # print(f"Factors all are prime? {only_primes}")
    if check != number:
        print(f"Pollard_Rho_all() did not correctly factor {number}")
        print(all_factors)
        raise ValueError
    return(all_factors)


# Driver function
def main():
    n = 10967535067
    # Below value is from RookieMistake challenge (p)
    # n = 0x16498bf7cc48a7465416e0f9ec8034f4030991e73aff9524ef74cc574228e36e6e1944c7686f69f0d1186a69b7aa77d7e954edc8a6932f006786f4648ecc8d4f4d3f6c03d9a1ee9fe61b28b6dd2791a63be581b8811a8ac90a387241ea68b7d36b4a274f64c7a721ad55cfcef23cd14c72542f576e4b507c11c4fa198e80021d484691b
    # n = n-1
    # Below value is from RookieMistake challenge (q)
    p = 0x16498bf7cc48a7465416e0f9ec8034f4030991e73aff9524ef74cc574228e36e6e1944c7686f69f0d1186a69b7aa77d7e954edc8a6932f006786f4648ecc8d4f4d3f6c03d9a1ee9fe61b28b6dd2791a63be581b8811a8ac90a387241ea68b7d36b4a274f64c7a721ad55cfcef23cd14c72542f576e4b507c11c4fa198e80021d484691b
    n = 0xbe30ccaf896c16f53515e298df25df9158d0a95295c119f0444398b94fae26c0b4cf3a43b120cf0fb657069e0621eb1d2dd832eef3065e80ddbc35854dd4585cc41fd6a5b36339c0d9fcc066272be6818be6a624f75482bbb9c408010ac8c27b20397d870bfcb14e6318097b1601f99e391c9b68c5c586f8da561ff8507be9212713b910b748370ce692c11afa09b74ce80c5f5dd72046415aeed85e1ecedca14abe17ed19ab97729b859120699d9f80dd13f8483773df15b938b8399702a6e846b8728a70f1940d4c6e5835a06a89925eb1ec91a796f270e2d9be1a2c4bee5517109c161f04333d9c0d4034fbbd2dcf69fe734b759a89937f4d8ea0ee6b8385aae14a2cce361
    q = (n // p)

    print(f"Attempting to factor: {p-1}")
    all_f_p = Pollard_Rho_all(p-1)
    print(all_f_p)
    print(f"Attempting to factor: {q-1}")
    all_f_q = Pollard_Rho_all(q-1)
    print(all_f_q)
     
  

# Driver function
if __name__ == "__main__":
    main()