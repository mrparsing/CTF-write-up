La funzione FUN_00101169 verifica che la somma cumulativa dei caratteri della flag corrisponda agli elementi di un array (param_2) nella sezione .data.

Quando un elemento in param_2 è negativo stampa la flag.

Se la somma corrente (param_3) corrisponde all’elemento corrente di param_2, si passa al carattere successivo.

Perché param_2 contiene la somma cumulativa dei caratteri della flag?

La funzione confronta param_3 (la somma cumulativa dei caratteri della flag) con i valori di param_2.

Se param_3 corrisponde a param_2, significa che la somma cumulativa fino a quel punto è corretta, e il programma passa al prossimo carattere e al prossimo valore di param_2.

Questo comportamento implica che param_2 contiene i valori attesi delle somme cumulative dei caratteri della flag.

Questo significa che per calcolare i caratteri della flag devo calcolare

carattere[i] = param_2[i] - param_2[i-1]

```jsx
param_2 = [84, 195, 290, 395, 479, 580, 694, 746, 862, 963, 1058, 1163, 1216, 1311, 1415, 1500, 1609, 1706, 1784, 1879, 1995, 2043, 2138, 2252, 2303, 2370, 2487, 2569, 2684, 2785, 2880, 2980, 3029, 3147, 3252, 3362, 3463, -1]

flag = ""
for i in range(len(param_2) - 1):
    if param_2[i] == -1:
        break
    char = param_2[i] - (param_2[i-1] if i > 0 else 0)
    flag += chr(char)

print("Flag:", flag)
```