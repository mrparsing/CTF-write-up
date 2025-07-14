from sys import exit

from Crypto.Util.number import long_to_bytes
from gmpy2 import *
from pwn import *

# e = 65537
# c = flag_encrypted

# c = m^e % n -> encrypt
# m = c^d % n -> decrypt
# n = ? --> 
HOST = "oracle.challs.cyberchallenge.it"
PORT = 9043
r = remote(HOST, PORT)

r.recvuntil('flag: ')
flag_encrypted = r.recvline().decode()[0:-1]

r.recvuntil('> ')
r.sendline(str(2).encode())

r.recvuntil('Ciphertext > ')
r.sendline(str(2).encode())

r.recvuntil('Decrypted: ')
p_decrypted = int(r.recvline().decode()[0:-1])

encrypt_x_2 = p_decrypted ** 2

r.recvuntil('> ')
r.sendline(str(2).encode())

r.recvuntil('Ciphertext > ')
r.sendline(str(4).encode())

r.recvuntil('Decrypted: ')
encrypt_x2 = int(r.recvline().decode()[0:-1])

multiple_n1 = encrypt_x_2 - encrypt_x2

r.recvuntil('> ')
r.sendline(str(2).encode())

r.recvuntil('Ciphertext > ')
r.sendline(str(167).encode())

r.recvuntil('Decrypted: ')
three_encrypted = int(r.recvline().decode()[0:-1])

encrypt_x_3 = three_encrypted ** 2

r.recvuntil('> ')
r.sendline(str(2).encode())

r.recvuntil('Ciphertext > ')
r.sendline(str(27889).encode())

r.recvuntil('Decrypted: ')
encrypt_x3 = int(r.recvline().decode()[0:-1])

multiple_n2 = encrypt_x_3 - encrypt_x3

n = int(gcd(multiple_n1, multiple_n2))

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

flags = p_decrypted * flag_

print('Flag:', long_to_bytes(pow(flags, 1, n)).decode())