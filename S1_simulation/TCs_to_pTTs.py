import numpy as np
from data_handle.tools import getuvsector,get_module_id
from collections import defaultdict


def add_TCs(pTTs,TCs,nb_selected_TCs, Sector,CEECEH):
    energytoadd= defaultdict(list)
    for module_idx in range(len(TCs.good_tc_layer)):
        if ((TCs.good_tc_layer[module_idx][0] < 27) and (CEECEH == 'CEE' )) or ((TCs.good_tc_layer[module_idx][0] >= 27) and (CEECEH == 'CEH' )):
            u,v,sector = getuvsector(TCs.good_tc_layer[module_idx][0],
                                        TCs.good_tc_waferu[module_idx][0],
                                        TCs.good_tc_waferv[module_idx][0])
            module = get_module_id(Sector, TCs.good_tc_layer[module_idx][0], u, v)
            if sector == Sector:
                for idx in range(min(len(nb_selected_TCs[module]),len(TCs.good_tc_layer[module_idx]))):
                    eta,phi = getetaphi(TCs.good_tc_phi[module_idx][idx] - Sector*2/3 *np.pi ,TCs.r_over_z[module_idx][idx])
                    S1Board_idx = S1Board(TCs.good_tc_layer[module_idx][idx])
                    if CEECEH == 'CEE': a = 0
                    if CEECEH == 'CEH': a = 1
                    pTT = get_pTT_id(Sector, S1Board_idx, a, eta,phi)
                    energytoadd[pTT].append(TCs.good_tc_pt[module_idx][idx])
    for pTT_idx in range(len(pTTs)):
        pTT = pTTs[pTT_idx]['pTT_id']
        for TC_idx in range(len( energytoadd[pTT])):
            pTTs[pTT_idx]['energy'] += energytoadd[pTT][TC_idx]
        
    return pTTs




def getetaphi(phi,roverz):
    teta = np.arctan(roverz)
    eta = -np.log(np.tan(teta/2))
    eta = int((eta-1.305)/(np.pi/36)) #1.305 offset
    phi = int((phi+ (15*np.pi/180))/(np.pi/36) ) # -15° offset
    return(eta,phi)
    
def S1Board(layer):
    S1_Boards =[[3, 34], [1, 36, 47], [33, 40, 41], [9, 39, 44], [7, 42, 43], [13, 38, 46], [17, 27], [25, 31], [23, 30], [15, 32], [19, 29], [21, 28], [5, 35], [11, 37, 45]]
    for S1board_idx in range(len(S1_Boards)) :
        if layer in S1_Boards[S1board_idx]:
            return(S1board_idx)
