import numpy as np
from PIL import Image
import timeit

np.set_printoptions(precision=4, suppress=False)


class AES():
    def __init__(self, iv):
        self.iv = iv


def strToHex(text):
    return hex(int(''.join(text), 2)).upper()[2:]


def hexTStr(text):
    strOut = []
    for i in text:
        strOut.append(chr(int(i, 16)))

    return ''.join(strOut)


def intToex(text):
    hexOut = []
    for i in text:
        hexOut.append(hex(i).upper()[2:])

    return hexOut


def hexTont(text):
    intOut = []
    for i in text:
        intOut.append(int(i, 16))

    return intOut


def hexToHex(text):
    for i in range(len(text)):
        text[i] = text[i][2:]

    return text


def hexToHex2D(text):
    for i in range(len(text)):
        for j in range(len(text[i])):
            text[i][j] = text[i][j][2:]

    return text


def sBox(sbox, byte):
    subByte = []
    for j in range(len(byte)):
        subByte.append([byte[j][i:i + 2] for i in range(0, len(byte[j]), 2)])
    for i in range(len(subByte)):
        for j in range(len(subByte)):
            x = int(subByte[i][j][0], 16)
            y = int(subByte[i][j][1], 16)

            subByte[i][j] = sbox[x][y]

    for i in range(len(subByte)):
        subByte[i] = ''.join(subByte[i])
    return subByte


# TODO change to read column not row
def shiftRow(byte):
    # temp = []
    # lByte = []
    #
    # for i in range(len(byte)):
    #     for j in range(0, len(byte[i]), 2):
    #         temp.append(''.join(list(byte[i])[j:j + 2]))
    #     lByte.append(temp)
    #     temp = []
    #
    # for i in range(len(lByte)):
    #     for j in range(len(lByte[i])):
    #         temp.append(lByte[j][i])

    for i in range(len(byte)):
        byte[i] = ''.join(
            hex(int(''.join(np.roll(np.array(list(bin(int(byte[i], 16))[2:].zfill(32))), -(i * 8))), 2)).upper()
            [2:].zfill(8))

    return byte


# TODO change to read column not row
def shiftRowInv(byte):
    for i in range(len(byte)):
        byte[i] = np.roll(byte[i], i)

    return byte


# def mixColumns(byte):
#     mixCol = []
#     for j in range(len(byte)):
#         mixCol.append([byte[j][i:i + 2] for i in range(0, len(byte[j]), 2)])
#
#     for i in range(len(mixCol)):
#         mixCol[0][i] = strToHex(xor(bitShift2(byte[0][i]), xor(bitShift3(byte[1][i]), xor(np.array(
#             list(bin(int(byte[2][i], 16))[2:].zfill(8))), np.array(
#             list(bin(int(byte[3][i], 16))[2:].zfill(8))))))).zfill(2)
#
#         mixCol[1][i] = strToHex(
#             xor(np.array(list(bin(int(byte[0][i], 16))[2:].zfill(8))), xor(bitShift2(byte[1][i]), xor(bitShift3(
#                 byte[2][i]), np.array(list(
#                 bin(int(
#                     byte[3][i],
#                     16))[
#                 2:].zfill(
#                     8))))))).zfill(2)
#
#         mixCol[2][i] = strToHex(xor(np.array(list(bin(int(byte[0][i], 16))[2:].zfill(8))),
#                                     xor(np.array(list(bin(int(byte[1][i], 16))[2:].zfill(8))),
#                                         xor(bitShift2(byte[2][i]), bitShift3(byte[3][i]))))).zfill(2)
#
#         mixCol[3][i] = strToHex(
#             xor(bitShift3(byte[0][i]), xor(np.array(list(bin(int(byte[1][i], 16))[2:].zfill(8))), xor(np.array(
#                 list(bin(int(byte[2][i], 16))[2:].zfill(8))), bitShift2(byte[3][i]))))).zfill(2)
#
#     for i in range(len(mixCol)):
#         mixCol[i] = ''.join(mixCol[i])
#
#     return mixCol
#
#
# def bitShift2(hNum):
#     # GF = np.array(['0', '0', '0', '1', '1', '0', '1', '1'])
#     # bNum = np.array(list(bin(int(hNum, 16))[2:].zfill(8)))
#     #
#     # if bNum[0] == '1':
#     #     bNum = np.roll(bNum, -1)
#     #     bNum[7] = 0
#     #     return xor(bNum, GF)
#     #
#     # else:
#     #     bNum = np.roll(bNum, -1)
#     #     bNum[7] = 0
#     #
#     #     return ''.join(bNum)
#     GF = np.array(['0', '0', '0', '1', '1', '0', '1', '1'])
#     bNum = np.array(list(bin(int(hNum, 16))[2:].zfill(8)))
#
#     if bNum[0] == '1':
#         bNum = np.roll(bNum, -1)
#         bNum[7] = 0
#         bNum = xor(bNum, GF)
#         return hex(int(''.join(bNum), 2))[2:].zfill(2)
#
#     else:
#         bNum = np.roll(bNum, -1)
#         bNum[7] = 0
#
#         # return bNum
#         return hex(int(''.join(bNum), 2))[2:].zfill(2)
#
#
# def bitShift3(hNum):
#     return xor(np.array(list(bin(int(hNum, 16))[2:].zfill(8))), bitShift2(hNum))


def xor(hNum1, hNum2):
    hNum1 = np.array(list(bin(int(hNum1, 16))[2:].zfill(8)))
    hNum2 = np.array(list(bin(int(hNum2, 16))[2:].zfill(8)))
    result = np.array([], dtype=int)
    for i in range(len(hNum1)):
        result = np.append(result, np.bitwise_xor(int(hNum1[i]), int(hNum2[i])))

    return hex(int(''.join(result.astype(str)), 2)).upper()[2:].zfill(2)


def addRoundKey(state, rKey):
    result = np.empty_like(state)

    for i in range(len(result)):
        result[i] = strToHex(xor(np.array(list(bin(int(state[i], 16))[2:].zfill(32))),
                                 np.array(list(bin(int(rKey[i], 16))[2:].zfill(32))))).zfill(8)

    # for i in range(len(result)):
    #     for j in range(len(result[0])):
    #         result[i][j] = strToHex(xor(np.array(list(bin(int(state[i][j], 16))[2:].zfill(8))),
    #                                     np.array(list(bin(int(rKey[i][j], 16))[2:].zfill(8)))))

    return result


def expandKey(key, sbox):
    # nK = 8
    nK = 4
    rCon = np.array(['01000000', '02000000', '04000000', '08000000', '10000000', '20000000', '40000000', '80000000',
                     '1B000000', '36000000', '6C000000', 'D8000000', 'AB000000', '4D000000', '9A000000', '2F000000'])
    temp = ''
    # w = [0] * 60
    w = [0] * 44
    for i in range(nK):
        w[i] = key[4 * i] + key[4 * i + 1] + key[4 * i + 2] + key[4 * i + 3]

    # for i in range(nK, 60):
    #     # print("i\t\t\t\t\t", i)
    #     temp = w[i - 1]
    #     # print("Temp\t\t\t\t", temp)
    #
    #     if i % nK == 0:
    #         rot = rotWord(temp)
    #         # print("After RotWord\t\t", rot)
    #         t = sBoxExpandKey(sbox, rot)
    #         # print("After SubWord\t\t", t)
    #         # print("Rcon\t\t\t\t", rCon[(i // nK) - 1])
    #         temp = ''.join(hex(int(''.join(
    #             xor(np.array(list(bin(int(sBoxExpandKey(sbox, rotWord(temp)), 16))[2:].zfill(32))),
    #                 np.array(list(bin(int(rCon[(i // nK) - 1], 16))[2:].zfill(32))))), 2)).upper()[2:].zfill(8))
    #         # print("After XOR with Rcon\t", temp)
    #
    #     elif nK > 6 and i % nK == 4:
    #         temp = sBoxExpandKey(sbox, temp)
    #
    #     # print("w[i-NK]\t\t\t\t", w[i - nK])
    #
    #     w[i] = ''.join(hex(int(''.join(
    #         xor(np.array(list(bin(int(w[i - nK], 16))[2:].zfill(32))),
    #             np.array(list(bin(int(temp, 16))[2:].zfill(32))))), 2)).upper()[2:].zfill(8))
    #     # print("w[i]\t\t\t\t", w[i], "\n\n")
    for i in range(nK, 44):
        # print("i\t\t\t\t\t", i)
        temp = w[i - 1]
        # print("Temp\t\t\t\t", temp)

        if i % nK == 0:
            rot = rotWord(temp)
            # print("After RotWord\t\t", rot)
            t = sBoxExpandKey(sbox, rot)
            # print("After SubWord\t\t", t)
            # print("Rcon\t\t\t\t", rCon[(i // nK) - 1])
            temp = ''.join(hex(int(''.join(
                xor(np.array(list(bin(int(sBoxExpandKey(sbox, rotWord(temp)), 16))[2:].zfill(32))),
                    np.array(list(bin(int(rCon[(i // nK) - 1], 16))[2:].zfill(32))))), 2)).upper()[2:].zfill(8))
            # print("After XOR with Rcon\t", temp)

        # print("w[i-NK]\t\t\t\t", w[i - nK])

        w[i] = ''.join(hex(int(''.join(
            xor(np.array(list(bin(int(w[i - nK], 16))[2:].zfill(32))),
                np.array(list(bin(int(temp, 16))[2:].zfill(32))))), 2)).upper()[2:].zfill(8))
        # print("w[i]\t\t\t\t", w[i], "\n\n")

    # print(w)
    return w


def rotWord(hNum):
    result = np.roll(np.array(list(bin(int(hNum, 16))[2:].zfill(32))), -8)
    hexResult = []

    for i in range(0, len(result), 8):
        temp = ''.join(result[i:i + 8])
        hexResult.append(hex(int(temp, 2)).upper()[2:].zfill(2))

    return ''.join(hexResult)


def sBoxExpandKey(sbox, byte):
    subByte = np.array([byte])
    result = []
    for i in range(0, len(subByte[0]), 2):
        x = int(subByte[0][i], 16)
        y = int(subByte[0][i + 1], 16)

        result.append(sbox[x][y])
    return ''.join(result)


def GF(hNum1, hNum2):
    bNum1 = bin(int(hNum1, 16))[2:].zfill(8)
    bNum2 = np.array(list(bin(int(hNum2, 16))[2:].zfill(8)))

    bMultiply = [0] * len(bNum1)
    bMultiply[0] = bNum1
    # bMultiply[0] = '0' * len(bNum1)

    for i in range(1, len(bNum1)):
        bMultiply[i] = bitShift2(hex(int(bMultiply[i - 1], 2))[2:].zfill(2))

    result = bNum1
    bNum2 = np.flip(bNum2)

    for i in range(1, len(bNum2)):
        if bNum2[i] == '1':
            result = xor(np.array(list(result)), np.array(list(bMultiply[i])))

    # print(result)
    return np.array(list(result))


def AES_Encrypt(inspect_mode, plaintext, iv, key, sbox_array):
    iv = hexToHex(iv)
    sbox_array = hexToHex2D(sbox_array)

    temp = expandKey(key, sbox_array)
    key = []
    for i in range(0, len(temp), 4):
        key.append(temp[i:i + 4])
    key = np.asarray(key)

    temp = plaintext
    plaintext = []
    for i in range(0, len(temp), 4):
        plaintext.append(''.join(temp[i:i + 4]))
    plaintext = np.asarray(plaintext)

    print("Round[0].input\t\t\t", plaintext)
    print("Round[0].k_sch\t\t\t", key[0])

    state = addRoundKey(plaintext, key[0])
    print("Round[0].start\t\t\t", state)

    for rNum in range(1, 10):
        state = sBox(sbox_array, state)
        print("Round[", rNum, "].s_box\t\t", state)

        state = shiftRow(state)
        print("Round[", rNum, "].s_row\t\t", state)

        state = mixColumns(state)
        print("Round[", rNum, "].m_col\t\t", state)

        state = addRoundKey(state, key[rNum])
        print("Round[", rNum, "].k_sch\t\t", state)

    state = sBox(sbox_array, state)
    print("Round[14].s_box\t\t\t", state)

    state = shiftRow(state)
    print("Round[14].s_row\t\t\t", state)

    state = addRoundKey(state, key[10])
    print("Round[14].k_sch\t\t\t", state)


def AES_Decrypt(inspect_mode, ciphertext, iv, key, inv_sbox_array):
    pass


def Testing():
    pText = "Testing if the encryption algorithm works properly"
    kText = "I am the key"
    pHex = np.array(['00', '11', '22', '33', '44', '55', '66', '77', '88', '99', 'AA', 'BB', 'CC', 'DD', 'EE', 'FF'])
    kHex = np.array(['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0A', '0B', '0C', '0D', '0E', '0F',
                     '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D', '1E', '1F'])
    # pHex = np.array(['01', '23', '45', '67', '89', 'AB', 'CD', 'EF', 'FE', 'DC', 'BA', '98', '76', '54', '32', '10'])
    # kHex = np.array(['0F', '15', '71', 'C9', '47', 'D9', 'E8', '59', '0C', 'B7', 'AD', 'D6', 'AF', '7F', '67', '98'])
    # pImg = Image.open('circuit_low.png')
    inspect = False
    ivFile = np.load('AES_CBC_IV.npy')
    # ivFile = None
    sboxFile = np.load('AES_Sbox_lookup.npy')
    invSboxFile = np.load('AES_Inverse_Sbox_lookup.npy')

    eText = AES_Encrypt(inspect, pHex, ivFile, kHex, sboxFile)


print(xor('57', '87'))
# start = timeit.default_timer()
# Testing()
# print("Done in ", timeit.default_timer() - start, "s\n")
# temp = ['0', '0', '1', '0', '1', '1', '0', '0']
# temp = '31'
# temp2 = [temp]
# for i in range(len(temp) * 8):
#     temp = bitShift2(temp)
#     temp2.append(bitShift2(temp2[i]))
# print(temp)
# print(temp2)

# print(hex(int(''.join(GF('53', '83')), 2))[2:].zfill(2))
# print(hex(int(''.join(GF('83', '53')), 2))[2:].zfill(2))
#
# print(GF('02', '87'))
# print(GF('87', '02'))
#
# print(GF('03', '6E'))
# print(GF('6E', '03'))
#
# print(GF('46', '01'))
# print(GF('01', '46'))

# print(xor(GF('87', '02'), xor(GF('6E', '03'), xor(GF('46', '00'), GF('A6', '00')))))
# print(hex(int(xor(GF('87', '02'), xor(GF('6E', '03'), xor(GF('46', '00'), GF('A6', '00')))), 2))[2:])
# print(xor(GF('02', '87'), xor(GF('03', '6E'), xor(GF('46', '00'), GF('A6', '00')))))
# print(hex(int(xor(GF('02', '87'), xor(GF('03', '6E'), xor(GF('46', '00'), GF('A6', '00')))), 2))[2:])
# print(xor(GF('02', '87'), xor(GF('6E', '03'), xor(GF('46', '00'), GF('A6', '00')))))
# print(hex(int(xor(GF('02', '87'), xor(GF('6E', '03'), xor(GF('46', '00'), GF('A6', '00')))), 2))[2:])

# print(xor(GF('02', '87'), xor(GF('6E', '03'), xor(GF('46', '01'), GF('A6', '01')))))
# print(hex(int(xor(GF('02', '87'), xor(GF('6E', '03'), xor(GF('46', '01'), GF('A6', '01')))), 2))[2:])
#
# print(xor(GF('87', '01'), xor(GF('02', '6E'), xor(GF('46', '03'), GF('A6', '01')))))
# print(hex(int(xor(GF('87', '01'), xor(GF('02', '6E'), xor(GF('46', '03'), GF('A6', '01')))), 2))[2:])
#
# print(xor(GF('87', '01'), xor(GF('6E', '01'), xor(GF('46', '02'), GF('A6', '03')))))
# print(hex(int(xor(GF('87', '01'), xor(GF('6E', '01'), xor(GF('46', '02'), GF('A6', '03')))), 2))[2:])
#
# print(xor(GF('87', '03'), xor(GF('6E', '01'), xor(GF('46', '01'), GF('02', 'A6')))))
# print(hex(int(xor(GF('87', '03'), xor(GF('6E', '01'), xor(GF('46', '01'), GF('02', 'A6')))), 2))[2:])
# hNum1 = '31'
# hNum2 = 'AC'
# hNum3 = '46'
# hNum4 = '6A'
#
# hMul1 = '0E'
# hMul2 = '0B'
# hMul3 = '0D'
# hMul4 = '09'
#
# temp1 = bin(int(hNum1, 16))[2:].zfill(8)
# temp2 = bin(int(hMul1, 16))[2:].zfill(8)
# temp3 = temp1 * temp2
# temp4 = hex(temp3 % 2)
# print(temp4)
# s0 = hex((int(hNum1, 16) * int(hMul1, 16)))[2:].zfill(2)
# print(s0)
# s1 = xor(
#     xor(xor(xor(xor(xor(bitShift2(hNum1), bitShift2(hNum1)), bitShift2(hNum1)), bitShift2(hNum1)), bitShift2(hNum1)),
#         bitShift2(hNum1)), bitShift2(hNum1))
# print(strToHex(s1))


# x = np.array(['60', '3D', 'EB', '10', '15', 'CA', '71', 'BE', '2B', '73', 'AE', 'F0', '85', '7D', '77', '81',
#               '1F', '35', '2C', '07', '3B', '61', '08', 'D7', '2D', '98', '10', 'A3', '09', '14', 'DF', 'F4'])
# sboxFile = np.load('AES_Sbox_lookup.npy')
# expandKey(x, hexToHex2D(sboxFile))
# state = np.array([['47', '40', 'A3', '4C'],
#                   ['37', 'D4', '70', '9F'],
#                   ['94', 'E4', '3A', '42'],
#                   ['ED', 'A5', 'A6', 'BC']])
#
# key = np.array([['AC', '19', '28', '57'],
#                 ['77', 'FA', 'D1', '5C'],
#                 ['66', 'DC', '29', '00'],
#                 ['F3', '21', '41', '6A']])
#
# print(addRoundKey(state, key))
# x = np.array(
#     ['0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '1', '1',
#     '1', '0', '0', '0', '0', '0', '1', '1', '1', '0'])
# y = np.array(['0', '0', '0', '1', '1', '0', '1', '1'])
#
# temp = xor(x, y)
# print(temp)
# print(bitShift3('6E'))
# sboxFile = np.load('AES_Sbox_lookup.npy')
# invSboxFile = np.load('AES_Inv_Sbox_lookup.npy')
# test = np.array([['EA', '04', '65', '85'],
#                  ['83', '45', '5D', '96'],
#                  ['5C', '33', '98', 'B0'],
#                  ['F0', '2D', 'AD', 'C5']])
# temp = np.array(test)
# temp = test
# print(test)
# print(temp)
# temp[2][3] = 'DD'
# print(test)
# print(temp)

# subBytes = sBox(hexToHex2D(sboxFile), test)
# invSubBytes = sBox(hexToHex2D(invSboxFile), subBytes)
# print(test)
# print(subBytes)
# print(invSubBytes)
# x = np.arange(16)
# print(x)
# x = x.reshape((4, 4))
# print(x)
# x = shiftRow(x)
# print(x)
# x = shiftRowInv(x)
# print(x)
# temp = np.array([['0x52', '0x09', '0x6A', '0xD5', '0x30', '0x36', '0xA5', '0x38', '0xBF', '0x40', '0xA3', '0x9E',
#                   '0x81', '0xF3', '0xD7', '0xFB'],
#                  ['0x7C', '0xE3', '0x39', '0x82', '0x9B', '0x2F', '0xFF', '0x87', '0x34', '0x8E', '0x43', '0x44',
#                   '0xC4', '0xDE', '0xE9', '0xCB'],
#                  ['0x54', '0x7B', '0x94', '0x32', '0xA6', '0xC2', '0x23', '0x3D', '0xEE', '0x4C', '0x95', '0x0B',
#                   '0x42', '0xFA', '0xC3', '0x4E'],
#                  ['0x08', '0x2E', '0xA1', '0x66', '0x28', '0xD9', '0x24', '0xB2', '0x76', '0x5B', '0xA2', '0x49',
#                   '0x6D', '0x8B', '0xD1', '0x25'],
#                  ['0x72', '0xF8', '0xF6', '0x64', '0x86', '0x68', '0x98', '0x16', '0xD4', '0xA4', '0x5C', '0xCC',
#                   '0x5D', '0x65', '0xB6', '0x92'],
#                  ['0x6C', '0x70', '0x48', '0x50', '0xFD', '0xED', '0xB9', '0xDA', '0x5E', '0x15', '0x46', '0x57',
#                   '0xA7', '0x8D', '0x9D', '0x84'],
#                  ['0x90', '0xD8', '0xAB', '0x00', '0x8C', '0xBC', '0xD3', '0x0A', '0xF7', '0xE4', '0x58', '0x05',
#                   '0xB8', '0xB3', '0x45', '0x06'],
#                  ['0xD0', '0x2C', '0x1E', '0x8F', '0xCA', '0x3F', '0x0F', '0x02', '0xC1', '0xAF', '0xBD', '0x03',
#                   '0x01', '0x13', '0x8A', '0x6B'],
#                  ['0x3A', '0x91', '0x11', '0x41', '0x4F', '0x67', '0xDC', '0xEA', '0x97', '0xF2', '0xCF', '0xCE',
#                   '0xF0', '0xB4', '0xE6', '0x73'],
#                  ['0x96', '0xAC', '0x74', '0x22', '0xE7', '0xAD', '0x35', '0x85', '0xE2', '0xF9', '0x37', '0xE8',
#                   '0x1C', '0x75', '0xDF', '0x6E'],
#                  ['0x47', '0xF1', '0x1A', '0x71', '0x1D', '0x29', '0xC5', '0x89', '0x6F', '0xB7', '0x62', '0x0E',
#                   '0xAA', '0x18', '0xBE', '0x1B'],
#                  ['0xFC', '0x56', '0x3E', '0x4B', '0xC6', '0xD2', '0x79', '0x20', '0x9A', '0xDB', '0xC0', '0xFE',
#                   '0x78', '0xCD', '0x5A', '0xF4'],
#                  ['0x1F', '0xDD', '0xA8', '0x33', '0x88', '0x07', '0xC7', '0x31', '0xB1', '0x12', '0x10', '0x59',
#                   '0x27', '0x80', '0xEC', '0x5F'],
#                  ['0x60', '0x51', '0x7F', '0xA9', '0x19', '0xB5', '0x4A', '0x0D', '0x2D', '0xE5', '0x7A', '0x9F',
#                   '0x93', '0xC9', '0x9C', '0xEF'],
#                  ['0xA0', '0xE0', '0x3B', '0x4D', '0xAE', '0x2A', '0xF5', '0xB0', '0xC8', '0xEB', '0xBB', '0x3C',
#                   '0x83', '0x53', '0x99', '0x61'],
#                  ['0x17', '0x2B', '0x04', '0x7E', '0xBA', '0x77', '0xD6', '0x26', '0xE1', '0x69', '0x14', '0x63',
#                  '0x55', '0x21', '0x0C', '0x7D']])
# np.save('AES_Inv_Sbox_lookup.npy', temp)
# print(temp)
