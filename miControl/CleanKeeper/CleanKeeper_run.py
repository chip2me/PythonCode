# -*- coding: iso-8859-1 -*-
from mc.pymc import Run
from mc.display import *
from mc.dsa import *
from pi_curr_betragsoptimum import CalcCurrKpKi

m = Run(node_id       = 127,                            # CANopen node address of the device
        prg_filename  = "CleanKeeper_mpu_state_machine.py",                   # File name of the MPU2 program
        mpu_filename  = None,                         # Optional file name of a compiled MPU2 program
        store         = True,                         # True = MPU2 program is stored in the device after transmission
        start         = True,                         # True = MPU2 program is started in the device after transmission
        dump          = 2)                            # dump Bit 0 = Compiled code of the MPU2 program is displayed
                                                      #      Bit 1 = Global variables are displayed
                                                      #      Bit 2 = Internal program labels are displayed


                                                      #      Bit 2 = Internal program labels are displayed