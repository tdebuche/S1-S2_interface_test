import numpy as np
from S1_simulation.TCs_to_pTTs import add_TCs
from S1_simulation.TS_to_pTTs import build_pTTsCEE,build_pTTsCEH
from S1_simulation.read_files import read_build_pTTs
from ECONT.read_nb_selected_TCs import get
from collections import defaultdict



def create_pTTs(event,args,Sector):
    file_CEE,file_CEH = read_build_pTTs(args,Sector)
    if args.Scenario == 'TS': ts = event.ds_ts
    if args.Scenario == 'unselected_TS': ts = event.ds_unselected_ts
    STCs = event.ds_stc
    pTTs_CEE = build_pTTsCEE(ts, args, file_CEE)
    #print(pTTs_CEE)
    pTTs_CEH = build_pTTsCEH(STCs, args, file_CEH) 
    #print(pTTs_CEH)
    if args.Scenario == 'unselected_TS': 
        nb_selected_TCs = get()
        pTTs_CEE = add_TCs(pTTs_CEE,event.ds_si,nb_selected_TCs, Sector,'CEE')
        #pTTs_CEH = add_TCs(pTTs_CEH,event.ds_si,nb_selected_TCs, Sector,'CEH')

    event.ds_pTTs['CEE']['Sector'+str(Sector)] = pTTs_CEE
    event.ds_pTTs['CEH']['Sector'+str(Sector)] = pTTs_CEH
        
