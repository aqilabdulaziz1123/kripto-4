import random

with open("primes.txt",'r') as f:
    primes = [int(x) for x in f.read().strip().replace("  "," ").split('\n')]


def generate_key():
    p = random.choice(primes)
    g = random.randint(-1000,p-1)
    x = random.randint(1,p-2)
    y = (g**x) % p
    if 'y' in input("Do you want to save file? y for yes"):
        name = input("Enter filename : ")
        with open(f"{name}.pub", 'w') as f:
            f.write(f"{y}\n{g}\n{p}")
        with open(f"{name}.priv", 'w') as f:
            f.write(f"{x}\n{p}")
    return p,g,x,y


def blocksplit(plainteks, bl):
    plainteks = plainteks.strip()
    blocklist = []
    for i in range(0,len(plainteks),bl):
        if i+bl <= len(plainteks):
            # a,b = str(ord(plainteks[i])), str(ord(plainteks[i+1]))
            block = "".join(['0'*(3 - len(str(ord(x)))) + str(ord(x)) for x in plainteks[i:i+bl]])
        else:
            block = "".join(['0'*(3 - len(str(ord(x)))) + str(ord(x)) for x in plainteks[i:len(plainteks)]])
            block = '0' * (len(block) % 3) + block + '0' * (bl*3 - len(block))
        blocklist.append(block)
    # for ch in plainteks:
    #     a = str(ord(ch))
    #     blocklist.append('0'*max(0,3-len(a)) + a)
    return blocklist

def encrypt(plainblocks,p,g,y):
    k = random.randint(1,p-2)
    ciphers = []
    for blocks in plainblocks:
        a = (g**k) % p
        b = ((y ** k) * int(blocks)) % p
        ciphers.append((a,b))
    return ciphers

def decrypt(ciphertuples, p, x):
    plainteks = []
    for tuples in ciphertuples:
        a,b = tuples
        axmin1 = a **(p-1-x)
        plain = (b * axmin1) % p
        plainteks.append(plain)
    return plainteks

if __name__=='__main__':
    p,g,x,y = generate_key()
    print(f"Randomly Generated\np = {p}\ng = {g}\nx = {x}\ny = {y}")
    plainteks = input("Masukkan Plainteks : ")
    blocks = blocksplit(plainteks,1)
    e = encrypt(blocks, p, g, y)
    print("Encrypted tuples = ")
    print(e)
    d = decrypt(e, p , x)
    print("Redecrypted = ")
    print("".join([chr(int(ch)) for ch in d]))