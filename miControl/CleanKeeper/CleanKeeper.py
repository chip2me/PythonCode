# -*- coding: iso-8859-1 -*-
#*===========================================================================*#
#*        Copyright (c) 1997-2013 by miControl. All rights reserved.         *#
#*                                                                           *#
#* File     : CleanKeeper.py                                                       *#
#*                                                                           *#
#* Project  : mPLC                                                           *#
#* System   : MPU2                                                           *#
#* Version  : 1.00                                                           *#
#* Company  : GCM A/S                                                        *#
#*                                                                           *#
#* Author   : Carsten Mols             mailto:cm@gearcentralene.dk           *#
#* Date     : 08.08.2015                                                     *#
#*---------------------------------------------------------------------------*#
#* Customer : CleanKeeper                                                    *#
#* Name     : Torben Bloch P                                                 *#
#* OrderNr. :                                                                *#
#* Descr.   : Brush application. 20 seconds CW/CCW.                          *#
#*                                                                           *#
#* History  : 8. August 2015: Tuning and run created                         *#
#*===========================================================================*#

from mc.dsa import *
from pi_curr_betragsoptimum import CalcCurrKpKi
import time




#-----------------------------------------------------------------------------
# Inputdata:
# insert the coorect data according to the steppermotor which is in use

NodeId         = 127       # CAN NodeId of the device
Up             = 24.0      # Power supply Voltage [V]

                           # Motor:
L              = 2*11.5E-3 # Motor-inductance [H]
R              = 28.2      # Motor-resistance [Ohm]

MotPolN        = 200       # Number of fullsteps per round

Microsteps     = 256       # 256 (default), 128, 64, 32, 16, 8, 4, 2, 1
Vel            = 100       # velocitiy [rpm]

Pos         = Microsteps*MotPolN*10

TunningCurrent = 300
CurrKvff       = 0

#-----------------------------------------------------------------------------
def GetAvgCurrFollowingError (n=16):
   curr = 0
   for i in xrange(n):
      curr += d.CurrFollowingError()
   return curr/n

def GetMaxCurrFollowingError (n=32):
   curr = 0
   for i in xrange(n):
      c = abs(d.CurrFollowingError())
      if c > curr:
         curr = c
   return curr

def GetAvgCurr (n = 16):
   curr = 0
   for i in xrange(n):
      curr += d.ActCurr()
   return curr/n

def StepperTunning (curr = 300):
   kp,ki = CalcCurrKpKi(l_H=L, r_Ohm=R, up_V=Up, tsamp_s=100E-6, fpwm_Hz=50E3)

   kp /= 5
   ki /= 5

   d.Disable()
   d.ClearError()

   d.SdoWr(0x3910,1, 1)                # MotMicrosteps = Fullstep

   d.ModePos()
   d.Curr(curr)

   d.CurrKp(100)
   d.CurrKi(100)

   d.SdoWr(0x3214,0, 0)                # Kvff
   d.SdoWr(0x3215,0, 0)                # Kaff = R_mOhm * 24000/Up_mV

   d.Vel(10)
   d.Enable()

   for p in xrange(4):
      time.sleep(0.100)
      if d.CmdCurr() > 0:
         break
      else:
         d.Movr(1)

   err = 0

   if abs(GetAvgCurrFollowingError()) > curr/2:
      print "ERROR: Motor coil not connected !"
      err = -1

   if not err:
      d.CurrKp(0)
      d.CurrKi(0)
      d.Disable()
      d.Enable()

      ok = False
      r  = 0
      dr = 100
      while not ok:
         d.SdoWr(0x3215,0, r)          # Kaff = R_mOhm * Up_mV/24000
         d.Mova(d.ActPos())
         r += dr
         fc = GetAvgCurrFollowingError()

         if fc < -(20*curr/100):
            err = -2
            break

         if fc < (5*curr/100):
            ok = True

   d.Disable()

   return err,kp,ki,r

#-----------------------------------------------------------------------------
#Motor data for MotoSmart 23
def InitPar ():
   print "PREinit"
   d.SdoWr(0x3004, 0x00, 0)                # DEV_Enable - Disable
   d.SdoWr(0x3000, 0x00, 0x1)              # DEV_Cmd - Clear error
   d.SdoWr(0x3000, 0x00, 0x82)             # DEV_Cmd - Default parameter
   #d.SdoWr(0x3003, 0x00, 7)                # DEV_Mode
   d.SdoWr(0x3900, 0x00, 2)                # MOTOR_Type
   d.SdoWr(0x3911, 0x00, 0)                # MOTOR_Polarity
   d.SdoWr(0x3910, 0x00, 200)              # MOTOR_PolN
   d.SdoWr(0x3901, 0x00, 3000)             # MOTOR_Nn
   d.SdoWr(0x3902, 0x00, 24000)            # MOTOR_Un
   d.SdoWr(0x3350, 0x00, 0x0)              # VEL_Feedback
   d.SdoWr(0x3221, 0x00, 10000)            # CURR_LimitMaxPos
   d.SdoWr(0x3223, 0x00, 10000)            # CURR_LimitMaxNeg
   d.SdoWr(0x3210, 0x00, 682)              # CURR_Kp
   d.SdoWr(0x3211, 0x00, 64)               # CURR_Ki
   d.SdoWr(0x3214, 0x00, 400)              # PAR_3214.00h
   d.SdoWr(0x3215, 0x00, 4000)             # PAR_3215.00h
   d.SdoWr(0x3910, 0x01, 256)              # PAR_3910.01h
   d.SdoWr(0x3004, 0x00, 1)                # DEV_Enable
   print "post init"



d = Dsa(NodeId)

print "Start..."
err,kp,ki,r, = StepperTunning(curr=TunningCurrent)

if not err:
   d.CurrKp(kp)
   d.CurrKi(ki)

   d.SdoWr(0x3214,0, CurrKvff)         # Kvff
   d.SdoWr(0x3215,0, r)                # Kaff = R_mOhm * 24000/Up_mV

   d.SdoWr(0x3910,0, MotPolN)          # MotPolN
   d.SdoWr(0x3910,1, Microsteps)       # MotMicrosteps

   print "Values of Parameters:"
   print "   CURR_Kp           (0x3210.0) =", kp
   print "   CURR_Ki           (0x3211.0) =", ki
   print "   CURR_Kvff         (0x3214.0) =", CurrKvff
   print "   CURR_Kaff         (0x3215.0) =", r
   print "   MOTOR_PolN        (0x3910,0) =", MotPolN
   print "   MOTOR_Microstepsd (0x3910,1) =", Microsteps
   print "Done"
   InitPar()


#-----------------------------------------------------------------------------
# driving test
if 1 and not err:
   d.Disable()
   d.PrintInfos()

   d.ClearError()
   d.ModePos()
   d.Curr(300)

   d.VelAcc_dV(1000)
   d.VelAcc_dT(1000)

   d.VelDec_dV(1000)
   d.VelDec_dT(1000)

   d.Vel(Vel)
   d.Enable()


   #- assistance functions --------------------------------------------------------
   def _mov (d, vel, pos, rel=False):
      d.SdoWr(0x3300,0, vel)           # Vel

      if rel:
         d.SdoWr(0x3791,0, pos)        # Movr
      else:
         d.SdoWr(0x3790,0, pos)        # Mova

      reached = False

      while not reached:
         status = d.SdoRd(0x3002,0)
         if status & (1<<4):           # Target reached ?
            reached = True
         elif status & (1<<1):         # Error ?
            # insert steps to correct error here
            break

      return reached

   def Mova (d, vel, pos):
      return _mov(d, vel, pos, False)

   def Movr (d, vel, pos):
      return _mov(d, vel, pos, True)


   def MovCW ():
      Movr(d, 55, 512000)
      print "CW #", ButtonRead


   def MovCCW ():
      Movr(d, 55, -512000)
      print "CCW #", ButtonRead


   # Read dig input buttons --------------------------------------------
   def ReadButtons():
      bButton = d.SdoRd(0x3120,0)                                 # Read the state of the digital inputs
      return bButton


   #- mainloop ----------------------------------------------------------
   IdleCount = 0
   IdleCountOld = 0
   bReadyCW = 1
   bReadyCCW = 1

   while 1:
      ButtonRead = ReadButtons()

      if ButtonRead == 1 and bReadyCW:
         MovCW()
         bReadyCW = 0
         bReadyCCW = 1
         IdleCount = 0

      if ButtonRead == 2 and bReadyCCW:
         MovCCW()
         bReadyCCW = 0
         bReadyCW = 1
         IdleCount = 0

      if ButtonRead == 0:
         IdleCount = IdleCount +1
         time.sleep(0.2)
         print "Idle #", IdleCount
         if IdleCount > 2:
            bReadyCCW = 1
            bReadyCW = 1

