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
