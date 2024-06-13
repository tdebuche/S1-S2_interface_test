    def provide_ts(self,args,xml):
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
