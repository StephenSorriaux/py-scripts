#!/usr/bin/env python

from _winreg import *
from subprocess import check_output

regKeys = []
regKeys.append(['SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate', '',REG_SZ, None])
regKeys.append(['SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU', '',REG_SZ, None])
regKeys.append(['SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU', 'NoAutoRebootWithLoggedOnUsers',REG_DWORD, 1])

for key,name,key_type,val in regKeys:
    print("writing key %s to registry" % key)
    registryKey = CreateKey(HKEY_LOCAL_MACHINE, key)
    SetValueEx(registryKey, name, 0, key_type, val)
    CloseKey(registryKey)

print("forcing reload of Windows Update configuration...")
check_output("gpupdate /force", shell=True)
print("done.")
