import random

with open("primes.txt",'r') as f:
    primes = [int(x) for x in f.read().strip().replace("  "," ").split('\n')]

O = (None,None)

def add_tuple(P, Q, p):
    px,py = P
    qx,qy = Q
    m = ((py-qy)/(px-qx)) % p
    rx = (m**2 - px - qx) % p
    ry = (m*(px-rx) - py) % p
    return (rx,ry)

def sub_tuple(P, Q, p):
    qx, qy = Q
    qy = (-1 * qy) % p 
    return add_tuple(P,(qx,qy),p)

def double_tuple(P, p, a):
    px,py = P
    if py == 0:
        return O
    m = (((3 * (px**2)) + a)/ (2*py)) % p 
    rx = (m**2 - 2*px) % p
    ry = (m*(px-rx) - py) % p
    return (rx,ry)

def scale_tuple(x,P,p,a):
    wasodd = False
    if x % 2 == 1:
        wasodd = True
        ext = P
        x -=1

    while x != 1:
        P = double_tuple(P, p, a)
        x /= 2
    
    if wasodd:
        return add_tuple(P,ext,p)
    else:
        return P


def generate_parameters():
    print("Curve data")
    a = int(input("a = "))
    b = int(input("b = "))
    p = int(input("Prime P = "))
    G = []
    for i in range(p-1):
        for j in range(p-1):
            if (j**2) == ((i**3 + a*i + b) % p):
                G.append((i,j))
    Base = random.choice(G)
    prikey = int(input("Private key (for decryption) = "))
    pubkey = scale_tuple(prikey, Base, p, a)
    print(f"Public key : {pubkey}")
    return a,b,p,G,Base,prikey,pubkey
    
def assign_point(plainteks, G):
    if len(set(plainteks)) > len(G):
        print("Not enough points for plainteks length")
        return []
    else:
        ttp = {}
        ptt = {}
        pt = set(plainteks)
        for i in pt:
            x = random.choice(G)
            ttp[i] = x
            ptt[x] = i
            G.remove(x)
    return ttp, ptt

def encrypt(plainteks, ttp, Base, p, pubkey, a):
    kr = random.randint(1,p-1)
    ciphertuples = []
    for pm in plainteks:
        pc = (scale_tuple(kr, Base, p, a), add_tuple(ttp[pm],scale_tuple(kr, pubkey, p, a), p))
        ciphertuples.append(pc)
    return ciphertuples

def decrypt(ciphertuples, ptt, prikey, p, a):
    plainteks = []
    for pc in ciphertuples:
        pm = sub_tuple(pc[1],scale_tuple(prikey, pc[0], p, a), p)
        plainteks.append(pm)
    return plainteks

if __name__=='__main__':
    a,b,p,G,Base,prikey,pubkey = generate_parameters()
    print(G)
    plainteks = input("Masukkan Plainteks : ")
    ttp, ptt = assign_point(plainteks, G)
    print(ttp)
    print(ptt)
    e = encrypt(plainteks, ttp, Base, p, pubkey, a)
    print(e)
    d = decrypt(e, ptt, prikey, p, a)
    print(d)