def pack5E3M_FromInt(energy): #Take integer value and pack it ino 5E3M format
    if(energy<8): #here the max number is 8 because mantissa has 3 bits, 2^3=8
        return int(energy)
    e = 1
    while(energy>=16):
        e+=1
        energy>>=1
    #print(e,energy)
    return int(8*(e-1)+energy) #format it in as 8 bits = eeeeemmm, where first 5 are exponent and last 3 are (mantissa - 8)

def unpack5E3M_ToInt(num): #Take 5E3M number as input and unpack it into integer
    assert(num<0x100);#make sure input is an 8 bit number

    e = ((num>>3)&0x1f);#Read first 5 bits from the input number to read the exponent
    m = ((num   )&0x07);#Read the last 3 bits as mantissa
    #print(e,m)

    if(e==0):
        return m
    elif(e==1):
        return 8+m
    else:
        return (16+2*m+1)<<(e-2)#Recover the fact that this is mantissa - 8, take into account first multiplication with 2 inside the bracket and then shift to right e-2 time which is equivalent to multiplying by 2

def pack5E4M_FromInt(energy): #Take intiger as input and pack it into 5E4M format
    if(energy<16): #here the max number is 16 because mantissa has 4 bits, 2^4=16
        return int(energy)
    e = 1
    while(energy>=32):
        e+=1
        energy>>=1
    #print(e,energy)
    return int(16*(e-1)+energy) #format it in as 9 bits = eeeeemmmm, where first 5 are exponent and last 4 are (mantissa - 8)

def unpack5E4M_ToInt(num): #Take 5E4M format and unpack it into intiger
    assert(num<0x200);#make sure input is an 9 bit number

    e = ((num>>4)&0x1f);#Read first 5 bits from the input number to read the exponent
    m = ((num   )&0x0f);#Read the last 4 bits as mantissa
    #print(e,m)

    if(e==0):
        return m
    elif(e==1):
        return 16+m
    else:
        return (32+2*m+1)<<(e-2)#Recover the fact that this is (mantissa - 8), take into account first multiplication with 2 inside the bracket and then shift to right e-2 time which is equivalent to multiplying by 2


def packInt_FromFloat(energy, constant=2**-12):
    return int(0.5+energy/constant)

def unpackFloat_FromInt(energy, constant=2**-12):
    return float((energy-0.5)*constant)








def compress_value(value, exponent_bits=4, mantissa_bits=3, truncation_bits=0):
    saturation_code = (1 << (exponent_bits + mantissa_bits)) - 1
    saturation_value = ((1 << (mantissa_bits + truncation_bits + 1)) - 1) << ((1 << exponent_bits) - 2)

    if value > saturation_value:
        return saturation_value, saturation_code

    bitlen = 0
    shifted_value = int(value) >> truncation_bits
    valcopy = shifted_value
    while valcopy != 0:
        valcopy >>= 1
        bitlen += 1

    if bitlen <= mantissa_bits:
        compressed_code = shifted_value
        compressed_value = shifted_value << truncation_bits
        return compressed_value, compressed_code

    # Build exponent and mantissa
    exponent = bitlen - mantissa_bits
    mantissa = (shifted_value >> (exponent - 1)) & ~(1 << mantissa_bits)
   
    # Assemble floating-point
    compressed_value = ((1 << mantissa_bits) | mantissa) << (exponent - 1)
    compressed_code = (mantissa << exponent_bits) | exponent #(exponent << mantissa_bits) | mantissa
    return compressed_value, compressed_code


def get_TC_numbering(u,v):
    if u == 0:
        return u+v
    if u == 1:
        return 3+u+v
    if u == 2:
        return 7+u+v
    if u == 3:
        return 12+u+v
    if u == 4:
        return 18+u+v
    if u == 5:
        return 24+u+v
    if u == 6:
        return 29+u+v
    if u == 7:
        return 33+u+v
