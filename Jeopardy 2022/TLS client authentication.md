### **1. Creazione della CA (Certificate Authority):**

```
openssl genrsa -out ca-key.pem 2048
```

Crea il certificato della CA:

```
openssl req -new -x509 -key ca-key.pem -sha256 -days 365 -out ca-crt.pem -subj "/C=IT/ST=Italy/L=Rome/O=CyberChallenge/CN=CyberChallenge"
```

---

### **2. Creazione della chiave privata del client:**

```
openssl genrsa -out client-key.pem 2048
```

---

### **3. Creazione della CSR (Certificate Signing Request) del client:**

```
openssl req -new -key client-key.pem -out client.csr -subj "/C=IT/ST=Italy/L=Rome/O=CyberChallenge/CN=Admin"
```

---

### **4. Firma del certificato client con la CA:**

```
openssl x509 -req -in client.csr -CA ca-crt.pem -CAkey ca-key.pem -CAcreateserial -out client-crt.pem -days 365 -sha256
```

---

### **5. Verifica del certificato client:**

```
openssl x509 -in client-crt.pem -text -noout
```

---

### **6. Verifica della CA:**

```
openssl x509 -in ca-crt.pem -text -noout
```

---

### **7. Connessione al server usando il certificato client:**

```
openssl s_client -connect cert.challs.cyberchallenge.it:9609 \
-cert client-crt.pem -key client-key.pem -CAfile ca-crt.pem -alpn CCIT
```