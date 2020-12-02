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
            parser.add_argument('task', help = 'The task')
            # task list:
                # getPos: get the position of an axis
                # move: move a target to a given position
                # isMoving: ask for an axis status (moving[True] or not[False])
                # stop: stops all movements
                # restart: restart the PLC if it was phisicaly stopped (not implemented)
                # getStatus: get the status of an axis
            
            parser.add_argument('-a','--axisName' ,help = 'Axis name')
            parser.add_argument('-t','--targetPos', type = float, help = 'Move anaxis to the given position')
            args = parser.parse_args(data.split())
    
            #get the position of a certain axis
            if args.task == 'getPos':
                conn.sendall(mot_dict[args.axisName].getPosition().encode('ascii'))
    
            #move an axis to a certain position
            if args.task == 'move':
                if mot_dict[args.axisName].move(args.targetPos):
                    conn.sendall('ACK'.encode('ascii'))
    
            #collect the status an axis
            if args.task == 'isMoving':
                if mot_dict[args.axisName].moving():
                    conn.sendall('True'.encode('ascii'))
                else:
                    conn.sendall('False'.encode('ascii'))
                    
            #stop's all or one axis movmements
            if args.task == 'stop':
                if args.axisName:
                    mot_dict[args.axisName].stop()
                    conn.sendall((args.axisName + ' axis stopped.').encode('ascii'))
                else: 
                    for nev in mot_dict.keys():
                        mot_dict[nev].stop()
                    conn.sendall('All movements are stopped.'.encode('ascii'))
                
            #restart after emergency shutdown
            if args.task == 'restart':
                # not correct line 
                PLC.write_by_name("GVL_APP.bReleaseEmStop", True, pyads.PLCTYPE_BOOL)
                conn.sendall('True'.encode('ascii'))
            
            if args.task == 'getStatus':
                mot_dict[args.axisName].status()
                
            if args.task == 'reset':
                if args.axisName:
                    mot_dict[args.axisName].reset()
                    conn.sendall((args.axisName + ' axis reset.').encode('ascii'))
                else: 
                    for nev in mot_dict.keys():
                        mot_dict[nev].reset()
                    conn.sendall('All axes are reset.'.encode('ascii'))
                    
            if args.task == 'homeAxis':
                if args.axisName:
                    mot_dict[args.axisName].homeAxis()
                    conn.sendall((args.axisName + ' axis started to go HOME.').encode('ascii'))
                else:
                    conn.sendall('Axis name incorrect!!'.encode('ascii'))
                    
