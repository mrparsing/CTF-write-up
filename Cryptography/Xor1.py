"""Un modo molto semplice ed efficace per offuscare un messaggio è utilizzare lo xor con una chiave segreta.
La definizione riguarda variabili logiche (True/False), ma il concetto può essere velocemente esteso in maniera naturale a stringhe di bit: lo xor tra due sequenze binarie diventa dunque lo xor bit a bit.
Per esempio: 00110000 xor 01100001 → 01010001.
In Python, lo xor tra due numeri interi è dato dall'operatore ^. Per fare lo xor tra due stringhe, è necessario convertirle dapprima in bytes, per poi effettuare l'operazione byte per byte.
Una funzione in Python per fare lo xor tra due oggetti bytes può essere:
def xor(a, b):
    return bytes([x^y for x,y in zip(a,b)])
Per ottenere la flag di questa challenge, effettua lo xor di questi due messaggi: fai attenzione a decodificare correttamente da esadecimale a bytes!
m1 = 158bbd7ca876c60530ee0e0bb2de20ef8af95bc60bdf m2 = 73e7dc1bd30ef6576f883e79edaa48dcd58e6aa82aa2
"""

hex1 = 0x158bbd7ca876c60530ee0e0bb2de20ef8af95bc60bdf
hex2 = 0x73e7dc1bd30ef6576f883e79edaa48dcd58e6aa82aa2

num_bytes = (hex1.bit_length() + 7) // 8

byte1 = hex1.to_bytes(num_bytes, 'big')
byte2 = hex2.to_bytes(num_bytes, 'big')


def xor(a, b):
    return bytes([x^y for x, y in zip(a,b)])
    
print(xor(byte1, byte2))