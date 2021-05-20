import numpy as np
from PIL import Image
import time

start_time = time.time()

from ehn2021_demo2_All import AES_Encrypt
from ehn2021_demo2_All import AES_Decrypt

from ehn2021_demo2_All import TDEA_Encrypt
from ehn2021_demo2_All import TDEA_Decrypt

from ehn2021_demo2_All import RC4_Encrypt
from ehn2021_demo2_All import RC4_Decrypt



IP = np.load("DES_Initial_Permutation.npy")
Inv_IP = np.load('DES_Inverse_Initial_Permutation.npy')



Plaintext = open("message.txt","r").read()

print("Plaintext:\n", Plaintext)

Key1_init = "Secret#1"
Key2_init = "2ndKey!!"
Key3_init = "Why3Keys"



# =====================================================
print("===============================")
print("==============AES==============")
print("===============================")




# =====================================================
# 3DES Testing
print("================================")
print("==============3DES==============")
print("================================")
inspect = False
if inspect == False:
    print('Encrypting.......')
    print()
    CT = TDEA_Encrypt(False,Plaintext,Key1_init, Key2_init, Key3_init, IP)
    print(CT)
    print()
    print('Decrypting.......')
    print()
    PT = TDEA_Decrypt(False,CT,Key1_init, Key2_init, Key3_init, Inv_IP)
    print(PT)

else:
    Plaintext = "Testing"
    print('Inspect Encrypting.......')
    print()
    CT = TDEA_Encrypt(True, Plaintext, Key1_init, Key2_init, Key3_init, IP)
    print('encrypted:', CT)
    print()
    print('Decrypting.......')
    print()
    PT = TDEA_Decrypt(True, CT["Ciphertext"], Key1_init, Key2_init, Key3_init, Inv_IP)
    print('decrypted:', PT)

pic = Image.open("cape_low.png", mode='r')
pix = np.array(pic)
# print(pix)
Encrypted_Image = TDEA_Encrypt(False, pix, Key1_init, Key2_init, Key3_init, IP)

print("--- %s seconds ---" % (time.time() - start_time))
#
original = Image.fromarray(np.uint8(Encrypted_Image))
# original.save('Original.png')
original.save("Encrypted.png")
original.show()
pix = np.asarray(Encrypted_Image)
# pic = Image.open("img2_Low.png", mode='r')
pix = np.array(Encrypted_Image)
Decrypted_Image = TDEA_Decrypt(False, pix, Key1_init, Key2_init, Key3_init, Inv_IP)

print("--- %s seconds ---" % (time.time() - start_time))

original = Image.fromarray(np.uint8(Decrypted_Image))
original.save("Decrypted.png")
original.show()

# =====================================================
print("===============================")
print("==============RC4==============")
print("===============================")

