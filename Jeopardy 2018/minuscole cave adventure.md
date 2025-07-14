```c
import struct

def forge_save(room: int, o1: int, o2: int, flag_index: int) -> bytes:
    signature = 0xcc18cc18
    ai0 = o1 + 1
    ai1 = o2 + 1
    ai2 = flag_index + 1
    checksum = room + ai0 * 0x7be + ai1 * 0x7be + ai2 * 0x7be
    return struct.pack("<6I", signature, room, ai0, ai1, ai2, checksum)

payload = forge_save(room=4, o1=0, o2=0, flag_index=4)

with open("cheat.save", "wb") as f:
    f.write(payload)
```

La funzione load() carica dati da un file binario e li copia in memoria.

Il contenuto letto include:

1. Firma fissa 0xcc18cc18
2. Posizione del giocatore (stanza in cui si trova: da 0 a 4)
3. Dati degli oggetti
4. Checksum

Il contenuto viene copiato direttamente nella struttura dati usata dal gioco.

È sufficiente creare un file .save con i giusti valori e checksum coerente.

Struttura del file:

| **Offset** | **Valore** | **Descrizione** |
| --- | --- | --- |
| 0x00 | 0xCC18CC18 | Firma del file |
| 0x04 | room_index | Stanza in cui iniziare |
| 0x08 | ai0 = obj1 + 1 | Oggetto 1 |
| 0x0C | ai1 = obj2 + 1 | Oggetto 2 |
| 0x10 | ai2 = flag_index + 1 | Oggetto 3 |
| 0x14 | checksum |  |

A questo punto basta caricare il file generato nel gioco e attraverso i comandi del gioco recuperare la flag.