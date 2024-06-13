import xml.etree.ElementTree as ET
from collections import defaultdict
import math
import numpy as np
import awkward as ak
import nb_selected_TCs 

def provide_ts(event):
    ts = defaultdict(list)
    for module_idx in range(len(event.ds_si.good_tc_layer)):
        if u != -999:
            layer = event.ds_si.good_tc_layer[module_idx][0],
            u,v,sector = getuvsector(layer,
                                     event.ds_si.good_tc_waferu[module_idx][0],
                                     event.ds_si.good_tc_waferv[module_idx][0])
            module = get_module_id(layer,sector,u,v)
            if event.ds_si.good_tc_layer[module_idx][0] < 48:   #change to 27 when STCs
                if ts[module] == []:
                    ts[module].append(0)
                for idx in range(len(event.ds_si.good_tc_layer[module_idx])):
                    ts[module][0] += event.ds_si.good_tc_pt[module_idx][idx]
    return(ts)


def provide_unselected_ts(event):
    nb_selected_TCs = nb_selected_TCs.get()
    unselected_ts = defaultdict(list)
    for module_idx in range(len(event.ds_si.good_tc_layer)):
        if u != -999:
            layer = event.ds_si.good_tc_layer[module_idx][0]
            u,v,sector = getuvsector(layer,
                                        event.ds_si.good_tc_waferu[module_idx][0],
                                        event.ds_si.good_tc_waferv[module_idx][0])
            module = get_module_id(sector,layer,u,v)
            if layer < 48:  #change to 27 when STCs
                if ts[module] == []:
                    ts[module].append(0)
                if nb_selected_TCs[module]:
                    for idx in range(nb_selected_TCs[module][0],len(event.ds_si.good_tc_layer[module_idx])):
                        ts[module][0] += event.ds_si.good_tc_pt[module_idx][idx]
                if not nb_selected_TCs[module]:
                    print(sector, event.ds_si.good_tc_layer[module_idx][0],u,v) #see the differences in geometries
         
        return(unselected_ts)
        
