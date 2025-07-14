# 🧨 MineCClicker - Write-up (CyberChallenge.IT 2023)

**Categoria:** Pwn  

## Descrizione del servizio

MineCClicker è un servizio stile *minesweeper* usato nella CTF Attack/Defense.  
Il backend è scritto in C, il client è una GUI in Python.

### Funzionalità:
- Registrazione e login utenti
- Creazione di game board (nome, secret, seed, dimensione, numero di bombe)
- Caricamento della board
- Gioco sulla board caricata

Le bombe sono generate randomicamente a partire da:
- un seed fornito dal creatore della board
- un seed casuale generato per ogni partita

Il creatore conosce entrambi i seed → può sempre rigenerare la posizione delle bombe.

> ⚠️ Le flag sono salvate nel campo `secret` di board speciali create dal checker.

---

## 🔓 Vulnerabilità

### 1. Play forever

**Bug:** la variabile globale `g_is_playing` non viene resettata dopo aver cliccato su una bomba.

**Exploit:**
1. Scopri celle a caso finché becchi una bomba
2. Continua comunque a giocare (il gioco non è terminato)
3. Ricavi la posizione reale delle bombe
4. Invia il layout corretto → ottieni la flag

**Fix:**  
Resettare `g_is_playing = false` nella funzione `uncover`.

---

### 2. Buffer Overflow nella rete

**Bug:** in `net_recv_req`, viene fatto un controllo *signed* sulla lunghezza del pacchetto → possibile overflow su un buffer nella BSS.

**Exploit:**
1. Invia un header con lunghezza negativa
2. Overflow sul buffer del pacchetto
3. Sovrascrivi la variabile globale con il layout delle bombe
4. Invia il layout arbitrario → vittoria e flag

**Fix:**  
Sostituire la comparazione signed (JLE) con una unsigned (JBE) in `net_recv_req`.

---

### 3. 1-byte Buffer Overflow nella login

**Bug:** overflow di 1 byte sulla password nella funzione `login`.

**Exploit:**
1. Usa il byte in overflow per sovrascrivere il LSB di `g_board_info`
2. Modifica i campi `num_bombs` e `seed`
3. Quando il server manda `num_bombs`, il client riceve in realtà `seed`
4. Conoscendo il seed → predici layout bombe → vittoria e flag

**Fix:**  
Ridurre il numero di byte letti dalla `strncpy` nella `login`.

---

🎯 **Flag store:** contenuto nel campo `secret` di board create dal checker.