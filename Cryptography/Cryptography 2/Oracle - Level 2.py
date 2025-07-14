from sys import exit

from Crypto.Util.number import long_to_bytes
from gmpy2 import *
from pwn import *

# encrypt(x)**2 - encrypt(x**2) is multiple of 'n'.
# e = 65537
# c = flag_encrypted
# n = ?
HOST = "oracle.challs.cyberchallenge.it"
PORT = 9042
r = remote(HOST, PORT)

r.recvuntil('flag: ')
flag_encrypted = r.recvline().decode()[0:-1]

r.recvuntil('> ')
r.sendline(str(1).encode())

r.recvuntil('Plaintext > ')
r.sendline(str(109).encode())

r.recvuntil('Encrypted: ')
two_encrypted = int(r.recvline().decode()[0:-1])

encrypt_x_2 = two_encrypted ** 2

r.recvuntil('> ')
r.sendline(str(1).encode())

r.recvuntil('Plaintext > ')
r.sendline(str(11881).encode())

r.recvuntil('Encrypted: ')
encrypt_x2 = int(r.recvline().decode()[0:-1])

multiple_n1 = encrypt_x_2 - encrypt_x2

r.recvuntil('> ')
r.sendline(str(1).encode())

r.recvuntil('Plaintext > ')
r.sendline(str(167).encode())

r.recvuntil('Encrypted: ')
three_encrypted = int(r.recvline().decode()[0:-1])

encrypt_x_3 = three_encrypted ** 2

r.recvuntil('> ')
r.sendline(str(1).encode())

r.recvuntil('Plaintext > ')
r.sendline(str(27889).encode())

r.recvuntil('Encrypted: ')
encrypt_x3 = int(r.recvline().decode()[0:-1])

multiple_n2 = encrypt_x_3 - encrypt_x3

r.recvuntil('> ')
r.sendline(str(1).encode())

r.recvuntil('Plaintext > ')
r.sendline(str(101).encode())

r.recvuntil('Encrypted: ')
seven_encrypted = int(r.recvline().decode()[0:-1])

encrypt_x_7 = seven_encrypted ** 2

r.recvuntil('> ')
r.sendline(str(1).encode())

r.recvuntil('Plaintext > ')
r.sendline(str(10201).encode())

r.recvuntil('Encrypted: ')
encrypt_x7 = int(r.recvline().decode()[0:-1])

multiple_n3 = encrypt_x_7 - encrypt_x7

n_ = gcd(multiple_n2, multiple_n3)
n = int(gcd(n_, multiple_n1))

if int(flag_encrypted[-1]) % 2 != 0:
    print('Repeat.')
    exit(1)

get_context().precision = 65536
flag = mul(int(flag_encrypted), 0.5)

r.recvuntil('> ')
r.sendline(str(2).encode())

r.recvuntil('Ciphertext > ')
r.sendline(str(int(flag)).encode())

r.recvuntil('Decrypted: ')
flag_ = int(r.recvline().decode()[0:-1])

r.recvuntil('> ')
r.sendline(str(2).encode())

r.recvuntil('Ciphertext > ')
r.sendline(str(2).encode())

r.recvuntil('Decrypted: ')
p_decrypt = int(r.recvline().decode()[0:-1])

flags = p_decrypt * flag_

print('Flag:', long_to_bytes(pow(flags, 1, n)).decode())