def frac_binary_twos_comp(num):
    # On augmente la plage de valeur représentable
    scaled_num = int(num * (2**14 - 1))
    print(scaled_num)
    
    # Représentation binaire du data
    bin_str = format(scaled_num & 0xffff, '016b')
    
    if scaled_num < 0:
        # Inversion des 1 et 0
        bin_str = ''.join(['1' if b == '0' else '0' for b in bin_str])
        # Ajout de 1
        bin_str = bin(int(bin_str, 2) + 1)[2:].zfill(16)
        bin_str = '1' + bin_str[1:]
        print(bin_str)
    else:
        # Retrait du 1 au MSB
        bin_str = '0' + bin_str[1:]
    
    return list(map(int, bin_str))


list = frac_binary_twos_comp(1000)
bin_str = ''.join(str(e) for e in list)

if list[0] == 1:
    bin_str = bin(int(bin_str, 2)- 1)[2:].zfill(16)
    bin_str = ''.join(['1' if b == '0' else '0' for b in bin_str])
    dec = -1*int(bin_str,2)
else:
    dec = int(bin_str[1:],2)
print(dec)


