import socket

ZsaMoIP='192.168.88.246'

def startMeas(time):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( (ZsaMoIP, 50007) )
    command='startMeas -T ' + str(time)
    sock.sendall(command.encode('ascii'))
    sock.recv(1024)
    sock.close()

def mov(axis, target):
    if axis not in ['monho', '2th', 'om', 'detang', 'ath']:
        print('axis must be: monho / 2th / om / detang / ath')
        return
    
    if (type(target) != int) and (type(target) != float):
        print('Targetpos not a number!!')
        return
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( (ZsaMoIP, 50007) )
    
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
    sock.connect( (ZsaMoIP, 50007) )
    
    msg = 'getPos -a '+ axis
    sock.sendall( msg.encode('ascii') )
    data = sock.recv(4096)
    #print(data)
    sock.close()
    print(data.decode('ascii').split(',')[3])

def getpfull(axis):
    if axis not in ['monho', '2th', 'om', 'detang', 'ath']:
        print('axis must be: monho / 2th / om / detang / ath')
        return
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( (ZsaMoIP, 50007) )
    
    msg = 'getPos -a '+ axis
    sock.sendall( msg.encode('ascii') )
    data = sock.recv(4096)
    print(data)
    sock.close()
    print(data.decode('ascii').split(',')[3])
    
def restart():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( (ZsaMoIP, 50007) )
    
    msg = 'restart'
    sock.sendall( msg.encode('ascii') )
    reply = sock.recv(4096)
    print(reply.decode('ascii'))
    sock.close()
    
def stop():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( (ZsaMoIP, 50007) )
    
    msg = 'stop'
    sock.sendall( msg.encode('ascii') )
    reply = sock.recv(4096)
    print(reply.decode('ascii'))
    sock.close() 
    
def reset(axis=''):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( (ZsaMoIP, 50007) )
    
    if axis == '':
        msg = 'reset'
    else:
        msg = 'reset -a ' + axis
    sock.sendall( msg.encode('ascii') )
    reply = sock.recv(4096)
    print(reply.decode('ascii'))
    sock.close() 

def homeAxis(axis):
    if axis not in ['monho', '2th', 'om', 'detang', 'ath']:
        print('axis must be: monho / 2th / om / detang / ath')
        return
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( (ZsaMoIP, 50007) )
    
    msg = 'homeAxis -a '+ axis
    sock.sendall( msg.encode('ascii') )
    data = sock.recv(4096)
    print(data)
    sock.close()
    
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


