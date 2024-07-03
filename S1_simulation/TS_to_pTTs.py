import numpy as np



def build_pTTsCEE(ts_energy, args, S1pTTCEE):
    pTTsCEE = []
    for pTT_idx in range(len(S1pTTCEE)):
        energyCEE = 0
        pTT_id = S1pTTCEE[pTT_idx]['pTT'] 
        ModulesCEE = S1pTTCEE[pTT_idx]['Modules'] 
        for module_idx in range(len(ModulesCEE)):
            module_id = ModulesCEE[module_idx]['module_id']
            energy = ModulesCEE[module_idx]['module_energy']
            if ts_energy[module_id] != []:
                energyCEE += ts_energy[module_id][0] * energy/16
        pTTsCEE.append({'pTT_id' : pTT_id, 'energy': energyCEE})
            #if energyCEE != 0:
            #print({'pTT_id' : pTT_id, 'energy': energyCEE})
    
    return(pTTsCEE)


def build_pTTsCEH(stc_energy,args,S1pTTCEH):
    pTTsCEH = []
    for pTT_idx in range(len(S1pTTCEH)):
        energyCEH = 0
        pTT_id = S1pTTCEH[pTT_idx]['pTT'] 
        STCs = S1pTTCEH[pTT_idx]['STCs'] 
        for stc_idx in range(len(STCs)):
            module_id = STCs[stc_idx]['module_id']
            stc_index = STCs[stc_idx]['stc_idx']
            energy = STCs[stc_idx]['stc_energy']
            if stc_energy[(module_id,stc_index)] != []:
                energyCEH += stc_energy[(module_id,stc_index)][0]* energy/16
        pTTsCEH.append({'pTT_id' : pTT_id, 'energy': energyCEH})
    return(pTTsCEH)
