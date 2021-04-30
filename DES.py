

import numpy as np

IP = np.load("DES_Initial_Permutation.npy")
PC1 = np.load("DES_Permutation_Choice1.npy")
PC2 = np.load("DES_Permutation_Choice2.npy")
KeyRoundShifts = np.load("DES_Round_Shifts.npy")

def Expansion(Ri):


    print("Expand")

def S_Box_Sub(input):


    print("S Box")

def To_Bits(Input):

    print("To bits")

def To_Hex(Input):

    print("To Hex")

def F_Function(Ri, Ki):


    print("F Function")

def Key_Mutation(key, pc1, pc2, roundshift):
        # Return array with keys [0..15]


    print("Key mutation")

def DES_Encrypt(plaintext, key, ip):


    print("DES Encrypt")

def DES_Decrypt(plaintext, key, ip):


    print("DES Decrypt")

def TDEA_Encrypt(inspect_mode, plaintext, key1, key2, key3, ip):


    print("3DES encrypt")

def TDEA_Decrypt(inspect_mode, plaintext, key1, key2, key3, inv_ip):


    print("3DES decrypt")