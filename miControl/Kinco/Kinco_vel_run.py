# -*- coding: iso-8859-1 -*-
from mc.pymc import Run
from mc.display import *

m = Run(node_id       = 1,                            # CANopen node address of the device
        prg_filename  = "Kinco_vel.py",                   # File name of the MPU2 program
        mpu_filename  = None,                         # Optional file name of a compiled MPU2 program
        store         = True,                         # True = MPU2 program is stored in the device after transmission
        start         = True,                         # True = MPU2 program is started in the device after transmission
        dump          = 2)                            # dump Bit 0 = Compiled code of the MPU2 program is displayed
                                                      #      Bit 1 = Global variables are displayed
                                                      #      Bit 2 = Internal program labels are displayed
# Request or change of the variables of the MPU2 program.
# m.GlobalVars contains all variables of the MPU2 program.
if m:
   d = m.Dev                                       # d = Dsa instance
   t = Display(d)

   # Prepare texts and store them in the device                                              # txt_nr for DispPrintTxt
   # In the MPU program, these texts are called via DispPrintTxt.
   t.AddText( "miControl - DEMO" )                                                           # 0
#   t.AddText(("Counter  = %-6ld",  m.GlobalVars.Counter))      # (Text, [Output parameter])  # 1
#   t.AddText(("Counter2 = %ld.%ld", m.GlobalVars.Integer, m.GlobalVars.Fraction))            # 2
#   t.AddText(("Position = %-6ld",  m.GlobalVars.ActEncPos))                                  # 3
#   t.AddText(("Buttons  = %-6ld",  m.GlobalVars.Buttons))                                    # 4
   #t.AddText(("Sidste tilstand = %d",  m.LastState))
   #t.AddText(("Aktiv tilstands  = %d",  m.State))                                    # 4
   t.AddText( "Hello World" )                                    # 4

   t.StoreTexts()                                  # Stores the predefined texts in the device
   m.Prg.Start()                                   # Starts the MPU program