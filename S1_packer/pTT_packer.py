from collections import defaultdict
import numpy as np
import math
from S1_packer.read_files import read_allocation_pTTs



def fill_links(pTTs,links,xml,S2_Sector):
    for pTT_idx in range(len(pTTs)):
        pTT = pTTs[pTT_idx]['pTT_id']
        pTT_xml = xml[pTT]
        if pTT_xml != [] :    #if pTTs is allocated in the 4 links
            if links[(S2_Sector,(pTT_xml[0]['frame'], pTT_xml[0]['n_link'],pTT_xml[0]['channel']%2))] == []:
                links[(S2_Sector,(pTT_xml[0]['frame'],pTT_xml[0]['n_link'],pTT_xml[0]['channel']%2))].append(pTTs[pTT_idx]['energy'])
            else: 
                print('error link is already filled',(pTT_xml[0]['frame'],pTT_xml[0]['n_link'],pTT_xml[0]['channel']%2), links[(pTT_xml[0]['frame'], pTT_xml[0]['n_link'],pTT_xml[0]['channel']%2)])
        #else : print('error pTT has no allocation')

            

def _process_pTT_data(event,args,xml_allocation,xml_duplication,S2_Sector,data_pTTs):

    #fill CEE links 
    fill_links(event.ds_pTTs['CEE']['Sector'+str(S2_Sector)],data_pTTs,xml_allocation,S2_Sector)
    fill_links(event.ds_pTTs['CEE']['Sector'+str((S2_Sector+1)%3)],data_pTTs,xml_duplication,S2_Sector)

    #fill CEH links
    fill_links(event.ds_pTTs['CEH']['Sector'+str(S2_Sector)],data_pTTs,xml_allocation,S2_Sector)
    fill_links(event.ds_pTTs['CEH']['Sector'+str((S2_Sector+1)%3)],data_pTTs,xml_duplication,S2_Sector)
    
    data_pTTs



def _pTT_packer(event, args):
    data_pTTs = defaultdict(list)
    for S2_Sector in range(3):
        xml_allocation = read_allocation_pTTs(args.Edges,S2_Sector,4)
        xml_duplication = read_allocation_pTTs(args.Edges,S2_Sector,2)
        _process_pTT_data(event,args,xml_allocation,xml_duplication,S2_Sector,data_pTTs)
    event.pTT_packer =  data_pTTs
