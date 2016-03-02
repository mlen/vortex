from pwn import *

s = ssh(host='vortex.labs.overthewire.org', user='vortex7', password='Y52jxHtt/')
s.download_file('/vortex/vortex7')

s.interactive()
