import socket
import struct
import re

def u32(data):
    return struct.unpack('<I', data)[0]

def p32(data):
    return struct.pack('<I', data)

r = socket.create_connection(('vortex.labs.overthewire.org', 5842))
s = sum(u32(r.recv(4)) for _ in range(4))

r.send(p32(s & 0xffffffff))
creds = r.recv(4096).decode()

if re.match('Username', creds):
    print('[+] Creds:', creds)
else:
    print('[-] Invalid sum')
