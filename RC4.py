import numpy as np

np.set_printoptions(precision=4, suppress=True)


def strToHex(text):
    hexOut = []
    for i in text:
        hexOut.append(hex(ord(i)).upper()[2:])

    return hexOut


def hexToStr(text):
    strOut = []
    for i in text:
        strOut.append(chr(int(i, 16)))

    return ''.join(strOut)


def RC4_Encrypt(inspect_mode, plaintext, key):
    bits = 256
    # Creating the initial variables
    S = []
    T = []
    K = list(strToHex(key))
    # print("S\n", S)
    # print("T\n", T)
    # print("K\n", K)

    # Initializing the variables
    for i in range(bits):
        S.append(hex(i).upper()[2:])
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

    # print("S\n", S)

    if type(plaintext) == str:
        hText = strToHex(plaintext)
        # print("Hex Text\n", hText)

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

        # print("k\n", kStream)
        # print("Encrypt Text\n", encryptText)

        encryptText = hexToStr(encryptText)
        print("Encrypt Text String\n", encryptText)
        return encryptText

    elif type(plaintext) == np.ndarray:
        pass


def RC4_Decrypt(inspect_mode, ciphertext, key):
    bits = 256
    # Creating the initial variables
    S = []
    T = []
    K = list(strToHex(key))
    # print("S\n", S)
    # print("T\n", T)
    # print("K\n", K)

    # Initializing the variables
    for i in range(bits):
        S.append(hex(i).upper()[2:])
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

    # print("S\n", S)

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
        print("Decrypt Text String\n", decryptText)
        # return decryptText

    elif type(ciphertext) == np.ndarray:
        pass


def Testing():
    pText = "Testing if the encryption algorithm works properly"
    kText = "I am the key"
    inspect = False
    eText = RC4_Encrypt(inspect, pText, kText)
    dText = RC4_Decrypt(inspect, eText, kText)

    # print(len(pText))
    # print(len(eText))
    # print(eText)
    # print(hex('12ef' ^ 'abcd'))
    # Text = "hello world"
    # print(strToHex(kText))
    # print(hexToStr(strToHex(Text)))

    # S = [0, 1, 2, 3, 4, 5, 6, 7]
    # K = [3, 1, 4, 1, 5, 3, 1, 4]
    # for i in range(256):
    #     S.append(i)
    #     T.append(K[i % len(key)])
    # S = np.asarray(S)
    # T = np.asarray(T)
    #
    # # Initial permutation of S
    # j = 0
    # for i in range(8):
    #     j = (j + S[i] + S[j]) % 8
    #     temp = S[i]
    #     S[i] = S[j]
    #     S[j] = temp
    #
    # SNew = [3, 5, 0, 1, 7, 6, 4, 2]
    # i = 0
    # j = 0
    # encryptText = []
    # hText = [6, 1, 5, 4]
    # for i in range(1, len(hText) + 1):
    #     j = (j + S[i]) % 8
    #
    #     temp = S[i]
    #     S[i] = S[j]
    #     S[j] = temp
    #
    #     t = (S[i] + S[j]) % 8
    #     k = str(S[t])
    #
    #     encryptText.append(hex(int(hText[i - 1], 16) ^ int(k, 16))[2:])


Testing()
