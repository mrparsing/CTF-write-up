![Screenshot 2025-03-13 alle 15.49.53.png](attachment:8f60a070-fdba-4fb9-862b-770e2f9aaadf:Screenshot_2025-03-13_alle_15.49.53.png)

`pagina_allocata = mmap(0, 4096, 7, 34, 0xffffffff, 0);`

- **`mmap`**: Questa funzione alloca una regione di memoria di 4096 byte (4 KB) con permessi di lettura, scrittura e esecuzione (`7` indica `PROT_READ | PROT_WRITE | PROT_EXEC`). La memoria è mappata in modo anonimo (`MAP_ANONYMOUS`), il che significa che non è associata a nessun file.
- **`pagina_allocata`**: Questo è il puntatore alla memoria allocata.

---

La funzione `FUN_001008d0` è responsabile dell'inizializzazione di un array globale (`ARRAY`) e della sua popolazione con puntatori a strutture di dati allocate dinamicamente.

`ARRAY = malloc(0xc0);`

- **`ARRAY`**: Questo è un puntatore globale a un array di 192 byte (`0xc0` in esadecimale).
- **`malloc(0xc0)`**: Alloca 192 byte di memoria e assegna l'indirizzo di questa memoria a `ARRAY`.

```jsx
for (i = 0; i < 23; i = i + 1) {
    punt_16_byte = (long *)malloc(16);
    *punt_16_byte = pagina_allocata + i * 17;
    *(char *)(punt_16_byte + 1) = (char)i * '\x11';
    *(char *)((long)punt_16_byte + 9) = (char)i;
    *(long **)((long)i * 8 + ARRAY) = punt_16_byte;
}
```

---

```jsx
if (param_1 != 2) {
    exit(1);
}
```

**`param_1`**: Questo è il numero di argomenti passati al programma. Se non è esattamente 2 (cioè il nome del programma e un argomento), il programma termina con un codice di errore.

```jsx
lVar3 = strlen(*(undefined8 *)(param_2 + 8));
if (lVar3 != 0x17) {
    exit(1);
}
```

La lunghezza della stringa deve essere esattamente 23 caratteri (0x17 in esadecimale). Se non lo è, il programma termina.

---

![Screenshot 2025-03-13 alle 16.00.54.png](attachment:a8cdea10-65fc-47b2-b4fa-5271619f6706:Screenshot_2025-03-13_alle_16.00.54.png)

Inizializza il generatore di numeri casuali (`rand`) con il seed ottenuto dal tempo corrente.

```jsx
random_1 = rand();
random_1 = random_1 % 22 + 1;
random_2 = rand();
random_2 = random_2 % 22 + 1;
```

**`random_1 % 22 + 1`**: Limita il numero casuale a un valore compreso tra 1 e 22 (inclusi). Questo perché l'array `ARRAY` ha 23 elementi (indici da 0 a 22), ma l'ultimo elemento è riservato come terminatore.

```jsx
uVar1 = *(undefined8 *)(ARRAY + (long)random_1 * 8);
*(undefined8 *)((long)random_1 * 8 + ARRAY) = *(undefined8 *)(ARRAY + (long)random_2 * 8);
*(undefined8 *)((long)random_2 * 8 + ARRAY) = uVar1;
```

**`uVar1`**: Memorizza temporaneamente il valore dell'elemento all'indice `random_1`. 
**Scambio**: L'elemento all'indice `random_1` viene sostituito con l'elemento all'indice `random_2`, e viceversa.

La funzione `randomize` mescola gli elementi dell'array globale `ARRAY` in modo casuale. Ogni elemento dell'array (tranne l'ultimo, che è riservato come terminatore) viene scambiato con un altro elemento scelto casualmente. Questo processo viene ripetuto 256 volte per garantire che l'array sia sufficientemente mescolato.

Nel codice principale che hai fornito in precedenza, `ARRAY` viene utilizzato per memorizzare puntatori a funzioni e dati. La funzione `randomize` mescola questi puntatori in modo casuale, il che significa che l'ordine in cui le funzioni vengono chiamate nel ciclo principale sarà diverso ogni volta che il programma viene eseguito.

---

- Il ciclo esegue 23 iterazioni (una per ogni carattere della stringa di input). Per ogni iterazione:
    - Recupera un puntatore a una funzione (`ppcVar1`) e un puntatore a dati (`puVar2`) dall'array.
    - Se `puVar2` è nullo, chiama la funzione puntata da `ppcVar1` con tre argomenti:
        - Un offset nella stringa di input (`(long *)(param_2 + 8) + (ulong)*(byte *)((long)ppcVar1 + 9)`).
        - La memoria allocata (`pagina_allocata`).
        - Un valore nullo (`0`).
    - Se `puVar2` non è nullo, chiama la funzione con tre argomenti:
        - Lo stesso offset nella stringa di input.
        - Il valore puntato da `puVar2`.
        - Un valore derivato da `puVar2` (`(int)*(char *)(puVar2 + 1)`).

```jsx
def estrai_flag():
    with open("morph", "rb") as file:
        dati = file.read()
    
    sequenza_iniziale = b'\x56\x52\x8a\x07\x3c\x43'
    posizione_iniziale = dati.find(sequenza_iniziale)

    if posizione_iniziale == -1:
        print("Sequenza iniziale non trovata.")
        return

    flag = ""
    for indice in range(23):
        offset = indice * 0x11
        carattere = dati[posizione_iniziale + offset + 5] ^ (offset & 0xff)
        flag += chr(carattere)

    print(flag)

if __name__ == "__main__":
    estrai_flag()
```