The ip command is one of the Linux tools for administering the network configuration.
In particular, you can assing an address to an interface using the following syntax:
ip addr add [ipaddress/netmask] dev [devicename] (for removing an existing address ip addr del [ipaddress/netmask] dev [devicename])
For example, you can add to eth0 the address 192.168.100.100 from the 192.168.100.0/24 network using:
ip addr add 192.168.100.100/24 dev eth0
Use this command for configuring the connection between node1 and node2 according to this updated network layout.
After you complete the above task, execute a 3-way handshake from node1 to node2 using the custom script level4 on node1.

```jsx
docker exec -it ns_node2_1 /bin/bash
```

- **docker exec**: Permette di eseguire comandi all’interno di un container Docker in esecuzione.
- **-it**: Interattivo, permette di aprire una shell.
- **ns_node2_1**: Nome del container a cui si accede.
- **/bin/bash**: Avvia una shell Bash dentro il container.

```jsx
ip addr add 192.168.100.2/24 dev eth1
```

- **ip addr add**: Aggiunge un indirizzo IP a un’interfaccia di rete.
- **192.168.100.2/24**: Nuovo IP assegnato.
- **dev eth1**: L’IP viene assegnato all’interfaccia di rete eth1.

```jsx
ip addr add 192.168.100.2/24 dev eth0
```

Comando da effettuare nel container 2

Eseguo level4