# S1-S2_interface_test

This repository allows one to simulate the pTT building in the Stage 1, their mapping in the optical links and the Trigger Towers building in the Stage 2, from a rooftile with energy deposite simulated in CMSSW. This repository uses the mappings created in the HGCAL_TPG_pTT repository, and thus allows one to check if they work. 

This repository is splitted in few parts, which follow each step of the pTT chain on the TPG system : 

- ECONT : create trigger sum (= module sums) --> not used if the trigger sums are already computed in the rootfile
- S1 simulation : compute the pTT energies from the module sum energies
- S1_packer : pack TCs and pTTs in the links
- S2_unpacker : unpack pTTs and TCs in the links, then compute and plot the Trigger Towers 
- data_handle : create the event class and read the rootfile with events
- Results : store the results of simulations
