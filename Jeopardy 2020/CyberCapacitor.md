Aprendo il file della challenge ho notato che c’erano degli oggetti HTTP. Quindi ho esportato tali oggetti. Come prima cosa ho analizzato i file html per capire come funziona il servizio. Poi ho notato che tra i file esportati c’è un file zip protetto da password.

Adesso non rimaneva che cercare la password. Analizzando i file esportati ho notato dei file txt POST che contengono delle stringhe in BASE64.

```jsx
bk1FZzNDZHRHREFaN0pOTjc4JCRiNDQ0NCQ3eDc=

OFhDTXBqNGJMZk1zakFCMDNRS01mSnUxTVlLTzRDcFZkc1NHcHNCVEI4ZW84dVpZaEpVZmFD
Vk5ENkRRVUh1S0pDM2tSMXVITjFuaWp0R09qYzlNRXpYYTY2S3VXanBGSmVQVGI2T0RYRnYx
YzRBWG1EbVRyQVc2bmhzR0RhTmcwWDRRREZ2djJHdkxwQmhFY2hiQzdBcHNROFl2czRnZUs3
S1A5SGlabFhON3VqM0tva1BSTXJtUnNpNGdtSnpEZmREZ1ppbjBJaVZiS1pCU2NNNUN1WERZ
Zk00TjM5Z1p6czJPVUxMTlhOYVdUZnVBREV0TVBZY0dtbzk2ME9YU1IwZno1b0J6em1lT2Yx
bTBZUVo2Y1V6MWJZalZFejlMU2lBRG9jRzNuOGxLNGpWZGxhbUFCMXVzUEU0TmpKakRCRHYx
VFhWRDBNRFBMdjVHQjhpNkM0ZHJRbkwwNlg5TWdMU21nUXZlODg3VGVGVFNPekhiQzZwbmFm
b05TZjZrMkJIWGhLNXVkUExaY3BwV1d1dDBLdkdrN29NdEJkU0VsRkNiQ21ybEg0TTFkS1pl
VG1tVlh0UVFpaWJQUzdYY3RJQm52b2hQQ25aTkg4ejBGb0MwMjczU2ZQVGdiREJja0paS1E2
b2ZTSmlMb0k1REtaODBVV0EyVkduWVZYNGxyR2s3NFFhZXRXRE1sdVdKb0FHejJRZk9LQVY1
bU9pS0daRFZiUkdvRDQ2WVVCU2IkJGNoMzNzM2M0azMkN3g3

ajZQVHV2NXBlNmNWVzVBWWVzZENGNTFkYWdqQiQkZjE0NiQ3eDc=

cjh2UkUxVnpRak5oSWokJDZuMyQ3eDc=

ejdHWUdmZk1XaFpzSDVpJCRISU5ERVgkN3g3

cDdMckE1YyQkaW1wcjNzc2l2M19wM2NzJDd4Nw==

UU5tUkdZUG1LbE1jJCRpbzckN3g3

Szd0QTF2JCRtaTYxeTRyZCQ3eDc=

N0k5THpiYXB6czJXcjdiSEpmWSQkbXljcjNkaTdjNHJkJDd4Nw==

ZlQ5bWNUelIkJG15cDRzc3dvcmQkN3g3

OGY1Y3pPUUF6TSQkcjQ0NDQ0aWQkN3g3

dDRsWlNKYm1kSnpVJCQ3b3Bjb25mJDd4Nw==

b4444 -> baaaa

ch33s3c4k3 -> cheesecake

f146 -> flag

6n3 -> gne

HINDEX

impr3ssiv3_p3cs impressive_pecs

io7 -> iot

mi61y4rd -> miglyard

mycr3di7c4rd -> mycreditcard

myp4ssword -> mypassword

r44444id -> raaaaid

7opconf -> topconf
```

Ho provato come password le stringhe che ho trovato ma niente.

Analizzando ancora i file esportati noto un’immagine che rappresenta 2020_2020 e mettendola nel file zip il file si è aperto.

All’interno c’è un file word che contiene delle MACRO.

Analizzando le funzioni noto che il codice prende tutti i file dell’utente li cifra con onetimepad (che fa uno XOR) e fa delle POST concatenando una chiave generata casualmente e il nome del file in base64 a cui applica un camuffamento molto semplice. Sostituendo alcune lettere con i numeri. Da qui ho capito che le stringhe trovato nei file txt POST sono stringhe che contengono una chiave e il nome del file. Tra questi ce n’è uno che si chiama fl46 → flag.

Non resta che cercare questo file. Analizzando il file pcap ho trovato il file zip il cui contenuto presumo sia proprio la flag cifrata.

A questo punto prendo il contenuto, prendo la chiave inviata nella richiesta post e tramite questo script recupero la flag

```jsx
import base64

cache_id_base64 = "ajZQVHV2NXBlNmNWVzVBWWVzZENGNTFkYWdqQiQkZjE0NiQ3eDc="
ciphertext_hex = "673c13173c224e17544050093a061e3b51100f1c2b4c6e020d530d3f0d0a"

decoded = base64.b64decode(cache_id_base64)

print(f"CACHE ID: {decoded}\n\n")

key = decoded[:30]

ciphertext = bytes.fromhex(ciphertext_hex)

print(f"CYPERTEXT: {ciphertext}\n\n")

plaintext = bytes([c ^ k for c, k in zip(ciphertext, key)])

print("Flag:")
print(plaintext.decode(errors="replace"))
```