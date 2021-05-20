import numpy as np
from PIL import Image
from timeit import default_timer
from datetime import datetime

np.set_printoptions(precision=4, suppress=True)


# Helper function the converts strings to hex numbers
def strToHex(text):
    hexOut = []
    for i in text:
        hexOut.append(hex(ord(i)).upper()[2:])

    return hexOut


# Helper function the converts hex numbers to strings
def hexToStr(text):
    strOut = []
    for i in text:
        strOut.append(chr(int(i, 16)))

    return ''.join(strOut)


# Helper function that converts int numbers to hex numbers
def intToHex(text):
    hexOut = []
    for i in text:
        hexOut.append(hex(i).upper()[2:])

    return hexOut


# Helper function that converts hex numbers to int numbers
def hexToInt(text):
    intOut = []
    for i in text:
        intOut.append(int(i, 16))

    return intOut


# Helper function that reshapes the state array for printing purposes
def state16x16Print(state):
    # state = state.reshape((16, 16))
    return state.reshape((16, 16)).tolist()


# Function that uses the RC4 stream cipher encryption method to
# encrypt plaintext messages or png images
def RC4_Encrypt(inspect_mode, plaintext, key):
    bits = 256
    sTemp = []
    sTable = []
    # Creating the initial variables
    S = []
    # S = np.asarray(S)
    T = []
    # T = np.asarray(T)
    K = list(strToHex(key))
    # K = np.asarray(K)

    # print("S\n", S)
    # print("T\n", T)
    # print("K\n", K)

    # Initializing the variables
    for i in range(bits):
        S.append(hex(i).upper()[2:].zfill(2))
        T.append(K[i % len(key)])
    S = np.asarray(S)
    T = np.asarray(T)
    # print("S\n", S)
    # print("T\n", T)

    # Initial permutation of S
    j = 0
    for i in range(bits):
        j = (j + int(S[i], 16) + int(T[i], 16)) % bits
        temp = S[i]
        S[i] = S[j]
        S[j] = temp

    # print("Encryption S\n", state16x16Print(S))

    # Checking if the plaintext provided is of type string or ndarray
    if type(plaintext) == str:
        hText = np.asarray(strToHex(plaintext))
        # print("Hex Text\n", hText)

        i = 0
        j = 0
        encryptText = []
        kStream = []
        for m in range(len(plaintext)):
            if inspect_mode:
                sTemp.append(state16x16Print(S))
            i = (i + 1) % bits
            j = (j + int(S[i], 16)) % bits

            temp = S[i]
            S[i] = S[j]
            S[j] = temp

            t = (int(S[i], 16) + int(S[j], 16)) % bits
            k = str(S[t])
            kStream.append(k)

            encryptText.append(hex(int(hText[m], 16) ^ int(k, 16)).upper()[2:])

        # print("k\n", kStream)
        # print("Encrypt Text\n", encryptText)
        if inspect_mode:
            sTable.append(np.reshape(sTemp, (len(plaintext), 16, 16)))
        encryptText = hexToStr(encryptText)
        # print("Encrypt Text String\n", encryptText)

        # Checking if inspect mode is true, if so then the dictionary
        # is returned otherwise just the encrypted text is returned
        if inspect_mode:
            return {"S-table": sTable, "Ciphertext": encryptText}
        else:
            return encryptText

    elif type(plaintext) == np.ndarray:
        yLength = len(plaintext)
        xLength = len(plaintext[0])
        sizeImgArray = int(yLength * xLength * 3)
        sizeImgRGB = int(yLength * xLength)
        imgArray = []
        imgR = []
        imgG = []
        imgB = []
        for i in range(yLength):
            for j in range(xLength):
                imgR.append(plaintext[i][j][0])
                imgG.append(plaintext[i][j][1])
                imgB.append(plaintext[i][j][2])

        imgArray.append(imgR)
        imgArray.append(imgG)
        imgArray.append(imgB)
        imgArray = np.asarray(imgArray).reshape((1, sizeImgArray))

        hImg = intToHex(imgArray[0])

        i = 0
        j = 0
        encryptImgHex = []
        kStream = []
        for m in range(sizeImgArray):
            if inspect_mode:
                sTemp.append(state16x16Print(S))

            i = (i + 1) % bits
            j = (j + int(S[i], 16)) % bits

            temp = S[i]
            S[i] = S[j]
            S[j] = temp

            t = (int(S[i], 16) + int(S[j], 16)) % bits
            k = str(S[t])
            kStream.append(k)

            encryptImgHex.append(hex(int(hImg[m], 16) ^ int(k, 16)).upper()[2:])

        # print("k\n", kStream[:25])
        # print("Encrypt Text\n", encryptImgHex[:25])
        if inspect_mode:
            sTable.append(np.reshape(sTemp, (len(encryptImgHex), 16, 16)))

        encryptImg = np.asarray(hexToInt(encryptImgHex))
        temp = []
        for i in range(sizeImgRGB):
            temp.append([encryptImg[i], encryptImg[i + sizeImgRGB], encryptImg[i + (2 * sizeImgRGB)]])
        encryptImg = np.asarray(temp)
        encryptImg.resize((yLength, xLength, 3))
        encryptImg = np.array(encryptImg, dtype=np.uint8)

        # print("Encrypt Image\n", encryptImg)

        # Checking if inspect mode is true, if so then the dictionary
        # is returned otherwise just the encrypted images is returned
        if inspect_mode:
            return {"S-table": sTable, "Ciphertext": Image.fromarray(encryptImg)}
        else:
            return Image.fromarray(encryptImg)


def RC4_Decrypt(inspect_mode, ciphertext, key):
    bits = 256
    sTable = []
    sTemp = []
    # Creating the initial variables
    S = []
    T = []
    K = list(strToHex(key))
    # print("S\n", S)
    # print("T\n", T)
    # print("K\n", K)

    # Initializing the variables
    for i in range(bits):
        S.append(hex(i).upper()[2:].zfill(2))
        T.append(K[i % len(key)])
    S = np.asarray(S)
    T = np.asarray(T)
    # print("S\n", S)
    # print("T\n", T)

    # Initial permutation of S
    j = 0
    for i in range(bits):
        j = (j + int(S[i], 16) + int(T[i], 16)) % bits
        temp = S[i]
        S[i] = S[j]
        S[j] = temp

    # print("Decryption S\n", S)

    # Checking if the plaintext provided is of type string or ndarray
    if type(ciphertext) == str:
        hText = strToHex(ciphertext)
        # print("Hex Text\n", hText)

        i = 0
        j = 0
        decryptText = []
        kStream = []
        for m in range(len(ciphertext)):
            if inspect_mode:
                sTemp.append(state16x16Print(S))

            i = (i + 1) % bits
            j = (j + int(S[i], 16)) % bits

            temp = S[i]
            S[i] = S[j]
            S[j] = temp

            t = (int(S[i], 16) + int(S[j], 16)) % bits
            k = str(S[t])
            kStream.append(k)

            decryptText.append(hex(int(hText[m], 16) ^ int(k, 16)).upper()[2:])

        # print("k\n", kStream)
        # print("Decrypt Text\n", decryptText)
        if inspect_mode:
            sTable.append(np.reshape(sTemp, (len(ciphertext), 16, 16)))

        decryptText = hexToStr(decryptText)
        # print("Decrypt Text String\n", decryptText)

        # Checking if inspect mode is true, if so then the dictionary
        # is returned otherwise just the decrypted text is returned
        if inspect_mode:
            return {"S-table": sTable, "Plaintext": decryptText}
        else:
            return decryptText

    elif type(ciphertext) == np.ndarray:
        yLength = len(ciphertext)
        xLength = len(ciphertext[0])
        sizeImgArray = int(yLength * xLength * 3)
        sizeImgRGB = int(yLength * xLength)
        imgArray = []
        imgR = []
        imgG = []
        imgB = []
        for i in range(yLength):
            for j in range(xLength):
                imgR.append(ciphertext[i][j][0])
                imgG.append(ciphertext[i][j][1])
                imgB.append(ciphertext[i][j][2])

        imgArray.append(imgR)
        imgArray.append(imgG)
        imgArray.append(imgB)
        imgArray = np.asarray(imgArray).reshape((1, sizeImgArray))

        hImg = intToHex(imgArray[0])
        # print("Hex Img\n", hImg)

        i = 0
        j = 0
        decryptImgHex = []
        kStream = []
        for m in range(sizeImgArray):
            if inspect_mode:
                sTemp.append(state16x16Print(S))

            i = (i + 1) % bits
            j = (j + int(S[i], 16)) % bits

            temp = S[i]
            S[i] = S[j]
            S[j] = temp

            t = (int(S[i], 16) + int(S[j], 16)) % bits
            k = str(S[t])
            kStream.append(k)

            decryptImgHex.append(hex(int(hImg[m], 16) ^ int(k, 16)).upper()[2:])

        # print("k\n", kStream)
        # print("Encrypt Text\n", encryptText)
        if inspect_mode:
            sTable.append(np.reshape(sTemp, (len(decryptImgHex), 16, 16)))

        decryptImg = np.asarray(hexToInt(decryptImgHex))
        temp = []
        for i in range(sizeImgRGB):
            temp.append([decryptImg[i], decryptImg[i + sizeImgRGB], decryptImg[i + (2 * sizeImgRGB)]])
        decryptImg = np.asarray(temp)
        decryptImg.resize((yLength, xLength, 3))
        decryptImg = np.array(decryptImg, dtype=np.uint8)

        # print("Encrypt Image\n", encryptImg)

        # Checking if inspect mode is true, if so then the dictionary
        # is returned otherwise just the decrypted image is returned
        if inspect_mode:
            return {"S-table": sTable, "Plaintext": Image.fromarray(decryptImg)}
        else:
            return Image.fromarray(decryptImg)


def Testing():
    inspect = False
    doImages = True
    imageToDo = "imgList"
    Images = {
        "imgList": ['circuit_small', 'circuit_small_big', 'circuit_low_small', 'circuit_low', 'circuit',
                    'brain_low',
                    'brain', 'starwars_low', 'starwars'],

        "imgListLow": ['circuit_small', 'circuit_small_big', 'circuit_low_small', 'circuit_low',
                       'brain_low',
                       'starwars_low'],

        "imgListLowLow": ['circuit_small', 'circuit_small_big', 'circuit_low_small'],

        "imgListLowOnly": ['circuit_low', 'brain_low', 'starwars_low'],

        "circuit": ['circuit'],

        "imgListLarge": ['circuit', 'brain', 'starwars']}

    if not inspect:

        pText = "You won't get me"
        kText = "I am the key that won't be broke"
        start = default_timer()

        eText = RC4_Encrypt(inspect, pText, kText)
        print(f"Encryption\nCiphertext:\n{eText}")

        if default_timer() - start > 60:
            print(
                f"Done encryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}")
        else:
            print(f"Done encryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}")

        start = default_timer()

        dText = RC4_Decrypt(inspect, eText, kText)
        print(f""
              f"\nDecryption\nPlaintext:\n{dText}")

        if default_timer() - start > 60:
            print(
                f"Done decryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}\n\n")
        else:
            print(
                f"Done decryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}\n\n")

        if doImages:

            for i in Images[imageToDo]:
                print(f"Running {i} now\t{datetime.now().strftime('%H:%M:%S')}\n")
                start = default_timer()

                pImg = Image.open(i + '.png')
                pImg.show()
                pImg.save(f"RC4_Images/{i}_original.png")
                npImg = np.array(pImg)
                kText = "I am the key"

                eImg = RC4_Encrypt(inspect, npImg, kText)
                eImg.show()
                eImg.save(f"RC4_Images/{i}_encrypted.png")
                eImg = np.array(eImg)

                if default_timer() - start > 60:
                    print(
                        f"Done encryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}")
                else:
                    print(
                        f"Done encryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}")

                start = default_timer()

                dImg = RC4_Decrypt(inspect, eImg, kText)
                dImg.show()
                dImg.save(f"RC4_Images/{i}_decrypted.png")

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

        eText = RC4_Encrypt(inspect, pText, kText)
        print(f"Encryption\nS-table:\n{eText['S-table']}\nCiphertext:\n{eText['Ciphertext']}")

        if default_timer() - start > 60:
            print(
                f"Done encryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}")
        else:
            print(f"Done encryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}")

        start = default_timer()

        dText = RC4_Decrypt(inspect, eText['Ciphertext'], kText)
        print(f"\nDecryption\nS-table:\n{dText['S-table']}\nPlaintext:\n{dText['Plaintext']}")

        if default_timer() - start > 60:
            print(
                f"Done decryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}\n\n")
        else:
            print(
                f"Done decryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}\n\n")

        if doImages:

            for i in Images[imageToDo]:
                print(f"Running {i} now\t{datetime.now().strftime('%H:%M:%S')}\n")
                start = default_timer()

                pImg = Image.open(i + '.png')
                pImg.show()
                pImg.save(f"RC4_Images/{i}_original.png")
                npImg = np.array(pImg)
                kText = "I am the key"

                eImg = RC4_Encrypt(inspect, npImg, kText)
                print(f"S-table:\n{eImg['S-table']}")
                eImg['Ciphertext'].show()
                eImg['Ciphertext'].save(f"RC4_Images/{i}_encrypted.png")
                eImg['Ciphertext'] = np.array(eImg['Ciphertext'])

                if default_timer() - start > 60:
                    print(
                        f"Done encryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}")
                else:
                    print(
                        f"Done encryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}")

                start = default_timer()

                dImg = RC4_Decrypt(inspect, eImg['Ciphertext'], kText)
                print(f"S-table:\n{dImg['S-table']}")
                dImg['Plaintext'].show()
                dImg['Plaintext'].save(f"RC4_Images/{i}_decrypted.png")

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
