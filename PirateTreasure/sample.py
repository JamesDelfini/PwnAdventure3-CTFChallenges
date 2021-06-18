
# # The alphanumeric that will be proccessed by the 5 checks
# k = 1
# for i in range(31):
#     j = 1
#     match = [0]*5

#     for i in range(5):
#         output = 1 if k & j != 0 else 0
#         match[i] = output

#         j <<= 1

#     print("{0:02d} | 0x{0:02X} | {1}".format(k, match))

#     k += 1

# print()

# # What array will be read and write into
# k = 1
# arrayPlacementInd = 2
# for i in range(24):
#     arrayPlacement = []

#     arrayPlacement.insert(0, arrayPlacementInd - 2 >> 3)
#     arrayPlacement.insert(0, arrayPlacementInd - 1 >> 3)
#     arrayPlacement.insert(0, arrayPlacementInd >> 3)
#     arrayPlacement.insert(0, arrayPlacementInd + 1 >> 3)
#     arrayPlacement.insert(0, arrayPlacementInd + 2 >> 3)

#     print(arrayPlacement)

#     k += 1
#     arrayPlacementInd += 5

# print()

# # The maximum value of each added
# k = 1
# for i in range(9):
#     print("{0:03d} | {0:08b}".format(k-1))
#     k <<= 1

# rolValArr = [1, 2, 4, 8, 16, 32, 64, 128]
# rolValInd = 0
# key2LoopCntrl = [1, 0, 1]

# for i in range(24):
#     rolVal = rolValArr[rolValInd]
#     rolValInd += 1

#     print("Index [{0:02d}] | Loop Control Index: {1:02d}".format(i, i >> 3))
#     print("   {0:08b} [{0:02d}]".format(key2LoopCntrl[i >> 3]))
#     print("&  {0:08b} [{0:02d}]".format(rolVal))
#     print("-> {0:08b} [{0:02d}]".format(key2LoopCntrl[i >> 3] & rolVal))
#     print()

#     if rolValInd == 8:
#         rolValInd = 0


# import math
# val = math.gcd(676649708177327432564254411, 10137482847357795588891061)
# print(val)

# data = bytes.fromhex(b'\x00\x00')
# data = b'\x00\x00'
data = b'\x00\x00\x00\x00'
print(len(data[2:]))
print(data[2:])
