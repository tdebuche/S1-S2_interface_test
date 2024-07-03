def get_pTT_numbers(pTT):
    S1Board = int(pTT[4:6],16) & 0x3F
    phi = int(pTT,16) & 0x1F
    eta = (int(pTT,16) & 0x3E0) //(16 * 2)
    CEECEH = (int(pTT,16) & 0x400) //(16*16*4)
    Sector = (int(pTT[2],16) &  0x6)//2
    return(Sector,S1Board,eta,phi,CEECEH)




def get_pTT_energy(word,pTT_number):
    if pTT_number == 1:
        coded_energy = (int(word[0:3],16) & 0x1fe)//2
    if pTT_number == 0:
        coded_energy = (int(word[2:5],16) & 0x1fe)//2
    energy_in_integer = unpack5E3M_ToInt(coded_energy)
    energy_in_GeV = unpackFloat_FromInt(energy_in_integer)
    return energy_in_GeV


def unpack5E3M_ToInt(num): #Take 5E3M format and unpackpack it into integer
    assert(num<0x100);#make sure input is an 8 bit number

    e = ((num>>3)&0x1f);#Read first 5 bits from the input number to read the exponent
    m = ((num   )&0x07);#Read the last 3 bits as mantissa
    #print(e,m)

    if(e==0):
        return m
    elif(e==1):
        return 8+m
    else:
        return (16+2*m+1)<<(e-2)



def unpackFloat_FromInt(energy):
    return float((energy-0.5)/(2**12))
