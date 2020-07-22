import pyads
import socket
import sys

#ZSAMO Server config
HOST = '192.168.1.121'                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port

#Motor config
speed = 30
target_position_1 = 500
target_position_2 = 0
acceleration = 100
deceleration = 100

#Initialize PLC
plc = pyads.Connection("5.59.19.32.1.1", 852)
plc.open()
plc.write_by_name("GVL.axes[1].control.bEnable", True, pyads.PLCTYPE_BOOL)
plc.write_by_name("GVL.axes[1].config.fVelocity", speed, pyads.PLCTYPE_LREAL)
plc.write_by_name("GVL.axes[1].config.fAcceleration", acceleration, pyads.PLCTYPE_LREAL)
plc.write_by_name("GVL.axes[1].config.fDeceleration", deceleration, pyads.PLCTYPE_LREAL)
plc.write_by_name("GVL.axes[1].control.eCommand", 0, pyads.PLCTYPE_INT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

while 1:
    conn, addr = s.accept()
    print ('Connected by'+ addr[0])
    while 1:
        #conn, addr = s.accept()
        #print ('Connected by'+ addr[0])
        tmpdata = conn.recv(1024)
        data = tmpdata.decode('ascii')
        if not data: break

        print(data)
        
        if data == "V1,Status":
            reply = 'V1,'
            reply += str(plc.read_by_name("GVL.axes[1].status.bBusy", pyads.PLCTYPE_BOOL))
            reply += ','
            reply += str(plc.read_by_name("GVL.axes[1].status.nErrorID", pyads.PLCTYPE_UDINT))
            reply += ','
            reply += "{:.2f}".format(plc.read_by_name("GVL.axes[1].status.fActPosition", pyads.PLCTYPE_LREAL))
            reply += ','
            reply += str(plc.read_by_name("GVL.axes[1].config.fPosition", pyads.PLCTYPE_LREAL))
            reply += ';'
            conn.sendall(reply.encode('ascii'))
        else:
            tmp=data.split(',')
            plc.write_by_name("GVL.axes[1].config.fPosition", float(tmp[1]), pyads.PLCTYPE_LREAL)
            plc.write_by_name("GVL.axes[1].control.bExecute", True, pyads.PLCTYPE_BOOL)
            conn.sendall('ACK;'.encode('ascii'))
    
plc.close()
