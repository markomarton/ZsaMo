import socket

class OTDCDet:
    def __init__(self, sharedFolderAddr, remoteFolderAddr, OTDCServerIP, OTDCServerPort):
        self.sharedFolderAddr=sharedFolderAddr
        self.remoteFolderAddr=remoteFolderAddr
        self.OTDCServerIP = OTDCServerIP
        self.OTDCServerPort = int(OTDCServerPort)
        # TODO Check if shared folder is mounted properly
        # TODO Builds a local database about the available files and folders
        pass
        
    def startMeas(self, directoryName, time):
        #Calculates the next file number
        #Indicate that a measurement started (isRunning = True ) to prevent accidental restart
        #Open communication socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('OTDCServerIP: ' + self.OTDCServerIP )
        print('OTDCServerPort: ' + str(self.OTDCServerPort) )
        client.connect( (self.OTDCServerIP, self.OTDCServerPort) )
        #Starts the measurement
        #Starts a thread which monitors if the measurement finished then save
            #Save file when measurement ended
            # isRunning=False
        hitlimit=0
        title='vmi'
        resolution=1024
        cmd="START %d %d %d %s" % (resolution, hitlimit, time, title)
        print(cmd)
        client.sendall(cmd.encode('ascii'))
        
        client.close()
        
    
    def stopMeas(self):
        #Stop the current measurement and save file
        #isRunning = False
        pass
        