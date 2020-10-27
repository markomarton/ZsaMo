import socket
import sys
from time import sleep

def mov(axis, target):
    if axis not in ['monho', '2th', 'om', 'detang', 'ath']:
        print('axis must be: monho / 2th / om / detang / ath')
        return
    
    if (type(target) != int) and (type(target) != float):
        print('Targetpos not a number!!')
        return
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( ('192.168.88.252', 50007) )
    
    msg = 'move -a '+axis+ ' -t' + str(target)
    sock.sendall( msg.encode('ascii') )
    data = sock.recv(4096)
    print(data.decode('ascii'))
    
    sock.close()
    
def getp(axis):
    if axis not in ['monho', '2th', 'om', 'detang', 'ath']:
        print('axis must be: monho / 2th / om / detang / ath')
        return
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( ('192.168.88.252', 50007) )
    
    msg = 'getPos -a '+ axis
    sock.sendall( msg.encode('ascii') )
    data = sock.recv(4096)
    sock.close()
    print(data.decode('ascii').split(',')[3])

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect( ('192.168.88.252', 50007) )

# #####################
# msg = 'move -a monho -t 500'
# sock.sendall( msg.encode('ascii') )
# data = sock.recv(4096)
# print(data.decode('ascii'))

# msg = 'move -a 2th -t 0'
# sock.sendall( msg.encode('ascii') )
# data = sock.recv(4096)
# print(data.decode('ascii'))

# msg = 'move -a detang -t -58'
# sock.sendall( msg.encode('ascii') )
# data = sock.recv(4096)
# print(data.decode('ascii'))

# msg = 'move -a ath -t 1'
# sock.sendall( msg.encode('ascii') )
# data = sock.recv(4096)
# print(data.decode('ascii'))
# sleep(5)

# ############
# while (1):
# msg = 'getPos -a monho'
# sock.sendall( msg.encode('ascii') )
# data = sock.recv(4096)
# print(data.decode('ascii'))
# sleep(1)

# msg = 'getPos -a 2th'
# sock.sendall( msg.encode('ascii') )
# data = sock.recv(4096)
# print(data.decode('ascii'))
# sleep(1)

# msg = 'getPos -a detang'
# sock.sendall( msg.encode('ascii') )
# data = sock.recv(4096)
# print(data.decode('ascii'))
# sleep(1)

# msg = 'getPos -a ath'
# sock.sendall( msg.encode('ascii') )
# data = sock.recv(4096)
# print(data.decode('ascii'))
# sleep(1)


###########
# msg = 'isMoving -a monho'
# sock.sendall( msg.encode('ascii') )
# data = sock.recv(4096)
# print(data.decode('ascii'))

# msg = 'stop'
# sock.sendall( msg.encode('ascii') )
# data = sock.recv(4096)
# print(data.decode('ascii'))

#sock.close()


