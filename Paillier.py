import random
from math import gcd
from RSA import modinv

with open("primes.txt",'r') as f:
    primes = [int(x) for x in f.read().strip().replace("  "," ").split('\n')]
    primes = primes[6:200]

def L(x,n):
    return (x-1)/n

def generate_key():
    p = random.choice(primes)
    q = random.choice(primes)
    # print(f"{p} {q} {p*q} {p-1} {q-1} {(p-1)*(q-1)}")
    while gcd(p*q,(p-1)*(q-1)) != 1 or p == q:
        print("retry")
        # print(f"{p} {q} {p*q} {p-1} {q-1} {(p-1)*(q-1)}")
        p = random.choice(primes)
        q = random.choice(primes)
    n = p*q
    delta = int(abs((p-1)*(q-1)) / gcd(p-1,q-1))
    g = random.randint(1, n**2 - 1)
    # print(p,q,n,delta,g)
    x = (g**delta) % (n**2)
    myu = modinv(((x-1)/n),n)
    if 'y' in input("Do you want to save file? y for yes"):
        name = input("Enter filename : ")
        with open(f"{name}.pub", 'w') as f:
            f.write(f"{g}\n{n}")
        with open(f"{name}.priv", 'w') as f:
            f.write(f"{delta}\n{myu}")
    return p,q,n,delta,g,x,myu

def encrypt(plainteks, g, n):
    r = random.randint(0,n)
    while gcd(r,n) != 1:
        r = random.randint(0,n-1)
    cipherteks = []
    for m in plainteks:
        mi = ord(m)
        ci = ((g ** mi) * (r ** n)) % (n**2)
        cipherteks.append(ci)
    return cipherteks

def decrypt(cipherteks, delta, n, myu, g):
    plainteks = []
    for ci in cipherteks:
        mi = (L((ci ** delta) % (n**2),n) * (myu)) % n
        plainteks.append(mi)
    # return plainteks
    # print(plainteks)
    return "".join([chr(int(x)) for x in plainteks])

if __name__=='__main__':
    p,q,n,delta,g,x,myu = generate_key()
    # print(p,q,n,delta,g,x,myu)
    # p,q,n,delta,g,myu = 7,11,77,30,5652,74
    plainteks = input("Masukkan Plainteks : ")
    e = (encrypt(plainteks,g,n))
    print("Cipher : ")
    print(e)
    d = decrypt(e,delta,n,myu,g)
    print("Redeciphered : ")
    print(d)