import numpy as np
from PIL import Image
import random
from timeit import default_timer

np.set_printoptions(precision=4, suppress=False, threshold=100000)


class AES():
    def __init__(self, iv):
        self.iv = iv


IV = AES('')

Galois_Field = np.load('Galois_Field.npy')


def hexToHex(text):
    for i in range(len(text)):
        text[i] = text[i].upper()[2:]

    return text


def hexToHex2D(text):
    for i in range(len(text)):
        for j in range(len(text[i])):
            text[i][j] = text[i][j].upper()[2:]

    return text


def npBin2Hex(bNum):
    return np.array(list(hex(int(bNum, 2)).upper()[2:].zfill(2)))


def bin2Hex(bNum):
    return hex(int(bNum, 2)).upper()[2:].zfill(len(bNum) // 4)


def npHex2Bin(hNum):
    return np.array(list(bin(int(hNum, 16))[2:].zfill(len(hNum) * 4)))


def hex2Bin(hNum):
    return bin(int(hNum, 16))[2:].zfill(8)


def hexToStr(text):
    text = np.asarray(stateResize(text, 2)).reshape((len(text) // 2))

    return ''.join(chr(int(i, 16)) for i in text)


def strToHex(text):
    hexOut = []
    for i in text:
        hexOut.append(hex(ord(i)).upper()[2:].zfill(2))

    return hexOut


def intToHex(text):
    hexOut = []
    for i in text:
        hexOut.append(hex(i).upper()[2:].zfill(2))

    return hexOut


def hexToInt(text):
    intOut = []
    for i in text:
        intOut.append(int(i, 16))

    return intOut


# print(npHex2Bin('473794ED'))
# print(hex2Bin('AA'))
#
# print(npBin2Hex(hex2Bin('AA')))
# print(bin2Hex(hex2Bin('AA')))


def xor(hNum1, hNum2):
    # bNum1 = npHex2Bin(hNum1)
    # bNum2 = npHex2Bin(hNum2)
    # result = np.array([], dtype=str)
    #
    # for i in range(len(bNum1)):
    #     result = np.append(result, np.bitwise_xor(int(bNum1[i], 2), int(bNum2[i], 2)))
    #
    # return bin2Hex(''.join(result))

    return hex(int(hNum1, 16) ^ int(hNum2, 16)).upper()[2:].zfill(len(hNum1))


def xorArray(hList1, hList2):
    return stateResize(hex(int(''.join(hList1), 16) ^ int(''.join(hList2), 16)).upper()[2:].zfill(len(
        ''.join(hList1))), 8)


# print(xor('47', 'AC'))


def addRoundKey(state, key):
    result = np.empty_like(state)

    for i in range(len(result)):
        result[i] = xor(''.join(state[i]), ''.join(key[i]))

    return np.asarray(result)


# state = np.array(['473794ED',
#                   '40D4E4A5',
#                   'A3703AA6',
#                   '4C9F42BC'])
#
# key = np.array(['AC7766F3',
#                 '19FADC21',
#                 '28D12941',
#                 '575C006A'])
#
# print(addRoundKey(state, key))


def stateResize(state, size):
    hBytes = []
    state = ''.join(state)
    for i in range(0, len(state), size):
        hBytes.append(''.join(state[i:i + size]).zfill(size))

    return np.array(hBytes)


def byteToStr(state):
    for i in range(len(state)):
        state[i] = ''.join(state[i])

    return np.asarray(state)


def sBox(state, sbox):
    # state = np.array(strToByte(''.join(state)))
    state = stateResize(state, 2)
    state = state.reshape((4, 4))
    # t = state
    for i in range(len(state)):
        for j in range(len(state[i])):
            x = int(state[i][j][0], 16)
            y = int(state[i][j][1], 16)

            state[i][j] = sbox[x][y]

    return byteToStr(state.tolist())


# sboxFile = hexToHex2D(np.load('AES_Sbox_lookup.npy'))
#
# state = np.array(['EA835CF0',
#                   '0445332D',
#                   '655D98AD',
#                   '8596B0C5'])
#
# print(sBox(state, sboxFile))


def shiftRow(state):
    state = stateResize(state, 2)
    state = state.reshape((4, 4))
    temp = np.array(state).tolist()

    for i in range(len(temp)):
        for j in range(len(temp[i])):
            state[i][j] = temp[j][i]

    for i in range(len(state)):
        state[i] = np.roll(state[i], -i).tolist()

    temp = np.array(state).tolist()

    for i in range(len(temp)):
        for j in range(len(temp[i])):
            state[i][j] = temp[j][i]

    return byteToStr(state.tolist())


def invShiftRow(state):
    state = stateResize(state, 2)
    state = state.reshape((4, 4))
    temp = np.array(state).tolist()

    for i in range(len(temp)):
        for j in range(len(temp[i])):
            state[i][j] = temp[j][i]

    for i in range(len(state)):
        state[i] = np.roll(state[i], i).tolist()

    temp = np.array(state).tolist()

    for i in range(len(temp)):
        for j in range(len(temp[i])):
            state[i][j] = temp[j][i]

    return byteToStr(state.tolist())


# state = np.array([['87EC4A8C'],
#                   ['F26EC3D8'],
#                   ['4D4C4695'],
#                   ['9790E7A6']])
#
# print(shiftRow(state))


def GF(hNum1, hNum2):
    #     bNum1 = np.flip(npHex2Bin(hNum1))
    #
    #     result = []
    #
    #     for i in range(len(bNum1)):
    #         if bNum1[i] == '1':
    #             result.append(bitShift2(hNum2, i))
    #
    #     if len(result) == 0:
    #         return '00'
    #     elif len(result) == 1:
    #         return result[0]
    #     else:
    #         for i in range(len(result) - 1):
    #             result[i + 1] = xor(result[i], result[i + 1])
    #
    #         return result[len(result) - 1]

    x = 0
    if hNum1 == '01':
        x = 0
    elif hNum1 == '02':
        x = 1
    elif hNum1 == '03':
        x = 2
    elif hNum1 == '09':
        x = 3
    elif hNum1 == '0B':
        x = 4
    elif hNum1 == '0D':
        x = 5
    elif hNum1 == '0E':
        x = 6

    y = int(hNum2, 16)

    temp = Galois_Field[x][y]
    return Galois_Field[x][y]


def mixColumns(state):
    state = stateResize(state, 2)
    state = state.reshape((4, 4))
    temp = np.array(state).tolist()
    galoisMatrix = [['02', '03', '01', '01'],
                    ['01', '02', '03', '01'],
                    ['01', '01', '02', '03'],
                    ['03', '01', '01', '02']]

    for i in range(len(state)):
        state[i][0] = xor(GF(galoisMatrix[0][0], temp[i][0]),
                          xor(GF(galoisMatrix[0][1], temp[i][1]),
                              xor(GF(galoisMatrix[0][2], temp[i][2]), GF(galoisMatrix[0][2], temp[i][3]))))

        state[i][1] = xor(GF(galoisMatrix[1][0], temp[i][0]),
                          xor(GF(galoisMatrix[1][1], temp[i][1]),
                              xor(GF(galoisMatrix[1][2], temp[i][2]), GF(galoisMatrix[1][3], temp[i][3]))))

        state[i][2] = xor(GF(galoisMatrix[2][0], temp[i][0]),
                          xor(GF(galoisMatrix[2][1], temp[i][1]),
                              xor(GF(galoisMatrix[2][2], temp[i][2]), GF(galoisMatrix[2][3], temp[i][3]))))

        state[i][3] = xor(GF(galoisMatrix[3][0], temp[i][0]),
                          xor(GF(galoisMatrix[3][1], temp[i][1]),
                              xor(GF(galoisMatrix[3][2], temp[i][2]), GF(galoisMatrix[3][3], temp[i][3]))))

    return byteToStr(state.tolist())


def invMixColumns(state):
    state = stateResize(state, 2)
    state = state.reshape((4, 4))
    temp = np.array(state).tolist()
    galoisMatrix = [['0E', '0B', '0D', '09'],
                    ['09', '0E', '0B', '0D'],
                    ['0D', '09', '0E', '0B'],
                    ['0B', '0D', '09', '0E']]

    for i in range(len(state)):
        state[i][0] = xor(GF(galoisMatrix[0][0], temp[i][0]),
                          xor(GF(galoisMatrix[0][1], temp[i][1]),
                              xor(GF(galoisMatrix[0][2], temp[i][2]),
                                  GF(galoisMatrix[0][3], temp[i][3]))))

        state[i][1] = xor(GF(galoisMatrix[1][0], temp[i][0]),
                          xor(GF(galoisMatrix[1][1], temp[i][1]),
                              xor(GF(galoisMatrix[1][2], temp[i][2]),
                                  GF(galoisMatrix[1][3], temp[i][3]))))

        state[i][2] = xor(GF(galoisMatrix[2][0], temp[i][0]),
                          xor(GF(galoisMatrix[2][1], temp[i][1]),
                              xor(GF(galoisMatrix[2][2], temp[i][2]),
                                  GF(galoisMatrix[2][3], temp[i][3]))))

        state[i][3] = xor(GF(galoisMatrix[3][0], temp[i][0]),
                          xor(GF(galoisMatrix[3][1], temp[i][1]),
                              xor(GF(galoisMatrix[3][2], temp[i][2]),
                                  GF(galoisMatrix[3][3], temp[i][3]))))

    return byteToStr(state.tolist())


# state = np.array(['02030101',
#                   '01020301',
#                   '01010203',
#                   '03010102'])
# num = 25
# print("Number", end="\n\t")
# for i in range(num):
#     print(i, end="\t")
# print()
#
# print("09", end="\t")
# for i in range(num):
#     print(Galois_Field[0][i], end="\t")
# print()
#
# print("0B", end="\t")
# for i in range(num):
#     print(Galois_Field[1][i], end="\t")
# print()
#
# print("0D", end="\t")
# for i in range(num):
#     print(Galois_Field[2][i], end="\t")
# print()
#
# print("0E", end="\t")
# for i in range(num):
#     print(Galois_Field[6][i], end="\t")
# print()
#
#
# # print(Galois_Field)
# print(invMixColumns(state))


# print(Galois_Field)
# print(GF('02', '87'))
# print()


def rotWord(word):
    return bin2Hex(''.join(np.roll(npHex2Bin(word), -8)))


def sBoxExpandKey(word, sbox):
    word = stateResize(word, 2)
    result = []

    for i in range(len(word)):
        x = int(word[i][0], 16)
        y = int(word[i][1], 16)

        result.append(sbox[x][y])
    return ''.join(result)


def expandKey(key):
    sbox = hexToHex2D(np.load("AES_Sbox_lookup.npy"))
    nK = 8
    rCon = np.array(['01000000', '02000000', '04000000', '08000000', '10000000', '20000000', '40000000', '80000000',
                     '1B000000', '36000000', '6C000000', 'D8000000', 'AB000000', '4D000000', '9A000000', '2F000000'])
    temp = ''
    w = [0] * 60
    for i in range(nK):
        w[i] = key[4 * i] + key[4 * i + 1] + key[4 * i + 2] + key[4 * i + 3]

    for i in range(nK, 60):
        # print("i\t\t\t\t\t", i)
        temp = w[i - 1]
        # print("Temp\t\t\t\t", temp)

        if i % nK == 0:
            # rot = rotWord(temp)
            # print("After RotWord\t\t", rot)
            # t = sBoxExpandKey(rot, sbox)
            # print("After SubWord\t\t", t)
            # print("Rcon\t\t\t\t", rCon[(i // nK) - 1])
            temp = xor(sBoxExpandKey(rotWord(temp), sbox), rCon[(i // nK) - 1])
            # print("After XOR with Rcon\t", temp)

        elif nK > 6 and i % nK == 4:
            temp = sBoxExpandKey(temp, sbox)
            # print("After SubWord\t\t", temp)

        # print("w[i-NK]\t\t\t\t", w[i - nK])

        w[i] = xor(w[i - nK], temp)
        # print("w[i]\t\t\t\t", w[i], "\n\n")

    return w


# x = np.array(['60', '3D', 'EB', '10', '15', 'CA', '71', 'BE', '2B', '73', 'AE', 'F0', '85', '7D', '77', '81',
#               '1F', '35', '2C', '07', '3B', '61', '08', 'D7', '2D', '98', '10', 'A3', '09', '14', 'DF', 'F4'])
# sboxFile = np.load('AES_Sbox_lookup.npy')
# print(stateResize(expandKey(x, hexToHex2D(sboxFile)),8))

def strResizePlaintext(text):
    temp = []
    modLength = len(text) % 16

    if modLength > 0:
        for i in range(16 - modLength):
            text.append('00')

    for i in range(0, len(text), 16):
        temp.append(text[i:i + 16])

    return temp


def strResizeKey(text):
    temp = []
    modLength = len(text) % 32

    if modLength > 0:
        for i in range(32 - modLength):
            text.append('00')

    return text


# def xorArray(hNum1, hNum2):
#     bNum1 = []
#     bNum2 = []
#     temp1 = []
#     temp2 = []
#     for i in range(len(hNum1)):
#         temp1.append(npHex2Bin(hNum1[i]).tolist())
#         temp2.append(npHex2Bin(hNum2[i]).tolist())
#
#     for i in range(len(temp1)):
#         for j in range(len(temp1[i])):
#             bNum1.append(temp1[i][j])
#             bNum2.append(temp2[i][j])
#
#     result = np.array([], dtype=str)
#
#     for i in range(len(bNum1)):
#         result = np.append(result, np.bitwise_xor(int(bNum1[i], 2), int(bNum2[i], 2)))
#
#     return bin2Hex(''.join(result))


def hexToIntFinal(state):
    intOut = []

    for i in range(len(state)):
        intOut.append(int(state[i], 16))

    return intOut


def AES_Encrypt(inspect_mode, plaintext, iv, key, sbox_array):
    isImg = False
    yLength = 0
    xLength = 0
    sizeImgArray = 0

    if type(plaintext) == str:
        plaintext = strResizePlaintext(strToHex(plaintext))
    elif type(plaintext) == np.ndarray:
        isImg = True
        imgArray = []
        # RGB Array
        if plaintext[0][0].size == 3:
            imgArray = plaintext
        # RGB and Alpha Array
        elif plaintext[0][0].size == 4:
            imgArray = np.zeros((len(plaintext), len(plaintext[0]), 3))
            for i in range(len(plaintext)):
                for j in range(len(plaintext[0])):
                    imgArray[i][j] = plaintext[i][j][0:3]

        yLength = len(imgArray)
        xLength = len(imgArray[0])

        sizeImgArray = int(yLength * xLength * 3)
        imgText = np.array(imgArray, dtype=int)
        imgText.resize((1, sizeImgArray))

        plaintext = strResizePlaintext(intToHex(imgText[0]))

    if iv is None:
        IV.iv = []
        for i in range(len(plaintext)):
            IV.iv.append(hex(random.randint(0, 255)).upper()[2:].zfill(2))
    else:
        iv = hexToHex(iv)

    sbox_array = hexToHex2D(sbox_array)
    stateFinal = []
    state = ""
    encryptedFinal = []
    encryptedText = iv
    # plaintext = strResizePlaintext(plaintext.tolist())
    plaintextCopy = plaintext
    key = strResizeKey(strToHex(key))

    # print(len(plaintextCopy))
    # print(key)
    # print(encryptedText)

    temp = expandKey(key)
    key = []
    for i in range(0, len(temp), 4):
        key.append(temp[i:i + 4])
    key = np.asarray(key)

    start = default_timer()
    length = 0
    num = 100000
    for pNum in range(len(plaintextCopy)):
        # if pNum % num == 0:
        #     print("Round ", pNum)
        stateArray = []
        plaintext = xorArray(encryptedText, plaintextCopy[pNum])
        # plaintext = stateResize(plaintextCopy[pNum], 8)

        # print("Round[ 0 ].input\t\t", plaintext)
        # print("Round[ 0 ].k_sch\t\t", key[0])

        state = addRoundKey(plaintext, key[0])

        for rNum in range(1, 14):
            # print("Round[", rNum, "].start\t\t", state)
            stateArray.append(state)

            state = sBox(state, sbox_array)
            # print("Round[", rNum, "].s_box\t\t", state)

            state = shiftRow(state)
            # print("Round[", rNum, "].s_row\t\t", state)

            state = mixColumns(state)
            # print("Round[", rNum, "].m_col\t\t", state)

            state = addRoundKey(state, key[rNum])
            # print("Round[", rNum, "].k_sch\t\t", key[rNum])

        # print("Round[ 14 ].start\t\t", state)
        stateArray.append(state)

        state = sBox(state, sbox_array)
        # print("Round[ 14 ].s_box\t\t", state)

        state = shiftRow(state)
        # print("Round[ 14 ].s_row\t\t", state)

        state = addRoundKey(state, key[14])
        # print("Round[ 14 ].k_sch\t\t", key[14])

        # print("Round[ 14 ].output\t\t", state)

        stateFinal.append(stateArray)
        encryptedText = stateResize(state, 2)
        length += len(encryptedText)
        encryptedFinal.append(''.join(encryptedText))
        # if pNum % num == 0:
        #     print("Round Done in ", default_timer() - start, "s")
        #     print("Encrypted length", len(encryptedFinal), "\n")
        #     start = default_timer()

    if isImg:
        encryptedText = np.array(hexToIntFinal(stateResize(encryptedFinal, 2)))[:sizeImgArray]
        encryptedText.resize((yLength, xLength, 3))
        encryptedText = np.array(encryptedText, dtype=np.uint8)
        if inspect_mode:
            return {"States": stateFinal, "Ciphertext": Image.fromarray(encryptedText)}
        else:
            return Image.fromarray(encryptedText)
    else:
        # print(stateResize(encryptedFinal, 8))
        encryptedFinal = ''.join(encryptedFinal)
        if inspect_mode:
            return {"States": stateFinal, "Ciphertext": hexToStr(encryptedFinal)}
        else:
            return hexToStr(encryptedFinal)


def AES_Decrypt(inspect_mode, ciphertext, iv, key, inv_sbox_array):
    isImg = False
    yLength = 0
    xLength = 0
    sizeImgArray = 0

    if type(ciphertext) == str:
        ciphertext = strResizePlaintext(strToHex(ciphertext))
    elif type(ciphertext) == np.ndarray:
        isImg = True
        imgArray = []
        # RGB Array
        if ciphertext[0][0].size == 3:
            imgArray = ciphertext
        # RGB and Alpha Array
        elif ciphertext[0][0].size == 4:
            imgArray = np.zeros((len(ciphertext), len(ciphertext[0]), 3))
            for i in range(len(ciphertext)):
                for j in range(len(ciphertext[0])):
                    imgArray[i][j] = ciphertext[i][j][0:3]

        yLength = len(imgArray)
        xLength = len(imgArray[0])

        sizeImgArray = int(yLength * xLength * 3)
        imgText = np.array(imgArray, dtype=int)
        imgText.resize((1, sizeImgArray))

        ciphertext = strResizePlaintext(intToHex(imgText[0]))

    if iv is None:
        IV.iv = []
        for i in range(len(ciphertext)):
            IV.iv.append(hex(random.randint(0, 255)).upper()[2:].zfill(2))
    else:
        iv = hexToHex(iv)

    inv_sbox_array = hexToHex2D(inv_sbox_array)
    stateFinal = []
    state = ""
    decryptedFinal = []
    decryptedText = iv

    ciphertextCopy = ciphertext
    key = strResizeKey(strToHex(key))

    # print(len(ciphertextCopy))
    # print(key)
    # print(encryptedText)

    temp = expandKey(key)
    key = []
    for i in range(0, len(temp), 4):
        key.append(temp[i:i + 4])
    key = np.flipud(np.asarray(key))

    start = default_timer()
    length = 0
    lenDText = 0
    num = 100
    for pNum in range(len(ciphertextCopy)):
        # if pNum % num == 0:
        #     print("Round ", pNum)
        stateArray = []

        ciphertext = stateResize(ciphertextCopy[pNum], 8)

        # print("Round[ 0 ].iinput\t\t", ciphertext)
        # print("Round[ 0 ].ik_sch\t\t", key[0])

        state = addRoundKey(ciphertext, key[0])

        for rNum in range(1, 14):
            # print("Round[", rNum, "].istart\t\t", state)
            stateArray.append(state)

            state = invShiftRow(state)
            # print("Round[", rNum, "].is_row\t\t", state)

            state = sBox(state, inv_sbox_array)
            # print("Round[", rNum, "].is_box\t\t", state)

            state = addRoundKey(state, key[rNum])
            # print("Round[", rNum, "].ik_sch\t\t", key[rNum])
            # print("Round[", rNum, "].ik_add\t\t", state)

            state = invMixColumns(state)
            # print("Round[", rNum, "].m_col\t\t", state)

        # print("Round[ 14 ].istart\t\t", state)
        stateArray.append(state)

        state = invShiftRow(state)
        # print("Round[ 14 ].is_row\t\t", state)

        state = sBox(state, inv_sbox_array)
        # print("Round[ 14 ].is_box\t\t", state)

        state = addRoundKey(state, key[14])
        # print("Round[ 14 ].ik_sch\t\t", key[14])

        # print("Round[ 14 ].ioutput\t\t", state)

        if pNum == 0:
            decryptedText = xorArray(state, iv)
        else:
            decryptedText = xorArray(state, ciphertextCopy[pNum - 1])

        stateFinal.append(stateArray)
        decryptedText = stateResize(decryptedText, 2)
        length += len(decryptedText)
        if len(decryptedText) < 16:
            lenDText += len(decryptedText)
            print(f"{pNum} \t {len(decryptedText)}")
        decryptedFinal.append(''.join(decryptedText))
        # if pNum % num == 0:
        #     print("Round Done in ", default_timer() - start, "s")
        #     print("Decrypted length", len(decryptedFinal), "\n")
        #     start = default_timer()
    if isImg:
        decryptedText = np.array(hexToIntFinal(stateResize(decryptedFinal, 2)))[:sizeImgArray]
        decryptedText.resize((yLength, xLength, 3))
        decryptedText = np.array(decryptedText, dtype=np.uint8)
        if inspect_mode:
            return {"States": stateFinal, "Plaintext": Image.fromarray(decryptedText)}
        else:
            return Image.fromarray(decryptedText)
    else:
        decryptedFinal = ''.join(decryptedFinal)
        if inspect_mode:
            return {"States": stateFinal, "Plaintext": hexToStr(decryptedFinal)}
        else:
            return hexToStr(decryptedFinal)


def Testing():
    inspect = False

    # pText = "You won't get me"
    # kText = "I am the key that won't be broke"
    #
    # print(pText)
    # print(len(kText))
    # print(''.join(hexToHex(ivFile)))
    # print(''.join(strToHex(pText)))
    # print(''.join(strToHex(kText)))
    # eText = AES_Encrypt(inspect, pText, np.load('AES_CBC_IV.npy'), kText, np.load('AES_Sbox_lookup.npy'))
    # print(eText)
    # dText = AES_Decrypt(inspect, eText, np.load('AES_CBC_IV.npy'), kText, np.load('AES_Inverse_Sbox_lookup.npy'))
    # print(dText)
    #
    # pHex = np.array(['00', '11', '22', '33', '44', '55', '66', '77', '88', '99', 'AA', 'BB', 'CC', 'DD', 'EE', 'FF'])
    # kHex = np.array(['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0A', '0B', '0C', '0D', '0E', '0F',
    #                  '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D', '1E', '1F'])
    #
    # print(len(pHex))
    # print(len(kHex))
    # print(''.join(hexToHex(ivFile)))
    # print(''.join((pHex)))
    # print(''.join((kHex)))
    # eHex = AES_Encrypt(inspect, pHex, np.load('AES_CBC_IV.npy'), kHex, np.load('AES_Sbox_lookup.npy'))
    # print(eHex)
    #
    # dHex = AES_Decrypt(inspect, eHex, np.load('AES_CBC_IV.npy'), kHex, np.load('AES_Inverse_Sbox_lookup.npy'))
    # print(dHex)
    Imagess = {
        "imgList": ['circuit_small', 'circuit_small_big', 'circuit_low_small', 'circuit_low', 'circuit', 'brain_low',
                    'brain', 'starwars_low', 'starwars'],

        "imgListLow": ['circuit_small', 'circuit_small_big', 'circuit_low_small', 'circuit_low', 'brain_low',
                       'starwars_low'],

        "imgListLarge": ['circuit', 'brain', 'starwars']}

    for i in Imagess["imgListLarge"]:
        print(f"Running {i} now\n")
        start = default_timer()

        pImg = Image.open(i + '.png')
        pImg.show()
        npImg = np.array(pImg)
        kText = "I am the key"

        eImg = AES_Encrypt(inspect, npImg, np.load('AES_CBC_IV.npy'), kText, np.load('AES_Sbox_lookup.npy'))
        eImg.show()
        eImg = np.array(eImg)

        if default_timer() - start > 60:
            print(f"Done encryption in {(default_timer() - start) / 60} minutes")
        else:
            print(f"Done encryption in {default_timer() - start} seconds")

        start = default_timer()

        dImg = AES_Decrypt(inspect, eImg, np.load('AES_CBC_IV.npy'), kText, np.load('AES_Inverse_Sbox_lookup.npy'))
        dImg.show()

        if default_timer() - start > 60:
            print(f"Done decryption in {(default_timer() - start) / 60} minutes\n\n")
        else:
            print(f"Done decryption in {default_timer() - start} seconds\n\n")


start = default_timer()
Testing()
if default_timer() - start > 60:
    print(f"Finally done in {(default_timer() - start) / 60} minutes\n")
else:
    print(f"Finally done in {default_timer() - start} s\n")
