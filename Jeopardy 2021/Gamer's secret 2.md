Aprendo il file pcapng non sembrano esserci indizi particolari. L’unico indizio che abbiamo è un pacchetto che ci dice che il traffico scambiato è quello di un server minecraft utilizzando il protocollo 754 e la versione 1.16.5, nient’altro. Tutti gli altri pacchetti sembrano cifrati.

Analizzando il payload dei pacchetti noto che alcuni contengono la firma 78 9C che rappresenta l’header di un file compresso con zlib. A questo punto ho iniziato a decodificare i pacchetti

```jsx
import zlib
import re

hex_data = """
140b789ce36660e0d9ffff6b81fb072900156f048c8f01b501789ce36460e0d9ffff6b813b271703030703ab737e4e7e11036b524e6272363303630503038311503824b5a2c48481bb5aa904c850b25252aa054a560225dda192c6e89255ffffff0f874a1a3108c1254b8b53158af24b946a391898325318f87233f352938b12d34aac8a33d3f3a01a0c19a4e11a0202c2dcab4d120b73e22b0d338dd36a956a19006f8631b3
""".replace("\n", "").strip()

# Trova tutti i blocchi che iniziano con '789c'
matches = [m.start() for m in re.finditer('789c', hex_data)]

# Estrai blocchi tra una firma e la successiva
blocks = []
for i in range(len(matches)):
    start = matches[i]
    end = matches[i + 1] if i + 1 < len(matches) else len(hex_data)
    blocks.append(hex_data[start:end])

# Decomprimere ogni blocco e stampare contenuto leggibile
for i, block in enumerate(blocks):
    print(f"\n🔹 Blocco {i + 1}:")
    try:
        decompressed = zlib.decompress(bytes.fromhex(block))
        # Trova tutte le sottostringhe leggibili (es. JSON o testo UTF-8)
        readable_parts = re.findall(rb'[\x20-\x7E]{4,}', decompressed)
        if readable_parts:
            for part in readable_parts:
                print("📄", part.decode('utf-8'))
        else:
            print("⚠️ Nessuna stringa leggibile trovata.")
    except zlib.error as e:
        print(f"Errore nella decompressione: {e}")
```

E ho cominciato a trovare alcune cose interessanti. Ad esempio

```jsx
·{"translate":"chat.type.text","with":[{"insertion":"John Wick","clickEvent":{"action":"suggest_command","value":"/tell John Wick "},"hoverEvent":{"action":"show_entity","contents":{"type":"minecraft:player","id":"aebe6ce9-8554-3c57-b365-b9abd0733742","name":{"text":"John Wick"}}},"text":"John Wick"},"Hi win"]}®¾léT<W³e¹«Ðs7B
```

```jsx
Á{"translate":"chat.type.text","with":[{"insertion":"John Wick","clickEvent":{"action":"suggest_command","value":"/tell John Wick "},"hoverEvent":{"action":"show_entity","contents":{"type":"minecraft:player","id":"aebe6ce9-8554-3c57-b365-b9abd0733742","name":{"text":"John Wick"}}},"text":"John Wick"},"find the message"]}®¾léT<W³e¹«Ðs7B
```

In questo John Wick diceva di “trovare il messaggio”…

Continuando ad analizzare i pacchetti ho trovato questo pacchetto molto interessante

```jsx
📄 Color
📄 black
📄 Text4
📄 {"text":""}
📄 Text3
📄 {"text":""}
📄 Text2
📄 {"text":""}
📄 minecraft:sign
📄 Text1
📄 {"text":""}
```

Il giocatore stava cercando di scrivere qualcosa sui cartelli di Minecraft

```jsx
📄 {"translate":"chat.type.text","with":[{"insertion":"Winston","clickEvent":{"action":"suggest_command","value":"/tell Winston "},"hoverEvent":{"action":"show_entity","contents":{"type":"minecraft:player","id":"ed5ba33c-39c0-3939-a0b3-01d226a17f7c","name":{"text":"Winston"}}},"text":"Winston"},"Okay, I will find it, I will search every sign!"]}
```

In questo pacchetto in particolare il giocatore Winston dice che lo troverà, lo cercherà in ogni cartello. E infatti qualche blocco più avanti…

```jsx
📄 Color
📄 black
📄 Text4
📄 {"text":""}
📄 Text3
📄 {"text":""}
📄 Text2
📄 {"text":"use rot"}
📄 minecraft:sign
📄 Text1
📄 {"text":"PPVG{4aql_y1i3f}"}
```

Ecco la flag cifrata con Cesare con chiave 13 → ***CCIT{4ndy_l1v3s}***