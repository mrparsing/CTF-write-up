def xor(a, b):
    return bytes([x ^ b for x in a])  # XOR tra ogni byte di a e il singolo byte b

ciphertext = bytes.fromhex("104e137f425954137f74107f525511457f5468134d7f146c4c")  # Converti l'esadecimale in bytes

# Prova tutte le chiavi da 0x00 a 0xFF
for key in range(256):
    plaintext = xor(ciphertext, key)
    try:
        decoded = plaintext.decode("utf-8")  # Prova a decodificare il testo
        if decoded.isprintable():  # Controlla se è un testo leggibile
            print(f"Chiave: {hex(key)} -> {decoded}")
    except UnicodeDecodeError:
        pass  # Salta le chiavi che generano errori di decodifica