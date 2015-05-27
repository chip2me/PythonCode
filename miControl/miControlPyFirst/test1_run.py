# -*- coding: iso-8859-1 -*-
from mc.pymc import Run

m = Run(node_id       = 1,                            # CANopen node address of the device
        prg_filename  = "test1.py",                   # File name of the MPU2 program
        mpu_filename  = None,                         # Optional file name of a compiled MPU2 program
        store         = True,                         # True = MPU2 program is stored in the device after transmission
        start         = True,                         # True = MPU2 program is started in the device after transmission
        dump          = 2)                            # dump Bit 0 = Compiled code of the MPU2 program is displayed
                                                      #      Bit 1 = Global variables are displayed
                                                      #      Bit 2 = Internal program labels are displayed