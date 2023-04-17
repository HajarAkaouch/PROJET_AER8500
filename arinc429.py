from bitarray import bitarray
import constants as const
import math

SSM_BNR = [1,1]


"""
    In this file you will find all the necessary functions needed to communicate via the arinc429 protocol
"""
class arinc429:
    def __init__(self, label, data, resolution):
        self.resolution = 0
        self.label = label
        self.data = data
        self.resolution = resolution
        self.sdi = []
        self.payload = []
        self.ssm = []
        self.parity = 0

        self.message = [0]*32

def build_arinc_mess(arinc_mess):
    match arinc_mess.label:
        case const.LABEL_ALT:
            arinc_mess.message[0:7] = octal_to_binary_list(const.LABEL_ALT[1]).reverse()
            arinc_mess.sdi[8:9] = [0,1]
            arinc_mess.message[12:28] = set_bnr_payload(arinc_mess)
            arinc_mess.ssm = []
            arinc_mess.message[31] = parity(arinc_mess)
        case const.LABEL_STATE:
            arinc_mess.message[0:7] = octal_to_binary_list(const.LABEL_STATE[1]).reverse()
            arinc_mess.message[8:28] = set_bcd_payload(arinc_mess)
            arinc_mess.ssm = []
            arinc_mess.message[31] = parity(arinc_mess)
        case const.LABEL_CLB_R:
            arinc_mess.message[0:7] = octal_to_binary_list(const.LABEL_CLB_R[1]).reverse()
            arinc_mess.message[8:28] = set_bcd_payload(arinc_mess)
            arinc_mess.message[30,29] = SSM_BNR
            arinc_mess.message[31] = parity(arinc_mess)
        case const.LABEL_ANGLE:
            arinc_mess.message[0:7] = octal_to_binary_list(const.LABEL_CLB_R[1]).reverse()
            arinc_mess.message[8:9] = [0,1]
            arinc_mess.message[12:28] = set_bcd_payload(arinc_mess)
            arinc_mess.message[30,29] = SSM_BNR
            arinc_mess.message[31] = parity(arinc_mess)

def parity(arinc_mess):
    ones = arinc_mess.message.count(1)
    if ones % 2 == 0:
        return 1
    else:
        return 0
    
def set_bnr_payload(arinc):
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
    
def set_bdc_payload(arinc):
    bcd_payload = []
    for digit in str(data):
        bcd_payload.append([int(i) for i in list('{0:0b}'.format(digit))])
    return bcd_payload

# def decode_frac_binary_twos_comp(arinc_mess):
#     bin_str = ''.join(str(e) for e in arinc_mess.payload)
#     bin_str = bin(int(bin_str, 2)- 1)[2:].zfill(16)
#     bin_str = ''.join(['1' if b == '0' else '0' for b in bin_str])
#     if list[0] == 1:
#         dec = -1*int(bin_str,2)
#     else:
#         dec = int(bin_str,2)



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
