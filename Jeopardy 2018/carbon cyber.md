La main page del sito ci dà tre indizi:

1. Il sito implementa XSS auditor. L’HTTP Response Header **X-XSS-Protection: 1; model=block.** L’XSS Auditor analizza il contenuto delle risposte HTTP provenienti da un server web alla ricerca di potenziali attacchi XSS. Se viene rilevato del codice JavaScript sospetto che potrebbe essere eseguito in modo non sicuro, l’Auditor cerca di bloccarlo prima che venga eseguito nel browser. In pratica, l’XSS Auditor cerca di rilevare e prevenire attacchi di tipo **Reflected XSS.**
2. Il sito implementa una CSP così definita:
    - **default-src 'self'**: Tutte le risorse devono provenire dallo stesso dominio.
    - **object-src 'none'**: I tag `<object>`, `<embed>` e `<applet>` non possono essere utilizzati.
    - **script-src 'self' 'sha256-NXhZUxLSMAeYjM0W8JlDZB4c3lVLTu9CQhVGWTqLgUo='**: Gli script possono essere caricati solo dallo stesso dominio o eseguiti se il loro contenuto inline produce esattamente l’hash specificato.
3. **Same-origin Policy (SOP)** impedisce a uno script (come JavaScript) su una pagina web di accedere o manipolare i dati di una pagina web che proviene da un dominio, protocollo o porta diversa. Questa politica di sicurezza protegge da attacchi come il **Cross-Site Scripting (XSS)**, evitando che dati sensibili vengano rubati o modificati da siti esterni.

http://carbon.challs.cyberchallenge.it/uploads/4ba5903f9d7c6837e691074a3c799527b8fa44b2

[http://carbon.challs.cyberchallenge.it/<script src%3D"%2Fuploads%2F4ba5903f9d7c6837e691074a3c799527b8fa44b2"><%2Fscript>](http://carbon.challs.cyberchallenge.it/%3Cscript%20src%3D%22%2Fuploads%2F4ba5903f9d7c6837e691074a3c799527b8fa44b2%22%3E%3C%2Fscript%3E)