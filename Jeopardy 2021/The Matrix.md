Analizzando il file pcapng notiamo che c’è uno scambio di pacchetti con il protocollo Modbus. Questo è un protocollo di comunicazione molto usato per il controllo e il monitoraggio di dispositivi industriali. Il protocollo ha diverse funzioni, nel nostro caso l’unica funzione usata è Write Single Coil, utilizzata per scrivere un singolo valore booliano: 0000 spegne, ff00 accende.

Analizzando gli altri file della challenge notiamo che abbiamo un dockerfile, avviando con docker, installando le librerie necessarie e avviando lo script matrix.py notiamo che apre una pagina con un display. Immenttendo un testo questo scorre lettera per lettera nel display.

Da qui possiamo capire che, dato che i pacchetti scambiati utilizzano una funzione per scrivere un valore booleano (spegni o accendi) questi non sono altro che dei comandi per accedere o spegnere i pixel del display.

Quindi come prima cosa ho estratto tutti i pacchetti che utilizzano il protocollo Modbus.

```jsx
import re

def extract_modbus_data(input_file, output_file):
    with open(input_file, 'r') as infile:
        data = infile.read()

    reference_number_pattern = r"Reference Number:\s*(\d+)"
    data_pattern = r"Data:\s*([0-9A-Fa-f]+)"
    
    reference_numbers = re.findall(reference_number_pattern, data)
    data_values = re.findall(data_pattern, data)

    with open(output_file, 'w') as outfile:
        for ref, val in zip(reference_numbers, data_values):
            outfile.write(f"{ref} {val}\n")
    
    return reference_numbers, data_values

input_file = 'file.txt'
output_file = 'output.txt'

reference_numbers, data_values = extract_modbus_data(input_file, output_file)

print("Reference Numbers:", reference_numbers)
print("Data Values:", data_values)
```

E li ho salvato in un file output.txt. Ho estratto anche il Refernce Number che rappresenta il pixel che dovrà accendersi nella matrice.

```jsx
1 0000
1 0000
2 0000
2 0000
3 0000
3 0000
4 0000
4 0000
5 0000
5 0000
6 0000
6 0000
7 0000
7 0000
8 0000
8 0000
9 0000
9 0000
10 0000
10 0000
11 ff00
11 ff00
12 0000
12 0000
13 0000
13 0000
14 0000
14 0000
15 0000
15 0000
16 0000
16 0000
17 ff00
17 ff00
18 0000
18 0000
19 0000
19 0000
20 0000
20 0000
21 0000
21 0000
22 0000
22 0000
23 ff00
23 ff00
24 0000
24 0000
25 0000
25 0000
26 0000
26 0000
27 0000
27 0000
28 0000
28 0000
29 ff00
29 ff00
30 0000
30 0000
31 0000
31 0000
32 0000
32 0000
33 0000
33 0000
34 0000
34 0000
35 ff00
35 ff00
36 0000
36 0000
37 0000
37 0000
38 0000
38 0000
39 0000
39 0000
40 0000
40 0000
41 0000
41 0000
42 0000
42 0000
43 0000
43 0000
44 0000
44 0000
45 0000
45 0000
46 0000
46 0000
47 0000
47 0000
```

```jsx
# Creazione della matrice 8x6, inizializzata con 0
matrix = [[_ for _ in range(6)] for _ in range(8)]

# apro il file
display = {}
j = 0
with open('output.txt', 'r') as file:
	for i, line in enumerate(file):
		# Se la riga è pari, la prendi
		if i % 2 == 0:
			word = line.split(" ")

			display.setdefault(f"Display {j}", "")
			display[f"Display {j}"] += " ".join(word)
			if int(word[0]) == 47:
				j += 1

def disegna_matrice(key, value):
	print(f"MATRICE {key}")

	val = value.split("\n")
	
	for i in val:
		if "ff00" in i:
			pos, v = i.split()

			row = int(pos) // 6
			col = int(pos) % 6
			
			matrix[row][col] = 1

	for row in matrix:
	    print(row)

for key, value in display.items():
	matrix = [[0 for _ in range(6)] for _ in range(8)]
	print("\n\n")
	disegna_matrice(key, value)
```

Attraverso questo script ho estratto il reference number dell’i-esimo valore e se il valore è ff00 cambio il valore i-esimo della matrice a 1, e stampo la matrice passo passo

```jsx
MATRICE Display 0
[0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0]

MATRICE Display 1
[0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 1]
[0, 0, 0, 0, 0, 1]
[0, 0, 0, 0, 0, 1]
[0, 0, 0, 0, 0, 1]
[0, 0, 0, 0, 0, 1]
[0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0]

MATRICE Display 2
[0, 0, 0, 0, 0, 1]
[0, 0, 0, 0, 1, 0]
[0, 0, 0, 0, 1, 0]
[0, 0, 0, 0, 1, 0]
[0, 0, 0, 0, 1, 0]
[0, 0, 0, 0, 1, 0]
[0, 0, 0, 0, 0, 1]
[0, 0, 0, 0, 0, 0]

...
```

Aiutandoci con il file font.js fornito dalla challenge possiamo decodificare la flag.