#- assistance functions --------------------------------------------------------
def Mov (vel, pos, rel=False):
   Sp(0x3300,0, vel)           # Vel
   
   if rel:
      Sp(0x3791,0, pos)        # Movr
   else:
      Sp(0x3790,0, pos)        # Mova
   
   reached = False
   
   while not reached:
      status = Gp(0x3002,0)
      if status & (1<<4):           # Target reached ?
         reached = True
      elif status & (1<<1):         # Error ?
         # insert steps to correct error here
         break

   return reached

def Mova (vel, pos):
   return Mov(vel, pos, False)

def Movr (vel, pos):
   return Mov(vel, pos, True)


def MovCW ():
   Movr(55, 512000)
   #print "CW #", ButtonRead


def MovCCW ():
   Movr(55, -512000)
   #print "CCW #", ButtonRead


# Read dig input buttons --------------------------------------------
def ReadButtons():
   bButton = Gp(0x3120,0)                                 # Read the state of the digital inputs
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
      Delay(200)
      #print "Idle #", IdleCount
      if IdleCount > 2:
         bReadyCCW = 1
         bReadyCW = 1
