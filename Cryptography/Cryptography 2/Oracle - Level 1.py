from Crypto.Util.number import *
from gmpy2 import c_div
from pwn import *

# decrypt(encrypt(FLAG) * encrypt(2)) == 2*FLAG

r = remote('oracle.challs.cyberchallenge.it', 9041)

r.recvuntil('flag: ')
flag_encrypted = r.recvline().decode()[0:-1]

r.recvuntil('> ')
r.sendline(str('1').encode())

r.recvuntil('Plaintext > ')
r.sendline(str('2').encode())

r.recvuntil('Encrypted: ')
two_encrypted = r.recvline().decode()[0:-1]

flag_two_encrypt = int(flag_encrypted) * int(two_encrypted)

r.recvuntil('> ')
r.sendline(str('2').encode())

r.recvuntil('Ciphertext > ')
r.sendline(str(flag_two_encrypt).encode())

r.recvuntil('Decrypted: ')
flag_two_decrypt = r.recvline().decode()[0:-1]

encrypted_flag = c_div(int(flag_two_decrypt), 2)
print('Flag:', long_to_bytes(encrypted_flag).decode())