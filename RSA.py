import random


def is_prime(n):
    if n in [2, 3]:
        return True
    if n == 1 or n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def mod_inverse(a, m):
    m0 = m
    x0 = 0
    x1 = 1

    if m == 1:
        return 0

    while a > 1:
        q = a // m
        t = m

        m = a % m
        a = t
        t = x0

        x0 = x1 - q * x0
        x1 = t

    if x1 < 0:
        x1 = x1 + m0

    return x1


def keys(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    elif p < 12 and q < 12 or q < 6 or q < 6:
        raise ValueError('p and q cannot be equal')
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 8
    while is_prime(e):
        e = random.randrange(1, phi)

    g = gcd(e, phi)
    while g != 1:
        # while (is_prime(e)):
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    print(e)
    d = mod_inverse(e, phi)
    print(len(str(e)))
    print(len(str(n)))
    print(len(str(d)))

    return (e, n), (d, n)


# def encrypt(pk, msg):
#     key, n = pk
#     enc_msg = [(ord(char) ** key) % n for char in msg]
#     return enc_msg
def encrypt(package, msg_plaintext):
    # unpack key value pair
    e, n = package
    msg_ciphertext = [pow(ord(c), e, n) for c in msg_plaintext]
    return msg_ciphertext


def decrypt(pk, e_msg):
    key, n = pk
    plain = [chr((char ** key) % n) for char in e_msg]
    return ''.join(plain)
