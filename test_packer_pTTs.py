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

parser = argparse.ArgumentParser(description='Stage-2 Emulator Parameters')
parser.add_argument('-n',          type=int, default=1,         help='Provide the number of events')
parser.add_argument('--particles', type=str, default='photons', help='Choose the particle sample')
parser.add_argument('--Scenario', type=str, default='TS', help='Choose TS or unselected_TS')
parser.add_argument('--pileup',    type=str, default='PU0',     help='Choose the pileup - PU0 or PU200')
parser.add_argument('--Sector',      type=int, default=0, help='Sector of S2 Board')
parser.add_argument('--Edges',   default = 'yes', help='20*24 or 20*28 bins')

args = parser.parse_args()


events = provide_events(args.n, args.particles, args.pileup)

#TS are created automatically

for idx, event in enumerate(events):
  #create pTTs
  create_pTTs(event,args,0)
  create_pTTs(event,args,1)

  #packing



  #print(event.pTT_packer)
  #event.provide_ts(args)
  #print(event.pTT_packer)
  #print(event.ds_ts)
  #print(xml_plot)
  #createEMPfile(event)
    
