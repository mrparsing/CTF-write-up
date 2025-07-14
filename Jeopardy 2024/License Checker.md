My license expired and I can't afford to renew it! Please buy me an activation code!

`nc licensechecker.challs.cyberchallenge.it 38204`

The license server port for this challenge is:

`38205`

---

Analisi del binario

```c
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
```

Analisi funzione main

Se esistono entrambe le variabili d’ambiente REMOTE e PORT entra nel blocco if e stampa il messaggio iniziale.

Usa *getline* per leggere l’input. *getline* alloca un buffer se local_50 è NULL e lo ridimensiona automaticamente.

Successivamente cerchiamo il primo ritorno a capo nell’input e lo sostituiamo con \0.

Calcola la **lunghezza della stringa** inserita. Se la lunghezza **non è un multiplo di 3**, stampa *“Invalid license…”* e termina il programma.

Poi c’è un while loop che scorre la stringa di input a passi di 3.

Successivamente mapp una pagina RW a indirizzo fisso 0x60000.

Poi, alloca una pagina **RWX** (!!!) — quindi leggibile, scrivibile **e eseguibile**. Senza indirizzo fisso (kernel sceglie). La salva in local_30, che è castato come puntatore a code * → ovvero a funzione eseguibile.

**connect_to_license_check_server**
fa una **connessione TCP a un server remoto**, il cui indirizzo e porta sono presi da variabili d’ambiente (REMOTE e PORT)

1. **Prende REMOTE e PORT dalle variabili d’ambiente.**
2. Risolve REMOTE in un indirizzo IP.
3. Fa una socket TCP verso REMOTE:PORT.
4. Ritorna il file descriptor della connessione (iVar2).

In pratica l’intero programma è un **interprete custom** per una pseudo-licenza, dove:

- Ogni blocco di **3 byte** dell’input (la “license”) è interpretato come un’**istruzione custom**.
- Ogni istruzione è **invocata dinamicamente da codice remoto**, ricevuto da un server di “license check”.
- C’è una **pagina fissa in memoria (fixed_page)** su cui probabilmente queste istruzioni operano.
- Alla fine, se la pagina contiene un certo **CRC32** (0xbadc0ff3), la licenza è accettata e viene stampata la FLAG.

Attraverso uno script python ho recuperato i dati che il server invia al client:

```c
from pwn import *

r = remote("licensechecker.challs.cyberchallenge.it", 38205)
for x in range(10):
    r.send(str(x).encode())
    size=r.recv(1)
    data=r.recv(int.from_bytes(size, 'little'))
    print(data)
```

```c
b'H\x8d\x04%\x00\x00\x06\x00H\x01\xf8H\x8b\x18H1\xf3H\x89\x18\xc3'
b'H\x8d\x04%\x00\x00\x06\x00H\x01\xf8H\x83\xc0\x19H\x8b\x18H1\xf3H\x89\x18\xc3'
b'H\x8d\x04%\x00\x00\x06\x00H\x01\xf8H\x83\xc02H\x8b\x18H1\xf3H\x89\x18\xc3'
b'H\x8d\x04%\x00\x00\x06\x00H\x01\xf8H\x83\xc0KH\x8b\x18H1\xf3H\x89\x18\xc3'
b'H\x8d\x04%\x00\x00\x06\x00H\x01\xf8\x8a\x18@0\xf3\x88\x18\xc3'
b'H\x8d\x04%\x00\x00\x06\x00H\x01\xf8H\x83\xc0\x19\x8a\x18@0\xf3\x88\x18\xc3'
b'H\x8d\x04%\x00\x00\x06\x00H\x01\xf8H\x83\xc02\x8a\x18@0\xf3\x88\x18\xc3'
b'H\x8d\x04%\x00\x00\x06\x00H\x01\xf8H\x83\xc0K\x8a\x18@0\xf3\x88\x18\xc3'
b'H\x8d\x04%\x00\x00\x06\x00H\xc7\xc3\x00\x00\x00\x00H\x83\xfbd}\x11H\x8b\x0c\x18H\xf7\xd1H\x89\x0c\x18H\x83\xc3\x08\xeb\xe9\xc3'
b'\xc3'
```

Che disassemblato diventa:

```c
;code 0
   0:   48 8d 04 25 00 00 06 00         lea    rax, ds:0x60000
   8:   48 01 f8                add    rax, rdi
   b:   48 8b 18                mov    rbx, QWORD PTR [rax]
   e:   48 31 f3                xor    rbx, rsi
  11:   48 89 18                mov    QWORD PTR [rax], rbx
  14:   c3                      ret

;code 1
   0:   48 8d 04 25 00 00 06 00         lea    rax, ds:0x60000
   8:   48 01 f8                add    rax, rdi
   b:   48 83 c0 19             add    rax, 0x19
   f:   48 8b 18                mov    rbx, QWORD PTR [rax]
  12:   48 31 f3                xor    rbx, rsi
  15:   48 89 18                mov    QWORD PTR [rax], rbx
  18:   c3                      ret

;code2
   0:   48 8d 04 25 00 00 06 00         lea    rax, ds:0x60000
   8:   48 01 f8                add    rax, rdi
   b:   48 83 c0 32             add    rax, 0x32
   f:   48 8b 18                mov    rbx, QWORD PTR [rax]
  12:   48 31 f3                xor    rbx, rsi
  15:   48 89 18                mov    QWORD PTR [rax], rbx
  18:   c3                      ret

;code3
   0:   48 8d 04 25 00 00 06 00         lea    rax, ds:0x60000
   8:   48 01 f8                add    rax, rdi
   b:   48 83 c0 4b             add    rax, 0x4b
   f:   48 8b 18                mov    rbx, QWORD PTR [rax]
  12:   48 31 f3                xor    rbx, rsi
  15:   48 89 18                mov    QWORD PTR [rax], rbx
  18:   c3                      ret

;code4
   0:   48 8d 04 25 00 00 06 00         lea    rax, ds:0x60000
   8:   48 01 f8                add    rax, rdi
   b:   8a 18                   mov    bl, BYTE PTR [rax]
   d:   40 30 f3                xor    bl, sil
  10:   88 18                   mov    BYTE PTR [rax], bl
  12:   c3                      ret

;code5
   0:   48 8d 04 25 00 00 06 00         lea    rax, ds:0x60000
   8:   48 01 f8                add    rax, rdi
   b:   48 83 c0 19             add    rax, 0x19
   f:   8a 18                   mov    bl, BYTE PTR [rax]
  11:   40 30 f3                xor    bl, sil
  14:   88 18                   mov    BYTE PTR [rax], bl
  16:   c3                      ret

;code6
   0:   48 8d 04 25 00 00 06 00         lea    rax, ds:0x60000
   8:   48 01 f8                add    rax, rdi
   b:   48 83 c0 32             add    rax, 0x32
   f:   8a 18                   mov    bl, BYTE PTR [rax]
  11:   40 30 f3                xor    bl, sil
  14:   88 18                   mov    BYTE PTR [rax], bl
  16:   c3                      ret

;code7
   0:   48 8d 04 25 00 00 06 00         lea    rax, ds:0x60000
   8:   48 01 f8                add    rax, rdi
   b:   48 83 c0 4b             add    rax, 0x4b
   f:   8a 18                   mov    bl, BYTE PTR [rax]
  11:   40 30 f3                xor    bl, sil
  14:   88 18                   mov    BYTE PTR [rax], bl
  16:   c3                      ret

;code8
   0:   48 8d 04 25 00 00 06 00         lea    rax, ds:0x60000
   8:   48 c7 c3 00 00 00 00    mov    rbx, 0x0
   f:   48 83 fb 64             cmp    rbx, 0x64
  13:   7d 11                   jge    0x26
  15:   48 8b 0c 18             mov    rcx, QWORD PTR [rax+rbx*1]
  19:   48 f7 d1                not    rcx
  1c:   48 89 0c 18             mov    QWORD PTR [rax+rbx*1], rcx
  20:   48 83 c3 08             add    rbx, 0x8
  24:   eb e9                   jmp    0xf
  26:   c3                      ret

;code9
   0:   c3                      ret
```

Vediamo cosa fa ciascun codice

- code0: opera su QWORD (8 byte): esegue *(u64*)(0x60000 + arg1) ^= arg2.
- code1: stesso di sopra, ma con offset +0x19 → lavora su un’altra zona della pagina.
- code2: come sopra, offset diverso: +0x32.
- code3: ancora XOR su QWORD, terza zona.
- code4: opera su BYTE singolo: *(u8*)(0x60000 + arg1) ^= arg2

Identici a code 4, ma su:

- code 5: offset + 0x19
- code 6: offset + 0x32
- code 7: offset + 0x4b
- code 8: NOT a ogni QWORD della pagina. Inverte i bit di ogni QWORD da 0x60000 a 0x60000 + 0x64. Serve per trasformare globalmente la pagina prima del CRC.