from collections import defaultdict
import numpy as np
import awkward as ak
import math
from data_handle.tools import getuvsector,get_module_id,get_MB_id
from link_packing.read_files import read_xml,MB_geometry


def _process_module(event, ds_TCs, idx, xml_alloc, data_TCs):
    
    n_TCs = xml_alloc[-1]['index']  # dangerous
    columns = [frame['column'] for frame in xml_alloc]
    
    # simulating the BC algorithm (ECON-T) and the phi sorting in the S1 FPGA
    mod_phi = ds_TCs.good_tc_phi[idx][:n_TCs+1]
    mod_energy = ds_TCs.good_tc_pt[idx][:n_TCs+1][ak.argsort(mod_phi)]
    mod_r_over_z = ds_TCs.r_over_z[idx][:n_TCs+1][ak.argsort(mod_phi)]
    mod_phi = ak.sort(mod_phi)
    
    # assigning each TCs to a columns
    xml_alloc = sorted(xml_alloc, key=lambda x: x['column'])  
    for tc_idx, TC_xml in enumerate(xml_alloc):
        if tc_idx > len(mod_energy)-1: break
        n_link = TC_xml['n_link']
        value_energy, code_energy = compress_value(mod_energy[tc_idx]/event.LSB)
        value_r_z = int(mod_r_over_z[tc_idx]/event.LSB_r_z) & 0xFFF # 12 bits
        value_phi = int((mod_phi[tc_idx]-event.offset_phi)/event.LSB_phi) & 0xFFF # 12 bits
        data_TCs[(TC_xml['frame'],n_link,TC_xml['channel']%3)] = [ code_energy, value_r_z, value_phi]
 
def _process_TC_data(event, args,xml,xml_MB):
    data_TCs = defaultdict(list)
    for module_idx in range(len(event.ds_si.good_tc_layer)):
        layer = event.ds_si.good_tc_layer[module_idx][0]
        u,v,sector = getuvsector(layer,
                                 event.ds_si.good_tc_waferu[module_idx][0],
                                 event.ds_si.good_tc_waferv[module_idx][0])
        if sector ==0:
            module = get_module_id(3,layer,u,v)
            xml_alloc = xml[0][module]
            if xml_alloc: 
                _process_module(event,event.ds_si, module_idx, xml_alloc, data_TCs)
    for MB_idx in range(len(event.ds_sci.good_tc_layer)):
        layer = event.ds_si.good_tc_layer[MB_idx][0]
        MB = get_MB_id(layer,event.ds_sci.MB_v[MB_idx][0], xml_MB)
        xml_alloc =xml[1][MB]
        if xml_alloc: _process_module(event,event.ds_sci, MB_idx, xml_alloc, data_TCs)
    return data_TCs


    
def _TC_packer(event, args):
    xml = read_xml()
    xml_MB = MB_geometry()
    data_TCs = _process_TC_data(event,args,xml,xml_MB)
    event.TC_packer = data_TCs

