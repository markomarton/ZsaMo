import pyads
import socket
import configparser

class connection:
    def __init__(self,iniName):
        self.iniName = iniName
        self.config = configparser.ConfigParser()
        self.config.read('{}.ini'.format(self.iniName))
        
    def nameList(self):
        l = []
        for i in self.config.sections():                   #checkint for motor names in the ini file
            if 'type' in self.config[i]:
                if self.config[i]['type'] == '"BCKHFF_MO"':
                    l.append(i)
        return l

    
    def TAS(self):
        HOST = self.config['ZSAMO_SERVER']['IP']              # Symbolic name meaning all available interfaces
        PORT = int(self.config['ZSAMO_SERVER']['port'])
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        return s
        
    def plc(self):
        ADSaddr = self.config['ADS_COMMUNICATION']['ADSaddr']  
        ADSport = int(self.config['ADS_COMMUNICATION']['ADSport'])
        ADS_IP = self.config['ADS_COMMUNICATION']['ADS_IP']
        l = [ADSaddr, ADSport, ADS_IP]
        return l
    
    def data(self,motName):        
        data ={'name':motName,'MotNum':self.config[motName]['MotNum'],'unit':self.config[motName]['unit'], 'AbsoluteEnc':self.config[motName]['AbsoluteEnc']}
        mn = self.config[motName]                       #motor name
        
        #előzetes adat
        data['SoftLimitLow'] = float("-inf")
        data['SoftLimitHigh'] = float("inf")
        data['Speed'] = -1.0
        data['Acceleration'] = -1.0
        data['Deceleration'] = -1.0
        data['Backlash'] = 0.0
        # calculation of the physical angle Ph from the encoder angle X: Ph=(X-ZeroAngle)*Direction
        data['ZeroAngle'] = 0.0
        data['Direction'] = 1
        
        #optional data check
        if 'SoftLimitLow' in mn: data['SoftLimitLow'] = float(mn['SoftLimitLow'])
        if 'SoftLimitHigh' in mn: data['SoftLimitHigh'] = float(mn['SoftLimitHigh'])
        if 'Speed' in mn: data['Speed'] = float(mn['Speed'])
        if 'Acceleration' in mn: data['Acceleration'] = float(mn['Acceleration'])
        if 'Deceleration' in mn: data['Deceleration'] = float(mn['Deceleration'])
        if 'Backlash' in mn: data['Backlash'] = float(mn['Backlash'])
        if 'ZeroAngle' in mn: data['ZeroAngle'] = float(mn['ZeroAngle'])
        if 'Direction' in mn: data['Direction'] = float(mn['Direction'])
        return data

        
