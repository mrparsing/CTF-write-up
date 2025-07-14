from pwn import *


def main():
 HOST = 'software-17.challs.olicyber.it'
 PORT = 13000

 r = remote(HOST, PORT)

 data = r.recvuntil(b"iniziare ...")

 r.sendline("a")
 
 for i in range(10):
  somma(r)
 
 r.interactive()

def somma(r):
 data = r.recvuntil(b"numeri")
 data = r.recvline()

 data = r.recvuntil(b"]")

 array = data.decode().strip('[]').split(", ")

 somma = 0
 for i in array:
  somma += int(i)
 print(somma)
 r.sendline(f"{somma}")


if __name__ == "__main__":
 main()