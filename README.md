# py-scripts
Some Python scripts to easier some boring tasks.

## avoid-windows-restart-after-os-update.py
Aim:
 * avoid Windows to forcely restart the computer after an OS update

Requires:
 * administrator session

Usage:
```
./avoid-windows-restart-after-os-update.py
```

## generate-keystore.py
Aim:
 * generates a keystore.jks containing key and certs signed with ca.cer
 * generates a truststore.jks containing ca.cert
 * generates a .cert

Requires:
 * a file ca.cert
 * a file ca.key

Usage:
```
./generate-keystore.py <ip or domain>
```
