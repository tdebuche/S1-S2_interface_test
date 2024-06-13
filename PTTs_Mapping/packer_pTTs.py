from collections import defaultdict
import numpy as np
import awkward as ak
import uproot
import math
import yaml


def _process_eventpTT(self,args, xml_allocation,xml_duplication,S1pTTCEE,S1pTTCEH,S1pTTCEEdup,S1pTTCEHdup,xml):
        data_pTTs = defaultdict(list)
        Sector = args.Sector
        nb_selected_TCs = self.provide_ts(args,xml)

        #CEE

        #Sector 0
        self.ds_pTTsCEE = build_pTTsCEE(self.ds_ts, args, S1pTTCEE)  #from module sums
        self.ds_pTTsCEE  = add_TCs(self.ds_pTTsCEE,self.ds_si,nb_selected_TCs,0,'CEE') #add selected TCs
        pTTs = self.ds_pTTsCEE
    

        #Sector 1
        self.ds_pTTsdupCEE = build_pTTsCEE(self.ds_ts, args, S1pTTCEEdup)
        self.ds_pTTsdupCEE  = add_TCs(self.ds_pTTsdupCEE,self.ds_si,nb_selected_TCs,1,'CEE')
        pTTsdup = self.ds_pTTsdupCEE

        #fill CEE links 
        
        for pTT_idx in range(len(pTTs)):
            pTT = pTTs[pTT_idx]['pTT_id']
            pTT_xml = self.get_pTT_allocation(xml_allocation, pTT)
            if pTT_xml != [] :    #if pTT is allocated in the 4 links
                data_pTTs[(pTT_xml[0]['frame'],pTT_xml[0]['n_link'],pTT_xml[0]['channel']%2)].append(pTTs[pTT_idx]['energy'])
        for pTT_idx in range(len(pTTsdup)):
            pTT = pTTsdup[pTT_idx]['pTT_id']
            pTT_xml = self.get_pTT_duplication(xml_duplication, pTT)
            if pTT_xml != [] :    #if pTT is allocated in the 2 links
                if data_pTTs[(pTT_xml[0]['frame'], pTT_xml[0]['n_link'],pTT_xml[0]['channel']%2)] == []:
                    data_pTTs[(pTT_xml[0]['frame'], pTT_xml[0]['n_link'],pTT_xml[0]['channel']%2)].append(pTTsdup[pTT_idx]['energy'])


        #CEH

        #Sector 0 
        self.ds_pTTsCEH = build_pTTsCEE(self.ds_ts, args, S1pTTCEH)
        self.ds_pTTsCEH  = add_TCs(self.ds_pTTsCEH,self.ds_si,nb_selected_TCs,0,'CEH')
        pTTs = self.ds_pTTsCEH

        #Sector 1
        self.ds_pTTsdupCEH = build_pTTsCEE(self.ds_ts, args, S1pTTCEHdup)
        self.ds_pTTsdupCEH  = add_TCs(self.ds_pTTsdupCEH,self.ds_si,nb_selected_TCs,1,'CEH')
        pTTsdup = self.ds_pTTsdupCEH

        #fill CEH links
        
        for pTT_idx in range(len(pTTs)):
            pTT = pTTs[pTT_idx]['pTT_id']
            pTT_xml = self.get_pTT_allocation(xml_allocation, pTT)
            if pTT_xml != [] :    #if pTT is allocated in the 4 links
                data_pTTs[(pTT_xml[0]['frame'],pTT_xml[0]['n_link'],pTT_xml[0]['channel']%2)].append(pTTs[pTT_idx]['energy'])
        for pTT_idx in range(len(pTTsdup)):
            pTT = pTTsdup[pTT_idx]['pTT_id']
            pTT_xml = self.get_pTT_duplication(xml_duplication, pTT)
            if pTT_xml != [] :    #if pTT is allocated in the 2 links
                if data_pTTs[(pTT_xml[0]['frame'], pTT_xml[0]['n_link'],pTT_xml[0]['channel']%2)] == []:
                    data_pTTs[(pTT_xml[0]['frame'], pTT_xml[0]['n_link'],pTT_xml[0]['channel']%2)].append(pTTsdup[pTT_idx]['energy'])

        return data_pTTs


    def _pTT_packer(self, args, xml_allocation,xml_duplication,S1pTTCEE,S1pTTCEH,S1pTTCEEdup,S1pTTCEHdup,xml):
        data_pTTs = self._process_eventpTT(args, xml_allocation,xml_duplication,S1pTTCEE,S1pTTCEH,S1pTTCEEdup,S1pTTCEHdup,xml)
        self.pTT_packer =  data_pTTs
