from random import randint
from PirateTreasureV4 import KeyVerify


def base32encode(s, alphabet):

    encoded = ''
    bits = 0
    i = 0
    while bits < (len(s)*8):

        encoded += alphabet[(s[i] & 0b11111)]
        bits += 5
        if bits > (len(s)*8):
            break

        encoded += alphabet[((s[i+1] << 3) | (s[i] >> 5)) & 0b11111]
        bits += 5
        if bits > (len(s)*8):
            break

        encoded += alphabet[(s[i+1] >> 2) & 0b11111]
        bits += 5
        if bits > (len(s)*8):
            break

        encoded += alphabet[((s[i+2] << 1) | (s[i+1] >> 7)) & 0b11111]
        bits += 5
        if bits > (len(s)*8):
            break

        encoded += alphabet[((s[i+3] << 4) | (s[i+2] >> 4)) & 0b11111]
        bits += 5
        if bits > (len(s)*8):
            break

        encoded += alphabet[(s[i+3] >> 1) & 0b11111]
        bits += 5
        if bits > (len(s)*8):
            break

        encoded += alphabet[((s[i+4] << 2) | (s[i+3] >> 6)) & 0b11111]
        bits += 5
        if bits > (len(s)*8):
            break

        encoded += alphabet[(s[i+4] >> 3) & 0b11111]
        bits += 5
        if bits > (len(s)*8):
            break

        i += 5

    return encoded


def InverseHex(intger, len, lb=False):
    if lb:
        return int.from_bytes(intger.to_bytes(len, byteorder='little'), byteorder="little")
    else:
        return int.from_bytes(intger.to_bytes(len, byteorder='big'), byteorder="little")


def keygen():
    b32alphabet = '0123456789ABCDEFHJKLMNPQRTUVWXYZ'
    # pubKey = 0xD6456C8BFAEA7969E6A19D
    privKey = 0x611C0519E05065E8F38DA1
    nModulus = 0x3C9921AC0185B3AAAE37E1B
    PWNADV3 = 0x50574E4144563300  # little endian base
    toXored = 0x0AEB7037B  # big endian base

    debug = True

    # gen = randint(0, pow(2, 32) - 1)
    # gen = randint(0, pow(2, 32) - 1) - 0x7A

    # gen = 0xf7bdef7b
    # gen = 0xf7bdef01

    gen = 0xf9df5000

    print(hex(gen)) if debug else 0

    # Xored the generated number by 0x0AEB7037B
    key = gen ^ toXored

    # Shift Right by 2
    key >>= 2

    # Inverted the PWNADV3 to big endian, due
    # to the inversion of generated value to
    # little endian, zeroes are neglected. When
    # concatenating the PWNADV3 and generated
    # value, resulting to incorrect results.
    # key = key.to_bytes(4, byteorder='little') + \
    #     PWNADV3.to_bytes(8, byteorder="big")
    key = PWNADV3.to_bytes(8, byteorder="little") + \
        key.to_bytes(4, byteorder='big')
    print(
        "Before encryption bytes not inverted- {0}".format(key)) if debug else 0

    print(hex(gen.to_bytes(4, byteorder="little")[0])) if debug else 0
    key = bytearray(key)
    # key[11] = key[11] | gen.to_bytes(4, byteorder="little")[0]
    # key[11] = key[11] | 30

    key = int.from_bytes(key, byteorder="big")
    print("Before encryption hex - {0}".format(hex(key))) if debug else 0
    print(
        "Before encryption bytes inverted - {0}".format(key.to_bytes(12, byteorder="little"))) if debug else 0
    print(hex(InverseHex(key, 12))) if debug else 0

    # RSA Encryption of the key
    rsa_encrypt = pow(key, privKey, nModulus)
    print("RSA - Not Inverted {0}".format(hex(rsa_encrypt))) if debug else 0
    print(
        "RSA - Inverted {0}".format(hex(InverseHex(rsa_encrypt, 12)))) if debug else 0

    # Add the last value of the encryption
    buffer = bytearray(rsa_encrypt.to_bytes(12, byteorder="little"))

    buffer[11] = buffer[11] | gen.to_bytes(4, byteorder="little")[0]
    # buffer[11] = buffer[11] | (gen.to_bytes(4, byteorder="little")[0] & 3)
    # buffer[11] = gen.to_bytes(4, byteorder="little")[3] & 3
    # print(gen.to_bytes(4, byteorder="little")[0] & 3)
    # buffer[11] = buffer[11] | 0x1E

    print("RSA 1 - {0}".format(hex(int.from_bytes(buffer,
          byteorder="big")))) if debug else 0
    buffer += gen.to_bytes(4, byteorder="little")[1:4]
    print("RSA 2 - {0}".format(hex(int.from_bytes(buffer,
          byteorder="big")))) if debug else 0

    # Custom Base 32 Encode
    encoded = base32encode(buffer, b32alphabet)
    print("Encoded - {0}".format(encoded)) if debug else 0

    check_sum = 0
    for char in encoded:
        check_sum += b32alphabet.find(char)

    encoded += b32alphabet[check_sum & 0b11111]

    return encoded


# key = keygen()
# print("Key - {0}".format(key))
# KeyVerify(key)

check = False
x = 0
while not (check):
    x += 1
    print(x)
    check = KeyVerify(keygen())
