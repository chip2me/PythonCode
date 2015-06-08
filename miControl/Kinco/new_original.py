# -*- coding: iso-8859-1 -*-
#==============================================================================
#                 Copyright (c) 1997-2015 by miControl(R). All rights reserved.
#
# System   : mcTools V1.04.00.00
# Company  : miControl(R)
#
# Date Time: 04.06.2015 13:11:30
#==============================================================================
# Description: This file was generated by mcTools
#==============================================================================

from _pymc_builtins_ import *

if not PYMC:
   SpGp_NodeId(1)
   Sp(0x5000,0, 3)

def InitPars ():
   Sp(0x3004, 0x00, 0)                # DEV_Enable - Disable
   Sp(0x3000, 0x00, 1)                # DEV_Cmd - Clear error
   Sp(0x3000, 0x00, 0x82)             # DEV_Cmd - Default parameter

   Sp(0x3900, 0x00, 0)                # MOTOR_Type
   Sp(0x3911, 0x00, 0)                # MOTOR_Polarity

   Sp(0x3910, 0x00, 4)                # MOTOR_PolN
   Sp(0x3962, 0x00, 2000)             # MOTOR_ENC_Resolution

   Sp(0x3901, 0x00, 3000)             # MOTOR_Nn
   Sp(0x3902, 0x00, 24000)            # MOTOR_Un

   Sp(0x3350, 0x00, 0)                # VEL_Feedback
   Sp(0x3550, 0x00, 0)                # SVEL_Feedback

   Sp(0x3221, 0x00, 50000)            # CURR_LimitMaxPos
   Sp(0x3223, 0x00, 50000)            # CURR_LimitMaxNeg

   Sp(0x3050, 0x00, 0)                # DEV_DinEnable
   Sp(0x3051, 0x00, 0)                # DEV_DinClearError
   Sp(0x3052, 0x00, 0)                # DEV_DinStartStop
   Sp(0x3055, 0x00, 0)                # DEV_DinLimitPos
   Sp(0x3056, 0x00, 0)                # DEV_DinLimitNeg
   Sp(0x3057, 0x00, 0)                # DEV_DinReference

   Sp(0x3060, 0x00, 0)                # DEV_DoutError

   Sp(0x3108, 0x00, 0)                # IO_AIN0_Offset
   Sp(0x310a, 0x00, 0)                # IO_AIN0_DeadBand

   Sp(0x3154, 0x00, 255)              # DEV_DoutEnable

   Sp(0x3204, 0x00, 512)              # CURR_DesiredValue_Source
   Sp(0x3205, 0x00, 1000)             # CURR_DesiredValue_Reference

   Sp(0x3210, 0x00, 20)               # CURR_Kp
   Sp(0x3211, 0x00, 30)               # CURR_Ki

   Sp(0x3224, 0x00, 0)                # CURR_DynLimitMode
   Sp(0x3224, 0x01, 50000)            # CURR_DynLimitPeak
   Sp(0x3224, 0x02, 50000)            # CURR_DynLimitCont
   Sp(0x3224, 0x03, 1000)             # CURR_DynLimitTime

   Sp(0x3240, 0x00, 1000)             # CURR_Acc_dI
   Sp(0x3241, 0x00, 1000)             # CURR_Acc_dT
   Sp(0x3242, 0x00, 1000)             # CURR_Dec_dI
   Sp(0x3243, 0x00, 1000)             # CURR_Dec_dT
   Sp(0x3244, 0x00, 1000)             # CURR_Dec_QuickStop_dI
   Sp(0x3245, 0x00, 100)              # CURR_Dec_QuickStop_dT
   Sp(0x324c, 0x00, 0)                # CURR_RampType

   Sp(0x3302, 0x00, 1)                # VEL_ScaleNum
   Sp(0x3303, 0x00, 1)                # VEL_ScaleDen
   Sp(0x3304, 0x00, 768)              # VEL_DesiredValue_Source
   Sp(0x3305, 0x00, 1000)             # VEL_DesiredValue_Reference
   Sp(0x330a, 0x00, 1)                # VEL_DimensionNum
   Sp(0x330b, 0x00, 1)                # VEL_DimensionDen

   Sp(0x3310, 0x00, 100)              # VEL_Kp
   Sp(0x3311, 0x00, 0)                # VEL_Ki
   Sp(0x3312, 0x00, 0)                # VEL_Kd
   Sp(0x3313, 0x00, 10000)            # VEL_ILimit
   Sp(0x3314, 0x00, 0)                # VEL_Kvff
   Sp(0x3315, 0x00, 0)                # VEL_Kaff
   Sp(0x3317, 0x00, 0)                # VEL_KIxR

   Sp(0x3321, 0x00, 2147483647)       # VEL_LimitMaxPos
   Sp(0x3323, 0x00, 2147483647)       # VEL_LimitMaxNeg

   Sp(0x3340, 0x00, 1000)             # VEL_Acc_dV
   Sp(0x3341, 0x00, 3000)             # VEL_Acc_dT
   Sp(0x3342, 0x00, 1000)             # VEL_Dec_dV
   Sp(0x3343, 0x00, 3000)             # VEL_Dec_dT
   Sp(0x3344, 0x00, 1000)             # VEL_Dec_QuickStop_dV
   Sp(0x3345, 0x00, 100)              # VEL_Dec_QuickStop_dT
   Sp(0x334c, 0x00, 1)                # VEL_RampType

   Sp(0x33c0, 0x00, 0)                # VEL_BlockageGuarding_ConfigFlags
   Sp(0x33c0, 0x01, -1)               # VEL_BlockageGuarding_VelLow
   Sp(0x33c0, 0x02, -1)               # VEL_BlockageGuarding_VelHigh
   Sp(0x33c0, 0x03, 10)               # VEL_BlockageGuarding_Time

   Sp(0x3502, 0x00, 1)                # SVEL_ScaleNum
   Sp(0x3503, 0x00, 1)                # SVEL_ScaleDen
   Sp(0x3504, 0x00, 1280)             # SVEL_DesiredValue_Source
   Sp(0x3505, 0x00, 1000)             # SVEL_DesiredValue_Reference

   Sp(0x3510, 0x00, 100)              # SVEL_Kp
   Sp(0x3511, 0x00, 100)              # SVEL_Ki
   Sp(0x3517, 0x00, 0)                # SVEL_KIxR

   Sp(0x3521, 0x00, 65535)            # SVEL_LimitMaxPos
   Sp(0x3523, 0x00, 65535)            # SVEL_LimitMaxNeg

   Sp(0x35a1, 0x00, 16383)            # SVEL_MaxVelRange

   Sp(0x3720, 0x00, -2147483648)      # POS_PositionLimitMin
   Sp(0x3720, 0x01, 2147483647)       # POS_PositionLimitMax

   Sp(0x3732, 0x00, 1000)             # POS_FollowingErrorWindow
   Sp(0x3732, 0x01, 4294967295)       # POS_FollowingErrorWindowDyn
   Sp(0x3733, 0x00, 0)                # POS_FollowingErrorTime
   Sp(0x3733, 0x01, 65535)            # POS_FollowingErrorTimeDyn
   Sp(0x3734, 0x00, 4294967295)       # POS_FollowingErrorLimit
   Sp(0x373a, 0x00, 4294967295)       # POS_PositionWindow
   Sp(0x373b, 0x00, 0)                # POS_PositionWindowTime
   Sp(0x373b, 0x01, 65535)            # POS_PositionWindowTimeout
   Sp(0x373c, 0x00, 0)                # POS_ReachedConfigFlags

   Sp(0x374c, 0x00, 1)                # POS_RampType

   Sp(0x37a4, 0x01, 0)                # POS_GearBacklashComp_Path
   Sp(0x37a4, 0x02, 100)              # POS_GearBacklashComp_Vel

   Sp(0x37b2, 0x00, 0)                # POS_HomingMethod
   Sp(0x37b3, 0x00, 0)                # POS_HomingOffset
   Sp(0x37b4, 0x00, 0)                # POS_HomingVelSwitch
   Sp(0x37b4, 0x01, 0)                # POS_HomingVelZero
   Sp(0x37b5, 0x00, 60000)            # POS_HomingAcc
   Sp(0x37b5, 0x01, 0)                # POS_HomingDec
   Sp(0x37b6, 0x00, 2147483647)       # POS_HomingMaxIndexPath
   Sp(0x37b6, 0x01, 0)                # POS_HomingIndexOffset
   Sp(0x37b7, 0x00, 0)                # POS_HomingBlock_ConfigFlags
   Sp(0x37b7, 0x01, 10)               # POS_HomingBlock_VelLow
   Sp(0x37b7, 0x02, -1)               # POS_HomingBlock_VelHigh
   Sp(0x37b7, 0x03, 1)                # POS_HomingBlock_Time
   Sp(0x37b7, 0x04, -1)               # POS_HomingBlock_FollowingErrorWindow

   Sp(0x39a0, 0x00, 0)                # MOTOR_BrakeManagement_Config
   Sp(0x39a0, 0x06, -1)               # MOTOR_BrakeManagement_VelMin
   Sp(0x39a0, 0x07, 0)                # MOTOR_BrakeManagement_Din
   Sp(0x39a0, 0x08, -352)             # MOTOR_BrakeManagement_Dout
   Sp(0x39a0, 0x09, 10000)            # MOTOR_BrakeManagement_UpBrakeOff
   Sp(0x39a0, 0x0a, 8000)             # MOTOR_BrakeManagement_UpBrakeOn
   Sp(0x39a0, 0x10, 0)                # MOTOR_BrakeManagement_OffDelay1
   Sp(0x39a0, 0x11, 0)                # MOTOR_BrakeManagement_OffDelay2
   Sp(0x39a0, 0x12, 0)                # MOTOR_BrakeManagement_OnDelay1
   Sp(0x39a0, 0x13, 0)                # MOTOR_BrakeManagement_OnDelay2
   Sp(0x39a0, 0x18, 1)                # MOTOR_BrakeManagement_OffOrConditionFlags
   Sp(0x39a0, 0x19, 0)                # MOTOR_BrakeManagement_OffAndConditionFlags
   Sp(0x39a0, 0x1a, 1)                # MOTOR_BrakeManagement_OnOrConditionFlags
   Sp(0x39a0, 0x1b, 0)                # MOTOR_BrakeManagement_OnAndConditionFlags

   Sp(0x3b00, 0x00, 1)                # FCT_Control
   Sp(0x3b00, 0x01, 0)                # FCT_Precision

   Sp(0x3b10, 0x00, 0)                # FCT_Polarity
   Sp(0x3b11, 0x00, 0)                # FCT_PosNotationIndex
   Sp(0x3b12, 0x00, 180)              # FCT_PosDimIndex
   Sp(0x3b13, 0x00, 0)                # FCT_VelNotationIndex
   Sp(0x3b14, 0x00, 164)              # FCT_VelDimIndex
   Sp(0x3b15, 0x00, 0)                # FCT_AccNotationIndex
   Sp(0x3b16, 0x00, 176)              # FCT_AccDimIndex
   Sp(0x3b17, 0x00, 1)                # FCT_PosScaleNum
   Sp(0x3b17, 0x01, 1)                # FCT_PosScaleDen
   Sp(0x3b18, 0x00, 1)                # FCT_VelScaleNum
   Sp(0x3b18, 0x01, 1)                # FCT_VelScaleDen
   Sp(0x3b19, 0x00, 1)                # FCT_GearRatio_MotorRev
   Sp(0x3b19, 0x01, 1)                # FCT_GearRatio_ShaftRev
   Sp(0x3b1a, 0x00, 1)                # FCT_FeedConstant_Feed
   Sp(0x3b1a, 0x01, 1)                # FCT_FeedConstant_ShaftRev

InitPars()

#- main loop ------------------------------------------------------------------

while 1:
   pass
