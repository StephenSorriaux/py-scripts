# py-scripts
Some Python scripts to easier some boring tasks.

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
