def mmi(a: int, m: int) -> int:
    for X in range(1, m):
        if ((a % m) * (X % m)) % m == 1:
            return X
    return -1






def gcd(p: int, q: int) -> int:
    while q != 0:
        p, q = q, p % q
    return p



def is_coprime(x: int, y: int) -> bool:
    return gcd(x, y) == 1
