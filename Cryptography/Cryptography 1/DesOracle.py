"""This service is so secure that you can decide its encryption parameters.
This is a remote service, you can access with:
nc desoracle.challs.cyberchallenge.it 9035
"""

"""
Per risolvere questa challenge ho sfruttato le chiavi deboli del DES che generano la stessa sottochiave per tutti i round. Usando una chiave debole, cifrare due volte di fila annulla l’operazione: DES(DES(pt)) = pt
"""

from pwn import *
import binascii

context.log_level = 'debug'
r = remote('desoracle.challs.cyberchallenge.it', 9035)

weak_keys = [
    '0101010101010101',
    'FEFEFEFEFEFEFEFE',
    'E0E0E0E0F1F1F1F1',
    '1F1F1F1F0E0E0E0E'
]

for key in weak_keys:
    try:
        # cifratura della flag
        r.sendlineafter(b'> ', b'2')
        r.sendlineafter(b'What key do you want to use (in hex)? ', key.encode())
        ct = r.recvline().strip().decode()
        
        # invio il ct ottenuto per cifrarlo con la stessa chiave
        r.sendlineafter(b'> ', b'1')
        r.sendlineafter(b'What do you want to encrypt (in hex)? ', ct.encode())
        r.sendlineafter(b'With what key (in hex)? ', key.encode())
       
    except:
        continue

r.close()
