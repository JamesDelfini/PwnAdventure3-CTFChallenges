from collections import namedtuple
from numpy import resize, int8


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
    CONST_OFFSET_ACCESS = [6, 12]
    val_tmp_a = 0
    allowToProcess = False

    for i in range(11):
        if ASM_BitRight(key2[12-i-1]) - HexToInt(key2Constants[12-i-1]) >= 0:
            if ASM_BitRight(key2[12-i-1]) > HexToInt(key2Constants[12-i-1]):
                allowToProcess = True
                break
        else:
            break

    if allowToProcess:
        for i in range(2):
            firstVal = HexToInt(key2Constants[CONST_OFFSET_ACCESS[i]-6])
            key2_val = ASM_BitRight(key2[CONST_OFFSET_ACCESS[i]-6], 16)
            key2_val = key2_val - firstVal
            key2_val = key2_val - val_tmp_a
            key2[CONST_OFFSET_ACCESS[i]-6] = ASM_BitRight(key2_val)

            key2_val >>= 8
            key2_val = int8(key2_val) * -1
            key2_val = ASM_BitRight(key2_val)
            key2_val = ASM_BitRight(
                key2[CONST_OFFSET_ACCESS[i]-5], 16) - ASM_BitRight(key2_val, 16)
            key2_val = ASM_BitRight(
                key2_val, 16) - HexToInt(key2Constants[(CONST_OFFSET_ACCESS[i]+2) - 7])
            key2[CONST_OFFSET_ACCESS[i]-5] = ASM_BitRight(key2_val)

            key2_val >>= 8
            key2_val = int8(key2_val) * -1
            key2_val = ASM_BitRight(key2_val)
            key2_val = ASM_BitRight(
                key2[CONST_OFFSET_ACCESS[i]-4], 16) - ASM_BitRight(key2_val, 16)
            key2_val = ASM_BitRight(
                key2_val, 16) - HexToInt(key2Constants[(CONST_OFFSET_ACCESS[i]+2) - 6])
            key2[CONST_OFFSET_ACCESS[i]-4] = ASM_BitRight(key2_val)

            key2_val >>= 8
            key2_val = int8(key2_val) * -1
            key2_val = ASM_BitRight(key2_val)
            key2_val = ASM_BitRight(
                key2[CONST_OFFSET_ACCESS[i]-3], 16) - ASM_BitRight(key2_val, 16)
            key2_val = ASM_BitRight(key2_val, 16) - HexToInt(
                key2Constants[(CONST_OFFSET_ACCESS[i]+2) - 5])
            key2[CONST_OFFSET_ACCESS[i]-3] = ASM_BitRight(key2_val)

            key2_val >>= 8
            key2_val = int8(key2_val) * -1
            key2_val = ASM_BitRight(key2_val)
            key2_val = ASM_BitRight(
                key2[CONST_OFFSET_ACCESS[i]-2], 16) - ASM_BitRight(key2_val, 16)
            key2_val = ASM_BitRight(key2_val, 16) - HexToInt(
                key2Constants[(CONST_OFFSET_ACCESS[i]+2) - 4])
            key2[CONST_OFFSET_ACCESS[i]-2] = ASM_BitRight(key2_val)

            key2_val >>= 8
            key2_val = int8(key2_val) * -1
            key2_val = ASM_BitRight(key2_val)
            key2_val = ASM_BitRight(
                key2[CONST_OFFSET_ACCESS[i]-1], 16) - ASM_BitRight(key2_val, 16)
            key2_val = ASM_BitRight(key2_val, 16) - HexToInt(
                key2Constants[(CONST_OFFSET_ACCESS[i]+2) - 3])
            key2[CONST_OFFSET_ACCESS[i]-1] = ASM_BitRight(key2_val)

            val_tmp_a = key2_val
            val_tmp_a >>= 8
            val_tmp_a = int8(val_tmp_a) * -1
            val_tmp_a = ASM_BitRight(val_tmp_a)


# @key2 - KEY15_CNTRL or KEY12
# @key12 - KEY12
def KeyVerifyCall3(key2, key12):
    CONST_OFFSET_ACCESS = [6, 12]
    val_tmp_a = 0

    for i in range(2):
        firstVal = ASM_BitRight(
            key12[CONST_OFFSET_ACCESS[i]-6], 16)  # firstVal of KEY12
        key2_val = ASM_BitRight(key2[CONST_OFFSET_ACCESS[i]-6], 16)
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


# Main Functions
# key2_8 - KEY15_8
# key2Constants - Constants at KeyVerify declarations
# key2Cntrl - KEY15_CNTRL
# key2 - KEY15 or KEY15_8
def KeyVerifyCall2(key8, key2Constants, key15Cntrl, key2):
    key12 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # KEY12

    # Clear the key15Cntrl
    for i in range(len(key15Cntrl)):
        key15Cntrl[i] = 0

    # Transfer the KEY15 values to KEY12
    for i in range(12):
        key12[i] = ASM_BitRight(key2[i])

    rolValArr = [1, 2, 4, 8, 16, 32, 64, 128]
    rolValInd = 0

    for i in range(96):
        rolVal = rolValArr[rolValInd]
        rolValInd += 1

        if (key8[i >> 3] & rolVal != 0):
            KeyVerifyCall3(key15Cntrl, key12)
            KeyVerifyCall4(key15Cntrl, key2Constants)

        KeyVerifyCall3(key12, key12)
        KeyVerifyCall4(key12, key2Constants)

        if rolValInd == 8:
            rolValInd = 0


def KeyVerify(input):
    # Note: Trait the alphanumeric as hexadecimal and the max value is 0x1F.
    Constants = namedtuple('Constants', ['alphanumeric'])
    constants = Constants('123456789ABCDEFHJKLMNPQRTUVWXYZ')

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

            print(f'key1 - {key1}')
            print(f'key1_tmp - {key1_tmp}')
            print(f'key1Verify1 - {key1Verify1}')
            wut = (ASM_BitRight(key1_tmp[15] + key1Verify1)) & HexToInt('1F')
            print(f'Last letter {ASM_BitRight(key1[24])}, {hex(wut)}')

            if (ASM_BitRight(key1[24]) == (ASM_BitRight(key1_tmp[15] + key1Verify1)) & HexToInt('1F')):
                # Calculation key verification 2
                for i in range(len(key1)):
                    if i+1 <= 24:
                        if ((key1[i] & 1) != 0):
                            tmpI = charCnt1 - 2
                            tmpI >>= 3

                            tmpJ = charCnt2 - 2
                            tmpJ &= 7

                            tmpK = ASM_ClearBitRight(tmpI) + 1
                            tmpK <<= ASM_BitRight(tmpJ)

                            tmpL = ASM_BitRight(tmpI)
                            key2[tmpL] = ASM_BitRight(key2[tmpL]) | tmpK

                        if ((key1[i] & 2) != 0):
                            tmpI = charCnt1 - 1
                            tmpI >>= 3

                            tmpJ = charCnt2 - 1
                            tmpJ &= 7

                            tmpK = ASM_ClearBitRight(tmpI) + 1
                            tmpK <<= ASM_BitRight(tmpJ)

                            tmpL = ASM_BitRight(tmpI)
                            key2[tmpL] = ASM_BitRight(key2[tmpL]) | tmpK

                        if ((key1[i] & 4) != 0):
                            tmpI = charCnt1
                            tmpI >>= 3

                            tmpJ = charCnt2
                            tmpJ &= 7

                            tmpK = ASM_ClearBitRight(tmpI) + 1
                            tmpK <<= ASM_BitRight(tmpJ)

                            tmpL = ASM_BitRight(tmpI)
                            key2[tmpL] = ASM_BitRight(key2[tmpL]) | tmpK

                        if ((key1[i] & 8) != 0):
                            tmpI = charCnt1 + 1
                            tmpI >>= 3

                            tmpJ = charCnt2 + 1
                            tmpJ &= 7

                            tmpK = ASM_ClearBitRight(tmpI) + 1
                            tmpK <<= ASM_BitRight(tmpJ)

                            tmpL = ASM_BitRight(tmpI)
                            key2[tmpL] = ASM_BitRight(key2[tmpL]) | tmpK

                        if ((key1[i] & 16) != 0):
                            tmpI = charCnt1 + 2
                            tmpI >>= 3

                            tmpJ = charCnt2 + 2
                            tmpJ &= 7

                            tmpK = ASM_ClearBitRight(tmpI) + 1
                            tmpK <<= ASM_BitRight(tmpJ)

                            tmpL = ASM_BitRight(tmpI)
                            key2[tmpL] = ASM_BitRight(key2[tmpL]) | tmpK

                        charCnt1 += 5
                        charCnt2 -= 3

                # Key Verification 2
                key2Verify2 = 0

                print(f'key2 - {key2}')

                # Calculation of Key 2 Verification 2
                for i in range(4):
                    # Calculation of key2 start at the last until to a 4th value
                    key2Verify2 = key2Verify2 + key2[len(key2)-1-i]
                    print(hex(key2Verify2))
                    if(i != 3):
                        key2Verify2 <<= 8

                print(f'key2Verify2 - {hex(key2Verify2)}')
                key2Verify2 ^= HexToInt('AEB7037B')  # 0AEB7037B
                print(f'key2Verify2 - {hex(key2Verify2)}')
                key2Verify2 >>= 2
                print(f'key2Verify2 - {hex(key2Verify2)}')

                # Calculation of Key 2 Verification 1 (KeyVerifyCall1)
                key2LoopCntrl = [1, 0, 1]
                key2Constants = ['1B', '7E', 'E3', 'AA',
                                 '3A', '5B', '18', 'C0',
                                 '1A', '92', 'C9', '3']  # The constants declared at KeyVerify
                key15 = [1, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0]  # KEY15
                key15Cntrl = [0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0]  # KEY15_CNTRL
                key8 = resize(key2, 12)  # KEY15_8 the size 12
                print(f'key8 - {key8}')
                key8[11] = key8[11] & 3  # Replace the 12th value
                print(f'key8 - {key8}')

                rolValArr = [1, 2, 4, 8, 16, 32, 64, 128]
                rolValInd = 0

                for i in range(24):
                    rolVal = rolValArr[rolValInd]
                    rolValInd += 1

                    if (key2LoopCntrl[i >> 3] & rolVal != 0):
                        KeyVerifyCall2(key8, key2Constants,
                                       key15Cntrl, key15)

                        # SubLoop1
                        for k in range(12):
                            key15[k] = ASM_BitRight(key15Cntrl[k])

                    KeyVerifyCall2(key8, key2Constants, key15Cntrl, key8)

                    # SubLoop2
                    for k in range(12):
                        key8[k] = ASM_BitRight(key15Cntrl[k])

                    if rolValInd == 8:
                        rolValInd = 0

                key15b_temp = hex(key2Verify2)
                key15b = []

                x_tmp = key15b_temp[8:10]
                key15b.append(HexToInt('0' if x_tmp == '' else x_tmp))
                x_tmp = key15b_temp[6:8]
                key15b.append(HexToInt('0' if x_tmp == '' else x_tmp))
                x_tmp = key15b_temp[4:6]
                key15b.append(HexToInt('0' if x_tmp == '' else x_tmp))
                x_tmp = key15b_temp[2:4]
                key15b.append(HexToInt('0' if x_tmp == '' else x_tmp))

                # PWNADV3
                key15b.append(HexToInt('50'))
                key15b.append(HexToInt('57'))
                key15b.append(HexToInt('4E'))
                key15b.append(HexToInt('41'))
                key15b.append(HexToInt('44'))
                key15b.append(HexToInt('56'))
                key15b.append(HexToInt('33'))
                key15b.append(HexToInt('00'))

                correctKey = False
                for i in range(12):
                    if (key15[i] == key15b[i]):
                        correctKey = True
                    else:
                        correctKey = False
                        break

                if correctKey:
                    print(f'The inputted key is correct {input}')
                    print(key15, key15b)
                    return True
                else:
                    IncorrectKey('Incorrect Key')
                    print(key15, key15b)
                    return False
            else:
                IncorrectKey('Last letter is not correct')
                return False
    else:
        IncorrectKey('Length of the input must be equal to 25.')


# keyInput = '123456789ABCDEFHJKLMNPQRTUVWXYZ'
# keyInput = 'WFNKR3WLKYHD3AP5XVZB9RQET'

# keyInput = 'BNVHZJ5754F4DVBARC0YYYYYU'
# keyInput = '3JL2RE8B8ZA0DHE4UC0YYYYYY'

keyInput = 'U81W7Q1N20J0NLC2T700NF7Z6'
KeyVerify(keyInput)

# p = 33759901540733
# q = 34719860683127
# # e = 0
# e = 259037971019840732176753053
# # e = int("611C0519E05065E8F38DA1", 16)
# pubKey, privKey = rsa(p, q, e)

# print(pubKey, privKey)
