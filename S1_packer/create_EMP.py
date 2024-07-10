from S1_packer.tools import *

def createEMPfile(event):
    pTTlinks = event.pTT_packer 
    TC_links = event.TC_packer
    file = open("Results/EMPfiles/S2_EMP_Input.txt", "w")
    file.write('')
    file.close()
    with open('Results/EMPfiles/S2_EMP_Input.txt', 'a') as file:   
      #write the first comments for the EMP file
        num_columns=84
        #file.write(f"ID: x1 \n")
        #file.write(f"Metadata: (strobe,) start of orbit, start of packet, end of packet, valid \n \n")
        column_str = '                    '.join(str(n_link).zfill(3) for n_link in range(num_columns))
        file.write(f"      Link            {column_str}\n")
        for frame_idx in range(108):
            if frame_idx == 0:
                metadata = 1101 
            elif frame_idx != 107:
                metadata = 1
            elif frame_idx == 107:
                metadata = 11
            
            frame = 'Frame '+ str(frame_idx).zfill(4).rjust(4) + "    " 
            frame += ' '.join(str(metadata).zfill(4) + " " + str(f'{int(word(pTTlinks,TC_links ,frame_idx,n_link),16):016x}' ) + " " for n_link in range(84))
            #frame += ' '.join(str(metadata).zfill(4) + " " + str(f'{0:016x}' ) + " " for j in range(84))
            file.write(f" {frame} \n")
        file.close()

def word(pTTlinks,TC_links,frame_idx,nb_link): #from the python link (pTT_packer and TC_packer) create an EMP file with 64 bits word composed of 2 pTT energies and 3 TC indices/energies
    #get the pTTs
    energypTT0 = 0
    energypTT1 = 0
    if pTTlinks[(frame_idx,nb_link,0)] != []:
        energypTT0 = pTTlinks[(frame_idx,nb_link,0)][0]
    code_energy0 = pack5E3M_FromInt(packInt_FromFloat(energypTT0)) #needed because python links are filed with float energies for the pTT

    if pTTlinks[(frame_idx,nb_link,1)] != []:
        energypTT1 = pTTlinks[(frame_idx,nb_link,1)][0]
    code_energy1 = pack5E3M_FromInt(packInt_FromFloat(energypTT1)) #needed because python links are filed with float energies for the pTT

    #get the TC energies and indices
    TC0_energy, TC0_numbering = 0,0
    TC1_energy, TC1_numbering = 0,0
    TC2_energy, TC2_numbering = 0,0
    if TC_links[(frame_idx,nb_link,0)] != []: 
        TC0_energy, TC0_numbering= TC_links[(frame_idx,nb_link,0)][0:2]
    if TC_links[(frame_idx,nb_link,1)] != []: 
        TC1_energy, TC1_numbering = TC_links[(frame_idx,nb_link,1)][0:2]
    if TC_links[(frame_idx,nb_link,2)] != []: 
        TC2_energy, TC2_numbering = TC_links[(frame_idx,nb_link,2)][0:2]


    return(hex(0x0000000000000000|(code_energy1 << 53)|(code_energy0<< 45)|(TC2_numbering<< 37)|(TC2_energy<< 30)|(TC1_numbering<< 22)|(TC1_energy<< 15)|(TC0_numbering<< 7)|(TC0_energy<< 0)))
    

