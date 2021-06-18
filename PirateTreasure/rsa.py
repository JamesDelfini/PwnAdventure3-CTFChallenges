import random
import math

# Modular Multiplicative Inverse explains at the reference [1]
# [1] https://en.wikipedia.org/wiki/Modular_multiplicative_inverse
#
# Iterative Python 3 program to find
# modular inverse using extended
# Euclid algorithm
#
# Returns modulo inverse of a with
# respect to m using extended Euclid
# Algorithm Assumption: a and m are
# coprimes, i.e., gcd(a, m) = 1
#
# [2] https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/


def modInverse(a, m):
    m0 = m
    y = 0
    x = 1

    if (m == 1):
        return 0

    while (a > 1):

        # q is quotient
        q = a // m

        t = m

        # m is remainder now, process
        # same as Euclid's algo
        m = a % m
        a = t
        t = y

        # Update x and y
        y = x - q * y
        x = t

    # Make x positive
    if (x < 0):
        x = x + m0

    return x


# Python3 program to calculate
# Euler's Totient Function
def phi(n):

    # Initialize result as n
    result = n

    # Consider all prime factors
    # of n and subtract their
    # multiples from result
    p = 2
    while(p * p <= n):

        # Check if p is a
        # prime factor.
        if (n % p == 0):

            # If yes, then
            # update n and result
            while (n % p == 0):
                n = int(n / p)
            result -= int(result / p)
        p += 1

    # If n has a prime factor
    # greater than sqrt(n)
    # (There can be at-most
    # one such prime factor)
    if (n > 1):
        result -= int(result / n)
    return result

# Key Generation explains at the reference link [1]
# [1] https://en.wikipedia.org/wiki/RSA_(cryptosystem)
# let n: Modulus
# let e: Public Key
# let d: Private Key
# let t: The text to cipher
# let c: = Ciphered text
# let p & q: Prime Numbers
# Returns a tuple of e and d


def rsa(p, q, e=0):
    # 1. Choose two distinct prime numbers p and q.
    # (N) Modulus = 03C9921AC0185B3AAAE37E1B
    # p = 33759901540733
    # q = 34719860683127

    # 2. Compute n = pq.
    n = p * q
    print("N = {0} | Length {1}".format(n, n.bit_length()))

    # 3. Compute λ(n), where λ is Carmichael's totient function. Since n = pq, λ(n) = lcm(λ(p),λ(q)), and since p and q are prime, λ(p) = φ(p) = p − 1 and likewise λ(q) = q − 1. Hence λ(n) = lcm(p − 1, q − 1).
    lcm = (p-1)*(q-1)
    print("LCM = {0}".format(lcm))

    # 4. Choose an integer e such that 1 < e < λ(n) and gcd(e, λ(n)) = 1; that is, e and λ(n) are coprime.
    # e = 0
    # e = 259037971019840732176753053

    while not ((1 < e and e < lcm) and math.gcd(e, lcm) == 1):
        e = random.randint(0, lcm)

    print("e = {0}".format(e))
    # 5. Determine d as d ≡ e−1 (mod λ(n)); that is, d is the modular multiplicative inverse of e modulo λ(n).
    d = modInverse(e, lcm)
    print("d = {0}".format(d))

    t = 19971505
    rsa_encrypt = pow(t, e, n)
    print("The encrypted value = {0}".format(rsa_encrypt))

    rsa_decrypt = pow(rsa_encrypt, d, n)
    print("The decrypted value = {0}".format(rsa_decrypt))

    return e, d


# Sample Usage
p = 33759901540733
q = 34719860683127
# e = 0
e = 259037971019840732176753053
# # e = int("611C0519E05065E8F38DA1", 16)
pubKey, privKey = rsa(p, q, e)
# print(hex(privKey))
# print(pubKey, privKey)
n = 0x03C9921AC0185B3AAAE37E1B
d = 475630479039977958915270053
key = 19971505
# Using the private key to encrypt and public key to encrypt
# print(pow(key, d, n)) # 229884806990311584260464218
# print(pow(pow(key, d, n), e, n))
# print(pow(key, e, n)) # 20821581874624798982971432
# print(pow(pow(key, e, n), d, n))

# Get the private key through the modulus and exponent, d = modInverse(exponent, n-(p+q-1))
n = 0x03C9921AC0185B3AAAE37E1B
exponent = 0x10001
d = modInverse(exponent, n-(p+q-1))
print((hex(d)))

# Get the public key through the private key
# e = modInverse(d, phi(n))
# print((hex(e)))

# cnt = 0
# pubKeyPrev = 259037971019840732176753053
# while(True):
#     cnt += 1
#     pubKey, privKey = rsa(p, q, e)

#     print(cnt)
#     gcd = math.gcd(pubKeyPrev, pubKey)
#     if (gcd != 1):
#         print(pubKey, pubKeyPrev, gcd)
#         break

#     pubKeyPrev = pubKey


msg = 0x1a057e6ea80244502713f900
print(hex(pow(msg, d, n)))
