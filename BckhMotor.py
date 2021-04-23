import pyads

class BckhMotor:
    #Constructor of Class
    def __init__(self, plc, MotName,
                 MotNum, # [int] Number of motor in PLC
                 unit,   # [string] Unit 
                 AbsEnc, # [bool] is it absolute?
                 SLimLow=float("-inf"), SLimHigh=float("inf"), #Soft limits
                 Speed=-1.0, Acc=-1.0, Dec=-1.0, BckLash=0.0,
                 ZeroAngle = 0.0, Direction = 1 # calculation the real angle
                 ):
        self.plc = plc
        self.MotNum = MotNum
        self.unit = unit
        self.AbsEnc = AbsEnc
        self.SLimHigh = SLimHigh
        self.SLimLow = SLimLow
        self.Speed = Speed
        self.Acc = Acc
        self.Dec = Dec
        self.BckLash = BckLash
        self.MotName = MotName
        self.ZeroAngle = ZeroAngle
        self.Direction = Direction

        #plc.write_by_name("GVL.axes[{}].control.bEnable".format(self.MotNum), True, pyads.PLCTYPE_BOOL)
        
        if Speed>0:
            plc.write_by_name("GVL.astAxes[{}].stControl.fVelocity".format(self.MotNum), Speed, pyads.PLCTYPE_LREAL)
        else:
            self.Speed = plc.read_by_name("GVL.astAxes[{}].stControl.fVelocity".format(self.MotNum), pyads.PLCTYPE_LREAL)

        if Acc>0:
            plc.write_by_name("GVL.astAxes[{}].stControl.fAcceleration".format(self.MotNum), Acc, pyads.PLCTYPE_LREAL)
        else:
            self.Acc = plc.read_by_name("GVL.astAxes[{}].stControl.fAcceleration".format(self.MotNum), pyads.PLCTYPE_LREAL)

        if Dec>0:
            plc.write_by_name("GVL.astAxes[{}].stControl.fDeceleration".format(self.MotNum), Dec, pyads.PLCTYPE_LREAL)
        else:
            self.Dec = plc.read_by_name("GVL.astAxes[{}].stControl.fDeceleration".format(self.MotNum), pyads.PLCTYPE_LREAL)


        plc.write_by_name("GVL.astAxes[{}].stControl.eCommand".format(self.MotNum), 0, pyads.PLCTYPE_INT)
        pass


    def getPosition(self):
        reply = 'Positon: ' + self.MotName + ' ,'
        reply += str(self.plc.read_by_name("GVL.astAxes[{}].stStatus.bBusy".format(self.MotNum), pyads.PLCTYPE_BOOL))
        reply += ','
        reply += str(self.plc.read_by_name("GVL.astAxes[{}].stStatus.nErrorID".format(self.MotNum), pyads.PLCTYPE_UDINT))
        reply += ','
        encoderAngle = float(self.plc.read_by_name("GVL.astAxes[{}].stStatus.fActPosition".format(self.MotNum), pyads.PLCTYPE_LREAL))                             
        reply += "{:.2f}".format(self.encoder2physicalAngle(encoderAngle))
        reply += ','
        encodertargetpos = float(self.plc.read_by_name("GVL.astAxes[{}].stControl.fPosition".format(self.MotNum), pyads.PLCTYPE_LREAL))
        reply += "{:.2f}".format(self.encoder2physicalAngle(encodertargetpos))
        reply += ';'
        return reply
        pass

    def move(self,targetPos):
        if self.SLimLow< float(targetpos) and float(targetpos) < self.SLimHigh
            realtargetPos=self.physical2encoderAngle(float(targetpos))
            self.plc.write_by_name("GVL.astAxes[{}].stControl.bEnable".format(self.MotNum), True, pyads.PLCTYPE_BOOL)
            self.plc.write_by_name("GVL.astAxes[{}].stControl.bStop".format(self.MotNum), False, pyads.PLCTYPE_BOOL)
            self.plc.write_by_name("GVL.astAxes[{}].stControl.eCommand".format(self.MotNum), 0, pyads.PLCTYPE_INT)
            self.plc.write_by_name("GVL.astAxes[{}].stControl.fPosition".format(self.MotNum), realtargetPos, pyads.PLCTYPE_LREAL)
            self.plc.write_by_name("GVL.astAxes[{}].stControl.bExecute".format(self.MotNum), True, pyads.PLCTYPE_BOOL)
            return True #with v1
        else
            return False
        pass

    def moving(self):
        return self.plc.read_by_name("GVL.astAxes[{}].stStatus.bBusy".format(self.MotNum), pyads.PLCTYPE_BOOL)
    
    def stop(self):
        self.plc.write_by_name("GVL.astAxes[{}].stControl.bStop".format(self.MotNum), True, pyads.PLCTYPE_BOOL)
        
    #def status(self):
        #not correct line
    #    self.plc.write_by_name("GVL.axes[{}].status.bStatus".format(self.MotNum), True, pyads.PLCTYPE_BOOL)
        
    def reset(self):
        self.plc.write_by_name("GVL.astAxes[{}].stControl.bReset".format(self.MotNum), True, pyads.PLCTYPE_BOOL)
    
    def homeAxis(self):
        self.plc.write_by_name("GVL.astAxes[{}].stControl.eCommand".format(self.MotNum), 10, pyads.PLCTYPE_INT) # 10 -> Motionfunctions::Home
        self.plc.write_by_name("GVL.astAxes[{}].stConfig.nHomeSeq".format(self.MotNum),  1,  pyads.PLCTYPE_UINT) # 1 -> HomeToLowLimit
        self.plc.write_by_name("GVL.astAxes[{}].stControl.bExecute".format(self.MotNum), True, pyads.PLCTYPE_BOOL)
    
    def encoder2physicalAngle(self, encoderAngle):
        return (encoderAngle - self.ZeroAngle) * self.Direction
            
    def physical2encoderAngle(self, physicalAngle):
        return physicalAngle / self.Direction + self.ZeroAngle





