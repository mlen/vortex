from pwn import *
import pwnlib.log

r = remote('vortex.labs.overthewire.org', 5842)
s = sum(u32(r.recvn(4)) for _ in xrange(4))

r.send(p32(s & 0xffffffff))
creds = r.recvall()

if re.match("Username", creds):
    log.success(creds)
else:
    log.failure('invalid sum')
