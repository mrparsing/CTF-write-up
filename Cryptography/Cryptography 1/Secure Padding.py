"""Passwords should be at least 32 characters long! Give us your password, we'll think about it!
This is a remote challenge, you can connect to the service with: nc padding.challs.cyberchallenge.it 9030
"""

"""Il server cifra in AES-ECB una stringa composta da: `password + FLAG + padding`

In ECB, blocchi di plaintext identici producono ciphertext identici.

L’idea è

1. Isolare un carattere della FLAG in un blocco AES composto da 16 byte.
2. Brute-forzare quel carattere testando tutti i possibili valori stampabili.
3. Confrontare i ciphertext per trovare corrispondenze.

Ad esempio, per trovare il primo carattere della flag, se inviamo una password di 15 caratteri il pt diventa `AAAAAAAAAAAAAAA + flag[0] + flag[1] + … + padding`. Quindi il primo blocco AES diventa `AAAAAAAAAAAAAAA + flag[0]`. Eseguiamo il bruteforce testando tutti i caratteri stampabili e confrontiamo i ct."""
from pwn import *
import string

def main():
    flag = []
    conn = remote('padding.challs.cyberchallenge.it', 9030)
    
    conn.recvuntil('encrypt:')
    
    n = 0 # posizione della flag
    while True:
        L = (15 - n) % 16 # numeri di caratteri A da inviare (la mia password)
        block_number = n // 16
        
        password1 = 'A' * L
        conn.sendline(password1)
        response = conn.recvuntil('encrypt:')
        
        for line in response.split(b'\n'):
            if b'Here is you secure encrypted password:' in line:
                encrypted_part = line.split(b': ')[1].strip()
                encrypted = encrypted_part.decode()
                break
        
        ciphertext = bytes.fromhex(encrypted)
	
	# estraggo il blocco da confrontare
        target_block = ciphertext[block_number*16 : (block_number+1)*16]
        
	# bruteforce
        for c in string.printable:
            known_part = ''.join(flag)
            
            brute_password = 'A' * L + known_part + c
            
            conn.sendline(brute_password)
            brute_response = conn.recvuntil('encrypt:')
            
            brute_encrypted = None
            for line in brute_response.split(b'\n'):
                if b'Here is you secure encrypted password:' in line:
                    brute_part = line.split(b': ')[1].strip()
                    brute_encrypted = brute_part.decode()
                    break

            
            ciphertext_brute = bytes.fromhex(brute_encrypted)
            
            brute_block = ciphertext_brute[block_number*16 : (block_number + 1)*16]
            
            if brute_block == target_block:
                flag.append(c)
                print(f"Found character {n}: {c}, current flag: {''.join(flag)}")
                break       
        
        n += 1 # passo al prossimo carattere della flag
        
        if flag and flag[-1] == '}':
            print(f"Flag found: {''.join(flag)}")
            break
    
    conn.close()

if __name__ == '__main__':
    main()