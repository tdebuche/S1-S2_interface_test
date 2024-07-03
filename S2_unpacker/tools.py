def get_pTT_numbers(pTT):
    S1Board = int(pTT[4:6],16) & 0x3F
    phi = int(pTT,16) & 0x1F
    eta = (int(pTT,16) & 0x3E0) //(16 * 2)
    CEECEH = (int(pTT,16) & 0x400) //(16*16*4)
    Sector = (int(pTT[2],16) &  0x6)//2
    return(Sector,S1Board,eta,phi,CEECEH)




def get_pTT_energy(word,pTT_number):
    
