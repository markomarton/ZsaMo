import pyads
import socket
import configparser

class connection:
    def __init__(self,iniName):
        self.iniName = iniName
        self.config = configparser.ConfigParser()
        self.config.read('{}.ini'.format(self.iniName))
        return self.config
    
    def connect(self):
        HOST = self.config[self.config]['IP']              # Symbolic name meaning all available interfaces
        PORT = int(self.config['ZSAMO_SERVER']['port'])
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        return s
        
    def ads(self):
        ADSaddr = self.config['ADS_COMMUNICATION']['ADSaddr']  
        ADSport = int(self.config['ADS_COMMUNICATION']['ADSport'])
        ADS_IP = self.config['ADS_COMMUNICATION']['ADS_IP']

        return pyads.Connection(ADSaddr, ADSport, ADS_IP)
    
    def data(self,motName):
        data ={'name':motName,'MotNum':self.config('MotNum'),'unit':self.config('unit'), 'AbsoluteEnc':self.config('AbsoluteEnc')}
        mn = self.config[motName]                       #motor name
        
        #előzetes adat
        data['SoftLimitLow'] = float("-inf")
        data['SoftLimitHigh'] = float("inf")
        data['Speed'] = -1.0
        data['Acceleration'] = -1.0
        data['Deceleration'] = -1.0
        data['Backlash'] = 0.0
        
        #optional data check
        if 'SoftLimitLow' in mn: data['SoftLimitLow'] = float(mn['SoftLimitLow'])
        if 'SoftLimitHigh' in mn: data['SoftLimitHigh'] = float(mn['SoftLimitHigh'])
        if 'Speed' in mn: data['Speed'] = float(mn['Speed'])
        if 'Acceleration' in mn: data['Acceleration'] = float(mn['Acceleration'])
        if 'Deceleration' in mn: data['Deceleration'] = float(mn['Deceleration'])
        if 'Backlash' in mn: data['Backlash'] = float(mn['Backlash'])
        return data
        