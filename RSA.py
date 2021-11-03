def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        print(f"Modular inverse for {a} and {m} do not exist")
        return 0
    else:
        return x % m
        
def rsa_key_gen():
    p = int(input("Masukkan P : "))
    q = int(input("Masukkan Q : "))
    n = p*q
    omegan = (p-1) * (q-1)
    e = int(input(f"Masukkan E, E harus relatif prima dengan {omegan} : "))
    while (omegan / e) % 1 == 0:
        e = int(input(f"Masukkan E, E harus relatif prima dengan {omegan} : "))
    d = modinv(e, omegan)
    if 'y' in input("Do you want to save file? y for yes"):
        name = input("Enter filename : ")
        with open(f"{name}.pub", 'w') as f:
            f.write(f"{n}\n{e}")
        with open(f"{name}.priv", 'w') as f:
            f.write(f"{p}\n{q}\n{omegan}\n{d}")
    return p,q,n,omegan,e,d

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

def encrypt(blocklist, n, e):
    bl = len(str(blocklist[0])) / 3
    cipherblocks = []
    for mi in blocklist:
        ci = (int(mi) ** e) % n
        cipherblocks.append(str(ci))
    return cipherblocks

def decrypt(cipherblocks, d, n):
    bl = (len(str(cipherblocks[0])) // 3) + 1
    deciphered = []
    for ci in cipherblocks:
        mi = (int(ci) ** d) % n
        deciphered.append('0'*(bl*3-len(str(mi))) + str(mi))
    return deciphered

def stringify(blocks):
    retval = ""
    for block in blocks:
        retval += chr(int(block))
    print(retval)
    return retval



if __name__=='__main__':
    plain = input("Masukkan plainteks : ")
    p,q,n,omegan,e,d = rsa_key_gen()
    print(f"{n} {omegan} {e} {d}")
    b = blocksplit(plain,1)
    print(f"blocksplit = ",end="")
    print(b)
    c = encrypt(b, n, e)
    print(f"cipherblocks = ",end="")
    print(c)
    print("Cipherteks : ",end="")
    stringify(c)
    de = decrypt(c, d, n)
    print(f"decipherd blocks = ",end="")
    print(de)
    print("Deciphered from Cipherteks : ",end="")
    stringify(de)