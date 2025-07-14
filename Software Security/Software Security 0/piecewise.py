"""
This service will give you the flag, piece by piece, if you answer correctly. Scripting the interaction is strongly suggested ;)
nc piecewise.challs.cyberchallenge.it 9110
"""


from pwn import *
import re

HOST = "piecewise.challs.cyberchallenge.it"
PORT = 9110

p = remote(HOST, PORT)

pattern = r"number\s+(\d+)\s+as\s+a\s+(\d+)-bit\s+(\w+)-endian"

while True:
    text = p.recvline().decode()

    print(text)

    if "empty" in text:
        p.sendline()
    else:
        match = re.search(pattern, text)
        if not match:
            continue
        number = int(match.group(1))     # 1464946940
        bits = int(match.group(2))       # 32
        endian = match.group(3)          # big
        print(f"[DEBUG] Number: {number}, Bits: {bits}, Endianness: {endian}")
        num_encoded = 0
        if bits == 32:
            if endian == "big":
                num_encoded = p32(number, endian='big')
                print(f"[DEBUG] 32-big", num_encoded)
            else:
                num_encoded = p32(number, endian='little')
                print(f"[DEBUG] 32-little", num_encoded)
        else:
            if endian == "big":
                num_encoded = p64(number, endian='big')
                print(f"[DEBUG] 64-big", num_encoded)
            else:
                num_encoded = p64(number, endian='little')
                print(f"[DEBUG] 64-little", num_encoded)
        p.send(num_encoded)
