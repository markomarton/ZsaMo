import pyads
import socket
import configparser
import BckhMotor
import argparse


config = configparser.ConfigParser()
config.read('ATOS_conf.ini')                          #conf.ini beolvasása

#ZSAMO Server config
HOST = config['ZSAMO_SERVER']['IP']              # Symbolic name meaning all available interfaces
PORT = int(config['ZSAMO_SERVER']['port'])       # Arbitrary non-privileged port

ADSaddr = config['ADS_COMMUNICATION']['ADSaddr']  
ADSport = int(config['ADS_COMMUNICATION']['ADSport'])
ADS_IP = config['ADS_COMMUNICATION']['ADS_IP']

#Initialize PLC
with pyads.Connection(ADSaddr, ADSport, ADS_IP) as plc:
    
    #Motor dictionary
    mot_dict = {}                                    #motor dictionary: key-motor name - value-motor object
    for i in config.sections():                      #checkint for motor names in the ini file
        if 'type' in config[i]:
            if config[i]['type'] == '"BCKHFF_MO"':   
                mn = config[i]                       #motor name
                
                #előzetes adat
                SoftLimitLow = float("-inf")
                SoftLimitHigh = float("inf")
                Speed = -1.0
                Acceleration = -1.0
                Deceleration = -1.0
                Backlash = 0.0
                
                #optional data check
                if 'SoftLimitLow' in mn: SoftLimitLow = float(mn['SoftLimitLow'])
                if 'SoftLimitHigh' in mn: SoftLimitHigh = float(mn['SoftLimitHigh'])
                if 'Speed' in mn: Speed = float(mn['Speed'])
                if 'Acceleration' in mn: Acceleration = float(mn['Acceleration'])
                if 'Deceleration' in mn: Deceleration = float(mn['Deceleration'])
                if 'Backlash' in mn: Backlash = float(mn['Backlash'])
                
                mot_dict[i] = BckhMotor.BckhMotor(plc, mot_dict[i], mn['MotNum'], mn['unit'], mn['AbsoluteEnc'],
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
    
    
            #parser creation
            parser = argparse.ArgumentParser()
            parser.add_argument('task', help = 'A feladat.')
            parser.add_argument('-a','--axisName' ,help = 'A tengely nevét kéri.')
            parser.add_argument('-t','--targetPos', type = float, help = 'A tengely új helyét kéri.')
            parser.add_argument('-m','--movingAx', help = 'Lekéri egy vagy az összes tengely mozgásállaptát.')
            parser.add_argument('-s','--stopMoving', help = "It stop's the moving axis")
            args = parser.parse_args(data.split())
    
            #get the position of a certain axis
            if args.task == 'getPos':
                conn.sendall(mot_dict[args.axisName].getPosition().encode('ascii'))
    
            #move an axis to a certain position
            if args.task == 'move':
                if mot_dict[args.axisName].move(args.targetPos):
                    conn.sendall('ACK;'.encode('ascii'))
    
            #collect the status of all or only one axis
            if args.task == 'isMoving':
    
                if args.movingAx: #collect the status of one axis
                    if mot_dict[args.movingAx].moving():
                        conn.sendall('The {} axis is moving'.format(args.movingAx).encode('ascii'))
                    else:
                        conn.sendall('The {} axis is not moving'.format(args.movingAx).encode('ascii'))
            
                else: #collect the status of all axis
                    reply='Moving axis: '
                    for nev in mot_dict.keys():
                        if mot_dict[nev].moving():
                            reply += nev + ', '
                    if reply == 'Moving axis: ':
                        reply = 'There are no moving axis.**'  
                    conn.sendall(reply[0:-2].encode('ascii'))
                    
            #stop's all or one axis movmements
            if args.task == 'stop':
                if args.stopMoving:
                    mot_dict[args.stopMoving].stop()
                else: 
                    for nev in mot_dict.keys():
                        mot_dict[nev].stop()
                conn.sendall('The movement is stoped.'.encode('ascii'))
