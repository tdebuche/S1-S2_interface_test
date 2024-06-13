from collections import defaultdict
import numpy as np
import awkward as ak
import uproot
import math
import yaml

def _process_module(self, ds_TCs, idx, xml_alloc, data_TCs):
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
        value_energy, code_energy = compress_value(mod_energy[tc_idx]/self.LSB)
        value_r_z = int(mod_r_over_z[tc_idx]/self.LSB_r_z) & 0xFFF # 12 bits
        value_phi = int((mod_phi[tc_idx]-self.offset_phi)/self.LSB_phi) & 0xFFF # 12 bits
        data_TCs[(TC_xml['frame'],n_link,TC_xml['channel']%3)] = [ code_energy, value_r_z, value_phi]
 
def _process_event(self, args, xml, MB_conv):
    data_TCs = defaultdict(list)
    for module_idx in range(len(self.ds_si.good_tc_layer)):
        u,v,sector = getuvsector(self.ds_si.good_tc_layer[module_idx][0],
                                        self.ds_si.good_tc_waferu[module_idx][0],
                                        self.ds_si.good_tc_waferv[module_idx][0])
        if sector ==0:
            module = self.get_module_id(3,self.ds_si.good_tc_layer[module_idx][0],u,v)
            xml_alloc = self.get_TC_allocation(xml[0], module)
            if xml_alloc: 
                self._process_module(self.ds_si, module_idx, xml_alloc, data_TCs)

    for MB_idx in range(len(self.ds_sci.good_tc_layer)):
        MB = self.get_MB_id(self.ds_sci.good_tc_layer[MB_idx][0],
                            self.ds_sci.MB_v[MB_idx][0], MB_conv)
        xml_alloc = self.get_TC_allocation(xml[1], MB)
        if xml_alloc: self._process_module(self.ds_sci, MB_idx, xml_alloc, data_TCs)
    return data_TCs


    
def _data_packer(self, args, xml, xml_MB):
    data_TCs = self._process_event(args, xml, xml_MB)
    self.data_packer = data_TCs


def get_pTT_allocation(self, xml_allocation, pTT):
    return xml_allocation[pTT]
        
def get_pTT_duplication(self,xml_duplication,pTT):
    return xml_duplication[pTT]
        
def get_TC_allocation(self, xml_data, module):
    return xml_data[module]
