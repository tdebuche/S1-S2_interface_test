import numpy as np
import awkward as ak
import uproot
import math
import yaml
import os
import argparse
import numpy as np

from data_handle.event import provide_events
from S1_simulation.S1_simulator import create_pTTs
from S1_packer.TC_packer import _TC_packer
from S1_packer.pTT_packer import _pTT_packer
from S1_packer.create_EMP import createEMPfile
from S2_unpacker.plot_TTs import record_plot
from S2_unpacker.plot_TTs import plot_EMPfile

parser = argparse.ArgumentParser(description='S1-S2_interface_test Parameters')

#version to test
parser.add_argument('--pTT_version', default='v3', help='pTT version to test')

#event type
parser.add_argument('-n',          type=int, default=1,         help='Provide the number of events')
parser.add_argument('--particles', type=str, default='photons', help='Choose the particle sample')
parser.add_argument('--pileup',    type=str, default='PU0',     help='Choose the pileup - PU0 or PU200')

#On scenarios 
parser.add_argument('--Scenario', type=str, default='TS', help='Choose TS or unselected_TS')
parser.add_argument('--Sector',      type=int, default=0, help='Sector of S2 Board, only the sector 0 works')
parser.add_argument('--Edges',   default = 'yes', help='20*24 or 20*28 bins')


#plot from EMP
parser.add_argument('--read_EMP',   default = 'no', help='plot with EMPfile')

args = parser.parse_args()




#plot EMP
if args.read_EMP == "yes":
  args.n = 0 
  plot_EMPfile(args,"Results/EMPfiles/EMP_S2_board_0.txt.txt")

events = provide_events(args,args.n, args.particles, args.pileup)

#TS are created automatically


for idx, event in enumerate(events):
  
  #create pTTs
  create_pTTs(event,args,0)
  create_pTTs(event,args,1)


  #packing
  _TC_packer(event,args)
  _pTT_packer(event,args)
  
  #createEMPfile
  createEMPfile(event)
  
  #unpack and plot
  record_plot(event,args,'pTT_event'+str(idx))


    
