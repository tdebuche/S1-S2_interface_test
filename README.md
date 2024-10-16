# S1-S2_interface_test

This repository allows one to simulate the pTT building in the Stage 1, their mapping in the optical links and the Trigger Towers building in the Stage 2, from a rooftile with energy deposite simulated in CMSSW. This repository uses the mappings created in the HGCAL_TPG_pTT repository, and thus allows one to check if they work. It produces energy maps (plots) thanks to the Trigger Towers for the CE-E and the CE-H.

This repository is splitted in few parts, which follow each step of the pTT chain on the TPG system : 

- ECONT : create trigger sum (= module sums) --> not used if the trigger sums are already computed in the rootfile
- S1 simulation : compute the pTT energies from the module sum energies
- S1_packer : pack TCs and pTTs in the links
- S2_unpacker : unpack pTTs and TCs in the links, then compute and plot the Trigger Towers 
- data_handle : create the event class and read the rootfile with events
- Results : store the results of simulations

  
The program "run" allows one to run every program of this repository
-

This program has many arguments to know which program has to run with which conditions. 

1) pTT version

  
  --pTT_version : pTT version depending on the geometry version and some other updates (default : 'v3' which corresponds to the geometry 'v13.1')

  
2) Select the event needed
   
  -n : number of event needed 
  
  --paricles : choose the particles type "photons" or "pions"
  
  
2) Choose the scenario

  --Scenario : choose to build the pTTs from module sums or unslected sums (current scenario : module sums)
  
  --whole_endcap : Choose to plot a whole endcap (3 sectors) or only one sector
  
  --Sector : Choose the S2 sector (needed if only one sector is run
  
  --Edges  : With (yes) or without edges(no) --> choose 20 * 28 or 20 * 24 pTTs per sector

  --read_EMP : plot the energymap from an EMP file (and not from a rootfile)

