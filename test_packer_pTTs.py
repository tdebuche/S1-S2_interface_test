import numpy as np
import awkward as ak
import uproot
import math
import yaml
import os
import argparse
import numpy as np

from data_handle.event_pTT import provide_events

parser = argparse.ArgumentParser(description='Stage-2 Emulator Parameters')
parser.add_argument('-n',          type=int, default=1,         help='Provide the number of events')
parser.add_argument('--particles', type=str, default='photons', help='Choose the particle sample')
parser.add_argument('--pileup',    type=str, default='PU0',     help='Choose the pileup - PU0 or PU200')
parser.add_argument('--plot',        action='store_true', help='Create plots')
parser.add_argument('--col',         action='store_true', help='Create plots using column numbers')
parser.add_argument('--phi',         action='store_true', help='Create plots using phi coordinates')
parser.add_argument('--performance', action='store_true', help='Create performance plots: distance gen_particle/max_TC')
parser.add_argument('--thr_seed',    action='store_true', help='Create efficiency plots post seeding')
parser.add_argument('--cl_energy',   action='store_true', help='Create plot of gen_pt vs recontructed energy')
parser.add_argument('--Sector',      type=int, default=0, help='Sector of S2 Board')
parser.add_argument('--Edges',   default = 'yes', help='20*24 or 20*28 bins')

args = parser.parse_args()
print('ok')
events = provide_events(args.n, args.particles, args.pileup)
print('ok event')
for idx, event in enumerate(events):
  #print(str(idx))
  #event._data_packer(args, xml_data, xml_MB)
  #print(event.data_packer)
  print(event.ds_ts)
  print(event.ds_unselected_ts )
  #print(event.data_packer)
  #print(event.phi_gen)
  #print(event.eta_gen)
  #print(event.pTT_packer)
  #event.provide_ts(args)
  #print(event.pTT_packer)
  #print(event.ds_ts)
  #print(xml_plot)
  record_plot(event,xml_plot,args,'pTT_event'+str(idx))
  #createEMPfile(event)
    
