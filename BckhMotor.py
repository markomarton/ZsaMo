# -*- coding: utf-8 -*-
#Motor class for the Beckhoff PLC motors
import math #-> for testing math.isnan(x)

class BckhMotor:
    #Constructor of Class
    def __init__(self, 
                 MotNum, # [int] Number of motor in PLC
                 unit,   # [string] Unit 
                 AbsEnc, # [bool] is it absolute?
                 SLimLow=float("-inf"), SLimHigh=float("inf"), #Soft limits
                 Speed=-1.0, Acc=-1.0, Dec=-1.0, BckLash=0.0):
        pass
    
    def getPosition():
        pass
    
    def move(targetPos):
        pass
    
    
    

