import numpy as np
from PIL import Image
import random
from timeit import default_timer
from datetime import datetime

np.set_printoptions(precision=4, suppress=False, threshold=100000, linewidth=3000)


# Class for the Initial Vector for the CBC. If the vector provided is
# none or empty then a random IV is created
class AES():
    def __init__(self, iv):
        self.iv = iv


# Initializing the class variable so that it can be used by the
# encryption and decryption algorithms
IV = AES('')

# Loading the look-up table for the Galois Filed Multiplications
Galois_Field = np.array([['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0A', '0B', '0C', '0D', '0E',
                          '0F', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                          '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '2A', '2B', '2C',
                          '2D', '2E', '2F', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                          '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '4A',
                          '4B', '4C', '4D', '4E', '4F', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                          '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63', '64', '65', '66', '67', '68',
                          '69', '6A', '6B', '6C', '6D', '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                          '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81', '82', '83', '84', '85', '86',
                          '87', '88', '89', '8A', '8B', '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                          '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F', 'A0', 'A1', 'A2', 'A3', 'A4',
                          'A5', 'A6', 'A7', 'A8', 'A9', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                          'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'C0', 'C1', 'C2',
                          'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                          'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'E0',
                          'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                          'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'FA', 'FB', 'FC', 'FD', 'FE',
                          'FF'],
                         ['00', '02', '04', '06', '08', '0A', '0C', '0E', '10', '12', '14', '16', '18', '1A', '1C',
                          '1E', '20', '22', '24', '26', '28', '2A', '2C', '2E', '30', '32', '34', '36', '38', '3A',
                          '3C', '3E', '40', '42', '44', '46', '48', '4A', '4C', '4E', '50', '52', '54', '56', '58',
                          '5A', '5C', '5E', '60', '62', '64', '66', '68', '6A', '6C', '6E', '70', '72', '74', '76',
                          '78', '7A', '7C', '7E', '80', '82', '84', '86', '88', '8A', '8C', '8E', '90', '92', '94',
                          '96', '98', '9A', '9C', '9E', 'A0', 'A2', 'A4', 'A6', 'A8', 'AA', 'AC', 'AE', 'B0', 'B2',
                          'B4', 'B6', 'B8', 'BA', 'BC', 'BE', 'C0', 'C2', 'C4', 'C6', 'C8', 'CA', 'CC', 'CE', 'D0',
                          'D2', 'D4', 'D6', 'D8', 'DA', 'DC', 'DE', 'E0', 'E2', 'E4', 'E6', 'E8', 'EA', 'EC', 'EE',
                          'F0', 'F2', 'F4', 'F6', 'F8', 'FA', 'FC', 'FE', '1B', '19', '1F', '1D', '13', '11', '17',
                          '15', '0B', '09', '0F', '0D', '03', '01', '07', '05', '3B', '39', '3F', '3D', '33', '31',
                          '37', '35', '2B', '29', '2F', '2D', '23', '21', '27', '25', '5B', '59', '5F', '5D', '53',
                          '51', '57', '55', '4B', '49', '4F', '4D', '43', '41', '47', '45', '7B', '79', '7F', '7D',
                          '73', '71', '77', '75', '6B', '69', '6F', '6D', '63', '61', '67', '65', '9B', '99', '9F',
                          '9D', '93', '91', '97', '95', '8B', '89', '8F', '8D', '83', '81', '87', '85', 'BB', 'B9',
                          'BF', 'BD', 'B3', 'B1', 'B7', 'B5', 'AB', 'A9', 'AF', 'AD', 'A3', 'A1', 'A7', 'A5', 'DB',
                          'D9', 'DF', 'DD', 'D3', 'D1', 'D7', 'D5', 'CB', 'C9', 'CF', 'CD', 'C3', 'C1', 'C7', 'C5',
                          'FB', 'F9', 'FF', 'FD', 'F3', 'F1', 'F7', 'F5', 'EB', 'E9', 'EF', 'ED', 'E3', 'E1', 'E7',
                          'E5'],
                         ['00', '03', '06', '05', '0C', '0F', '0A', '09', '18', '1B', '1E', '1D', '14', '17', '12',
                          '11', '30', '33', '36', '35', '3C', '3F', '3A', '39', '28', '2B', '2E', '2D', '24', '27',
                          '22', '21', '60', '63', '66', '65', '6C', '6F', '6A', '69', '78', '7B', '7E', '7D', '74',
                          '77', '72', '71', '50', '53', '56', '55', '5C', '5F', '5A', '59', '48', '4B', '4E', '4D',
                          '44', '47', '42', '41', 'C0', 'C3', 'C6', 'C5', 'CC', 'CF', 'CA', 'C9', 'D8', 'DB', 'DE',
                          'DD', 'D4', 'D7', 'D2', 'D1', 'F0', 'F3', 'F6', 'F5', 'FC', 'FF', 'FA', 'F9', 'E8', 'EB',
                          'EE', 'ED', 'E4', 'E7', 'E2', 'E1', 'A0', 'A3', 'A6', 'A5', 'AC', 'AF', 'AA', 'A9', 'B8',
                          'BB', 'BE', 'BD', 'B4', 'B7', 'B2', 'B1', '90', '93', '96', '95', '9C', '9F', '9A', '99',
                          '88', '8B', '8E', '8D', '84', '87', '82', '81', '9B', '98', '9D', '9E', '97', '94', '91',
                          '92', '83', '80', '85', '86', '8F', '8C', '89', '8A', 'AB', 'A8', 'AD', 'AE', 'A7', 'A4',
                          'A1', 'A2', 'B3', 'B0', 'B5', 'B6', 'BF', 'BC', 'B9', 'BA', 'FB', 'F8', 'FD', 'FE', 'F7',
                          'F4', 'F1', 'F2', 'E3', 'E0', 'E5', 'E6', 'EF', 'EC', 'E9', 'EA', 'CB', 'C8', 'CD', 'CE',
                          'C7', 'C4', 'C1', 'C2', 'D3', 'D0', 'D5', 'D6', 'DF', 'DC', 'D9', 'DA', '5B', '58', '5D',
                          '5E', '57', '54', '51', '52', '43', '40', '45', '46', '4F', '4C', '49', '4A', '6B', '68',
                          '6D', '6E', '67', '64', '61', '62', '73', '70', '75', '76', '7F', '7C', '79', '7A', '3B',
                          '38', '3D', '3E', '37', '34', '31', '32', '23', '20', '25', '26', '2F', '2C', '29', '2A',
                          '0B', '08', '0D', '0E', '07', '04', '01', '02', '13', '10', '15', '16', '1F', '1C', '19',
                          '1A'],
                         ['00', '09', '12', '1B', '24', '2D', '36', '3F', '48', '41', '5A', '53', '6C', '65', '7E',
                          '77', '90', '99', '82', '8B', 'B4', 'BD', 'A6', 'AF', 'D8', 'D1', 'CA', 'C3', 'FC', 'F5',
                          'EE', 'E7', '3B', '32', '29', '20', '1F', '16', '0D', '04', '73', '7A', '61', '68', '57',
                          '5E', '45', '4C', 'AB', 'A2', 'B9', 'B0', '8F', '86', '9D', '94', 'E3', 'EA', 'F1', 'F8',
                          'C7', 'CE', 'D5', 'DC', '76', '7F', '64', '6D', '52', '5B', '40', '49', '3E', '37', '2C',
                          '25', '1A', '13', '08', '01', 'E6', 'EF', 'F4', 'FD', 'C2', 'CB', 'D0', 'D9', 'AE', 'A7',
                          'BC', 'B5', '8A', '83', '98', '91', '4D', '44', '5F', '56', '69', '60', '7B', '72', '05',
                          '0C', '17', '1E', '21', '28', '33', '3A', 'DD', 'D4', 'CF', 'C6', 'F9', 'F0', 'EB', 'E2',
                          '95', '9C', '87', '8E', 'B1', 'B8', 'A3', 'AA', 'EC', 'E5', 'FE', 'F7', 'C8', 'C1', 'DA',
                          'D3', 'A4', 'AD', 'B6', 'BF', '80', '89', '92', '9B', '7C', '75', '6E', '67', '58', '51',
                          '4A', '43', '34', '3D', '26', '2F', '10', '19', '02', '0B', 'D7', 'DE', 'C5', 'CC', 'F3',
                          'FA', 'E1', 'E8', '9F', '96', '8D', '84', 'BB', 'B2', 'A9', 'A0', '47', '4E', '55', '5C',
                          '63', '6A', '71', '78', '0F', '06', '1D', '14', '2B', '22', '39', '30', '9A', '93', '88',
                          '81', 'BE', 'B7', 'AC', 'A5', 'D2', 'DB', 'C0', 'C9', 'F6', 'FF', 'E4', 'ED', '0A', '03',
                          '18', '11', '2E', '27', '3C', '35', '42', '4B', '50', '59', '66', '6F', '74', '7D', 'A1',
                          'A8', 'B3', 'BA', '85', '8C', '97', '9E', 'E9', 'E0', 'FB', 'F2', 'CD', 'C4', 'DF', 'D6',
                          '31', '38', '23', '2A', '15', '1C', '07', '0E', '79', '70', '6B', '62', '5D', '54', '4F',
                          '46'],
                         ['00', '0B', '16', '1D', '2C', '27', '3A', '31', '58', '53', '4E', '45', '74', '7F', '62',
                          '69', 'B0', 'BB', 'A6', 'AD', '9C', '97', '8A', '81', 'E8', 'E3', 'FE', 'F5', 'C4', 'CF',
                          'D2', 'D9', '7B', '70', '6D', '66', '57', '5C', '41', '4A', '23', '28', '35', '3E', '0F',
                          '04', '19', '12', 'CB', 'C0', 'DD', 'D6', 'E7', 'EC', 'F1', 'FA', '93', '98', '85', '8E',
                          'BF', 'B4', 'A9', 'A2', 'F6', 'FD', 'E0', 'EB', 'DA', 'D1', 'CC', 'C7', 'AE', 'A5', 'B8',
                          'B3', '82', '89', '94', '9F', '46', '4D', '50', '5B', '6A', '61', '7C', '77', '1E', '15',
                          '08', '03', '32', '39', '24', '2F', '8D', '86', '9B', '90', 'A1', 'AA', 'B7', 'BC', 'D5',
                          'DE', 'C3', 'C8', 'F9', 'F2', 'EF', 'E4', '3D', '36', '2B', '20', '11', '1A', '07', '0C',
                          '65', '6E', '73', '78', '49', '42', '5F', '54', 'F7', 'FC', 'E1', 'EA', 'DB', 'D0', 'CD',
                          'C6', 'AF', 'A4', 'B9', 'B2', '83', '88', '95', '9E', '47', '4C', '51', '5A', '6B', '60',
                          '7D', '76', '1F', '14', '09', '02', '33', '38', '25', '2E', '8C', '87', '9A', '91', 'A0',
                          'AB', 'B6', 'BD', 'D4', 'DF', 'C2', 'C9', 'F8', 'F3', 'EE', 'E5', '3C', '37', '2A', '21',
                          '10', '1B', '06', '0D', '64', '6F', '72', '79', '48', '43', '5E', '55', '01', '0A', '17',
                          '1C', '2D', '26', '3B', '30', '59', '52', '4F', '44', '75', '7E', '63', '68', 'B1', 'BA',
                          'A7', 'AC', '9D', '96', '8B', '80', 'E9', 'E2', 'FF', 'F4', 'C5', 'CE', 'D3', 'D8', '7A',
                          '71', '6C', '67', '56', '5D', '40', '4B', '22', '29', '34', '3F', '0E', '05', '18', '13',
                          'CA', 'C1', 'DC', 'D7', 'E6', 'ED', 'F0', 'FB', '92', '99', '84', '8F', 'BE', 'B5', 'A8',
                          'A3'],
                         ['00', '0D', '1A', '17', '34', '39', '2E', '23', '68', '65', '72', '7F', '5C', '51', '46',
                          '4B', 'D0', 'DD', 'CA', 'C7', 'E4', 'E9', 'FE', 'F3', 'B8', 'B5', 'A2', 'AF', '8C', '81',
                          '96', '9B', 'BB', 'B6', 'A1', 'AC', '8F', '82', '95', '98', 'D3', 'DE', 'C9', 'C4', 'E7',
                          'EA', 'FD', 'F0', '6B', '66', '71', '7C', '5F', '52', '45', '48', '03', '0E', '19', '14',
                          '37', '3A', '2D', '20', '6D', '60', '77', '7A', '59', '54', '43', '4E', '05', '08', '1F',
                          '12', '31', '3C', '2B', '26', 'BD', 'B0', 'A7', 'AA', '89', '84', '93', '9E', 'D5', 'D8',
                          'CF', 'C2', 'E1', 'EC', 'FB', 'F6', 'D6', 'DB', 'CC', 'C1', 'E2', 'EF', 'F8', 'F5', 'BE',
                          'B3', 'A4', 'A9', '8A', '87', '90', '9D', '06', '0B', '1C', '11', '32', '3F', '28', '25',
                          '6E', '63', '74', '79', '5A', '57', '40', '4D', 'DA', 'D7', 'C0', 'CD', 'EE', 'E3', 'F4',
                          'F9', 'B2', 'BF', 'A8', 'A5', '86', '8B', '9C', '91', '0A', '07', '10', '1D', '3E', '33',
                          '24', '29', '62', '6F', '78', '75', '56', '5B', '4C', '41', '61', '6C', '7B', '76', '55',
                          '58', '4F', '42', '09', '04', '13', '1E', '3D', '30', '27', '2A', 'B1', 'BC', 'AB', 'A6',
                          '85', '88', '9F', '92', 'D9', 'D4', 'C3', 'CE', 'ED', 'E0', 'F7', 'FA', 'B7', 'BA', 'AD',
                          'A0', '83', '8E', '99', '94', 'DF', 'D2', 'C5', 'C8', 'EB', 'E6', 'F1', 'FC', '67', '6A',
                          '7D', '70', '53', '5E', '49', '44', '0F', '02', '15', '18', '3B', '36', '21', '2C', '0C',
                          '01', '16', '1B', '38', '35', '22', '2F', '64', '69', '7E', '73', '50', '5D', '4A', '47',
                          'DC', 'D1', 'C6', 'CB', 'E8', 'E5', 'F2', 'FF', 'B4', 'B9', 'AE', 'A3', '80', '8D', '9A',
                          '97'],
                         ['00', '0E', '1C', '12', '38', '36', '24', '2A', '70', '7E', '6C', '62', '48', '46', '54',
                          '5A', 'E0', 'EE', 'FC', 'F2', 'D8', 'D6', 'C4', 'CA', '90', '9E', '8C', '82', 'A8', 'A6',
                          'B4', 'BA', 'DB', 'D5', 'C7', 'C9', 'E3', 'ED', 'FF', 'F1', 'AB', 'A5', 'B7', 'B9', '93',
                          '9D', '8F', '81', '3B', '35', '27', '29', '03', '0D', '1F', '11', '4B', '45', '57', '59',
                          '73', '7D', '6F', '61', 'AD', 'A3', 'B1', 'BF', '95', '9B', '89', '87', 'DD', 'D3', 'C1',
                          'CF', 'E5', 'EB', 'F9', 'F7', '4D', '43', '51', '5F', '75', '7B', '69', '67', '3D', '33',
                          '21', '2F', '05', '0B', '19', '17', '76', '78', '6A', '64', '4E', '40', '52', '5C', '06',
                          '08', '1A', '14', '3E', '30', '22', '2C', '96', '98', '8A', '84', 'AE', 'A0', 'B2', 'BC',
                          'E6', 'E8', 'FA', 'F4', 'DE', 'D0', 'C2', 'CC', '41', '4F', '5D', '53', '79', '77', '65',
                          '6B', '31', '3F', '2D', '23', '09', '07', '15', '1B', 'A1', 'AF', 'BD', 'B3', '99', '97',
                          '85', '8B', 'D1', 'DF', 'CD', 'C3', 'E9', 'E7', 'F5', 'FB', '9A', '94', '86', '88', 'A2',
                          'AC', 'BE', 'B0', 'EA', 'E4', 'F6', 'F8', 'D2', 'DC', 'CE', 'C0', '7A', '74', '66', '68',
                          '42', '4C', '5E', '50', '0A', '04', '16', '18', '32', '3C', '2E', '20', 'EC', 'E2', 'F0',
                          'FE', 'D4', 'DA', 'C8', 'C6', '9C', '92', '80', '8E', 'A4', 'AA', 'B8', 'B6', '0C', '02',
                          '10', '1E', '34', '3A', '28', '26', '7C', '72', '60', '6E', '44', '4A', '58', '56', '37',
                          '39', '2B', '25', '0F', '01', '13', '1D', '47', '49', '5B', '55', '7F', '71', '63', '6D',
                          'D7', 'D9', 'CB', 'C5', 'EF', 'E1', 'F3', 'FD', 'A7', 'A9', 'BB', 'B5', '9F', '91', '83',
                          '8D']])


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
    sizeImgRGB = 0

    # Checking if the plaintext provided is string message or a png image
    if type(plaintext) == str:
        plaintext = strResizePlaintext(strToHex(plaintext))
    elif type(plaintext) == np.ndarray:
        isImg = True
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

        plaintext = strResizePlaintext(intToHex(imgArray[0]))

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
        temp = []
        for i in range(sizeImgRGB):
            temp.append([encryptedText[i], encryptedText[i + sizeImgRGB], encryptedText[i + (2 * sizeImgRGB)]])
        encryptedText = np.asarray(temp)
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
    sizeImgRGB = 0

    # Checking if the plaintext provided is string message or a png image
    if type(ciphertext) == str:
        ciphertext = strResizePlaintext(strToHex(ciphertext))
    elif type(ciphertext) == np.ndarray:
        isImg = True
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

        ciphertext = strResizePlaintext(intToHex(imgArray[0]))

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
        temp = []
        for i in range(sizeImgRGB):
            temp.append([decryptedText[i], decryptedText[i + sizeImgRGB], decryptedText[i + (2 * sizeImgRGB)]])
        decryptedText = np.asarray(temp)
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
    ivCBCProvided = True
    doImages = False
    imageToDo = "imgList"
    Images = {
        "imgList": ['cat_low', 'cape_low']}
    if not inspect:

        pText = "Testing5789218"
        kText = "Secret Key #@! 123456"
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
                    pImg.save(f"AES_Images/{i}_original.png")
                    npImg = np.array(pImg)
                    kText = "I am the key"

                    eImg = AES_Encrypt(inspect, npImg, np.load('AES_CBC_IV.npy'), kText, np.load('AES_Sbox_lookup.npy'))
                    eImg.show()
                    eImg.save(f"AES_Images/{i}_encrypted.png")
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
                    dImg.save(f"AES_Images/{i}_decrypted.png")

                    if default_timer() - start > 60:
                        print(
                            f"Done decryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}\n\n")
                    else:
                        print(
                            f"Done decryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}\n\n")
    else:

        pText = "123#@!Teet!@#321"
        kText = "Secret Key #@! 123456"
        start = default_timer()

        if not ivCBCProvided:

            eText = AES_Encrypt(inspect, pText, None, kText, np.load('AES_Sbox_lookup.npy'))
            # print(f"Encryption\nStates:\n{eText['States']}\nCiphertext:\n{eText['Ciphertext']}")

            if default_timer() - start > 60:
                print(
                    f"Done encryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}")
            else:
                print(f"Done encryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}")

            start = default_timer()

            dText = AES_Decrypt(inspect, eText['Ciphertext'], None, kText,
                                np.load('AES_Inverse_Sbox_lookup.npy'))
            # print(f"\nDecryption\nStates:\n{dText['States']}\nPlaintext:\n{dText['Plaintext']}")

            if default_timer() - start > 60:
                print(
                    f"Done decryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}\n\n")
            else:
                print(
                    f"Done decryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}\n\n")

        else:

            eText = AES_Encrypt(inspect, pText, np.load('AES_CBC_IV.npy'), kText, np.load('AES_Sbox_lookup.npy'))
            # print(f"Encryption\nStates:\n{eText['States']}\nCiphertext:\n{eText['Ciphertext']}")
            print(f"Encryption\nCiphertext:\n{eText['Ciphertext']}")

            if default_timer() - start > 60:
                print(
                    f"Done encryption in {(default_timer() - start) / 60} minutes at {datetime.now().strftime('%H:%M:%S')}")
            else:
                print(f"Done encryption in {default_timer() - start} seconds at {datetime.now().strftime('%H:%M:%S')}")

            start = default_timer()

            dText = AES_Decrypt(inspect, eText['Ciphertext'], np.load('AES_CBC_IV.npy'), kText,
                                np.load('AES_Inverse_Sbox_lookup.npy'))
            # print(f"\nDecryption\nStates:\n{dText['States']}\nPlaintext:\n{dText['Plaintext']}")
            print(f"\nDecryption\nPlaintext:\n{dText['Plaintext']}")

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
                    kText = "I am the key"

                    eImg = AES_Encrypt(inspect, npImg, np.load('AES_CBC_IV.npy'), kText, np.load('AES_Sbox_lookup.npy'))
                    print(f"States:\n{eImg['States']}")
                    eImg['Ciphertext'].show()
                    eImg['Ciphertext'].save(f"{i}_encrypted.png")
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
                    dImg['Plaintext'].save(f"{i}_encrypted.png")

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
