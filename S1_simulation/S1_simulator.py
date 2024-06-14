import numpy as np
from S1_simulation.TCs_to_pTTs import add_TCs
from S1_simulation.TS_to_pTTs import build_pTTsCEE,build_pTTsCEH
from S1_simulation.read_files import read_build_pTTs
from ECONT.read_nb_selected_TCs import get
from collections import defaultdict



def create_pTTs(event,args,Sector):
    file_CEE,file_CEH = read_build_pTTs(args.Edges,Sector)
    print(file_CEE)
    print(file_CEH)
    if args.Scenario == 'TS': ts = event.ds_ts
    if args.Scenario == 'unselected_TS': ts = event.ds_unselected_ts
    pTTs_CEE = build_pTTsCEE(ts, args, file_CEE)
    pTTs_CEH = build_pTTsCEE(ts, args, file_CEH) #wihtout STCs
    if args.Scenario == 'unselected_TS': 
        nb_selected_TCs = get()
        pTTs_CEE = add_TCs(pTTs_CEE,event.ds_si,nb_selected_TCs, Sector,'CEE')
        pTTs_CEH = add_TCs(pTTs_CEH,event.ds_si,nb_selected_TCs, Sector,'CEH')
    if Sector == args.Sector:
        event.ds_pTTsCEE = pTTs_CEE
        event.ds_pTTsCEH = pTTs_CEH
    if Sector != args.Sector:
        event.ds_pTTsdupCEE = pTTs_CEE
        event.ds_pTTsdupCEH = pTTs_CEH
        
