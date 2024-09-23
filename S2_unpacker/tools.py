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
    energy_in_integer =  unpack4E4M_ToInt(coded_energy)
    energy_in_integer = undo_trimming(energy_in_integer, 19, 35)
    energy_in_GeV = unpackFloat_FromInt(energy_in_integer)
    return energy_in_GeV

def undo_trimming(inputData, targetNumberBits, maxNumberBits):
    criticalBitNumber = maxNumberBits - targetNumberBits
    return inputData << criticalBitNumber


def pack4E4M_FromInt(energy): #Take input integer and pack it into 4E4M format
    assert(energy<0x80000);#make sure input is an 19 bit number

    if(energy<16): #here the max number is 16 because mantissa has 4 bits, 2^4=16
        return int(energy)
    e = 1
    while(energy>=32):
        e+=1
        energy>>=1
    return int(16*(e-1)+energy) #format it in as 16 bits = eeeemmm, where first 4 are exponent and last 4 are (mantissa - 16)

def unpack4E4M_ToInt(num): #Take 4E4M as input and unpack it to integer
    assert(num<0x100);#make sure input is an 8 bit number

    e = ((num>>4)&0x0f);#Read first 4 bits from the input number to read the exponent
    m = ((num   )&0x0f);#Read the last 4 bits as mantissa
    #print(e,m)

    if(e==0):
        return m
    elif(e==1):
        return 16+m
    else:
        return (32+2*m+1)<<(e-2)#Recover the fact that this is (mantissa - 8), take into account first multiplication with 2 inside the bracket and then shift to right e-2 time which is equivalent to multiplying by 2


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
    return float((energy-0.5)/(10**8))



def S1_phi_to_S2_phi(args,phi,sameS1S2sector):

    if args.Edges == 'yes': offset = 3
    if args.Edges == 'no' : offset = 0
 
    if sameS1S2sector == 'yes':
        return(phi - 6 - offset)

    if sameS1S2sector == 'no':
        return(phi +18-offset)
