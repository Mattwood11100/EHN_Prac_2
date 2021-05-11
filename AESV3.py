import numpy as np
from PIL import Image
import random
from timeit import default_timer
from datetime import datetime

np.set_printoptions(precision=4, suppress=False, threshold=100000)


# Class for the Initial Vector for the CBC. If the vector provided is
# none or empty then a random IV is created
class AES():
    def __init__(self, iv):
        self.iv = iv


# Initializing the class variable so that it can be used by the
# encryption and decryption algorithms
IV = AES('')

# Loading the look-up table for the Galois Filed Multiplications
Galois_Field = np.load('Galois_Field.npy')


# Helper function that removes the '0x' part from a hex string
# for a 1 dimensional array
def hexToHex(text):
    for i in range(len(text)):
        text[i] = text[i].upper()[2:]

    return text


# Helper function that removes the '0x' part from a hex string
# for a 2 dimensional array
def hexToHex2D(text):
    for i in range(len(text)):
        for j in range(len(text[i])):
            text[i][j] = text[i][j].upper()[2:]

    return text


# Helper function that converts hex numbers to the respective
# ASCII character
def hexToStr(text):
    text = np.asarray(stateResize(text, 2)).reshape((len(text) // 2))

    return ''.join(chr(int(i, 16)) for i in text)


# Helper function that converts the ASCII character to the
# respective hex number
def strToHex(text):
    hexOut = []
    for i in text:
        hexOut.append(hex(ord(i)).upper()[2:].zfill(2))

    return hexOut


# Helper function that converts int numbers to hex numbers, this
# is used when encrypting and decrypting images
def intToHex(text):
    hexOut = []
    for i in text:
        hexOut.append(hex(i).upper()[2:].zfill(2))

    return hexOut


# Helper function that converts hex numbers to int numbers, this
# is used when encrypting and decrypting images
def hexToIntFinal(state):
    intOut = []

    for i in range(len(state)):
        intOut.append(int(state[i], 16))

    return intOut


# Helper function that returns the XOR result of two strings
def xor(hNum1, hNum2):
    return hex(int(hNum1, 16) ^ int(hNum2, 16)).upper()[2:].zfill(len(hNum1))


# Helper function that returns the XOR result of two arrays
def xorArray(hList1, hList2):
    return stateResize(hex(int(''.join(hList1), 16) ^ int(''.join(hList2), 16)).upper()[2:].zfill(len(
        ''.join(hList1))), 8)


# This function is part of the encryption and decryption process,
# the functions returns the result of XORing the provided state
# with the provided key
def addRoundKey(state, key):
    result = np.empty_like(state)

    for i in range(len(result)):
        result[i] = xor(''.join(state[i]), ''.join(key[i]))

    return np.asarray(result)


# Helper function that changes the shape of the state array, the
# size is how many hex numbers must be in each element of the
# returned array
def stateResize(state, size):
    hBytes = []
    state = ''.join(state)
    for i in range(0, len(state), size):
        hBytes.append(''.join(state[i:i + size]).zfill(size))

    return np.array(hBytes)


# Helper function that takes the state array of the form
# "['FE', 'A5', '58', '42']" and returns the elements as
# one continuous string
def byteToStr(state):
    for i in range(len(state)):
        state[i] = ''.join(state[i])

    return np.asarray(state)


# This function is part of the encryption and decryption process,
#  depending on the sbox provided, the sbox is used to substitute
#  the hex numbers in the state array, using the values of the hex
#  number in the state array as the index of the sbox elements.
def sBox(state, sbox):
    state = stateResize(state, 2)
    state = state.reshape((4, 4))
    for i in range(len(state)):
        for j in range(len(state[i])):
            x = int(state[i][j][0], 16)
            y = int(state[i][j][1], 16)

            state[i][j] = sbox[x][y]

    return byteToStr(state.tolist())


# This function is part of the encryption process, it performs
# a circular right shifts on each row of the state array,
# 0 shifts for the first row, 1 shift for the second row,
# 2 shifts for the third row and 3 shifts for the fourth row
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


# This function is part of the decryption process, it performs
# a circular left shifts on each row of the state array,
# 0 shifts for the first row, 1 shift for the second row,
# 2 shifts for the third row and 3 shifts for the fourth row

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


# Helper function that returns the multiplication of two
# hex numbers with in the GF(2^8) field
def GF(hNum1, hNum2):
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

    return Galois_Field[x][y]


# This function is part of the encryption process, it performs
# the required column mixing by using multiplication of the GF(2^8) field.
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


# This function is part of the decryption process, it performs
# the required column mixing by using multiplication of the GF(2^8) field.
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


# Helper function that returns a word that has be circularly left shift once.
def rotWord(word):
    return ''.join(np.roll(stateResize(word, 2), -1).tolist())


# Helper function used to perform the substitution of the elements in the provided word
def sBoxExpandKey(word, sbox):
    word = stateResize(word, 2)
    result = []

    for i in range(len(word)):
        x = int(word[i][0], 16)
        y = int(word[i][1], 16)

        result.append(sbox[x][y])
    return ''.join(result)


# This is used in both encryption and decryption process, in order
# to expand the key to the required length
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
        temp = w[i - 1]

        if i % nK == 0:
            temp = xor(sBoxExpandKey(rotWord(temp), sbox), rCon[(i // nK) - 1])

        elif nK > 6 and i % nK == 4:
            temp = sBoxExpandKey(temp, sbox)

        w[i] = xor(w[i - nK], temp)

    return w


# Helper function that appends the require amount in order to make the plaintext
# length divisible by 16 bytes
def strResizePlaintext(text):
    temp = []
    modLength = len(text) % 16

    if modLength > 0:
        for i in range(16 - modLength):
            text.append('00')

    for i in range(0, len(text), 16):
        temp.append(text[i:i + 16])

    return temp


# Helper function that appends the require amount in order to make the key
# length divisible by 32 bytes
def strResizeKey(text):
    temp = []
    modLength = len(text) % 32

    if modLength > 0:
        for i in range(32 - modLength):
            text.append('00')

    return text


# Helper function that reshapes the state array for printing purposes
def state4x4Print(state):
    state = stateResize(state, 2)
    state = state.reshape((4, 4))
    temp = np.array(state).tolist()

    for i in range(len(temp)):
        for j in range(len(temp[i])):
            state[i][j] = temp[j][i]

    return state.tolist()


# Function that uses CBC AES encryption to encrypt either plaintext messages or png images
def AES_Encrypt(inspect_mode, plaintext, iv, key, sbox_array):
    isImg = False
    yLength = 0
    xLength = 0
    sizeImgArray = 0

    # Checking if the plaintext provided is string message or a png image
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

    # Checking if the IV provided is empty, if so then random bytes are
    # generated otherwise the provided IV is used
    if iv is None or len(iv) == 0:
        IV.iv = []
        for i in range(len(plaintext[0])):
            IV.iv.append(hex(random.randint(0, 255)).upper()[2:].zfill(2))
        iv = IV.iv
        print(f"The random IV is {iv}\n")
    else:
        iv = hexToHex(iv)

    sbox_array = hexToHex2D(sbox_array)
    stateFinal = []
    state = ""
    encryptedFinal = []
    encryptedText = iv

    plaintextCopy = plaintext

    # Expanding the key to required length
    key = strResizeKey(strToHex(key))
    temp = expandKey(key)
    key = []
    for i in range(0, len(temp), 4):
        key.append(temp[i:i + 4])
    key = np.asarray(key)

    # For loop for encrypting each 16 byte piece of the provided plaintext
    for pNum in range(len(plaintextCopy)):
        stateArray = []
        plaintext = xorArray(encryptedText, plaintextCopy[pNum])

        state = addRoundKey(plaintext, key[0])

        # for loop to go through the 14 required rounds for encrypting the provided plaintext
        for rNum in range(1, 14):
            stateArray.append(state4x4Print(state))

            state = sBox(state, sbox_array)

            state = shiftRow(state)

            state = mixColumns(state)

            state = addRoundKey(state, key[rNum])

        state = sBox(state, sbox_array)

        state = shiftRow(state)

        state = addRoundKey(state, key[14])

        stateArray.append(state4x4Print(state))

        stateFinal.append(np.reshape(stateArray, (14, 4, 4)))
        encryptedText = stateResize(state, 2)
        encryptedFinal.append(''.join(encryptedText))

    # Checking if the provided plaintext is an png image,
    # if so then the encrypted text is reshaped and converted to
    # int numbers otherwise the encrypted text is returned
    if isImg:
        encryptedText = np.array(hexToIntFinal(stateResize(encryptedFinal, 2)))[:sizeImgArray]
        encryptedText.resize((yLength, xLength, 3))
        encryptedText = np.array(encryptedText, dtype=np.uint8)
        if inspect_mode:
            return {"States": stateFinal, "Ciphertext": Image.fromarray(encryptedText)}
        else:
            return Image.fromarray(encryptedText)
    else:
        if inspect_mode:
            return {"States": stateFinal, "Ciphertext": hexToStr(''.join(encryptedFinal))}
        else:
            return hexToStr(''.join(encryptedFinal))


# Function that uses CBC AES decryption to decrypt either ciphertext messages or png images
def AES_Decrypt(inspect_mode, ciphertext, iv, key, inv_sbox_array):
    isImg = False
    yLength = 0
    xLength = 0
    sizeImgArray = 0

    # Checking if the plaintext provided is string message or a png image
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

    # Checking if the IV provided is empty, if so then random bytes that were
    # generated during the encryption process are used otherwise the provided IV is used
    if iv is None or len(iv) == 0:
        iv = IV.iv
        print(f"The random IV is {iv}\n")
    else:
        iv = hexToHex(iv)

    inv_sbox_array = hexToHex2D(inv_sbox_array)
    stateFinal = []
    state = ""
    decryptedFinal = []
    decryptedText = iv

    ciphertextCopy = ciphertext

    # Expanding the key to required length
    key = strResizeKey(strToHex(key))
    temp = expandKey(key)
    key = []
    for i in range(0, len(temp), 4):
        key.append(temp[i:i + 4])
    key = np.flipud(np.asarray(key))

    # For loop for encrypting each 16 byte piece of the provided ciphertext
    for pNum in range(len(ciphertextCopy)):
        stateArray = []

        ciphertext = stateResize(ciphertextCopy[pNum], 8)

        state = addRoundKey(ciphertext, key[0])

        # for loop to go through the 14 required rounds for decrypting the provided ciphertext
        for rNum in range(1, 14):
            stateArray.append(state4x4Print(state))

            state = invShiftRow(state)

            state = sBox(state, inv_sbox_array)

            state = addRoundKey(state, key[rNum])

            state = invMixColumns(state)

        state = invShiftRow(state)

        state = sBox(state, inv_sbox_array)

        state = addRoundKey(state, key[14])

        stateArray.append(state4x4Print(state))

        if pNum == 0:
            decryptedText = xorArray(state, iv)
        else:
            decryptedText = xorArray(state, ciphertextCopy[pNum - 1])

        stateFinal.append(np.reshape(stateArray, (14, 4, 4)))
        decryptedText = stateResize(decryptedText, 2)
        decryptedFinal.append(''.join(decryptedText))


    # Checking if the provided ciphertext is an png image,
    # if so then the decrypted text is reshaped and converted to
    # int numbers otherwise the decrypted text is returned
    if isImg:
        decryptedText = np.array(hexToIntFinal(stateResize(decryptedFinal, 2)))[:sizeImgArray]
        decryptedText.resize((yLength, xLength, 3))
        decryptedText = np.array(decryptedText, dtype=np.uint8)
        if inspect_mode:
            return {"States": stateFinal, "Plaintext": Image.fromarray(decryptedText)}
        else:
            return Image.fromarray(decryptedText)
    else:
        if inspect_mode:
            return {"States": stateFinal, "Plaintext": hexToStr(''.join(decryptedFinal))}
        else:
            return hexToStr(''.join(decryptedFinal))


# Testing function
def Testing():
    inspect = True
    ivCBC = True
    doImages = False

    if not inspect:

        pText = "You won't get me"
        kText = "I am the key that won't be broke"
        start = default_timer()
        if not ivCBC:
            eText = AES_Encrypt(inspect, pText, None, kText, np.load('AES_Sbox_lookup.npy'))
            print(f"Encryption\nCiphertext:\n{eText}")

            if default_timer() - start > 60:
                print(
                    f"Done encryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}")
            else:
                print(f"Done encryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}")

            start = default_timer()

            dText = AES_Decrypt(inspect, eText, None, kText,
                                np.load('AES_Inverse_Sbox_lookup.npy'))
            print(f""
                  f"\nDecryption\nPlaintext:\n{dText}")

            if default_timer() - start > 60:
                print(
                    f"Done decryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}\n\n")
            else:
                print(
                    f"Done decryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}\n\n")

        else:

            eText = AES_Encrypt(inspect, pText, np.load('AES_CBC_IV.npy'), kText, np.load('AES_Sbox_lookup.npy'))
            print(eText)

            if default_timer() - start > 60:
                print(
                    f"Done encryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}")
            else:
                print(f"Done encryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}")

            start = default_timer()

            dText = AES_Decrypt(inspect, eText, np.load('AES_CBC_IV.npy'), kText,
                                np.load('AES_Inverse_Sbox_lookup.npy'))
            print(dText)

            if default_timer() - start > 60:
                print(
                    f"Done decryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}\n\n")
            else:
                print(
                    f"Done decryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}\n\n")

        if doImages:
            Images = {
                "imgList": ['circuit_small', 'circuit_small_big', 'circuit_low_small', 'circuit_low', 'circuit',
                            'brain_low',
                            'brain', 'starwars_low', 'starwars'],

                "imgListLow": ['circuit_small', 'circuit_small_big', 'circuit_low_small', 'circuit_low', 'brain_low',
                               'starwars_low'],

                "imgListLarge": ['circuit', 'brain', 'starwars']}

            for i in Images["imgListLow"]:
                print(f"Running {i} now\t{datetime.now().strftime('%H:%M:%S')}\n")
                start = default_timer()

                pImg = Image.open(i + '.png')
                pImg.show()
                npImg = np.array(pImg)
                kText = "I am the key"

                eImg = AES_Encrypt(inspect, npImg, np.load('AES_CBC_IV.npy'), kText, np.load('AES_Sbox_lookup.npy'))
                eImg.show()
                eImg = np.array(eImg)

                if default_timer() - start > 60:
                    print(
                        f"Done encryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}")
                else:
                    print(
                        f"Done encryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}")

                start = default_timer()

                dImg = AES_Decrypt(inspect, eImg, np.load('AES_CBC_IV.npy'), kText,
                                   np.load('AES_Inverse_Sbox_lookup.npy'))
                dImg.show()

                if default_timer() - start > 60:
                    print(
                        f"Done decryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}\n\n")
                else:
                    print(
                        f"Done decryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}\n\n")
    else:
        pText = "You won't get me"
        kText = "I am the key that won't be broke"
        start = default_timer()

        if not ivCBC:
            eText = AES_Encrypt(inspect, pText, None, kText, np.load('AES_Sbox_lookup.npy'))
            print(f"Encryption\nStates:\n{eText['States']}\nCiphertext:\n{eText['Ciphertext']}")

            if default_timer() - start > 60:
                print(
                    f"Done encryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}")
            else:
                print(f"Done encryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}")

            start = default_timer()

            dText = AES_Decrypt(inspect, eText['Ciphertext'], None, kText,
                                np.load('AES_Inverse_Sbox_lookup.npy'))
            print(f""
                  f"\nDecryption\nStates:\n{dText['States']}\nPlaintext:\n{dText['Plaintext']}")

            if default_timer() - start > 60:
                print(
                    f"Done decryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}\n\n")
            else:
                print(
                    f"Done decryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}\n\n")

        else:

            eText = AES_Encrypt(inspect, pText, np.load('AES_CBC_IV.npy'), kText, np.load('AES_Sbox_lookup.npy'))
            print(f"Encryption\nStates:\n{eText['States']}\nCiphertext:\n{eText['Ciphertext']}")

            if default_timer() - start > 60:
                print(
                    f"Done encryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}")
            else:
                print(f"Done encryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}")

            start = default_timer()

            dText = AES_Decrypt(inspect, eText['Ciphertext'], np.load('AES_CBC_IV.npy'), kText,
                                np.load('AES_Inverse_Sbox_lookup.npy'))
            print(f""
                  f"\nDecryption\nStates:\n{dText['States']}\nPlaintext:\n{dText['Plaintext']}")

            if default_timer() - start > 60:
                print(
                    f"Done decryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}\n\n")
            else:
                print(
                    f"Done decryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}\n\n")

        if doImages:
            Images = {
                "imgList": ['circuit_small', 'circuit_small_big', 'circuit_low_small', 'circuit_low', 'circuit',
                            'brain_low',
                            'brain', 'starwars_low', 'starwars'],

                "imgListLow": ['circuit_small', 'circuit_small_big', 'circuit_low_small', 'circuit_low', 'brain_low',
                               'starwars_low'],

                "imgListLarge": ['circuit', 'brain', 'starwars']}

            for i in Images["imgListLow"]:
                print(f"Running {i} now\t{datetime.now().strftime('%H:%M:%S')}\n")
                start = default_timer()

                pImg = Image.open(i + '.png')
                pImg.show()
                npImg = np.array(pImg)
                kText = "I am the key"

                eImg = AES_Encrypt(inspect, npImg, np.load('AES_CBC_IV.npy'), kText, np.load('AES_Sbox_lookup.npy'))
                print(f"States:\n{eImg['States']}")
                eImg['Ciphertext'].show()
                eImg['Ciphertext'] = np.array(eImg)

                if default_timer() - start > 60:
                    print(
                        f"Done encryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}")
                else:
                    print(
                        f"Done encryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}")

                start = default_timer()

                dImg = AES_Decrypt(inspect, eImg, np.load('AES_CBC_IV.npy'), kText,
                                   np.load('AES_Inverse_Sbox_lookup.npy'))
                print(f"States:\n{dImg['States']}")
                dImg['Ciphertext'].show()

                if default_timer() - start > 60:
                    print(
                        f"Done decryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}\n\n")
                else:
                    print(
                        f"Done decryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}\n\n")


start = default_timer()
Testing()
if default_timer() - start > 60:
    print(f"Finally finished in {(default_timer() - start) / 60} minutes at"
          f" {datetime.now().strftime('%H:%M:%S')}\n\n")
else:
    print(f"Finally finished in {default_timer() - start} seconds a"
          f"t {datetime.now().strftime('%H:%M:%S')}\n\n")
