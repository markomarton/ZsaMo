import pyads
import socket
import configparser
import BckhMotor
import argparse


config = configparser.ConfigParser()
config.read('conf.ini')                          #conf.ini beolvasása

#ZSAMO Server config
HOST = config['ZSAMO_SERVER']['IP']              # Symbolic name meaning all available interfaces
PORT = config['ZSAMO_SERVER']['port']            # Arbitrary non-privileged port

ADSaddr = config['ADS_COMMUNICATION']['ADSaddr']  
ADSport = int(config['ADS_COMMUNICATION']['ADSport'])

#Initialize PLC
plc = pyads.Connection(ADSaddr, ADSport)
plc.open()



#Motor dictionary
mot_dict = {}                                    #motor dictionary: tartalmazza a motor száma - motor objektum párosokat
for i in config.sections():                      #végigemegyünk minden key-en az ini file-ban
    if 'type' in config[i]:
        if config[i]['type'] == '"BCKHFF_MO"':   #ellenörzi hogy motor e amit kiolvasunk az ini file-ból
            mn = config[i]                       #motor name
            
            #előzetes adat
            SoftLimitLow = float("-inf")
            SoftLimitHigh = float("inf")
            Speed = -1.0
            Acceleration = -1.0
            Deceleration = -1.0
            Backlash = 0.0
            
            #adat meglétének vizsgálta és cseréje
            if 'SoftLimitLow' in mn: SoftLimitLow = float(mn['SoftLimitLow'])
            if 'SoftLimitHigh' in mn: SoftLimitHigh = float(mn['SoftLimitHigh'])
            if 'Speed' in mn: Speed = float(mn['Speed'])
            if 'Acceleration' in mn: Acceleration = float(mn['Acceleration'])
            if 'Deceleration' in mn: Deceleration = float(mn['Deceleration'])
            if 'Backlash' in mn: Backlash = float(mn['Backlash'])
            
            mot_dict[i] = BckhMotor.BckhMotor(plc, mn['MotNum'], mn['unit'], mn['AbsoluteEnc'],
                                              SoftLimitLow, SoftLimitHigh, Speed, Acceleration, Deceleration, Backlash)



#Plc-be irom GVL- könyvtárba
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
        motor_name = data
        if not data: break


        #parser létrehozása
        parser = argparse.ArgumentParser()
        parser.add_argument('task', help = 'A feladat.')
        parser.add_argument('-a','--axisName' ,help = 'A tengely nevét kéri.')
        parser.add_argument('-t','--targetPos', type = int, help = 'A tengely új helyét kéri.')
        parser.add_argument('-m','--movingAx', help = 'Lekéri egy vagy az összes tengely mozgásállaptát.')
        args = parser.parse_args(data.split())

        #Lekéri ehy adott tengely állását.
        if args.task == 'getPos':
            conn.sendall(mot_dict[args.axisName].getPosition().encode('ascii'))

        #Adott pozícióba állítja a tengelyt.
        if args.task == 'move':
            if mot_dict[args.axisName].move(args.targetPos):
                conn.sendall('ACK;'.encode('ascii'))

        # Lekéri egy vagy az összes tengely mozgásállaptát.
        if args.task == 'isMoving':

            if args.movingAx: #Lekéri egy tengely mozgásállaptát.
                if mot_dict[args.movingAx].moving():
                    conn.sendall('The {} axis is moving'.format(args.movingAx).encode('ascii'))
                else:
                    conn.sendall('The {} axis is not moving'.format(args.movingAx).encode('ascii'))
        
            else: #Lekéri az összes tengely mozgásállaptát.  
                reply='Moving axis: '
                for nev in mot_dict.keys:
                    if mot_dict[nev].moving:
                        reply += nev + ', '
                if reply == 'Moving axis: ': #ellenörzés: ha minden tengely áll
                    reply = 'There are no moving axis.**'  
                conn.sendall(reply[0:-2].encode('ascii'))

plc.close()
