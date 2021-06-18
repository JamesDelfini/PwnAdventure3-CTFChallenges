from collections import namedtuple
from numpy import resize, uint8
from numpy import array_equal
from numpy import trim_zeros
from numpy import append
from numpy import left_shift
from numpy import right_shift
from numpy import int8
from numpy import int32
from numpy import copy
# import numpy as np

# Note: Trait the alphanumeric as hexadecimal and the max value is 0x1F.
Constants = namedtuple('Constants', ['alphanumeric'])
constants = Constants('123456789ABCDEFHJKLMNPQRTUVWXYZ')

input = 'AAAAAAAAAAAAAAAAYYYYYYYYH'
debugKey2 = False
debugKeyV4 = False


def IncorrectKey(reason):
    print(f'Incorrect Key: {reason}')


def HexToInt(hex):
    return int(hex, 16)


def ASM_BitRight(num, bits=8):
    newNum = num >> bits
    newNum <<= bits
    return num - newNum


def ASM_ClearBitRight(num, bits=8):
    newNum = num >> bits
    return newNum << bits


def ASM_MMXRight(array, size):
    # Changes must start above the size
    size = size + 1
    # Minus one due to array
    shift_size = size - 1

    tmp_cnt = 0
    prevArray = array.copy()
    for i in range(len(array)):
        if i >= shift_size:
            array[i] += prevArray[tmp_cnt]
            tmp_cnt += 1

    return array


def tohex(val, nbits):
    return hex((val + (1 << nbits)) % (1 << nbits))


# @key2 - KEY15_CNTRL or KEY12
# @key2Constants - Key 2 Constants
def KeyVerifyCall4(key2, key2Constants):
    global debugKeyV4

    CONST_OFFSET_ACCESS = [6, 12]
    val_tmp_a = 0
    allowToProcess = False

    for i in range(11):
        # if ASM_BitRight(key2[i]) >= HexToInt(key2Constants[12-i-1]):
        #     if ASM_BitRight(key2[i]) == HexToInt(key2Constants[12-i-1]):
        if ASM_BitRight(key2[12-i-1]) - HexToInt(key2Constants[12-i-1]) >= 0:
            # print(
            #     # f'{key2[12-i-1]} - {hex(key2[12-i-1])} | {HexToInt(key2Constants[12-i-1])} - {key2Constants[12-i-1]}')
            #     f'{hex(key2[12-i-1])} | 0x{key2Constants[12-i-1]}')
            if ASM_BitRight(key2[12-i-1]) > HexToInt(key2Constants[12-i-1]):
                # if debugKeyV4:
                #     print(f'{hex(key2[12-i-1])} - 0x{key2Constants[12-i-1]}')
                allowToProcess = True
                break
        else:
            break

    if allowToProcess:
        for i in range(2):
            # firstVal = ASM_BitRight(
            #     key2Constants[CONST_OFFSET_ACCESS[i]-6], 16)  # firstVal of constant
            # firstVal of constant
            firstVal = HexToInt(key2Constants[CONST_OFFSET_ACCESS[i]-6])
            key2_val = ASM_BitRight(key2[CONST_OFFSET_ACCESS[i]-6], 16)
            # print(hex(key2_val), hex(firstVal))
            key2_val = key2_val - firstVal
            key2_val = key2_val - val_tmp_a
            key2[CONST_OFFSET_ACCESS[i]-6] = ASM_BitRight(key2_val)

            key2_val >>= 8
            # key2_val *= -1
            key2_val = int8(key2_val) * -1
            key2_val = ASM_BitRight(key2_val)
            key2_val = ASM_BitRight(
                key2[CONST_OFFSET_ACCESS[i]-5], 16) - ASM_BitRight(key2_val, 16)
            key2_val = ASM_BitRight(
                key2_val, 16) - HexToInt(key2Constants[(CONST_OFFSET_ACCESS[i]+2) - 7])
            key2[CONST_OFFSET_ACCESS[i]-5] = ASM_BitRight(key2_val)

            key2_val >>= 8
            # key2_val *= -1
            key2_val = int8(key2_val) * -1
            key2_val = ASM_BitRight(key2_val)
            key2_val = ASM_BitRight(
                key2[CONST_OFFSET_ACCESS[i]-4], 16) - ASM_BitRight(key2_val, 16)
            key2_val = ASM_BitRight(
                key2_val, 16) - HexToInt(key2Constants[(CONST_OFFSET_ACCESS[i]+2) - 6])
            key2[CONST_OFFSET_ACCESS[i]-4] = ASM_BitRight(key2_val)

            key2_val >>= 8
            # key2_val *= -1
            key2_val = int8(key2_val) * -1
            key2_val = ASM_BitRight(key2_val)
            key2_val = ASM_BitRight(
                key2[CONST_OFFSET_ACCESS[i]-3], 16) - ASM_BitRight(key2_val, 16)
            key2_val = ASM_BitRight(key2_val, 16) - HexToInt(
                key2Constants[(CONST_OFFSET_ACCESS[i]+2) - 5])
            key2[CONST_OFFSET_ACCESS[i]-3] = ASM_BitRight(key2_val)

            key2_val >>= 8
            # key2_val *= -1
            key2_val = int8(key2_val) * -1
            key2_val = ASM_BitRight(key2_val)
            key2_val = ASM_BitRight(
                key2[CONST_OFFSET_ACCESS[i]-2], 16) - ASM_BitRight(key2_val, 16)
            key2_val = ASM_BitRight(key2_val, 16) - HexToInt(
                key2Constants[(CONST_OFFSET_ACCESS[i]+2) - 4])
            key2[CONST_OFFSET_ACCESS[i]-2] = ASM_BitRight(key2_val)

            key2_val >>= 8
            # key2_val *= -1
            key2_val = int8(key2_val) * -1
            key2_val = ASM_BitRight(key2_val)
            key2_val = ASM_BitRight(
                key2[CONST_OFFSET_ACCESS[i]-1], 16) - ASM_BitRight(key2_val, 16)
            key2_val = ASM_BitRight(key2_val, 16) - HexToInt(
                key2Constants[(CONST_OFFSET_ACCESS[i]+2) - 3])
            key2[CONST_OFFSET_ACCESS[i]-1] = ASM_BitRight(key2_val)

            val_tmp_a = key2_val
            val_tmp_a >>= 8
            # val_tmp_a *= -1
            val_tmp_a = int8(val_tmp_a) * -1
            val_tmp_a = ASM_BitRight(val_tmp_a)

        key2_tmp = key2.copy()
        for i in range(len(key2_tmp)):
            key2_tmp[i] = hex(key2_tmp[i]).upper()
        keyName = 'KEY15_CNTRL' if len(key2) == 15 else 'KEY12'
        # print(f'[K4] {keyName} - {key2_tmp}')

# @key2 - KEY15_CNTRL or KEY12
# @key12 - KEY12


def KeyVerifyCall3(key2, key12):
    CONST_OFFSET_ACCESS = [6, 12]
    val_tmp_a = 0

    for i in range(2):
        firstVal = ASM_BitRight(
            key12[CONST_OFFSET_ACCESS[i]-6], 16)  # firstVal of KEY12
        key2_val = ASM_BitRight(key2[CONST_OFFSET_ACCESS[i]-6], 16)
        # print(f'key2_val - {key2_val} | firstVal - {firstVal}')
        key2_val += firstVal
        key2_val += val_tmp_a
        key2[CONST_OFFSET_ACCESS[i]-6] = ASM_BitRight(key2_val)

        key2_val >>= 8
        key2_val = ASM_BitRight(key2_val)
        key2_val += ASM_BitRight(key12[(CONST_OFFSET_ACCESS[i]+2) - 7], 16)
        key2_val += ASM_BitRight(key2[CONST_OFFSET_ACCESS[i]-5], 16)
        key2[CONST_OFFSET_ACCESS[i]-5] = ASM_BitRight(key2_val)

        key2_val >>= 8
        key2_val = ASM_BitRight(key2_val)
        key2_val += ASM_BitRight(key12[(CONST_OFFSET_ACCESS[i]+2) - 6], 16)
        key2_val += ASM_BitRight(key2[CONST_OFFSET_ACCESS[i]-4], 16)
        key2[CONST_OFFSET_ACCESS[i]-4] = ASM_BitRight(key2_val)

        key2_val >>= 8
        key2_val = ASM_BitRight(key2_val)
        key2_val += ASM_BitRight(key12[(CONST_OFFSET_ACCESS[i]+2) - 5], 16)
        key2_val += ASM_BitRight(key2[CONST_OFFSET_ACCESS[i]-3], 16)
        key2[CONST_OFFSET_ACCESS[i]-3] = ASM_BitRight(key2_val)

        key2_val >>= 8
        key2_val = ASM_BitRight(key2_val)
        key2_val += ASM_BitRight(key12[(CONST_OFFSET_ACCESS[i]+2) - 4], 16)
        key2_val += ASM_BitRight(key2[CONST_OFFSET_ACCESS[i]-2], 16)
        key2[CONST_OFFSET_ACCESS[i]-2] = ASM_BitRight(key2_val)

        key2_val >>= 8
        key2_val = ASM_BitRight(key2_val)
        key2_val += ASM_BitRight(key12[(CONST_OFFSET_ACCESS[i]+2) - 3], 16)
        key2_val += ASM_BitRight(key2[CONST_OFFSET_ACCESS[i]-1], 16)
        key2[CONST_OFFSET_ACCESS[i]-1] = ASM_BitRight(key2_val)

        val_tmp_a = key2_val
        val_tmp_a >>= 8
        val_tmp_a = ASM_BitRight(val_tmp_a)

    key2_tmp = key2.copy()
    for i in range(len(key2_tmp)):
        key2_tmp[i] = hex(key2_tmp[i]).upper()
    keyName = 'KEY15_CNTRL' if len(key2) == 15 else 'KEY12'
    # print(f'[K3] {keyName} - {key2_tmp}')


# Main Functions
# key2_8 - KEY15_8
# key2Constants - Constants at KeyVerify declarations
# key2Cntrl - KEY15_CNTRL
# key2 - KEY15 or KEY15_8
def KeyVerifyCall2(key8, key2Constants, key15Cntrl, key2):
    global debugKeyV4
    key12 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # KEY12
    # print(f'key 8 - {key8}')

    # Clear the key15Cntrl
    for i in range(len(key15Cntrl)):
        key15Cntrl[i] = 0

    # Transfer the KEY15 values to KEY12
    for i in range(12):
        key12[i] = ASM_BitRight(key2[i])

    # print(f'key12 - {key12}')

    CONST_VAL = 1
    rolVal_tmp = 1
    rolVal = 0

    for i in range(96):
        # Simulate the assembly shift rotate (ROL)
        # Reset the value if zero
        if rolVal_tmp == 0:
            rolVal_tmp = CONST_VAL

        rolVal = HexToInt(hex(rolVal_tmp).strip('-'))

        if (key8[i >> 3] & rolVal != 0):
            KeyVerifyCall3(key15Cntrl, key12)
            # print(f'KeyVerifyCall3 [{hex(i)}] - {key15Cntrl}')

            # if array_equal(trim_zeros(key15Cntrl), key8):
            #     print('[STATUS] key15Cntrl are equal key8')
            #     debugKeyV4 = True

            KeyVerifyCall4(key15Cntrl, key2Constants)
            # print(f'KeyVerifyCall4 [{hex(i)}] - {key15Cntrl}')
            # debugKeyV4 = False

        KeyVerifyCall3(key12, key12)
        KeyVerifyCall4(key12, key2Constants)

        # print(f'key2Verify4 - {key2Verify4}')

        # Simulate the assembly shift rotate (ROL)
        rolVal_tmp = left_shift(int8(rolVal_tmp), int8(1))


if len(input) == 25:
    if input.find(' ') != -1 or input.find('-') != -1:
        IncorrectKey('Detected space or hyphen.')
    else:
        key1 = []
        key1Verify1 = 0
        key1Verify2 = 0
        val = []

        key2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # KEY15
        charCnt1 = 2
        charCnt2 = 2

        # Calculation key verification 1
        for i in range(len(input)):
            # Convert all inputs to uppercase
            char = input[i].upper()

            # Store the position of the character found at @constants.alphanumeric
            # Added plus 1 since array starts at 0
            pos = constants.alphanumeric.find(char) + 1
            key1.append(pos)

            # Calculate the key verification starting at 17th character
            if i+1 >= 17 and i+1 <= 24:
                key1Verify1 += pos

        # Copy the first 16 of the data of @key1
        key1_tmp = resize(key1, 16)
        key1_tmp = ASM_MMXRight(key1_tmp, 8)
        key1_tmp = ASM_MMXRight(key1_tmp, 4)
        key1_tmp = ASM_MMXRight(key1_tmp, 2)
        key1_tmp = ASM_MMXRight(key1_tmp, 1)

        # The tohex is not stable temporary check the last value array of key1_tmp
        # # Calculatin of key1Verify2 start at 13th value
        # for i in range(4):
        #     key1Verify2 += key1_tmp[13-1+i]
        #     print(key1_tmp[13-1+i])
        #     if i < 3:
        #         key1Verify2 <<= 8

        # if key1Verify2 < 0:
        #     key1Verify2 = tohex(key1Verify2, 32)

        # Key Verification 1
        # Compare the last letter from the key verification
        # if (ASM_BITRIGHT(key1[24]) == (key1Verify1 & HexToInt('1F'))):
        # print((ASM_BitRight(key1_tmp[15] + key1Verify1)) & HexToInt('1F'))
        if (ASM_BitRight(key1[24]) == (ASM_BitRight(key1_tmp[15] + key1Verify1)) & HexToInt('1F')):
            print('[STATUS] Key Verification 1 Valid!')
            # Calculation key verification 2
            for i in range(len(key1)):
                if i+1 <= 24:
                    if debugKey2:
                        # print(f"INDEX: {i-1}")
                        print(f"INDEX: {i}")
                        print(f"POS: {key1[i]} | {hex(key1[i]).upper()}")

                    if ((key1[i] & 1) != 0):
                        tmpI = charCnt1 - 2
                        tmpI >>= 3

                        tmpJ = charCnt2 - 2
                        tmpJ &= 7

                        if debugKey2:
                            print()
                            print(f'1 -> {tmpI}, {tmpJ}')
                            print(key2)

                        tmpK = ASM_ClearBitRight(tmpI) + 1
                        tmpK <<= ASM_BitRight(tmpJ)

                        tmpL = ASM_BitRight(tmpI)
                        key2[tmpL] = ASM_BitRight(key2[tmpL]) | tmpK

                        if debugKey2:
                            print(key2)
                    if ((key1[i] & 2) != 0):
                        tmpI = charCnt1 - 1
                        tmpI >>= 3

                        tmpJ = charCnt2 - 1
                        tmpJ &= 7

                        if debugKey2:
                            print()
                            print(f'2 -> {tmpI}, {tmpJ}')
                            print(key2)

                        tmpK = ASM_ClearBitRight(tmpI) + 1
                        tmpK <<= ASM_BitRight(tmpJ)

                        tmpL = ASM_BitRight(tmpI)
                        key2[tmpL] = ASM_BitRight(key2[tmpL]) | tmpK

                        if debugKey2:
                            print(key2)
                    if ((key1[i] & 4) != 0):
                        tmpI = charCnt1
                        tmpI >>= 3

                        tmpJ = charCnt2
                        tmpJ &= 7

                        if debugKey2:
                            print()
                            print(f'4 -> {tmpI}, {tmpJ}')
                            print(key2)

                        tmpK = ASM_ClearBitRight(tmpI) + 1
                        tmpK <<= ASM_BitRight(tmpJ)

                        tmpL = ASM_BitRight(tmpI)
                        key2[tmpL] = ASM_BitRight(key2[tmpL]) | tmpK

                        if debugKey2:
                            print(key2)
                    if ((key1[i] & 8) != 0):
                        tmpI = charCnt1 + 1
                        tmpI >>= 3

                        tmpJ = charCnt2 + 1
                        tmpJ &= 7

                        if debugKey2:
                            print()
                            print(f'8 -> {tmpI}, {tmpJ}')
                            print(key2)

                        tmpK = ASM_ClearBitRight(tmpI) + 1
                        tmpK <<= ASM_BitRight(tmpJ)

                        tmpL = ASM_BitRight(tmpI)
                        key2[tmpL] = ASM_BitRight(key2[tmpL]) | tmpK

                        if debugKey2:
                            print(key2)
                    if ((key1[i] & 16) != 0):
                        tmpI = charCnt1 + 2
                        tmpI >>= 3

                        tmpJ = charCnt2 + 2
                        tmpJ &= 7

                        if debugKey2:
                            print()
                            print(f'16 -> {tmpI}, {tmpJ}')
                            print(key2)

                        tmpK = ASM_ClearBitRight(tmpI) + 1
                        tmpK <<= ASM_BitRight(tmpJ)

                        tmpL = ASM_BitRight(tmpI)
                        key2[tmpL] = ASM_BitRight(key2[tmpL]) | tmpK

                        if debugKey2:
                            print(key2)

                    charCnt1 += 5
                    charCnt2 -= 3
                if debugKey2:
                    print()

            # Key Verification 2
            # print(key2)
            key2Verify2 = 0

            # for i in range(len(key2)):
            #     print(f'{key2[i]} - {hex(key2[i])}')

            # Calculation of Key 2 Verification 2
            for i in range(4):
                # OLD: Original assumption start at 10th value
                # keyVerify2 = keyVerify2 + key2[10+i]
                # UPDATE: Calculation of key2 start at the last until to a 4th value
                key2Verify2 = key2Verify2 + key2[len(key2)-1-i]
                if(i != 3):
                    key2Verify2 <<= 8

            # print(hex(keyVerify2))
            key2Verify2 ^= HexToInt('AEB7037B')
            # print(hex(keyVerify2))
            key2Verify2 >>= 2

            # print(
            #     f'Key 2 - [1]: {hex(ASM_BitRight(key2[0]))}, [2]: {hex(ASM_BitRight(key2Verify2))}')
            # print()
            # print(hex(key2Verify2))

            # Calculation of Key 2 Verification 1 (KeyVerifyCall1)
            key2LoopCntrl = [1, 0, 1]
            key2Constants = ['1B', '7E', 'E3', 'AA',
                             '3A', '5B', '18', 'C0',
                             '1A', '92', 'C9', '3']  # The constants declared at KeyVerify
            key15 = [1, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0]  # KEY15
            key15Cntrl = [0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0]  # KEY15_CNTRL
            key2Verify3 = [0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0]  # KEY12
            key8 = resize(key2, 12)  # KEY15_8 the size 12
            key8[11] = 3  # Replace the 12th value
            # print(f'key8 - {key8}')

            CONST_VAL = 1
            rolVal_tmp = 1
            rolVal = 0

            for i in range(24):
                # Simulate the assembly shift rotate (ROL)
                # Reset the value if zero
                if rolVal_tmp == 0:
                    rolVal_tmp = CONST_VAL

                rolVal = HexToInt(hex(rolVal_tmp).strip('-'))

                if (key2LoopCntrl[i >> 3] & rolVal != 0):
                    KeyVerifyCall2(key8, key2Constants,
                                   key15Cntrl, key15)

                    # key15Cntrl_tmp = key15Cntrl.copy()
                    # for k in range(len(key15Cntrl_tmp)):
                    #     key15Cntrl_tmp[k] = hex(key15Cntrl_tmp[k]).upper()
                    # print(f'key15Cntrl - {key15Cntrl_tmp}')
                    # print()

                    # SubLoop1
                    for k in range(12):
                        key15[k] = ASM_BitRight(key15Cntrl[k])
                        # key15[i] = ASM_BitRight(key15Cntrl[i])
                        # key2Verify3[i] = ASM_BitRight(key2Cntrl[i])

                KeyVerifyCall2(key8, key2Constants, key15Cntrl, key8)

                # SubLoop2
                # key8_tmp = ['', '', '', '', '', '', '', '', '', '', '', '']
                # for k in range(len(key8)):
                #     key8_tmp[k] = hex(key8[k])
                # print(f'key8 - [BEFORE] - {key8_tmp}')

                for k in range(12):
                    # key2Verify3[i] = ASM_BitRight(key15Cntrl[i])
                    key8[k] = ASM_BitRight(key15Cntrl[k])

                # key8_tmp = ['', '', '', '', '', '', '', '', '', '', '', '']
                # for k in range(len(key8)):
                #     key8_tmp[k] = hex(key8[k])
                # print(f'key8 - [AFTER]  - {key8_tmp}')

                # Simulate the assembly shift rotate (ROL)
                rolVal_tmp = left_shift(int8(rolVal_tmp), int8(1))

            # print(
            #     '------------------------------------------------------------------------------')
            # print(f'key15 - {key15}')
            # key15_tmp = ['', '', '', '', '', '',
            #              '', '', '', '', '', '', '', '', '']
            # for k in range(len(key15)):
            #     key15_tmp[k] = hex(key15[k])
            # print(f'key15 - {key15_tmp}')

            print(hex(key2Verify2))
            key15b_temp = hex(key2Verify2)
            key15b = [HexToInt(key15b_temp[8:10]), HexToInt(key15b_temp[6:8]), HexToInt(
                key15b_temp[4:6]), HexToInt(key15b_temp[2:4])]
            key15b = append(key15b, [HexToInt('50'), HexToInt('57'), HexToInt('4E'), HexToInt(
                '41'), HexToInt('44'), HexToInt('56'), HexToInt('33'), HexToInt('00')])  # PWNADV3

            key15_tmp = ['', '', '', '', '', '',
                         '', '', '', '', '', '', '', '', '']
            for k in range(len(key15)):
                key15_tmp[k] = hex(key15[k])
            print(f'key15a - {key15_tmp}')

            key15b_tmp = ['', '', '', '', '', '',
                          '', '', '', '', '', '', '', '', '']
            for k in range(len(key15b)):
                key15b_tmp[k] = hex(key15b[k])
            print(f'key15b - {key15b_tmp}')
        else:
            IncorrectKey('Last letter is not correct')
else:
    IncorrectKey('Length of the input must be equal to 25.')

# print(ASM_BITRIGHT(HexToInt('22AB')))
# print(ASM_CLEARBITRIGHT(HexToInt('22AB')))
