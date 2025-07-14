numbers = [
    0xabb6bcbc, 0x9d9b9884,
    0xa0cf8ba0, 0xa0cc978b,
    0x9cca9a8d, 0xff829a8a
]

def bitwise_not_to_ascii(num):
    inverted = ~num & 0xFFFFFFFF
    byte_array = inverted.to_bytes(4, 'big')
    return ''.join(chr(b) for b in reversed(byte_array) if 32 <= b <= 126)

ascii_strings = [bitwise_not_to_ascii(num) for num in numbers]
print(ascii_strings)