from collections import defaultdict
import numpy as np
import math
from S1_packer.read_files import read_allocation_pTTs



def fill_links(pTTs,links,xml):
    for pTT_idx in range(len(pTTs)):
        pTT = pTTs[pTT_idx]['pTT_id']
        pTT_xml = xml[pTT]
        if pTT_xml != [] :    #if pTTs is allocated in the 4 links
            if links[(pTT_xml[0]['frame'], pTT_xml[0]['n_link'],pTT_xml[0]['channel']%2)] == []:
                links[(pTT_xml[0]['frame'],pTT_xml[0]['n_link'],pTT_xml[0]['channel']%2)].append(pTTs[pTT_idx]['energy'])
            else: 
                print('error link is already filled',(pTT_xml[0]['frame'],pTT_xml[0]['n_link'],pTT_xml[0]['channel']%2), links[(pTT_xml[0]['frame'], pTT_xml[0]['n_link'],pTT_xml[0]['channel']%2)])
        #else : print('error pTT has no allocation')
    #print(links)
            

def _process_pTT_data(event,args,xml_allocation,xml_duplication):
    data_pTTs = defaultdict(list)
    
    #fill CEE links 
    fill_links(event.ds_pTTsCEE,data_pTTs,xml_allocation)
    fill_links(event.ds_pTTsdupCEE,data_pTTs,xml_duplication)

    #fill CEH links
    fill_links(event.ds_pTTsCEH,data_pTTs,xml_allocation)
    fill_links(event.ds_pTTsdupCEH,data_pTTs,xml_duplication)
    
    return data_pTTs



def _pTT_packer(event, args):
    xml_allocation = read_allocation_pTTs(args.Edges,args.Sector,4)
    xml_duplication = read_allocation_pTTs(args.Edges,args.Sector,2)
    data_pTTs = _process_pTT_data(event,args,xml_allocation,xml_duplication)
    event.pTT_packer =  data_pTTs
