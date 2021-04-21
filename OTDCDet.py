import socket
import subprocess
import os   
import sys
import re   #Regular expressions
import termcolor 
import threading
import time

##TTOK: 
#       -saveMeas fuggvenyt be kell fejezni
#       -Meg kell nezni, hogy a kinai program milyen detektoros fuggvenyeket hiv

#TODO:
#       -Valahogy uzenni kellene a controlnak, hogy nem sikerult a fajl mentese

class OTDCDet:
    def __init__(self, sharedFolderAddr, remoteFolderAddr, OTDCServerIP, OTDCServerPort):
        self.sharedFolderAddr=sharedFolderAddr
        self.remoteFolderAddr=remoteFolderAddr
        self.OTDCServerIP = OTDCServerIP
        self.OTDCServerPort = int(OTDCServerPort)
        
        self.nextFileNameIndex = 100000   #Default value which changed when the directory is scanned
        
        #Check if shared folder is mounted properly
        print("Shared detector data folder: ", self.sharedFolderAddr)
        mntCheck = subprocess.run(["findmnt", "-M", self.sharedFolderAddr], capture_output=True)
        if mntCheck.returncode == 0:
            print(self.sharedFolderAddr + " seems to be mounted")
        else: 
            print(self.sharedFolderAddr + " is not mounted")
            print("Trying to mount direcotry")
            mountResult=subprocess.run(["mount", self.sharedFolderAddr])
            if mountResult.returncode == 0:
                print(self.sharedFolderAddr + " was succesfully mounted")
            else:
                termcolor.cprint("   Shared folder for detector data access could not be mounted.   ",  'grey', 'on_red') 
                termcolor.cprint("   Check documentataion about setting the shared folder access!   ",  'grey', 'on_red' )
                sys.exit()
        
        # Search through the subdirectories to find out the next filename
        for root, dirs, files in os.walk(self.sharedFolderAddr):
            for fileName in files:
                if re.match(r"M\d\d\d\d\d\d.(?:csv|tdc)", fileName):
                    fileNameIndex = int(re.split(r"M|\.", fileName)[1])
                    if fileNameIndex >= self.nextFileNameIndex:
                        self.nextFileNameIndex = fileNameIndex+1
        print("\nNext filename will be: M" + str(self.nextFileNameIndex) + ".tdc/csv" )
        
        #Check if measurement is running
        self.isRunning = bool(self.getStatus()[1])
        if self.isRunning:
            termcolor.cprint('   Measurement is running on OTDC!!! Stop manually and retry!! ', 'grey', 'on_red' )
            sys.exit()
            
    def send_cmd(self, cmd) :
        #Send a command to the OTDC computer
        #Returns the answer as a list of numbers. The number and meaning of the returned values depend on the command
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.OTDCServerIP, self.OTDCServerPort))
        
        client.send(cmd.encode('ascii'))
        client_recv = client.recv(4096)
        client.close()
        
        raw_list = client_recv.split()
        
        resp = []
        for txt in raw_list : resp.append(int(txt))
        
        return resp
    
    def getStatus(self):
        #Get the status of the measurement
        #Returns a list: [isOK, isStarted, time, detectedHits]
            # isOK: Checks if OTDC2D window is opened -1->not Opened 0->Opened
            # isStarted: Checks if measurement is running
            # time: measurement time
            # detectedHits: detected hits in the measurement
        
        return self.send_cmd("STATUS")
    
        
    def startMeas(self, directoryName, time, title):
        #Starts a measurement with the OTDC.
        #Returns a list: [errorString, fileName]
            # errorString: "OK" if measurement started, otherwise the description of the error
            # fileName: The filename where the measurement will be saved without the extensions (csv/tdc)
        
        
        #Indicate that a measurement started (isRunning = True ) to prevent accidental restart
        if self.getStatus()[1] != 0:
            return["Measurement is already running", "0"]
        
        #Starts the measurement
        hitlimit=0
        resolution=1024
        cmd="START %d %d %d %s" % (resolution, hitlimit, time, title)
        print("Command to OTDC: " + cmd)
        startError = self.send_cmd(cmd)
        if startError[0]:
            return["Error while starting the measurement on OTDC", "0"]
        
        #Updates the next file number in self.nextFileNameIndex
        # Search through the subdirectories to find out the next filename
        for root, dirs, files in os.walk(self.sharedFolderAddr):
            for fileName in files:
                if re.match(r"M\d\d\d\d\d\d.(?:csv|tdc)", fileName):
                    fileNameIndex = int(re.split(r"M|\.", fileName)[1])
                    if fileNameIndex >= self.nextFileNameIndex:
                        self.nextFileNameIndex = fileNameIndex+1
        
        #Starts a thread which monitors if the measurement finished then save
        saveThread = threading.Thread(target=self.saveMeas, args=(directoryName, self.nextFileNameIndex, time))
        saveThread.start()
        
        #Normal return
        return [ "OK", "M"+str(self.nextFileNameIndex) ]
        
    def saveMeas(self, directoryName, fileNameIndex, measTime):
        # Saves the measurement file on OTDC computer
        
        #Check if directory exist, create if not existing
        if directoryName not in os.listdir(self.sharedFolderAddr):
            mkdirRes=subprocess.run(["mkdir", self.sharedFolderAddr+"/"+directoryName],  capture_output=True)
            if mkdirRes.returncode != 0:
                termcolor.cprint("   WARNING: Folder could not be created, trying to save to default directory   ", 'grey', 'on_cyan')
                directoryName = "default"
        
        # wait until the end is close
        if measTime-self.getStatus()[2] >= 1.0:  #Remaining time is geq 1.0
            time.sleep(measTime-1)
            
        # Wait for the measurement to finish
        while self.getStatus()[1]:
            time.sleep(1)
            
        #Save the measurement
        fullOTDCSaveDirPath=self.remoteFolderAddr + "\\" + directoryName +"\\"
        print( "SAVE "+fullOTDCSaveDirPath+" M"+ str(fileNameIndex) )
        retSave=self.send_cmd("SAVE "+fullOTDCSaveDirPath+" M"+ str(fileNameIndex) )
        
        if retSave[0] != 0:
            termcolor.cprint("   ERROR! Saving of measurement failed!  ", 'grey', 'on_red')
    
    def stopMeas(self):
        # Stop the current measurement
        # Saving the data is done by the thread started by the startMeas function 
        #isRunning = False
        pass
    
#For debug:
#o=OTDCDet("/home/athos/SharedDetectorData", "D:\AthosDATA", "192.168.88.248", 65432)
        