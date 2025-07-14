Per risolvere questa challenge ho sfruttato il fatto che Nginx non controlla l’input dell’utente quando si accede a /static. In questo modo possiamo accedere a file non permessi come app.py.

[http://notabug.challs.cyberchallenge.it/static/../../app.py](http://notabug.challs.cyberchallenge.it/static..%2fapp.py)

Così non funziona quindi ho provato a codificare l’url

[http://notabug.challs.cyberchallenge.it/static..%2Fapp.py](http://notabug.challs.cyberchallenge.it/static..%2fapp.py)