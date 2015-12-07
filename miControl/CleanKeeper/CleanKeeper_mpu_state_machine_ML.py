# -*- coding: iso-8859-1 -*-
#*===========================================================================*#
#*        Copyright (c) 1997-2013 by miControl. All rights reserved.         *#
#*                                                                           *#
#* File     : demo_statemachine.py                                           *#
#*                                                                           *#
#* Project  : mPLC                                                           *#
#* System   : MPU2                                                           *#
#* Version  : 1.10                                                           *#
#* Company  : miControl                                                      *#
#*                                                                           *#
#* Author   : miControl             mailto:support@miControl.de              *#
#* Date     : 30.01.2013                                                     *#
#*---------------------------------------------------------------------------*#
#* Customer : miControl                                                      *#
#* Name     : Support                                                        *#
#* OrderNr. :                                                                *#
#* Descr.   : Example for the state machine in MPU2                          *#
#* Motor    : Optimized for "ML23HSAP4300"  (secondary "PL23HSAP4300")       *#
#* History  : 1.20/2015DEC07  Re-establish after overload alarm              *#
#*          : 1.10/2015DEC07  Abrupt change of direction if activated        *#
#*                            during run.                                     *#
#*===========================================================================*#
from _pymc_builtins_ import *          # Import for simulation on PC

RUN_TIME = 20  # Seconds
RUN_SPEED = 51 # RPM
SCALE = 100
RUN_DISTANCE = ((RUN_SPEED*SCALE/60)*RUN_TIME*200*256)/SCALE # Pulses for requested run time

# Global variables for program identification ---------------------------------
AppId       = 0x00000001               # Unique identifier of the application
AppVersion  = 0x01000000               # Version of the application e.g. 01.00.00.00

# Global variables for user interface -----------------------------------------
Cmd               = 0                  # Command
InputFilterTime   = 10                 # Input filter time in ms

# Constants -------------------------------------------------------------------
STATE_Init                    = 0
STATE_Idle                    = 1
STATE_Move2PosCW              = 2
STATE_Move2PosCCW             = 3
STATE_Wait4Pos                = 4
STATE_Error                   = 5

CMD_BIT_StartPosCW            = (1<<0)
CMD_BIT_StartPosCCW           = (1<<1)

DIN_MASK_CMD                  = 0x03

# Global helper variables -----------------------------------------------------
State                         = STATE_Init
LastState                     = STATE_Init
LastCmd                       = 0
LastDin                       = 0

# Initialization - simulation -------------------------------------------------
if not PYMC:
   '''
   This section is executed when the program is launched directly in mPLC.
   The MPU2 program is simulated on the PC (in combination with the device).
   This allows a simplified diagnosis because "print" commands are possible.
   NOTE: The timing of the program changes since the execution of the Sp()/Gp() functions
   is delayed by the communication between the PC and the device.

   If you don't want to use simulation mode, start the program using the Run() function.
   '''
   SpGp_NodeId(1)                      # Set the node id of the device for Sp()/Gp() functions (for simulation mode)
   Sp(0x5000,0, 3)                     # Stop possibly existing MPU2 program on the device (otherwise it may disturb the simulation)

# Helper functions ------------------------------------------------------------
# Stores the current state in LastState and sets the next state
def NextState(state):
   global State, LastState
   LastState = State
   State     = state

# Reads the state of the digital inputs with a filter (prevents bouncing)
def DigitalInputFilter(last_din):
   din = Gp(0x3120,0)                                 # Read the state of the digital inputs
   if din != last_din:                                # Check if the input has changed
      time_start = Clock()                            # Read start time for filter
      while DiffClock(time_start) < InputFilterTime:  # Read state of the digital inputs during InputFilterTime in ms
         new_din = Gp(0x3120,0)                       # Read the state of the digital inputs
         if din != new_din:                           # Digital inputs have changed => bouncing? => do not apply a new value for the input!
            break
      else:                                           # Loop has been passed completely, without a change of the digital inputs
         last_din = din                               # Accept the new value of the digital inputs
   return last_din

# Edge detection 0->1 of Bit "mask"
def IsBitEdgeChangeToHigh(last, new, mask):
   return ((new ^ last) & new) & mask

# Checks if there is an error and starts the error handling if necessary
def CheckError():
   if Gp(0x3001,0):
      NextState(STATE_Error)

# Evaluation of the digital inputs --------------------------------------------
def CheckInputs():
   global din, LastDin, Cmd
   din = DigitalInputFilter(LastDin)
   if din != LastDin:
      Cmd = din & DIN_MASK_CMD
      LastDin = din

#- assistance functions --------------------------------------------------------
def Mov (vel, pos, rel=False):
   Sp(0x3300,0, vel)           # Vel
   Sp(0x3004,0, 1)             # Enable power stage

   if rel:
      Sp(0x3791,0, pos)        # Movr
   else:
      Sp(0x3790,0, pos)        # Mova

def Mova (vel, pos):
   Mov(vel, pos, False)

def Movr (vel, pos):
   Mov(vel, pos, True)

# Initialization - controller -------------------------------------------------
def InitPars ():
   #Sp(0x3004, 0x00, 0)               # DEV_Enable - Disable
   Sp(0x3000, 0x00, 0x1)              # DEV_Cmd - Clear error
   Sp(0x3000, 0x00, 0x82)             # DEV_Cmd - Default parameter
   Sp(0x3003, 0x00, 7)                # DEV_Mode

   # Motor Data for MotoSmart 23
   Sp(0x3900, 0x00, 2)                # MOTOR_Type
   Sp(0x3911, 0x00, 0)                # MOTOR_Polarity
   Sp(0x3910, 0x00, 200)              # MOTOR_PolN
   Sp(0x3901, 0x00, 3000)             # MOTOR_Nn
   Sp(0x3902, 0x00, 12000)            # MOTOR_Un      24000
   Sp(0x3350, 0x00, 0x0)              # VEL_Feedback
   Sp(0x3221, 0x00, 10000)            # CURR_LimitMaxPos
   Sp(0x3223, 0x00, 10000)            # CURR_LimitMaxNeg
   Sp(0x3210, 0x00, 30)               # CURR_Kp       682
   Sp(0x3211, 0x00, 3)                # CURR_Ki       64
   Sp(0x3314, 0x00, 1000)             # VEL_Kvff
   Sp(0x3830, 0x00, 32000)            # PWM_Frequency 32000
   Sp(0x3214, 0x00, 400)              # PAR_3214.00h
   Sp(0x3215, 0x00, 4000)             # PAR_3215.00h
   Sp(0x3910, 0x01, 256)              # PAR_3910.01h

   ### PL4300 (data found via mcDSA-S65-tuning_en.py)
   #CURR_Kp           (0x3210.0) = 1147
   #CURR_Ki           (0x3211.0) = 501
   #CURR_Kvff         (0x3214.0) = 0
   #CURR_Kaff         (0x3215.0) = 1100
   #MOTOR_PolN        (0x3910,0) = 200
   #MOTOR_Microstepsd (0x3910,1) = 256

   ### ML4300 (data found via mcDSA-S65-tuning_en.py)
   #CURR_Kp           (0x3210.0) = 338
   #CURR_Ki           (0x3211.0) = 39
   #CURR_Kvff         (0x3214.0) = 0
   #CURR_Kaff         (0x3215.0) = 3300
   #MOTOR_PolN        (0x3910,0) = 200
   #MOTOR_Microstepsd (0x3910,1) = 64

   #Test data for both PL and ML versions:
   ##Sp(0x3210, 0x00, 3)   # 338) #PL=30     # CURR_Kp      1147
   ##Sp(0x3211, 0x00, 30)  # 39)  #PL=3      # CURR_Ki     501
   ##Sp(0x3314, 0x00, 0)   # PL=0 # VEL_Kvff
   ##Sp(0x3315, 0x00, 3000)# 3300)#PL=3000   # _Kaff
   ##Sp(0x3910, 0x00, 1)   # 1    # PAR_3910.01h        200
   ##Sp(0x3910, 0x01, 256) # 64)  #256       # PL=1             # PAR_3910.01h
   ##Sp(0x3004, 0x00, 1)                     # DEV_Enable
   
   # Actual Motor Data START
   #                ML     PL 
   Sp(0x3210, 0x00, 10)    #30    # CURR_Kp   
   Sp(0x3211, 0x00, 1)     #3     # CURR_Ki   
   Sp(0x3314, 0x00, 0)     #0     # VEL_Kvff
   Sp(0x3315, 0x00, 9000)  #3000  # Kaff
   Sp(0x3910, 0x00, 200)   #200   # PAR_     
   Sp(0x3910, 0x01, 256)   #256   # PAR_     
   Sp(0x3004, 0x00, 1)     #1     # DEV_Enable
   # Actual Motor Data END 

# Main program ================================================================
# Main loop -------------------------------------------------------------------
while 1:
   CheckError()                              # Error check at each loop cycle
   CheckInputs()                             # Check of the digital inputs at each loop cycle

   #---------------------------------------------------------------------------
   if State == STATE_Init:
      InitPars()
      NextState(STATE_Idle)

   #---------------------------------------------------------------------------
   elif State == STATE_Idle:
      # Command evaluation -----------------------------------------------------
      if Cmd != LastCmd:
         if Cmd == CMD_BIT_StartPosCW:
            NextState(STATE_Move2PosCW)      # Start positioning CW
            LastCmd = Cmd
         elif Cmd == CMD_BIT_StartPosCCW:
            NextState(STATE_Move2PosCCW)     # Start positioning CCW
            LastCmd = Cmd

   #---------------------------------------------------------------------------
   elif State == STATE_Move2PosCW:
      Movr(RUN_SPEED, RUN_DISTANCE)
      NextState(STATE_Wait4Pos)

   #---------------------------------------------------------------------------
   elif State == STATE_Move2PosCCW:
      Movr(RUN_SPEED, -RUN_DISTANCE)
      NextState(STATE_Wait4Pos)

   #---------------------------------------------------------------------------
   elif State == STATE_Wait4Pos:
      if Gp(0x3002,0) & (1<<4):              # Target reached
         Cmd = 0                             # Reset Cmd to receive new commands
         LastCmd = 0                         # Reset LastCmd to receive new commands
         NextState(STATE_Idle)

      # If button pressed while running - evaluation --------------------------
      if Cmd != LastCmd:
         if Cmd == CMD_BIT_StartPosCW:
            NextState(STATE_Move2PosCW)      # Start positioning CW
            LastCmd = Cmd
         elif Cmd == CMD_BIT_StartPosCCW:
            NextState(STATE_Move2PosCCW)     # Start positioning CCW
            LastCmd = Cmd



   #---------------------------------------------------------------------------
   elif State == STATE_Error:
      error = Gp(0x3001,0)
      if error == 0:
         NextState(STATE_Idle)
      # Command evaluation -----------------------------------------------------
      else:
         Sp(0x3004,0, 0)                     # Disable power stage