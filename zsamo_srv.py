import BckhMotor
import argparse
import connection
import pyads

ini_name = 'ATHOS_conf'
con = connection.connection(ini_name)
li = con.plc()

with pyads.Connection(li[0], li[1], li[2]) as PLC:
    s = con.TAS()
    
    mot_dict = {}                                    #motor dictionary: key-motor name - value-motor object
    for i in con.nameList():                         #checkint for motor names in the ini file 
        data=con.data(i)          
        mot_dict[i] = BckhMotor.BckhMotor(PLC, data['name'], data['MotNum'], data['unit'], data['AbsoluteEnc'],
                                          data['SoftLimitLow'], data['SoftLimitHigh'], data['Speed'],
                                          data['Acceleration'], data['Deceleration'], data['Backlash'])
    
    
    while 1:
        conn, addr = s.accept()
        print ('Connected by'+ addr[0])
        while 1:
            #conn, addr = s.accept()
            #print ('Connected by'+ addr[0])
            tmpdata = conn.recv(4096)
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
                    conn.sendall('ACK'.encode('ascii'))
    
            #collect the status of all or only one axis
            if args.task == 'isMoving':
    
                if args.movingAx: #collect the status of one axis
                    if mot_dict[args.movingAx].moving():
                        conn.sendall(True)
                    else:
                        conn.sendall(False)
            
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
                conn.sendall('All movements are stopped.'.encode('ascii'))
                
            #restart after emergency shutdown
            if args.task == 'restart':
                for nev in mot_dict.keys():
                        mot_dict[nev].restart()
