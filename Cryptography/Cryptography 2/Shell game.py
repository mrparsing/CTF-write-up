from pwn import *
import math
from Crypto.Util.number import inverse
from Crypto.Util.number import long_to_bytes
from crt_solver import crt_solver
import gmpy2
import decimal
from decimal import *
e = 5


def fifth_root(x):
    return decimal.Decimal(x) ** (decimal.Decimal(1) / decimal.Decimal(5))




r = remote("shell.challs.cyberchallenge.it", 9048)
r.recv()
r.sendline(b"1")
n = int(r.recvline().decode().split(" ")[1])
cipher_text = int(r.recvline().decode().split(" ")[1])


r.recvline()
r.recvline()
r.recvline()

first_choice = {}
second_choice = {}
third_choice = {}

for i in range (5):
    r.sendline(b"1")
    r.recv()
    n = int(r.recvline().decode().split(" ")[1])
    cipher_text = int(r.recvline().decode().split(" ")[1])
    first_choice[n] = cipher_text


    r.recvline()
    r.recvline()
    r.recvline()

    r.sendline(b"2")
    r.recv()
    n = int(r.recvline().decode().split(" ")[1])
    cipher_text = int(r.recvline().decode().split(" ")[1])
    second_choice[n] = cipher_text


    r.recvline()
    r.recvline()
    r.recvline()


    r.sendline(b"3")
    r.recv()
    print(i)
    n = int(r.recvline().decode().split(" ")[1])
    cipher_text = int(r.recvline().decode().split(" ")[1])
    third_choice[n] = cipher_text


    r.recvline()
    r.recvline()
    r.recvline()




L1=[]
M1=[]
for key, value in first_choice.items():
    L1.append(value)
    M1.append(key)

L2=[]
M2=[]
for key, value in second_choice.items():
    L2.append(value)
    M2.append(key)

L3=[]
M3=[]
for key, value in third_choice.items():
    L3.append(value)
    M3.append(key)

m1_5 = crt_solver(L1,M1)
m2_5 = crt_solver(L2,M2)
m3_5 = crt_solver(L3,M3)

with decimal.localcontext() as context:
    context.prec = 500

    m1 = int(fifth_root(m1_5))
    m2 = int(fifth_root(m2_5))
    m3 = int(fifth_root(m3_5))

print(m1)
print(m2)
print(m3)



print(long_to_bytes(m1))
print(long_to_bytes(m2))
print(long_to_bytes(m3))