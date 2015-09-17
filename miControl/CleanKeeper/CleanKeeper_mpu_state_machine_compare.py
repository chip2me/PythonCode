# -*- coding: iso-8859-1 -*-
#*===========================================================================*#
#*        Copyright (c) 1997-2013 by miControl. All rights reserved.         *#
#*                                                                           *#
#* File     : demo_statemachine.py                                           *#
#*                                                                           *#
#* Project  : mPLC                                                           *#
#* System   : MPU2                                                           *#
#* Version  : 1.00                                                           *#
#* Company  : miControl                                                      *#
#*                                                                           *#
#* Author   : miControl             mailto:support@miControl.de              *#
#* Date     : 30.01.2013                                                     *#
#*---------------------------------------------------------------------------*#
#* Customer : miControl                                                      *#
#* Name     : Support                                                        *#
#* OrderNr. :                                                                *#
#* Descr.   : Example for the state machine in MPU2                          *#
#* History  :                                                                *#
#*===========================================================================*#
from _pymc_builtins_ import *          # Import for simulation on PC

RUN_DISTANCE = 51200                   # Should correspond to 20 seconds run

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
   Sp(0x3004,0, 1)                     # Enable power stage
   
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
   pass
   #Sp(0x3004, 0x00, 0)                 # DEV_Enable - Disable
   #Sp(0x3000, 0x00, 1)                 # DEV_Cmd - Clear error
   #Sp(0x3000, 0x00, 0x82)              # DEV_Cmd - Default parameter
   #Sp(0x3900, 0x00, 1)                 # MOTOR_Type
   #Sp(0x3911, 0x00, 2)                 # MOTOR_Polarity
   #Sp(0x3910, 0x00, 10)                # MOTOR_PolN
   #Sp(0x3962, 0x00, 2000)              # MOTOR_ENC_Resolution
   #Sp(0x3901, 0x00, 3000)              # MOTOR_Nn
   #Sp(0x3902, 0x00, 24000)             # MOTOR_Un
   #Sp(0x3350, 0x00, 2410)              # VEL_Feedback
   #Sp(0x3550, 0x00, 2410)              # SVEL_Feedback
   #Sp(0x3221, 0x00, 15000)             # CURR_LimitMaxPos
   #Sp(0x3223, 0x00, 15000)             # CURR_LimitMaxNeg
   #Sp(0x3003,0,7)                      # PosMode

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
      Movr(55, 51200)
      NextState(STATE_Wait4Pos)

   #---------------------------------------------------------------------------
   elif State == STATE_Move2PosCCW:
      Movr(55, -51200)
      NextState(STATE_Wait4Pos)

   #---------------------------------------------------------------------------
   elif State == STATE_Wait4Pos:
      if Gp(0x3002,0) & (1<<4):              # Target reached
         Cmd = 0                             # Reset Cmd to receive new commands
         LastCmd = 0                         # Reset LastCmd to receive new commands
         NextState(STATE_Idle)

   #---------------------------------------------------------------------------
   elif State == STATE_Error:
      error = Gp(0x3001,0)
      if error == 0:
         NextState(STATE_Idle)
      # Command evaluation -----------------------------------------------------
      else:
         Sp(0x3004,0, 0)                     # Disable power stage