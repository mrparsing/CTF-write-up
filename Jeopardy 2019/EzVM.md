Il manuale fornito descrive una micro-VM a byte singolo con:

- **10 istruzioni**, tutte a controllo di flusso *fisso* salvo chk, che termina il programma con exit-code 1 se il confronto fallisce.
- **Memoria di 256 byte**, inizializzata a 0.
- **Nessun registro di uso generale**: ogni operazione legge e scrive direttamente dalla RAM.

---

```
xxd -g1 -c8 check_login_key | head -n 15
```

I primi byte rivelano subito la struttura di alto livello:

| **offset** | **opcode** | **significato** |
| --- | --- | --- |
| 0x00 | 01 18 00 | in 0x18 0x00  → legge **24 byte** di input in RAM [0×00-0×17] |
| 0x03 | 02 2d ff | sto 0x2D 0xFF → RAM 0xFF ← '-' (0x2d) |
| 0x06 | 09 04 ff | chk 0x04 0xFF → pretende '-' a RAM 0x04 |
| … |  | altri tre chk analoghi su RAM 0x09, 0x0E, 0x13 |

I caratteri d’ingresso hanno lunghezza 24 e *devono* contenere i trattini - alle posizioni **4, 9, 14, 19** (contando da 0).

---

Poco più avanti:

```
02 f0 ff        ; sto 0xF0 → 0xFF  (maschera 11110000)
06 00 ff 80     ; and RAM[0],0xFF → RAM[0x80]
...
02 40 ff        ; sto 0x40 → 0xFF
09 80 ff        ; chk RAM[0x80],0xFF
```

Per ogni carattere:

1. viene azzerato il nibble basso (AND 0xF0);
2. il valore risultante dev’essere 0x40.

**Tutti** i caratteri (=16 dei 24, escludendo i 4 trattini) devono perciò avere *nibble alto fisso a 0x4*.

Sono quindi valori ASCII da 0x40 a 0x4F

Il nostro problema si riduce a trovare i **16 nibbles bassi** n.

---

Il programma entra in un loop ripetuto **5 volte**; ogni iterazione lavora su un blocco di 4 caratteri (gli indici 0-3, 5-8, 10-13, 15-18, 20-23).

Pseudo-codice di ciascuna iterazione:

```
acc = 0
per i 4 char nel blocco:
    nib = char AND 0x0F          # estrai nibble basso
    t   = 0x0F - nib             # T(n) = 15 - nib
    acc = acc + t
acc = acc - C            # C è una costante diversa per blocco
acc = acc XOR K          # K costante per blocco
chk acc, 0xD0            # deve essere 0
```

Il chk finale impone

```
(acc - C) XOR K = 0  →  acc - C = K  →  acc = (K + C)  (mod 256)
```

### **4.1 Costanti per blocco**

Dalle istruzioni sto nel binario estraiamo (K, C):

| **Bloc-co** | **indici RAM** | K **(XOR)** | C **(SUB)** |
| --- | --- | --- | --- |
| 1 | 0–3 | 0x27 = 39 | 0xF3 = 243 |
| 2 | 5–8 | 0x37 = 55 | 0xCD = 205 |
| 3 | 10–13 | 0x14 = 20 | 0x1A = 26 |
| 4 | 15–18 | 0xAF = 175 | 0x66 = 102 |
| 5 | 20–23 | 0xBA = 186 | 0x4D =  77 |

Calcoliamo **target = (K + C) mod 256** e la conseguente somma desiderata dei nibbles n_i (ricordando che Σ n_i = 60 − target):

| **Bloc-co** | K + C | **target** | **Σ nibbles** |
| --- | --- | --- | --- |
| 1 | 39 + 243 = 282 → 26 | 26 | **34** |
| 2 | 55 + 205 = 260 → 4 | 4 | **56** |
| 3 | 20 + 26  = 46 | 46 | **14** |
| 4 | 175+ 102 = 277 → 21 | 21 | **39** |
| 5 | 186+ 77  = 263 → 7 | 7 | **53** |

Ora il puzzle è puramente combinatorio: per ogni blocco troviamo **4 numeri 0-15** la cui somma vale il rispettivo valore a destra.

---

```
# solve_ezvm.py
from itertools import product

sums = [34, 56, 14, 39, 53]

blocks = []
for need in sums:
    for quad in product(range(16), repeat=4):
        if sum(quad) == need:
            blocks.append(quad)
            break                # basta il primo match
# ricomponi la chiave
nibbles = [*blocks[0], *blocks[1], *blocks[2], *blocks[3], *blocks[4]]
chars   = [0x40 | n for n in nibbles]           # rimetti nibble alto = 4
key     = ''.join(map(chr, chars))
key_fmt = key[:4] + '-' + key[4:8] + '-' + key[8:12] + '-' + key[12:16] + '-' + key[16:]
print(key_fmt)
```

Output:
```
@DOO-KOOO-@@@N-@IOO-HOOO
```