```c
from pwn import *

HOST = "maze.challs.cyberchallenge.it"
PORT = 9404

p = remote(HOST, PORT)

path = b'ddd' + b'r'*16 + b'dd'

cheat = b'\x1b:q!\n'

p.send(path + cheat)
p.interactive()
```

Il gioco è un labirinto.

Analizzando il codice c’è una riga `system("cat flag.txt")` che viene eseguita sotto delle specifiche condizioni.

1. Il personaggio (&) deve trovare nella posizione (17, 6)
2. Lo stato deve avere valore 4
    1. Per fare ciò inviamo la sequenza di comandi:
        1. \x1b (che corrisponde a ESC)
        2. : (che imposta lo stato a 2)
        3. q (che imposta lo stato a 3)
        4. ! (che imposta lo stato a 4)
        5. \n (per stampare la flag)

| **Comando** | **Condizione** | **Stato** |
| --- | --- | --- |
| d - u - l - r |  | stato = 0 |
| q | stato == 2 | stato = 3 |
| : | stato == 1 | stato = 2 |
| ! | stato == 3 | stato = 4 |
| \x1b | pos == (17, 6) && stato == 0 | stato = 1 |