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
        
        #optional data check
        if 'SoftLimitLow' in mn: data['SoftLimitLow'] = float(mn['SoftLimitLow'])
        if 'SoftLimitHigh' in mn: data['SoftLimitHigh'] = float(mn['SoftLimitHigh'])
        if 'Speed' in mn: data['Speed'] = float(mn['Speed'])
        if 'Acceleration' in mn: data['Acceleration'] = float(mn['Acceleration'])
        if 'Deceleration' in mn: data['Deceleration'] = float(mn['Deceleration'])
        if 'Backlash' in mn: data['Backlash'] = float(mn['Backlash'])
        return data

    def isOTDCInstalled(self):
        #Test if OTDC is in the config file
        #Returns True/False
        if 'OTDC' in self.config.sections():
            return True
        else:
            return False
        
    def OTDCpaths(self):
        #Return a list with folder paths [SharedFolderAddr, RemoteFolderAddr]
        #SharedFolderAddr: Folder name on the server machine where OTDC is mounted to
        #RemoteFolderAddr: Address of data folder on the OTDC machine
        
        return [self.config['OTDC']['SharedFolderAddr'], self.config['OTDC']['RemoteFolderAddr']]
    
    def OTDCIPandPort(self):
        #Return a list with IP address and port of the OTDC machine
        
        return [self.config['OTDC']['OTDC_IP'], self.config['OTDC']['OTDC_Port']]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        