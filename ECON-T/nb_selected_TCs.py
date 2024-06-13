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
