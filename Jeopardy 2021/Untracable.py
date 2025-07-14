def xor_decrypt(data, key):
    key_len = len(key)
    decrypted = bytearray() # crea un array di byte modificabile
    for i in range(len(data)):
        decrypted.append(data[i] ^ ord(key[i % key_len]))
    return decrypted

with open("img.bin", "rb") as f:
    encrypted_data = f.read()

key = "s3cret_k3y"

decrypted_data = xor_decrypt(encrypted_data, key)

with open("file_decifrato.bin", "wb") as f:
    f.write(decrypted_data)