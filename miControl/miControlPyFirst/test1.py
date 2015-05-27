# -*- coding: iso-8859-1 -*-
#*===========================================================================*#
#*        Copyright (c) 1997-2013 by miControl. All rights reserved.         *#
#*                                                                           *#
#* File     : test1.py                                                       *#
#*                                                                           *#
#* Project  : mPLC                                                           *#
#* System   : MPU2                                                           *#
#* Version  : 1.00                                                           *#
#* Company  : GCM A/S                                                        *#
#*                                                                           *#
#* Author   : Carsten Mols             mailto:cm@gearcentralene.dk           *#
#* Date     : 20.05.2015                                                     *#
#*---------------------------------------------------------------------------*#
#* Customer : Kinco                                                          *#
#* Name     :                                                                *#
#* OrderNr. :                                                                *#
#* Descr.   : Lifting application JOG UP/DOWN including Brake management.    *#
#* History  : Cyclic CW/CCW playground.                                      *#
#*===========================================================================*#
from _pymc_builtins_ import *          # Import for simulation on PC

# Global variables for program identification ---------------------------------
AppId       = 0x00000001               # Unique identifier of the application
AppVersion  = 0x01000000               # Version of the application e.g. 01.00.00.00

# Global variables for user interface -----------------------------------------
Cmd               = 0                  # Command
InputFilterTime   = 10                 # Input filter time in ms

# Constants -------------------------------------------------------------------
STATE_Init                    = 0
STATE_Idle                    = 1
STATE_StartHoming             = 2
STATE_Wait4HomingDone         = 3
STATE_Move2Pos1               = 4
STATE_Wait4PosReached         = 5
STATE_Error                   = 6
STATE_Move2Pos2               = 7

CMD_BIT_DIN3                  = (1<<3) # = 0x08
CMD_BIT_DIN2                  = (1<<2) # = 0x04
CMD_BIT_DIN1                  = (1<<1) # = 0x02
CMD_BIT_ClearError            = (1<<0) # = 0x01

#DIN_BIT_TRIGGER               = 0x10
DIN_MASK_CMD                  = 0x0F

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
   ###SpGp_NodeId(1)                      # Set the node id of the device for Sp()/Gp() functions (for simulation mode)
   ###Sp(0x5000,0, 3)                     # Stop possibly existing MPU2 program on the device (otherwise it may disturb the simulation)

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
      #if IsBitEdgeChangeToHigh(LastDin, din, DIN_BIT_TRIGGER):
      Cmd = din & DIN_MASK_CMD
      LastDin = din

# Initialization - controller -------------------------------------------------
def InitPars ():
   Sp(0x3004, 0x00, 0)                # DEV_Enable - Disable
   Sp(0x3000, 0x00, 1)                # DEV_Cmd - Clear error
   Sp(0x3000, 0x00, 0x82)             # DEV_Cmd - Default parameter

   Sp(0x3900, 0x00, 1)                # MOTOR_Type
   Sp(0x3911, 0x00, 2)                # MOTOR_Polarity

   Sp(0x3910, 0x00, 4)                # MOTOR_PolN
   Sp(0x3962, 0x00, 200)              # MOTOR_ENC_Resolution

   Sp(0x3901, 0x00, 4000)             # MOTOR_Nn
   Sp(0x3902, 0x00, 24000)            # MOTOR_Un

   Sp(0x3350, 0x00, 2378)             # VEL_Feedback
   Sp(0x3550, 0x00, 2378)             # SVEL_Feedback

   Sp(0x3221, 0x00, 2000)             # CURR_LimitMaxPos
   Sp(0x3223, 0x00, 2000)             # CURR_LimitMaxNeg


   Sp(0x3210, 0x00, 30)               # CURR_Kp
   Sp(0x3211, 0x00, 30)               # CURR_Ki

   Sp(0x3241, 0x00, 200)              # CURR_Acc_dT
   Sp(0x3243, 0x00, 200)              # CURR_Dec_dT

   Sp(0x3310, 0x00, 400)              # VEL_Kp
   Sp(0x3311, 0x00, 50)               # VEL_Ki
   Sp(0x3312, 0x00, 20)               # VEL_Kd
   Sp(0x3313, 0x00, 2000)             # VEL_ILimit
   Sp(0x3314, 0x00, 50)               # VEL_Kvff
   Sp(0x3315, 0x00, 50)               # VEL_Kaff
   Sp(0x3317, 0x00, 5)                # VEL_KIxR

   Sp(0x3341, 0x00, 50)               # VEL_Acc_dT
   Sp(0x3343, 0x00, 50)               # VEL_Dec_dT
   Sp(0x3345, 0x00, 20)               # VEL_Dec_QuickStop_dT

   Sp(0x33c0, 0x03, 7)                # VEL_BlockageGuarding_Time

   Sp(0x3510, 0x00, 10)               # SVEL_Kp
   Sp(0x3511, 0x00, 1)                # SVEL_Ki
   Sp(0x3517, 0x00, 1)                # SVEL_KIxR

   Sp(0x3733, 0x00, 10)               # POS_FollowingErrorTime
   Sp(0x373b, 0x00, 10)               # POS_PositionWindowTime
   Sp(0x3003, 0x00, 7)                 # Position Mode



# Main program ================================================================

# Main loop -------------------------------------------------------------------
counter = 0
while 1:
   CheckError()                              # Error check at each loop cycle
   CheckInputs()                             # Check of the digital inputs at each loop cycle

   counter = counter + 1
   if counter == 5000:
      Cmd =  CMD_BIT_DIN3

   if counter == 10000:
      counter = 0 # restart
      Cmd =  CMD_BIT_DIN1


   if State == STATE_Init:
      InitPars()
      NextState(STATE_Idle)

   #---------------------------------------------------------------------------
   elif State == STATE_Idle:

      if Cmd != LastCmd:
         if Cmd == CMD_BIT_DIN2:
            NextState(STATE_StartHoming)     # Homing starten
            LastCmd = Cmd
         if Cmd == CMD_BIT_DIN3:
            NextState(STATE_Move2Pos1)        # Positionierung CW starten
            LastCmd = Cmd
         if Cmd == CMD_BIT_DIN1:
            NextState(STATE_Move2Pos2)        # Positionierung CCW starten
            LastCmd = Cmd

   #---------------------------------------------------------------------------
   elif State == STATE_Move2Pos1:
      Sp(0x3004,0, 1)                        # Endstufe aktivieren
      Sp(0x3000,1,0)                         # Gerätekommando - Ausführbar bei Änderung - Togglekommando
      Sp(0x3000,0x10, 777)                  # Gerätekommando - Daten0 - Geschwindigkeit
      Sp(0x3000,0x11, 222)                   # Gerätekommando - Daten1 - Zielposition
      Sp(0x3000,1,0x34)                      # Gerätekommando - Ausführbar bei Änderung - CMD_Movr
      NextState(STATE_Wait4PosReached)

   #---------------------------------------------------------------------------
   elif State == STATE_Move2Pos2:
      Sp(0x3004,0, 1)                        # Endstufe aktivieren
      Sp(0x3000,1,0)                         # Gerätekommando - Ausführbar bei Änderung - Togglekommando
      Sp(0x3000,0x10, 999)                  # Gerätekommando - Daten0 - Geschwindigkeit
      Sp(0x3000,0x11, -222)                 # Gerätekommando - Daten1 - Zielposition
      Sp(0x3000,1,0x34)                      # Gerätekommando - Ausführbar bei Änderung - CMD_Movr
      NextState(STATE_Wait4PosReached)

   #---------------------------------------------------------------------------
   elif State == STATE_Wait4PosReached:
      if Gp(0x3002,0) & (1<<4):              # Target position reached
         Cmd = 0                             # Cmd zurücksetzen damit neuer Befehl empfangen werden kann
         LastCmd = 0                         # LastCmd zurücksetzen damit neuer Befehl empfangen werden kann
         NextState(STATE_Idle)
   #---------------------------------------------------------------------------
   elif State == STATE_Error:
      if Gp(0x3002,0) & (1<<4):              # Target position reached
         Cmd = 0                             # Cmd zurücksetzen damit neuer Befehl empfangen werden kann
         LastCmd = 0                         # LastCmd zurücksetzen damit neuer Befehl empfangen werden kann
         NextState(STATE_Idle)

   #---------------------------------------------------------------------------

   elif State == STATE_Error:
      error = Gp(0x3001,0)
      if error == 0:
         NextState(STATE_Idle)
      # Command evaluation -----------------------------------------------------
      else:
         Sp(0x3004,0, 0)                     # Disable power stage
         if (Cmd != LastCmd) and (Cmd == CMD_BIT_ClearError):
            Sp(0x3000,0,1)                   # Clear error
            LastCmd = Cmd                    # Retry until solved ...
