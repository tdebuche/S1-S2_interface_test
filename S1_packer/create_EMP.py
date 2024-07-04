from S1_packer.tools import compress_value

def createEMPfile(event):
    pTTlinks = event.pTT_packer 
    file = open("Results/EMPfiles/S2_EMP_Input.txt", "w")
    file.write('')
    file.close()
    with open('Results/EMPfiles/S2_EMP_Input.txt', 'a') as file:   
      #write the first comments for the EMP file
        num_columns=84
        file.write(f"ID: x1 \n")
        file.write(f"Metadata: (strobe,) start of orbit, start of packet, end of packet, valid \n \n")
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
            frame += ' '.join(str(metadata).zfill(4) + " " + str(f'{int(word(pTTlinks,frame_idx,n_link),16):016x}' ) + " " for n_link in range(84))
            #frame += ' '.join(str(metadata).zfill(4) + " " + str(f'{0:016x}' ) + " " for j in range(84))
            file.write(f" {frame} \n")
        file.close()

def word(pTTlinks,frame_idx,nb_link):
    energypTT0 = 0
    if pTTlinks[(frame_idx,nb_link,0)] != []:
        energypTT0 = pTTlinks[(frame_idx,nb_link,0)][0]
    value_energy0, code_energy0 = compress_value(energypTT0*10000,5,3,0)
    energypTT1 = 0
    if pTTlinks[(frame_idx,nb_link,1)] != []:
        energypTT1 = pTTlinks[(frame_idx,nb_link,1)][0]
    value_energy1, code_energy1 = compress_value(energypTT1*10000,5,3,0)
    return(hex(0x0000000000000000|(code_energy1) << 53 | (code_energy0)<< 45))
    

