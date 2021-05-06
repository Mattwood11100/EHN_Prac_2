import numpy as np
from PIL import Image
import timeit

np.set_printoptions(precision=4, suppress=True)


def strToHex(text):
    hexOut = []
    for i in text:
        hexOut.append(hex(ord(i)).upper()[2:])

    return hexOut


def intToHex(text):
    hexOut = []
    for i in text:
        hexOut.append(hex(i).upper()[2:])

    return hexOut


def hexToInt(text):
    intOut = []
    for i in text:
        intOut.append(int(i, 16))

    return intOut


def hexToStr(text):
    strOut = []
    for i in text:
        strOut.append(chr(int(i, 16)))

    return ''.join(strOut)


def RC4_Encrypt(inspect_mode, plaintext, key):
    bits = 256
    iDict = {}
    # Creating the initial variables
    S = []
    # S = np.asarray(S)
    T = []
    # T = np.asarray(T)
    K = list(strToHex(key))
    # K = np.asarray(K)

    print("S\n", S)
    print("T\n", T)
    print("K\n", K)

    # Initializing the variables
    for i in range(bits):
        S.append(hex(i).upper()[2:].zfill(2))
        T.append(K[i % len(key)])
    S = np.asarray(S)
    T = np.asarray(T)
    print("S\n", S)
    print("T\n", T)

    # Initial permutation of S
    j = 0
    for i in range(bits):
        j = (j + int(S[i], 16) + int(T[i], 16)) % bits
        temp = S[i]
        S[i] = S[j]
        S[j] = temp

    print("Encryption S\n", S)

    if type(plaintext) == str:
        hText = np.asarray(strToHex(plaintext))
        print("Hex Text\n", hText)

        i = 0
        j = 0
        encryptText = []
        kStream = []
        for m in range(len(plaintext)):
            i = (i + 1) % bits
            j = (j + int(S[i], 16)) % bits

            temp = S[i]
            S[i] = S[j]
            S[j] = temp

            t = (int(S[i], 16) + int(S[j], 16)) % bits
            k = str(S[t])
            kStream.append(k)

            encryptText.append(hex(int(hText[m], 16) ^ int(k, 16)).upper()[2:])

        print("k\n", kStream)
        print("Encrypt Text\n", encryptText)

        encryptText = hexToStr(encryptText)
        print("Encrypt Text String\n", encryptText)
        if inspect_mode:
            sTable = S
            ct = encryptText
            iDict.update({"S-table": sTable})
            iDict.update({"Ciphertext": ct})
            return iDict
        else:
            return encryptText

    elif type(plaintext) == np.ndarray:
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
        # imgText = imgText[0]

        print(imgArray[0][:25])
        print(imgText[0][:25])

        hImg = intToHex(imgText[0])
        print("Hex Img\n", hImg[:25])

        i = 0
        j = 0
        encryptImgHex = []
        kStream = []
        for m in range(sizeImgArray):
            i = (i + 1) % bits
            j = (j + int(S[i], 16)) % bits

            temp = S[i]
            S[i] = S[j]
            S[j] = temp

            t = (int(S[i], 16) + int(S[j], 16)) % bits
            k = str(S[t])
            kStream.append(k)

            encryptImgHex.append(hex(int(hImg[m], 16) ^ int(k, 16)).upper()[2:])

        print("k\n", kStream[:25])
        print("Encrypt Text\n", encryptImgHex[:25])

        encryptImg = np.asarray(hexToInt(encryptImgHex))
        encryptImg.resize((1, sizeImgArray))
        encryptImg.resize((yLength, xLength, 3))

        print("Encrypt Image\n", encryptImg)

        if inspect_mode:
            sTable = S
            ct = encryptImg
            iDict.update({"S-table": sTable})
            iDict.update({"Ciphertext": ct})
            return iDict
        else:
            return encryptImg


def RC4_Decrypt(inspect_mode, ciphertext, key):
    bits = 256
    iDict = {}
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

    if type(ciphertext) == str:
        hText = strToHex(ciphertext)
        # print("Hex Text\n", hText)

        i = 0
        j = 0
        decryptText = []
        kStream = []
        for m in range(len(ciphertext)):
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

        decryptText = hexToStr(decryptText)
        # print("Decrypt Text String\n", decryptText)

        if inspect_mode:
            sTable = np.asarray(S.tolist())
            pt = decryptText
            iDict.update({"S-table": sTable})
            iDict.update({"Plaintext": pt})
            return iDict
        else:
            return decryptText

    elif type(ciphertext) == np.ndarray:
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
        # imgText = imgText[0]

        # print(imgArray)
        # print(imgText)

        hImg = intToHex(imgText[0])
        # print("Hex Img\n", hImg)

        i = 0
        j = 0
        decryptImgHex = []
        kStream = []
        for m in range(sizeImgArray):
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

        decryptImg = np.asarray(hexToInt(decryptImgHex))
        decryptImg.resize((1, sizeImgArray))
        decryptImg.resize((yLength, xLength, 3))

        # print("Encrypt Image\n", encryptImg)

        if inspect_mode:
            sTable = S
            pt = decryptImg
            iDict.update({"S-table": sTable})
            iDict.update({"Plaintext": pt})
            return iDict
        else:
            return decryptImg


def Testing():
    pText = "Testing if the encryption algorithm works properly"
    kText = "I am the key"
    pImg = Image.open('circuit.png')
    inspect = True

    eText = RC4_Encrypt(inspect, pText, kText)
    print(eText['S-table'], "\n\n")
    print(eText['Ciphertext'], "\n\n")
    print(eText, "\n\n")

    if type(eText) == dict:
        dText = RC4_Decrypt(inspect, eText["Ciphertext"], kText)
    else:
        dText = RC4_Decrypt(inspect, eText, kText)

    print(dText['S-table'], "\n\n")
    print(dText['Plaintext'], "\n\n")

    # pImg.show()
    # npImg = np.array(pImg)
    #
    # eImg = RC4_Encrypt(inspect, npImg, kText)
    # # print(eImg, "\n\n")
    #
    # if type(eImg) == dict:
    #     pImg = Image.fromarray((eImg["Ciphertext"] * 255).astype(np.uint8))
    #     pImg.show()
    #     dImg = RC4_Decrypt(inspect, eImg["Ciphertext"], kText)
    # else:
    #     pImg = Image.fromarray((eImg * 255).astype(np.uint8))
    #     pImg.show()
    #     dImg = RC4_Decrypt(inspect, eImg, kText)
    #
    # # print(dImg, "\n\n")
    #
    # if type(dImg) == dict:
    #     pImg = Image.fromarray((dImg["Plaintext"]).astype(np.uint8))
    #     pImg.show()
    # else:
    #     pImg = Image.fromarray((dImg).astype(np.uint8))
    #     pImg.show()

    # pImg = Image.open('brain_low.png')
    #
    # pImg.show()
    # npImg = np.array(pImg)
    #
    # eImg = RC4_Encrypt(inspect, npImg, kText)
    # # print(eImg, "\n\n")
    #
    # if type(eImg) == dict:
    #     pImg = Image.fromarray((eImg["Ciphertext"] * 255).astype(np.uint8))
    #     pImg.show()
    #     dImg = RC4_Decrypt(inspect, eImg["Ciphertext"], kText)
    # else:
    #     pImg = Image.fromarray((eImg * 255).astype(np.uint8))
    #     pImg.show()
    #     dImg = RC4_Decrypt(inspect, eImg, kText)
    #
    # # print(dImg, "\n\n")
    #
    # if type(dImg) == dict:
    #     pImg = Image.fromarray((dImg["Plaintext"]).astype(np.uint8))
    #     pImg.show()
    # else:
    #     pImg = Image.fromarray((dImg).astype(np.uint8))
    #     pImg.show()
    #
    # pImg = Image.open('starwars.png')
    #
    # pImg.show()
    # npImg = np.array(pImg)
    #
    # eImg = RC4_Encrypt(inspect, npImg, kText)
    # # print(eImg, "\n\n")
    #
    # if type(eImg) == dict:
    #     pImg = Image.fromarray((eImg["Ciphertext"] * 255).astype(np.uint8))
    #     pImg.show()
    #     dImg = RC4_Decrypt(inspect, eImg["Ciphertext"], kText)
    # else:
    #     pImg = Image.fromarray((eImg * 255).astype(np.uint8))
    #     pImg.show()
    #     dImg = RC4_Decrypt(inspect, eImg, kText)
    #
    # # print(dImg, "\n\n")
    #
    # if type(dImg) == dict:
    #     pImg = Image.fromarray((dImg["Plaintext"]).astype(np.uint8))
    #     pImg.show()
    # else:
    #     pImg = Image.fromarray((dImg).astype(np.uint8))
    #     pImg.show()


start = timeit.default_timer()
Testing()
print("Done in ", timeit.default_timer() - start, "s\n\n")
