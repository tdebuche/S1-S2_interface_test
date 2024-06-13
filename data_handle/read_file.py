
import xml.etree.ElementTree as ET
from collections import defaultdict
import math
import numpy as np
import awkward as ak

################################################### ALLOCATION  #############################################################################
def read_allocation_pTTs(Edges,Sector,nb_links):
    if Edges == 'yes':
        if nb_links == 4:
            tree = ET.parse('config_files/pTTs/Sector'+str(Sector)+'/AllocationpTTsEdges.xml')
        if nb_links == 2:
            tree = ET.parse('config_files/pTTs/Sector'+str(Sector)+'/DuplicationpTTsEdges.xml')
    if Edges == 'no':
        if nb_links == 4:
            tree = ET.parse('config_files/pTTs/Sector'+str(Sector)+'/AllocationpTTsNoEdges.xml')
        if nb_links == 2:
            tree = ET.parse('config_files/pTTs/Sector'+str(Sector)+'/DuplicationpTTsNoEdges.xml')
        
    root = tree.getroot()
    reversed_data_pTT  = defaultdict(list)

    S1_index = 0
    for s1_element in root.findall('.//S1'):
        for channel_element in s1_element.findall('.//Channel'):
            channel = int(channel_element.get('aux-id'))
            for frame_element in channel_element.findall('.//Frame'):
                if all(attr in frame_element.attrib for attr in ['id','pTT']):
                    frame  = int(frame_element.get('id'))
                    pTT     = hex(int(frame_element.get('pTT'),16))
                    if nb_links == 4:
                        n_link = 14 + 14*math.floor(channel/2) + S1_index
                    if nb_links == 2:
                        if channel//2 == 4:
                            n_link =  S1_index
                        if channel//2 == 5:
                            n_link = 70 + S1_index
                    reversed_data_pTT[pTT].append({'frame'  : frame, 
                                                  'channel': channel, 
                                                  'n_link' : n_link,})

        S1_index += 1
    return reversed_data_pTT

################################################## BUILD PTTS ###########################################################################
def get_pTT_id(Sector, S1Board, CEECEH, x):
    eta = x[x.find('eta')+3]
    if x[x.find('eta')+4] != '-':
        eta += x[x.find('eta')+4]
    phi = x[x.find('phi')+3]
    if x[x.find('phi')+4] != '*':
        phi += x[x.find('phi')+4]
    eta = int(eta)
    phi = int(phi)
    S1Board = (int(S1Board[4],16)*16 + int(S1Board[5],16)) & 0x3F
    pTT_id = hex(0x00000000 | ((Sector & 0x3) << 29) | ((1 & 0x3) << 26)  | ((6 & 0xF) << 22) | ((S1Board & 0x3F) << 16) | ((CEECEH & 0x1) << 10) | ((eta & 0x1F) << 5) | ((phi & 0x1F) << 0))
    #while len(pTT_id) <10:
    #    pTT_id = '0x'+ str(0) +pTT_id[2:]
    return pTT_id
    
def get_moduleCEE(x,Sector):
    start_cursor = 0
    end_cursor = x[start_cursor:].find(',') + start_cursor
    layer = int(x[start_cursor:end_cursor])
    start_cursor = x[end_cursor+1].find(',') + end_cursor + 1 +1
    end_cursor = x[start_cursor:].find(',') + start_cursor
    u = int(x[start_cursor:end_cursor])
    start_cursor = x[end_cursor+1].find(',') + end_cursor + 1 +1
    v = int(x[start_cursor:])
    module_id = hex(0x00000000 | ((Sector & 0x3) << 29) | ((0 & 0x3) << 26)  | ((0 & 0xF) << 22) | ((layer & 0x3F) << 16) |  ((u & 0xF) << 12) | ((v & 0xF) << 8))
    #while len(module_id) <10:
    #    module_id = '0x'+ str(0) +module_id[2:]
    return(module_id,layer,u,v)
                                                                                                                                                 

def get_moduleCEH(x,Sector):
    start_cursor = 0
    end_cursor = x[start_cursor:].find(',') + start_cursor
    layer = int(x[start_cursor:end_cursor])
    start_cursor = x[end_cursor+1].find(',') + end_cursor + 1 +1
    end_cursor = x[start_cursor:].find(',') + start_cursor
    u = int(x[start_cursor:end_cursor])
    start_cursor = x[end_cursor+1].find(',') + end_cursor + 1 +1
    end_cursor = x[start_cursor:].find(',') + start_cursor
    v = int(x[start_cursor:end_cursor])
    start_cursor = x[end_cursor+1].find(',') + end_cursor + 1 +1
    stc = int(x[start_cursor:])
    module_id = hex(0x00000000 | ((Sector & 0x3) << 29) | ((0 & 0x3) << 26)  | ((0 & 0xF) << 22) | ((layer & 0x3F) << 16) |  ((u & 0xF) << 12) | ((v & 0xF) << 8))
    #while len(module_id) <10:
    #    module_id = '0x'+ str(0) +module_id[2:]
    return(module_id,layer,u,v,stc)


def read_pTT(x,S1Board,CEECEH,Sector):
    pTT = {'pTT' :get_pTT_id(Sector,S1Board,CEECEH,x), 'Modules':[]}
    cursor = x.find('\t')+1
    nb_module = int(x[cursor])
    for k in range(nb_module): 
        start_module = x[cursor:].find('(') +1 +cursor
        end_module = x[cursor:].find(')')  +cursor
        energy = x[end_module+2:end_module+2+x[end_module+2:].find(',')]
        if CEECEH==0:
            module_id,layer,u,v = get_moduleCEE(x[start_module: end_module],Sector)
            pTT['Modules'].append({'module_id' : module_id, 'module_layer' : layer,'module_u' : u,'module_v' : v,'module_energy' : int(energy)})
        if CEECEH==1:
            module_id,layer,u,v = get_moduleCEE(x[start_module: end_module],Sector) #,stc_idx
            pTT['Modules'].append({'module_id' : module_id,'module_layer' : layer,'module_u' : u,'module_v' : v,'module_energy' : int(energy)}) #'stc_idx': stc_idx ,
        cursor = end_module+2+x[end_module+2:].find('(')
    return(pTT)
        
def read_build_pTTs(Edges,Sector):
    if Edges == 'yes':
        fCEE = open('config_files/pTTs/Sector'+str(Sector)+'/CE_E_allBoards_Edges.txt', 'r')
        data_CEE = fCEE.readlines()
        fCEE.close()
        fCEH = open('config_files/pTTs/Sector'+str(Sector)+'/CE_H_allBoards_EdgesNoSTCs.txt', 'r')
        data_CEH = fCEH.readlines()
        fCEH.close()
    if Edges == 'no':
        fCEE = open('config_files/pTTs/Sector'+str(Sector)+'/CE_E_allBoards_NoEdges.txt', 'r')
        data_CEE = fCEE.readlines()
        fCEE.close()
        fCEH = open('config_files/pTTs/Sector'+str(Sector)+'/CE_H_allBoards_NoEdgesNoSTCs.txt', 'r')
        data_CEH = fCEH.readlines()
        fCEH.close()
    pTTs_CEE = []
    for x in data_CEE:
        if x[0:5] == 'Board':
            S1Board = x[6:16]
        if x[0] == '/':
            pTTs_CEE.append(read_pTT(x,S1Board,0,Sector))
    pTTs_CEH = []
    for x in data_CEH:
        if x[0:5] == 'Board':
            S1Board = x[6:16]
        if x[0] == '/':
            pTTs_CEH.append(read_pTT(x,S1Board,1,Sector))
    return(pTTs_CEE,pTTs_CEH)
    
