from collections import defaultdict
import numpy as np
import awkward as ak
import uproot
import math
import yaml
from data_handle.tools import compress_value, printProgressBar, getuvsector,get_module_id
from ECONT.Trigger_Sums import provide_ts, provide_unselected_ts,provide_STCs
from collections import defaultdict

class EventData():
    def __init__(self,args, ds_si, ds_sci, gen,ts):
        self.args  = args
        self.ds_si  = ds_si
        self.ds_sci  = ds_sci
        #self.ds_ts = provide_ts(self)
        self.ds_ts = ts
        self.ds_unselected_ts = provide_unselected_ts(self)
        self.ds_stc = provide_STCs(args,self)
        self.ds_pTTs = {'CEE':{'Sector0':[],'Sector1':[],'Sector2':[]},'CEH':{'Sector0':[],'Sector1':[],'Sector2':[]}}
        self.TC_packer = None
        self.pTT_packer = None
        self.gen     = gen
        self.event   = gen.event
        self.eta_gen = gen.good_genpart_exeta[0]
        self.phi_gen = gen.good_genpart_exphi[0]
        self.energy_gen = gen.good_genpart_energy[0]       
        self.LSB = 1/10000 # 100 keV
        self.LSB_r_z = 0.7/4096
        self.LSB_phi = np.pi/1944
        self.offset_phi = -0.8

    def _compute_pt(self, eta, energy):
        return energy/np.cosh(eta)

with open('config.yaml', "r") as afile:
    cfg_particles = yaml.safe_load(afile)["particles"]

def apply_sort(df, counts, axis):
    for field in df.fields:
        df[field] = ak.unflatten(df[field], counts, axis)
    return df
    
def provide_event(args,ev, gen,ts):
    ev['r_over_z'] = np.sqrt(ev.good_tc_x**2 + ev.good_tc_y**2)/ev.good_tc_z
    ev['MB_v'] = np.floor((ev.good_tc_cellv-1)/4)
    #ev = ev[[x for x in ak.fields(ev) if not x in ["good_tc_x","good_tc_y","good_tc_z"]]]
    
    # dividing silicon and scintillators
    sci = ev[ev['good_tc_subdet'] == 10]
    si  = ev[ev['good_tc_subdet'] != 10]
    
    # selecting first 120 sector only
    sci = sci[sci['good_tc_cellv']<=48]
    #si = si[si['good_tc_layer'] < 27]

    # sorting by modules  
    sorted_waferu = si[ak.argsort(si['good_tc_waferu'])]
    counts = ak.flatten(ak.run_lengths(sorted_waferu.good_tc_waferu), axis=None)
    sorted_si = apply_sort(sorted_waferu, counts, 1)

    sorted_waferv = sorted_si[ak.argsort(sorted_si['good_tc_waferv'])]
    counts = ak.flatten(ak.run_lengths(sorted_waferv.good_tc_waferv), axis=None)
    sorted_si = apply_sort(sorted_waferv, counts, 2)

    sorted_layer = sorted_si[ak.argsort(sorted_si['good_tc_layer'])]
    counts = ak.flatten(ak.run_lengths(sorted_layer.good_tc_layer), axis=None)
    sorted_si = apply_sort(sorted_layer, counts, 3)
    sorted_si = ak.flatten(sorted_si, axis=3)
    sorted_si = ak.flatten(sorted_si, axis=2)

    # sorting by transverse energy, simulating the ECONT_T
    sorted_si = sorted_si[ak.argsort(sorted_si['good_tc_pt'], ascending=False)][0]
    
    # sorting sci by MB (cellv) and plane
    sorted_MB = sci[ak.argsort(sci['MB_v'])]
    counts = ak.flatten(ak.run_lengths(sorted_MB.MB_v), axis=None)
    sorted_sci = apply_sort(sorted_MB, counts, 1)

    sorted_layer = sorted_sci[ak.argsort(sorted_sci['good_tc_layer'])]
    counts = ak.flatten(ak.run_lengths(sorted_layer.good_tc_layer), axis=None)
    sorted_sci = apply_sort(sorted_layer, counts, 2)
    sorted_sci = ak.flatten(sorted_sci, axis=2)

    # sorting by transverse energy, simulating the ECONT_T
    sorted_sci = sorted_sci[ak.argsort(sorted_sci['good_tc_pt'], ascending=False)][0]



    list_ts = defaultdict(list)
    ts   = ts[ts['good_ts_z'] >0]
    for module_index in range(len(ts['good_ts_layer'])):
        u,v,sector = getuvsector(ts['good_ts_layer'][module_index],ts['good_ts_waferu'][module_index],ts['good_ts_waferv'][module_index])
        module_id = get_module_id(sector,ts['good_ts_layer'][module_index],u,v)
        list_ts[module_id].append(ts['good_ts_energy'][module_index])


    return EventData(args,sorted_si, sorted_sci,gen,list_ts)



def provide_events(args,n, particles, PU):
    base_path = cfg_particles['base_path']
    name_tree = cfg_particles[PU][particles]["tree"]
    filepath  = base_path + cfg_particles[PU][particles]["file"]

    branches_tc = [
        'good_tc_x', 'good_tc_y', 'good_tc_z',
        'good_tc_phi', 'good_tc_layer', 'good_tc_cellu','good_tc_cellv',
        'good_tc_waferu', 'good_tc_waferv',
        'good_tc_pt', 'good_tc_subdet'
    ]
    branches_ts = ['good_ts_layer', 'good_ts_z','good_ts_waferu', 'good_ts_waferv','good_ts_energy']

    branches_gen = ['event', 'good_genpart_exeta', 'good_genpart_exphi', 'good_genpart_energy']
    if args.rootfile == 'from_Toni':
        root = uproot.open("/eos/user/t/tsculac/BigStuff/HGCAL/V16_data_ntuples_15June2024/SinglePhotonPU0V16.root")
        tree = root.get("l1tHGCalTriggerNtuplizer/HGCalTriggerNtuple")
        first_event = 49
    if args.rootfile == 'from_Marco':
        tree = uproot.open(filepath)[name_tree]
        first_event = 0
    events_ds = []
    printProgressBar(0,n, prefix='Reading '+str(n)+' events from ROOT file:', suffix='Complete', length=50)
    for ev in range(first_event,first_event+n):
      data = tree.arrays(branches_tc, entry_start=ev, entry_stop=ev+1, library='ak')
      data_gen = tree.arrays(branches_gen, entry_start=ev, entry_stop=ev+1, library='ak')[0]
      data_ts = tree.arrays(branches_ts, entry_start=ev, entry_stop=ev+1, library='ak')[0]
      events_ds.append(provide_event(args,data, data_gen,data_ts))
      printProgressBar(ev+1, n, prefix='Reading '+str(n)+' events from ROOT file:', suffix='Complete', length=50)
    return events_ds
         
