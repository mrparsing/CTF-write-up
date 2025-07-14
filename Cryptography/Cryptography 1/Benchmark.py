"""Performance is the most important thing when it comes to cryptography. This is a remote challenge, you can connect to the service with: nc benchmark.challs.cyberchallenge.it 9031
"""

import re
from pwn import *

flag = ''

times_dict = {}

r = remote('benchmark.challs.cyberchallenge.it', 9031)

for i in range(5):
	r.recvline()

while '}' not in flag:
	for i in range(33, 126):
		r.recvline()
		r.sendline(flag+chr(i))
		
		data = r.recvline().decode()
		times_dict[int(re.findall(r'\d+', data)[0])] = chr(i)
		r.recvline()
		
	flag += times_dict[max(times_dict.keys())]
	print(flag)
