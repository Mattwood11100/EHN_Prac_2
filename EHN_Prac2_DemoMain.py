import numpy as np
from PIL import Image
import time
from timeit import default_timer
from datetime import datetime

np.set_printoptions(precision=4, suppress=True)

start_time = time.time()

from ehn2021_demo2_All import AES_Encrypt
from ehn2021_demo2_All import AES_Decrypt

from ehn2021_demo2_All import TDEA_Encrypt
from ehn2021_demo2_All import TDEA_Decrypt

from ehn2021_demo2_All import RC4_Encrypt
from ehn2021_demo2_All import RC4_Decrypt

IP = np.load("DES_Initial_Permutation.npy")
Inv_IP = np.load('DES_Inverse_Initial_Permutation.npy')

Plaintext = open("message.txt", "r").read()

print("Plaintext:\n", Plaintext)

Key1_init = "Secret#1"
Key2_init = "2ndKey!!"
Key3_init = "Why3Keys"

# =====================================================
print("===============================")
print("==============AES==============")
print("===============================")


# Testing function
def Testing():
    inspect = False
    ivCBCProvided = True
    doImages = False
    imageToDo = "imgList"
    Images = {"imgList": ['cat_low', 'cape_low']}

    if not inspect:

        pText = Plaintext
        kText = Key1_init
        # kText = Key2_init
        # kText = Key3_init
        start = default_timer()
        if not ivCBCProvided:

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

                for i in Images[imageToDo]:
                    print(f"Running {i} now\t{datetime.now().strftime('%H:%M:%S')}\n")
                    start = default_timer()

                    pImg = Image.open(i + '.png')
                    pImg.show()
                    # pImg.save(f"{i}_original.png")
                    npImg = np.array(pImg)
                    kText = Key1_init
                    # kText = Key2_init
                    # kText = Key3_init = "I am the key"

                    eImg = AES_Encrypt(inspect, npImg, np.load('AES_CBC_IV.npy'), kText, np.load('AES_Sbox_lookup.npy'))
                    eImg.show()
                    # eImg.save(f"{i}_encrypted.png")
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
                    # dImg.save(f"{i}_decrypted.png")

                    if default_timer() - start > 60:
                        print(
                            f"Done decryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}\n\n")
                    else:
                        print(
                            f"Done decryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}\n\n")
    else:

        pText = Plaintext
        kText = Key1_init
        # kText = Key2_init
        # kText = Key3_init
        start = default_timer()

        if not ivCBCProvided:

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

                for i in Images[imageToDo]:
                    print(f"Running {i} now\t{datetime.now().strftime('%H:%M:%S')}\n")
                    start = default_timer()

                    pImg = Image.open(i + '.png')
                    pImg.show()
                    npImg = np.array(pImg)
                    kText = Key1_init
                    # kText = Key2_init
                    # kText = Key3_init

                    eImg = AES_Encrypt(inspect, npImg, np.load('AES_CBC_IV.npy'), kText, np.load('AES_Sbox_lookup.npy'))
                    print(f"States:\n{eImg['States']}")
                    eImg['Ciphertext'].show()
                    # eImg['Ciphertext'].save(f"{i}_encrypted.png")
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
                    dImg['Plaintext'].show()
                    # dImg['Plaintext'].save(f"{i}_encrypted.png")

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


#
# # =====================================================
# # 3DES Testing
# print("================================")
# print("==============3DES==============")
# print("================================")
# inspect = False
# if inspect == False:
#     print('Encrypting.......')
#     print()
#     CT = TDEA_Encrypt(False, Plaintext, Key1_init, Key2_init, Key3_init, IP)
#     print(CT)
#     print()
#     print('Decrypting.......')
#     print()
#     PT = TDEA_Decrypt(False, CT, Key1_init, Key2_init, Key3_init, Inv_IP)
#     print(PT)
#
# else:
#     Plaintext = "Testing"
#     print('Inspect Encrypting.......')
#     print()
#     CT = TDEA_Encrypt(True, Plaintext, Key1_init, Key2_init, Key3_init, IP)
#     print('encrypted:', CT)
#     print()
#     print('Decrypting.......')
#     print()
#     PT = TDEA_Decrypt(True, CT["Ciphertext"], Key1_init, Key2_init, Key3_init, Inv_IP)
#     print('decrypted:', PT)
#
# pic = Image.open("cape_low.png", mode='r')
# pix = np.array(pic)
# # print(pix)
# Encrypted_Image = TDEA_Encrypt(False, pix, Key1_init, Key2_init, Key3_init, IP)
#
# print("--- %s seconds ---" % (time.time() - start_time))
# #
# original = Image.fromarray(np.uint8(Encrypted_Image))
# # original.save('Original.png')
# original.save("Encrypted.png")
# original.show()
# pix = np.asarray(Encrypted_Image)
# # pic = Image.open("img2_Low.png", mode='r')
# pix = np.array(Encrypted_Image)
# Decrypted_Image = TDEA_Decrypt(False, pix, Key1_init, Key2_init, Key3_init, Inv_IP)
#
# print("--- %s seconds ---" % (time.time() - start_time))
#
# original = Image.fromarray(np.uint8(Decrypted_Image))
# original.save("Decrypted.png")
# original.show()
#
# # =====================================================
# print("===============================")
# print("==============RC4==============")
# print("===============================")
#
#
# def Testing():
#     inspect = False
#     doImages = True
#     imageToDo = "imgList"
#     Images = {"imgList": ['cat_low', 'cape_low']}
#
#     if not inspect:
#
#         pText = Plaintext
#         kText = Key1_init
#         # kText = Key2_init
#         # kText = Key3_init
#         start = default_timer()
#
#         eText = RC4_Encrypt(inspect, pText, kText)
#         print(f"Encryption\nCiphertext:\n{eText}")
#
#         if default_timer() - start > 60:
#             print(
#                 f"Done encryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}")
#         else:
#             print(f"Done encryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}")
#
#         start = default_timer()
#
#         dText = RC4_Decrypt(inspect, eText, kText)
#         print(f""
#               f"\nDecryption\nPlaintext:\n{dText}")
#
#         if default_timer() - start > 60:
#             print(
#                 f"Done decryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}\n\n")
#         else:
#             print(
#                 f"Done decryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}\n\n")
#
#         if doImages:
#
#             for i in Images[imageToDo]:
#                 print(f"Running {i} now\t{datetime.now().strftime('%H:%M:%S')}\n")
#                 start = default_timer()
#
#                 pImg = Image.open(i + '.png')
#                 pImg.show()
#                 # pImg.save(f"{i}_original.png")
#                 npImg = np.array(pImg)
#                 kText = Key1_init
#                 # kText = Key2_init
#                 # kText = Key3_init
#
#                 eImg = RC4_Encrypt(inspect, npImg, kText)
#                 eImg.show()
#                 # eImg.save(f"{i}_encrypted.png")
#                 eImg = np.array(eImg)
#
#                 if default_timer() - start > 60:
#                     print(
#                         f"Done encryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}")
#                 else:
#                     print(
#                         f"Done encryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}")
#
#                 start = default_timer()
#
#                 dImg = RC4_Decrypt(inspect, eImg, kText)
#                 dImg.show()
#                 # dImg.save(f"{i}_decrypted.png")
#
#                 if default_timer() - start > 60:
#                     print(
#                         f"Done decryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}\n\n")
#                 else:
#                     print(
#                         f"Done decryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}\n\n")
#     else:
#
#         pText = Plaintext
#         kText = Key1_init
#         # kText = Key2_init
#         # kText = Key3_init
#         start = default_timer()
#
#         eText = RC4_Encrypt(inspect, pText, kText)
#         print(f"Encryption\nS-table:\n{eText['S-table']}\nCiphertext:\n{eText['Ciphertext']}")
#
#         if default_timer() - start > 60:
#             print(
#                 f"Done encryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}")
#         else:
#             print(f"Done encryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}")
#
#         start = default_timer()
#
#         dText = RC4_Decrypt(inspect, eText['Ciphertext'], kText)
#         print(f"\nDecryption\nS-table:\n{dText['S-table']}\nPlaintext:\n{dText['Plaintext']}")
#
#         if default_timer() - start > 60:
#             print(
#                 f"Done decryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}\n\n")
#         else:
#             print(
#                 f"Done decryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}\n\n")
#
#         if doImages:
#
#             for i in Images[imageToDo]:
#                 print(f"Running {i} now\t{datetime.now().strftime('%H:%M:%S')}\n")
#                 start = default_timer()
#
#                 pImg = Image.open(i + '.png')
#                 pImg.show()
#                 # pImg.save(f"{i}_original.png")
#                 npImg = np.array(pImg)
#                 kText = Key1_init
#                 # kText = Key2_init
#                 # kText = Key3_init
#
#                 eImg = RC4_Encrypt(inspect, npImg, kText)
#                 print(f"S-table:\n{eImg['S-table']}")
#                 eImg['Ciphertext'].show()
#                 # eImg['Ciphertext'].save(f"{i}_encrypted.png")
#                 eImg['Ciphertext'] = np.array(eImg['Ciphertext'])
#
#                 if default_timer() - start > 60:
#                     print(
#                         f"Done encryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}")
#                 else:
#                     print(
#                         f"Done encryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}")
#
#                 start = default_timer()
#
#                 dImg = RC4_Decrypt(inspect, eImg['Ciphertext'], kText)
#                 print(f"S-table:\n{dImg['S-table']}")
#                 dImg['Plaintext'].show()
#                 # dImg['Plaintext'].save(f"{i}_decrypted.png")
#
#                 if default_timer() - start > 60:
#                     print(
#                         f"Done decryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}\n\n")
#                 else:
#                     print(
#                         f"Done decryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}\n\n")
#
#
# start = default_timer()
# Testing()
# if default_timer() - start > 60:
#     print(f"Finally finished in {(default_timer() - start) / 60} minutes at"
#           f" {datetime.now().strftime('%H:%M:%S')}\n\n")
# else:
#     print(f"Finally finished in {default_timer() - start} seconds a"
#           f"t {datetime.now().strftime('%H:%M:%S')}\n\n")
