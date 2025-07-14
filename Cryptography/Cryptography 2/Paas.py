from pwn import *
import math
from Crypto.Util.number import inverse
from Crypto.Util.number import long_to_bytes


e = 65537
modulus = {}
r = remote("paas.challs.cyberchallenge.it", 9047)
r.recv()
r.sendline(b"1")
n = int(r.recvline().decode().split(" ")[1])
cipher_text = int(r.recvline().decode().split(" ")[1])
modulus[n] = cipher_text

r.recvline()
r.recvline()
r.recvline()



for i in range (20):
	r.sendline(b"1")
	r.recv()
	print(i)
	n = int(r.recvline().decode().split(" ")[1])
	cipher_text = int(r.recvline().decode().split(" ")[1])
	modulus[n] = cipher_text


	r.recvline()
	r.recvline()
	r.recvline()

found = False
shared_prime = 0;
n= 0;
cipher = 0;

for key1 in modulus:
    for key2 in modulus:
        if math.gcd(key1, key2) != 1 and math.gcd(key1, key2) != key1  and math.gcd(key1, key2) != key2:
            print("this is shared_prime: " + str(math.gcd(key1, key2)))
            shared_prime = math.gcd(key1, key2)
            print("this is one of the modulus: " + str(key1))
            n = key1
            print("this is the cipher_text associated with that modulus: "+ str(modulus[key1]))
            cipher = modulus[key1]
            print("this is the other modulus: " + str(key2))
            print("this is the cipher_text associated with the other modulus: "+ str(modulus[key2]))
            found = True
            break
    if found:
        break

q = n//shared_prime
phi_n = (q-1)*(shared_prime-1)
d = inverse (e, phi_n)
print(long_to_bytes(pow(cipher, d, n)))