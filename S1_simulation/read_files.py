import xml.etree.ElementTree as ET
from collections import defaultdict
import math
import numpy as np
import awkward as ak
from data_handle.tools import get_pTT_id,get_module_id


def get_pTT_id_bis(Sector, S1Board, CEECEH, x):
    eta = x[x.find('eta')+3]
    if x[x.find('eta')+4] != '-':
        eta += x[x.find('eta')+4]
    phi = x[x.find('phi')+3]
    if x[x.find('phi')+4] != '*':
        phi += x[x.find('phi')+4]
    eta = int(eta)
    phi = int(phi)
    S1Board = (int(S1Board[4],16)*16 + int(S1Board[5],16)) & 0x3F
    return get_pTT_id(Sector, S1Board, CEECEH,eta,phi)
    
def get_moduleCEE(x,Sector):
    start_cursor = 0
    end_cursor = x[start_cursor:].find(',') + start_cursor
    layer = int(x[start_cursor:end_cursor])
    start_cursor = x[end_cursor+1].find(',') + end_cursor + 1 +1
    end_cursor = x[start_cursor:].find(',') + start_cursor
    type = x[start_cursor:end_cursor]
    start_cursor = x[end_cursor+1].find(',') + end_cursor + 1 +1
    end_cursor = x[start_cursor:].find(',') + start_cursor
    u = int(x[start_cursor:end_cursor])
    start_cursor = x[end_cursor+1].find(',') + end_cursor + 1 +1
    v = int(x[start_cursor:])
    module_id = get_module_id(Sector, layer, u, v)
    if type == 'Si': type = 'silicon'
    if type == 'Sc': type = 'scintillator'    
    return(module_id,layer,type,u,v)
                                                                                                                                                 

def get_moduleCEH(x,Sector):
    start_cursor = 0
    end_cursor = x[start_cursor:].find(',') + start_cursor
    layer = int(x[start_cursor:end_cursor])
    start_cursor = x[end_cursor+1].find(',') + end_cursor + 1 +1
    end_cursor = x[start_cursor:].find(',') + start_cursor
    type = x[start_cursor:end_cursor]
    start_cursor = x[end_cursor+1].find(',') + end_cursor + 1 +1
    end_cursor = x[start_cursor:].find(',') + start_cursor
    u = int(x[start_cursor:end_cursor])
    start_cursor = x[end_cursor+1].find(',') + end_cursor + 1 +1
    end_cursor = x[start_cursor:].find(',') + start_cursor
    v = int(x[start_cursor:end_cursor])
    start_cursor = x[end_cursor+1].find(',') + end_cursor + 1 +1
    stc_idx = int(x[start_cursor:])
    module_id = get_module_id(Sector, layer, u, v)
    if type == 'Si': type = 'silicon'
    if type == 'Sc': type = 'scintillator'
    return(module_id,layer,type,u,v,stc_idx)


def read_pTT(x,S1Board,CEECEH,Sector):
    if CEECEH==0:
        pTT = {'pTT' :get_pTT_id_bis(Sector,S1Board,CEECEH,x), 'Modules':[]}
    if CEECEH==1:
        pTT = {'pTT' :get_pTT_id_bis(Sector,S1Board,CEECEH,x), 'STCs':[]}
    cursor = x.find('\t')+1
    nb_module = int(x[cursor])
    for k in range(nb_module): 
        start_module = x[cursor:].find('(') +1 +cursor
        end_module = x[cursor:].find(')')  +cursor
        energy = x[end_module+1:end_module+1+x[end_module+1:].find(',')]
        if CEECEH==0:
            module_id,layer,type,u,v = get_moduleCEE(x[start_module: end_module],Sector)
            pTT['Modules'].append({'module_id' : module_id,'module_type' : type, 'module_layer' : layer,'module_u' : u,'module_v' : v,'module_energy' : int(energy)})
        if CEECEH==1:
            module_id,layer,type,u,v,stc_idx = get_moduleCEH(x[start_module: end_module],Sector) #,stc_idx
            pTT['STCs'].append({'module_id' : module_id,'module_type' : type,'module_layer' : layer,'module_u' : u,'module_v' : v,'stc_idx': stc_idx ,'stc_energy' : int(energy)}) 
        cursor = end_module+2+x[end_module+2:].find('(')
    return(pTT)
        
def read_build_pTTs(args,Sector):
    Edges = args.Edges
    pTT_version = args.pTT_version
    if Edges == 'yes':
        fCEE = open('config_files/build_pTTs/'+pTT_version+'/28_phi_bins/CE_E_allBoards.txt', 'r')
        data_CEE = fCEE.readlines()
        fCEE.close()
        fCEH = open('config_files/build_pTTs/'+pTT_version+'/28_phi_bins/CE_H_allBoards.txt', 'r')
        data_CEH = fCEH.readlines()
        fCEH.close()
    if Edges == 'no':
        fCEE = open('config_files/build_pTTs/'+pTT_version+'/24_phi_bins/CE_E_allBoards.txt', 'r')
        data_CEE = fCEE.readlines()
        fCEE.close()
        fCEH = open('config_files/build_pTTs/'+pTT_version+'/24_phi_bins/CE_H_allBoards.txt', 'r')
        data_CEH = fCEH.readlines()
        fCEH.close()
    pTTs_CEE = []
    for x in data_CEE:
        if x[0:5] == 'Board':
            S1Board = x[6:16]
        if x[0:6] == '/* out':
            pTTs_CEE.append(read_pTT(x,S1Board,0,Sector))
    pTTs_CEH = []
    for x in data_CEH:
        if x[0:5] == 'Board':
            S1Board = x[6:16]
        if x[0:6] == '/* out':
            pTTs_CEH.append(read_pTT(x,S1Board,1,Sector))
    return(pTTs_CEE,pTTs_CEH)
