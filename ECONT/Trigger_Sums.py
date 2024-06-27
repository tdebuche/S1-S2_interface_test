import xml.etree.ElementTree as ET
from collections import defaultdict
import math
import numpy as np
import awkward as ak
from ECONT.read_nb_selected_TCs import get
from data_handle.tools import getuvsector,get_module_id
from ECONT.tools import create_list_HDorLD,get_STC_index_from_TC

def provide_ts(event):
    ts = defaultdict(list)
    for module_idx in range(len(event.ds_si.good_tc_layer)):
        if event.ds_si.good_tc_waferu[module_idx][0] != -999:
            layer = event.ds_si.good_tc_layer[module_idx][0]
            u,v,sector = getuvsector(layer,
                                     event.ds_si.good_tc_waferu[module_idx][0],
                                     event.ds_si.good_tc_waferv[module_idx][0])
            module = get_module_id(sector,layer,u,v)
            if event.ds_si.good_tc_layer[module_idx][0] < 27:   #change to 27 when STCs
                if ts[module] == []:
                    ts[module].append(0)
                for idx in range(len(event.ds_si.good_tc_layer[module_idx])):
                    ts[module][0] += event.ds_si.good_tc_pt[module_idx][idx]
    return(ts)


def provide_unselected_ts(event):
    nb_selected_TCs = get()
    unselected_ts = defaultdict(list)
    for module_idx in range(len(event.ds_si.good_tc_layer)):
        if event.ds_si.good_tc_waferu[module_idx][0]!= -999:
            layer = event.ds_si.good_tc_layer[module_idx][0]
            u,v,sector = getuvsector(layer,
                                        event.ds_si.good_tc_waferu[module_idx][0],
                                        event.ds_si.good_tc_waferv[module_idx][0])
            module = get_module_id(sector,layer,u,v)
            module_alloc = get_module_id(3,layer,u,v)
            if layer < 27:  #change to 27 when STCs
                if unselected_ts[module] == []:
                    unselected_ts[module].append(0)
                if nb_selected_TCs[module_alloc]:
                    for idx in range(nb_selected_TCs[module_alloc][0],len(event.ds_si.good_tc_layer[module_idx])):
                        unselected_ts[module][0] += event.ds_si.good_tc_pt[module_idx][idx]
                if not nb_selected_TCs[module_alloc]:
                    print('not allocated = ',sector, layer,u,v) #see the differences in geometries
         
    return(unselected_ts)
        
def provide_STCs(args,event):
    HDorLD_list = create_list_HDorLD(args)
    STCs = defaultdict(list)
    for module_idx in range(len(event.ds_si.good_tc_layer)):
        if event.ds_si.good_tc_layer[module_idx][0] > 26:   
            layer = event.ds_si.good_tc_layer[module_idx][0]
            u,v,sector = getuvsector(layer,
                                     event.ds_si.good_tc_waferu[module_idx][0],
                                     event.ds_si.good_tc_waferv[module_idx][0])
            module = get_module_id(sector,layer,u,v)
            HDorLD =  HDorLD_list[(layer,u,v)][0]
            for stc_idx in range(len(event.ds_si.good_tc_layer[module_idx])):
                cell_u,cell_v = event.ds_si.good_tc_cellu[module_idx][stc_idx],event.ds_si.good_tc_cellv[module_idx][stc_idx]
                stc_index = get_STC_index_from_TC(HDorLD,cell_u,cell_v)
                STCs[(module,stc_index)].append(event.ds_si.good_tc_pt[module_idx][stc_idx])

    return(STCs)
