from pwn import *

process('cc -mtune=native -O2 -o break break.c', shell=True).wait_for_close()

passwd = process('./break').recvall()

log.success('Found password: %s', passwd)

s = ssh(host='vortex.labs.overthewire.org', user='vortex5', password=':4VtbC4lr')
p = s.run('/vortex/vortex5')
p.sendline(passwd)
p.send('cat /etc/vortex_pass/vortex6\n')

log.success(p.recvline())
