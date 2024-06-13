from collections import defaultdict
import numpy as np
import awkward as ak
import uproot
import math
import yaml
from data_handle.S1simulator import build_pTTsCEE,add_TCs
from data_handle.tools import compress_value, printProgressBar, getuvsector


class EventData():
    def __init__(self, ds_si, ds_sci, gen):
        self.ds_si  = ds_si
        self.ds_sci  = ds_sci
        self.ds_ts = None
        self.ds_stc = None
        self.ds_pTTsCEE = None
        self.ds_pTTsdupCEE = None
        self.ds_pTTsCEH = None
        self.ds_pTTsdupCEH = None
        self.gen     = gen
        self.event   = gen.event
        self.eta_gen = gen.good_genpart_exeta[0]
        self.phi_gen = gen.good_genpart_exphi[0]
        self.pT_gen  = self._compute_pt(self.eta_gen,
                             gen.good_genpart_energy[0])

        self.data_packer = None
        self.pTT_packer = None          ######################add##################
        self.LSB = 1/10000 # 100 keV
        self.LSB_r_z = 0.7/4096
        self.LSB_phi = np.pi/1944
        self.offset_phi = -0.8

    def _compute_pt(self, eta, energy):
        return energy/np.cosh(eta)

    def ObjectType(self, object_type):
        return ((object_type & 0xF) << 22)

    def provide_ts(self,args,xml):
        nb_selected_TCs = defaultdict(list)
        selected_TCs = self.ds_si
        for module_idx in range(len(self.ds_si.good_tc_layer)):
            u,v,sector = getuvsector(self.ds_si.good_tc_layer[module_idx][0],
                                        self.ds_si.good_tc_waferu[module_idx][0],
                                        self.ds_si.good_tc_waferv[module_idx][0])
            module_alloc = self.get_module_id(3,self.ds_si.good_tc_layer[module_idx][0],u,v)
            module = self.get_module_id(sector,self.ds_si.good_tc_layer[module_idx][0],u,v)
            xml_alloc = self.get_TC_allocation(xml[0], module_alloc)
            if xml_alloc: 
                n_TCs = xml_alloc[-1]['index']
                nb_selected_TCs[module].append(n_TCs)  

        TCs = self.ds_si
        ts = defaultdict(list)
        Sector = args.Sector
        for module_idx in range(len(self.ds_si.good_tc_layer)):
            u,v,sector = getuvsector(self.ds_si.good_tc_layer[module_idx][0],
                                        self.ds_si.good_tc_waferu[module_idx][0],
                                        self.ds_si.good_tc_waferv[module_idx][0])
            if u != -999:
                module = self.get_module_id(sector,self.ds_si.good_tc_layer[module_idx][0],u,v)
                if self.ds_si.good_tc_layer[module_idx][0] < 48:
                    if ts[module] == []:
                        ts[module].append(0)
                    #for idx in range(len(self.ds_si.good_tc_layer[module_idx])):
                    if nb_selected_TCs[module]:
                        for idx in range(nb_selected_TCs[module][0],len(self.ds_si.good_tc_layer[module_idx])):
                            ts[module][0] += self.ds_si.good_tc_pt[module_idx][idx]
                    else : 
                        print(sector, self.ds_si.good_tc_layer[module_idx][0],u,v)
        
        self.ds_ts = ts
        return(nb_selected_TCs)


         
