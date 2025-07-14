Update node2 and node3 configuration according to this diagram.
Then, complete the configuration so that HOST can reach node3 using the private address on 172.16.44.0/24 and ssh.

Su node2:

```jsx
ip addr add 172.16.44.100/24 dev eth1

ip link set eth1 up
```

Su node3:

```jsx
ip addr add 172.16.44.200/24 dev eth0

ip route add default via 172.16.44.100
```

Su node1:

```jsx
sysctl -w net.ipv4.ip_forward=1

ip route add 172.16.44.0/24 via 10.0.0.2 dev eth1

iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT
iptables -A FORWARD -i eth1 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
```

Su node2:

```jsx
sysctl -w net.ipv4.ip_forward=1

iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT
iptables -A FORWARD -i eth1 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
```

Su HOST:

```jsx
ssh root@172.16.44.200
```