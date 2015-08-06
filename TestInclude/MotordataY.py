
def Sp(x, y, z):
   print "x=", x, "y=", y, "z=", z

def MotorVars():
   #Motor data for MotoSmart 23
   Sp(0x3900, 0x00, 2)                # MOTOR_Type
   Sp(0x3911, 0x00, 0)                # MOTOR_Polarity
   Sp(0x3910, 0x00, 200)              # MOTOR_PolN
   Sp(0x3901, 0x00, 3000)             # MOTOR_Nn
   Sp(0x3902, 0x00, 12000)            # MOTOR_Un
   Sp(0x3350, 0x00, 0x0)              # VEL_Feedback
   Sp(0x3221, 0x00, 10000)            # CURR_LimitMaxPos
   Sp(0x3223, 0x00, 10000)            # CURR_LimitMaxNeg
   Sp(0x3210, 0x00, 682)              # CURR_Kp
   Sp(0x3211, 0x00, 64)               # CURR_Ki
   Sp(0x3314, 0x00, 1000)             # VEL_Kvff
   Sp(0x3830, 0x00, 32000)            # PWM_Frequency
   Sp(0x3214, 0x00, 400)              # PAR_3214.00h
   Sp(0x3215, 0x00, 4000)             # PAR_3215.00h
   Sp(0x3910, 0x01, 256)              # PAR_3910.01h
   

def data(test):
	MotorVars()
   

		