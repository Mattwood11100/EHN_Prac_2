
import numpy as np

IP = np.load("DES_Initial_Permutation.npy")
PC1 = np.load("DES_Permutation_Choice1.npy")
PC2 = np.load("DES_Permutation_Choice2.npy")
KeyRoundShifts = np.load("DES_Round_Shifts.npy")

Expand_table = [32, 1, 2, 3, 4, 5, 4, 5,
                6, 7, 8, 9, 8, 9, 10, 11,
                12, 13, 12, 13, 14, 15, 16, 17,
                16, 17, 18, 19, 20, 21, 20, 21,
                22, 23, 24, 25, 24, 25, 26, 27,
                28, 29, 28, 29, 30, 31, 32, 1]

S_Box = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

    # Permutation forafter applying  S Box
SBox_per = [16, 7, 20, 21,
       29, 12, 28, 17,
       1, 15, 23, 26,
       5, 18, 31, 10,
       2, 8, 24, 14,
       32, 27, 3, 9,
       19, 13, 30, 6,
       22, 11, 4, 25]

Inv_IP = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]

HtB = {'0': "0000",
       '1': "0001",
       '2': "0010",
       '3': "0011",
       '4': "0100",
       '5': "0101",
       '6': "0110",
       '7': "0111",
       '8': "1000",
       '9': "1001",
       'A': "1010",
       'B': "1011",
       'C': "1100",
       'D': "1101",
       'E': "1110",
       'F': "1111"}

BtH = {"0000": '0',
       "0001": '1',
       "0010": '2',
       "0011": '3',
       "0100": '4',
       "0101": '5',
       "0110": '6',
       "0111": '7',
       "1000": '8',
       "1001": '9',
       "1010": 'A',
       "1011": 'B',
       "1100": 'C',
       "1101": 'D',
       "1110": 'E',
       "1111": 'F'}


def Expansion(Ri, expand):
    Expanded = []
        # Apply expansion on Ri to return 48 bits
    for i in range(len(expand)):
        Expanded.append(Ri[expand[i]-1])

    return Expanded


def S_Box_Sub(input):
    Si = []
    Row_i = []
    Column_i = []
    Output_int = []
        # Extract 6 S bits grouping
    for i in range(int(48/6)):
        Si.append(input[i*6:i*6+6])
        Row_T = ""
        Column_T = ""
            # Get Rows and Colums
        Row_T += Si[i][0] + Si[i][5]
        Column_T += Si[i][1] + Si[i][2] + Si[i][3] + Si[i][4]
        Row_i.append(int(Row_T,2))
        Column_i.append(int(Column_T,2))

            # Use row and column to get value from S Boxes
        Output_int.append(S_Box[i][Row_i[i]][Column_i[i]])

    Output = []
        # Convert Integer values to Bits
    for i in range(len(Output_int)):
        Temp = "{0:04b}".format(Output_int[i])
        for j in range(len(Temp)):
            Output.append(Temp[j])

        # Output size is 32
    return Output


def To_Bits(Input):
    Temp = ""
    Input = Input.upper()
    for i in range(len(Input)):
        Temp += HtB[Input[i]]
    Bits = []
    for i in range(len(Temp)):
        Bits.append(Temp[i])
    return Bits


def To_Hex(Input):
    Output = ""
    for i in range(int(len(Input)/4)):
        Output += BtH[Input[i*4:i*4+4]]

    return Output


def C_LeftShift(Input, i):
    Temp = np.roll(Input, -1 * i).tolist()
    return Temp


def Apply_Per(Input, Per):
    Temp = []
    for i in range(len(Per)):
        Temp.append(Input[Per[i] - 1])
    return Temp


def XOR(Ri, Ki):
    Output = []
        # Apply bit-wise XOR between Ri and Ki
    for i in range(len(Ri)):
        if (Ri[i] == '1' and Ki[i] == '0') or (Ri[i] == '0' and Ki[i] == '1'):
            Output.append('1')
        else:
            Output.append('0')

    return Output


def F_Function(Ri, Ki):
        # Step 1: Expand Ri
    Ri_Exp = Expansion(Ri,Expand_table)
        # Step 2: XOR expanded Ri and Ki
    XORed = XOR(Ri_Exp,Ki)
        # Step 3: Apply S-Box substitution
    S_Boxed = S_Box_Sub(XORed)
        # Step 4: Apply S-Box permutation
    S_Per = []
    for i in range(len(SBox_per)):
        S_Per.append(S_Boxed[SBox_per[i]-1])

    return S_Per

    print("F Function")


def Key_Mutation(key, pc1, pc2, roundshift):
        # Return array with keys [0..15]
    K = To_Bits(key)

        # Apply Permutation 1
    K_PC1 = Apply_Per(K, pc1)
        # Get Ki before PC2
    Ki = []
    for i in range(len(roundshift)):
        left = K_PC1[0:28]
        right = K_PC1[28:]
        left = C_LeftShift(left, roundshift[i])
        right = C_LeftShift(right, roundshift[i])
        left.extend(right)
        K_PC1 = left
        Ki.append(K_PC1)

        # Apply Permutation 2 to Ki
    Ki_PC2 = []
    for i in range(len(Ki)):
        Ki_PC2.append(Apply_Per(Ki[i] ,pc2))

    return Ki_PC2


def DES_Encrypt(plaintext, key, ip, inspect_mode):    # Plaintext and key input must be 64 bits in Hex/ ASCII
    Keys = Key_Mutation(key, PC1, PC2, KeyRoundShifts)

# Add check for size of text
    PT = To_Bits(plaintext)

        # Apply Initial Permutation
    P_IP = Apply_Per(PT, ip)

    Li = []
    Ri = []

    Li.append(P_IP[0:32])
    Ri.append(P_IP[32:])

    for i in range(16):
        Li.append(Ri[i])
        F_Function_Out = F_Function(Ri[i],Keys[i])
        Ri_Temp = XOR(F_Function_Out, Li[i])
        Ri.append(Ri_Temp)

        # Convert to Hex
    Li_Hex = []
    Ri_Hex = []
    for i in range(len(Li)):
        L_Temp = ""
        R_Temp = ""
        for j in range(int(len(Li[i])/4)):
            L_Temp += Li[i][j * 4] + Li[i][j * 4 + 1] + Li[i][j * 4 + 2] + Li[i][j * 4 + 3]
            R_Temp += Ri[i][j * 4] + Ri[i][j * 4 + 1] + Ri[i][j * 4 + 2] + Ri[i][j * 4 + 3]
        Li_Hex.append(To_Hex(L_Temp))
        Ri_Hex.append(To_Hex(R_Temp))

    Keys_Hex = []
    for i in range(len(Keys)):
        T = ""
        for j in range(len(Keys[i])):
            T += Keys[i][j]
        Keys_Hex.append(To_Hex(T))

        # Print round outputs and keys
    # for i in range(len(Li)-1):
    #     print("round",i+1, "\tLi:", Li_Hex[i+1], "\tRi:", Ri_Hex[i+1], "\tKey:", Keys_Hex[i])

    if (inspect_mode == True):
        Rounds = []
        for i in range(1,len(Li)):
            Tl = Li_Hex[i]
            Tl += Ri_Hex[i]
            Rounds.append(Tl)

    TL = Li[16]
    TR = Ri[16]
        # Left and right swap for final permutation
    TR.extend(TL)
        # Apply final permutation
    CText = Apply_Per(TR,Inv_IP)
    Final_B = ""
    for i in range(len(CText)):
        Final_B += CText[i]
    CText = To_Hex(Final_B)

    if (inspect_mode == True):
        Out = {"ROutputs":Rounds, "Ciphertext":CText}
        return Out
    else:
        return CText
    print("DES Encrypt")


def DES_Decrypt(plaintext, key, ip):


    print("DES Decrypt")


def TDEA_Encrypt(inspect_mode, plaintext, key1, key2, key3, ip):


    print("3DES encrypt")


def TDEA_Decrypt(inspect_mode, plaintext, key1, key2, key3, inv_ip):


    print("3DES decrypt")



Plaintext = "02468aceeca86420"
Key1_init = "0f1571c947d9e859"

Plantext = "Testing1"
Key1_init ="Encrypt1"

CT = DES_Encrypt(Plaintext, Key1_init, IP, False)
print(CT)
