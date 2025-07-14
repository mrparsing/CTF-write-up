def rol(byte, index):
    """ruota a sinistra i bit di un byte di index posizioni"""
    for _ in range(index):
        byte = ((byte << 1) & 0xFF) | (byte >> 7) # 0xFF serve a limitare il valore entro 8 bit
    return byte


def main():
    try:
        with open("flag.txt.aes", "rb") as f:
            i = 0
            while True:
                byte = f.read(1)  # legge un byte alla volta
                if not byte:
                    break  # esce se non ci sono più dati
                
                i += 1
                decoded_byte = rol(byte[0], i)
                print(chr(decoded_byte), end=" ")
    except FileNotFoundError:
        print("File 'flag.txt.aes' non trovato.")


if __name__ == "__main__":
    main()