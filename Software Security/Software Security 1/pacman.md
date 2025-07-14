Il programma simula il gioco Pacman

```jsx
undefined8 main(int param_1,long param_2)

{
  long lVar1;
  char *pcVar2;
  undefined **i;
  
  if ((param_1 == 2) && (lVar1 = ptrace(PTRACE_TRACEME,0,1,0), lVar1 != -1)) {
    clock_gettime(0,(timespec *)&CURRENT_TIME);
    for (i = &PTR_s_pacmanpacman_00303060; *i != (char *)0; i = i + 1) {
      pcVar2 = strdup(*i);
      *i = pcVar2;
    }
    FUN_00100b7d(*(undefined8 *)(param_2 + 8));
    return 0;
  }
  return 0xffffffff;
}
```

La funzione main controlla se l’input è costituito da due parametri (il nome del programma e la sequenza di comandi), ptrace controlla se il programma è sotto un debugger.

Mette in CURRENT_TIME il tempo attuale.

Attraverso il ciclo for itera sulla stringa “pacmanpacman”. 

**`PTR_s_pacmanpacman_00303060`** è un array di stringhe terminato da `NULL` (es: `["pacmanpacman", NULL]`).

**`strdup(*i)`**: Crea una copia in heap di ogni stringa.

Viene chiamata la funzione FUN_00100b7d a cui passiamo l’input del programma (la sequenza di comandi)

```jsx
void FUN_00100b7d(char *param_1)

{
  char *pcVar1;
  char cVar2;
  char struct_time;
  ushort **ppuVar3;
  long in_FS_OFFSET;
  char *movimenti_utente;
  int local_144;
  int coord_x;
  int coord_y;
  timespec current_time;
  char local_128 [4];
  undefined local_124;
  undefined local_123;
  undefined local_122;
  long local_20;
  
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  memset(local_128,0,0x100);
  local_144 = 0;
  coord_x = 1;
  coord_y = 1;
  movimenti_utente = param_1;
  do {
    clock_gettime(0,&current_time);
    cVar2 = (&PTR_s_pacmanpacman_00303060)[coord_y][coord_x];
    struct_time = time_diff(CURRENT_TIME,DAT_003030e8,current_time.tv_sec,current_time.tv_nsec);
    struct_time = struct_time + cVar2;
    switch(struct_time) {
    case 'a':
    case 'c':
    case 'm':
    case 'n':
    case 'p':
switchD_00100c74_caseD_61:
      puts("Game over.");
                    /* WARNING: Subroutine does not return */
      exit(-1);
    default:
      ppuVar3 = __ctype_b_loc();
      if (((*ppuVar3)[struct_time] & 1024) != 0) {
        local_128[local_144] = struct_time;
        (&PTR_s_pacmanpacman_00303060)[coord_y][coord_x] = 97;
        ppuVar3 = __ctype_b_loc();
        local_144 = local_144 + 1;
        if (((*ppuVar3)[struct_time] & 256) != 0) {
          FUN_001009ca(local_128[0],local_128[2],local_124,local_123,local_122);
          if (local_20 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
            __stack_chk_fail();
          }
          return;
        }
      }
      if (*movimenti_utente == '\0') goto switchD_00100c74_caseD_61;
    }
    pcVar1 = movimenti_utente + 1;
    cVar2 = *movimenti_utente;
    movimenti_utente = pcVar1;
    if (cVar2 == 'j') {
      coord_y = coord_y + 1;
    }
    else if (cVar2 < 'k') {
      if (cVar2 == 'h') {
        coord_x = coord_x + -1;
      }
    }
    else if (cVar2 == 'k') {
      coord_y = coord_y + -1;
    }
    else if (cVar2 == 'l') {
      coord_x = coord_x + 1;
    }
  } while( true );
}
```

Questa funzione simula un labirinto interattivo. Qua viene creato il labirinto inserendo dei caratteri basati sul tempo e sulla posizione nel labirinto. Da notare che se la lettera calcolata è una lettera tra: ‘a’, ‘c’, ‘m’, ‘n’, ‘p’ il gioco termina. Queste lettere rappresentano gli ostacoli da non toccare. I comandi possibili sono quelli di vi, ovvero

- h → sinistra
- l → destra
- j → giù
- k → su

**Quindi l’obiettivo è trovare il labirinto e fornire la sequenza di comandi corretta.**

La funzione FUN_001009ca verifica se la sequenza fornita è quella corretta

```jsx
if ((local_44 == '{') && (local_1d == '}')) {
	puts(flag);
	uVar1 = 0;
}
```

La funzione FUN_001009ca chiama altre due funzioni FUN_00101150 **e** FUN_001011e0 che implementano un algoritmo crittografico simile a ChaCha20. Ma in realtà queste due funzioni non mi interessano.

Quello che mi interessa è trovare il labirinto e trovare la sequenza corretta di comandi da dare in input al programma, perché questi comandi verrano dati in input alle funzioni crittografiche che controlleranno se la sequenza è corretta, in caso affermativo verrà stampata la flag.

Per trovare il labirinto so che PTR_s_pacmanpacman_00303060 contiene la stringa “pacmanpacman” quindi attraverso il comando

```jsx
strings pacman | grep -A 20 "pacmanpacman"
```

Il comando cerca la stringa "pacmanpacman" all’interno del file binario e, se la trova, stampa quella riga più le 10 righe successive.

```jsx
pacmanpacman
cho4$aaagioc
caaarmmmmmmc
cz1pia66600c
cx4p2c00666c
cg8a2pacmanc
ci_cz737373c
co1pacpaconc
c4____pac0ac
czxgioN1234c
c0ZXGIOacpac
Game over.
expand 32-byte k
;*3$"
GCC: (Ubuntu 7.4.0-1ubuntu1~18.04.1) 7.4.0
.shstrtab
.interp
.note.ABI-tag
.note.gnu.build-id
.gnu.hash
.dynsym
```

Come possiamo vedere abbiamo trovato il labirinto. Ora bisogna trovare la sequenza corretta senza toccare le lettere proibite. Provando alcune sequenze ho trovato

![Screenshot 2025-04-03 alle 09.34.02.png](attachment:0a57ec44-ceb1-44aa-86b2-47fd0bc543a4:Screenshot_2025-04-03_alle_09.34.02.png)

che è la sequenza corretta.

```jsx
./pacman llljjjjjllllllhjjjlhhhhjhhhhhkkkkkkkljjjjjjlllkhhh

CCIT{videogame_starts_with_vi_coincidences?}
```