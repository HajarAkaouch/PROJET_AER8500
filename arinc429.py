from bitarray import bitarray
import constants as const
import math

"""
    In this file you will find all the necessary functions needed to communicate via the arinc429 protocol
"""
class arinc429:
    def __init__(self, label, data, resolution):
        self.resolution = 0
        self.label = label
        self.data = data
        self.payload = []
        self.ssm = []
        self.parity = 0

        self.message = []

def parity(self):
    ones = self.message.count(1)
    if ones % 2 == 0:
        return 1
    else:
        return 0
    
def set_arinc_payloadd(arinc):
    if arinc.label == const.LABEL_ALT:
        # On augmente la plage de valeur représentable
        scaled_num = int(arinc.data * (2**14 - 1))
        # Représentation binaire du data
        bin_str = format(scaled_num & 0xffff, '016b')
        print(bin_str)
        
        if scaled_num < 0:
            # Inversion des 1 et 0
            bin_str = ''.join(['1' if b == '0' else '0' for b in bin_str])
            # Ajout de 1
            bin_str = bin(int(bin_str, 2) + 1)[2:].zfill(16)
        else:
            bin_str = '0' + bin_str[1:]
        
        return string_to_binary_list(bin_str)
    
    if arinc.label == const.LABEL_STATE:
        # On augmente la plage de valeur représentable
        scaled_num = int(arinc.data * (2**14 - 1))
        # Représentation binaire du data
        bin_str = format(scaled_num & 0xffff, '016b')
        print(bin_str)
        
        if scaled_num < 0:
            # Inversion des 1 et 0
            bin_str = ''.join(['1' if b == '0' else '0' for b in bin_str])
            # Ajout de 1
            bin_str = bin(int(bin_str, 2) + 1)[2:].zfill(16)
        else:
            bin_str = '0' + bin_str[1:]
        
        return string_to_binary_list(bin_str)
    
    if arinc.label == const.LABEL_ALT:
        match arinc.data:
            case 0:
                

def decode_frac_binary_twos_comp(arinc_mess):
    bin_str = ''.join(str(e) for e in arinc_mess.payload)
    bin_str = bin(int(bin_str, 2)- 1)[2:].zfill(16)
    bin_str = ''.join(['1' if b == '0' else '0' for b in bin_str])
    if list[0] == 1:
        dec = -1*int(bin_str,2)
    else:
        dec = int(bin_str,2)

def build_arinc_mess(self, label, data, ssm):
    match label:
        case const.LABEL_ALT:
            self.message[13:28] = data

    self.message[0] = self.parity()

def bcd_payload(self):
    bcd_payload = []
    for digit in str(self.data):
        bcd_payload.append([int(i) for i in list('{0:0b}'.format(digit))])
    return bcd_payload

def int_to_binary_list(int_num):
    bin_list = [int(i) for i in list('{0:0b}'.format(int_num))]
    return bin_list

def octal_to_binary_list(octal_num):
    binary_list = []
    binary_str = format(octal_num, 'o')
    for digit in binary_str:
        binary_digit = bin(int(digit))[2:].zfill(3) 
        binary_list.extend(list(map(int, binary_digit)))
    binary_list = [0] * (8 - len(binary_list)) + binary_list 

    return binary_list

def string_to_binary_list(str):
    return list(map(int, str))

def convert_label_to_rev_oct(label):
    label_oct = [int(i) for i in bin(label)[2:]]
    return label_oct
