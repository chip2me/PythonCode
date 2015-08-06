# -*- coding: iso-8859-1 -*-
import mc, time

PYMC         = 0
PYMC_VERSION = 0x00000000
MPU2         = 0
MPU2_VERSION = 0x00000000

_SpGp_NodeId    = 1
_SpGp_Timeout   = 0xFFFF
_SpGp_TxCobId   = 0xFFFFFFFF
_SpGp_RxCobId   = 0xFFFFFFFF

_SpxGpx_NodeId  = 1
_SpxGpx_Timeout = 0xFFFF
_SpxGpx_TxCobId = 0xFFFFFFFF
_SpxGpx_RxCobId = 0xFFFFFFFF

#------------------------------------------------------------------------------
def Sp (index, subindex, value):
   global _SpGp_NodeId, _SpGp_Timeout, _SpGp_TxCobId, _SpGp_RxCobId
   mc.Can.SdoWr(_SpGp_NodeId, index, subindex, value, _SpGp_Timeout, _SpGp_TxCobId, _SpGp_RxCobId)

def Gp (index, subindex):
   global _SpGp_NodeId, _SpGp_Timeout, _SpGp_TxCobId, _SpGp_RxCobId
   return mc.Can.SdoRd(_SpGp_NodeId, index, subindex, _SpGp_Timeout, _SpGp_TxCobId, _SpGp_RxCobId)

def SpGp_NodeId (node_id):
   global _SpGp_NodeId
   _SpGp_NodeId = node_id

def SpGp_Timeout (time_ms):
   global _SpGp_Timeout
   _SpGp_Timeout = time_ms

def SpGp_TxCobId (tx_cob_id):
   global _SpGp_TxCobId
   _SpGp_TxCobId = tx_cob_id

def SpGp_RxCobId (rx_cob_id):
   global _SpGp_RxCobId
   _SpGp_RxCobId = rx_cob_id

#------------------------------------------------------------------------------
def Spx (a1, a2, a3, a4=None):
   global _SpxGpx_NodeId, _SpxGpx_Timeout, _SpxGpx_TxCobId, _SpxGpx_RxCobId

   if a4 == None:                   # Form1:  Spx (index, subindex, value)
      node_id  = _SpxGpx_NodeId
      index    = a1
      subindex = a2
      value    = a3
   else:                            # Form2: Spx (node_id, index, subindex, value)
      node_id  = a1
      index    = a2
      subindex = a3
      value    = a4

   mc.Can.SdoWr(node_id, index, subindex, value, _SpxGpx_Timeout, _SpxGpx_TxCobId, _SpxGpx_RxCobId)

def Gpx (a1, a2, a3=None):
   global _SpxGpx_NodeId, _SpxGpx_Timeout, _SpxGpx_TxCobId, _SpxGpx_RxCobId

   if a3 == None:                   # Form1: Gpx (index, subindex)
      node_id  = _SpxGpx_NodeId
      index    = a1
      subindex = a2
   else:                            # Form2: Gpx (node_id, index, subindex)
      node_id  = a1
      index    = a2
      subindex = a3

   return mc.Can.SdoRd(node_id, index, subindex, _SpxGpx_Timeout, _SpxGpx_TxCobId, _SpxGpx_RxCobId)

def SpxGpx_NodeId (node_id):
   global _SpxGpx_NodeId
   _SpxGpx_NodeId = node_id

def SpxGpx_Timeout (time_ms):
   global _SpxGpx_Timeout
   _SpxGpx_Timeout = time_ms

def SpxGpx_TxCobId (tx_cob_id):
   global _SpxGpx_TxCobId
   _SpxGpx_TxCobId = tx_cob_id

def SpxGpx_RxCobId (rx_cob_id):
   global _SpxGpx_RxCobId
   _SpxGpx_RxCobId = rx_cob_id

#------------------------------------------------------------------------------
def Delay (time_ms):
   time.sleep(time_ms/1000.0)

def Clock ():
   return int(time.clock()*1000)

def DiffClock (timestamp):
   return int(Clock()-int(timestamp))

#------------------------------------------------------------------------------
def Boost (steps=10):
   pass

def MpuSet (nr,value):
   pass

def MpuGet (nr):
   return 0
