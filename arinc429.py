from bitarray import bitarray

"""
    In this file you will find all the necessary functions needed to communicate via the arinc429 protocol
"""



def parity(message):
    for i in range(message):
        pass

def build_arinc_429_mess(label, data, ssm):
    word = bitarray(32)
    word.setall(0)

    

if __name__ == "__main__":
    print(build_arinc_429_mess(8,4000, 2))