import struct
import time

MASTER_SERVER_PORT = 3333
SERVER = 'server'
GAME = 'game'

SERVER_QUEUE = []
CLIENT_QUEUE = []
CLOSE_CLIENT = 0


def h_noop(data):
    # print("[unknown] %s" % data.hex())
    return data[1:]


def h_position(data):
    # print("[position] %s" % data.hex())

    return data[20:]


def h_jumping_hold(data):
    # print("[jumping] %s" % data.hex())
    isJumping = struct.unpack('B', data[0:1])[0]
    print("Jumping: %s" % ("pressed" if isJumping else "released"))

    return data[1:]


def h_spawn(data):
    print("[spawn] %s" % data.hex())
    """
    Spawn:
    id   sId   x       y        z        pp   rr   yy   mv                                 
    7273 6d76 233ce2c5 fb515f47 62bfea44 0afc fbf7 0000 0000
    """
    x, y, z, pp, rr, yy, mv = struct.unpack('<fffhhhh', data[2:])
    pp = 0
    rr = 0
    yy = 0
    mv = 0

    # GreatBallsOfFire
    #x, y, z = -43655.0, -56210.625, 471.536132812

    # Meet the Famer
    #x, y, z = 21162.375, 41232.0, 2255.0703125

    # Meet MichaelAngelo
    #x, y, z = 260255.0, -249336.25, 1476.03515625

    # Go to Town
    #x, y, z = -39130.5,  -20279.3300781, 2528.47998047

    # Bear Chest bottom
    # x, y, z = -7894.0  64482.0, 2418.859375

    # Bear Chest top
    #x, y, z = -7894.0, 64482.0,  6112.8125

    # Ballmer Peak Poster
    # x, y, z = -6101.0, -10956.0, 24419.25

    # Balmer Egg
    #x, y, z = -2778.0, -11035.0, 11480.5625

    # Lava Cave
    #x, y, z = 50876.0, -5243.0, 1645.0703125

    # Blocky Cave
    # x, y, z = -18450.0, -4360.0, 2225.0

    # Reverse id and sId
    # sId is position
    # newSpawn = struct.pack('=HHfffhhhh', 0x7372, 0x766d,
    #                        x, y, z, pp, rr, yy, mv)

    # print('newSpawn %s' % newSpawn.hex())
    # SERVER_QUEUE.append(newSpawn)

    return data[22:]


def h_chat(data):
    print("[chat] %s" % data.hex())


def h_weapon_slot_change(data):
    # print("[weapon slot change] %s" % data.hex())
    weaponChange = struct.unpack('B', data[0:1])[0]
    print("Weapon Slot Change: %i" % (weaponChange + 1))

    return data[1:]


def h_weapon_use(data):
    """
    Player Weapon Use:
    id   nLen (n) + weapon name                   direction                sId  -+
    2a69 1000 477265617442616c6c734f6646697265    e08a72c1e01e46c1f771ed34                6d7688225ec61b270c4783239c4438f531f700000000 (Fire Ball)
    2a69 0a00 5374617469634c696e6b                e08a72c1e01e46c1f771ed34 6672 01        6d7688225ec61b270c4783239c4438f531f700000000 (Static Link +)
    2a69 0a00 5374617469634c696e6b                e08a72c1e01e46c1f771ed34 6672 00        6d7688225ec61b270c4783239c4438f531f700000000 (Static Link -)
    2a69 0600 506973746f6c                        e08a72c1e01e46c1f771ed34                6d7688225ec61b270c4783239c4438f531f700000000 (G7 Pistol)
    sample when changing direction
    2a69 1000 477265617442616c6c734f6646697265 e08a72c1608540c1f771ed34 6d7688225ec61b270c4783239c4438f571f700000000 (Fire Ball)
    2a69 1000 477265617442616c6c734f6646697265 a0b438c168912d4200000000 6d7688225ec61b270c4783239c44caf7db1e00000000 (Fire Ball)
    """
    # print("[h_weapon_use] %s" % data.hex())
    nameLen = struct.unpack('H', data[0:2])[0] + 2
    name = data[2:nameLen]
    # print("Weapon: %s" % name.decode('utf-8'))

    # +12 is the direction
    return data[nameLen+12:]


def h_weapon_hold(data):
    # print("[weapon slot change] %s" % data.hex())
    isUsing = struct.unpack('B', data[0:1])[0]
    print("Weapon Hold: %s" % ("pressed" if isUsing else "released"))

    return data[1:]


def h_npc_talk_start(data):
    dataLen = len(data)

    print("[npc talk start] %s" % data.hex())

    return data[dataLen:]


def h_npc_talk_end(data):
    dataLen = len(data)
    print("[npc talk end] %s" % data.hex())

    return data[dataLen:]


def h_item_pickup(data):
    """
    Player Item Pickup:
    6565 8b0a0000 6d76cbc268c699610c47a74a9744f2fe371b00000000 (White Ball)
    6565 9b0a0000 6d76188859c61f0b0d471f91a244ddf9bc5100000000 (Green Ball)
         c80a0000
    """
    # rarity = {
    #     "0x8b0a0000": "White Ball",
    #     "0x9b0a0000": "Green Ball"
    # }
    # rarityId = struct.unpack('I', data[0:4])[0]
    # rarityColor = rarity.get(hex(rarityId), "Unkown Ball %s" % data.hex())
    print("[item pickup] %s" % data.hex())

    return data[4:]

# Server


def h_mana_regen(data):
    """
    Player Mana Regen:
    id   val      sId
    6d61 60000000 6d6b
    6d61 63000000 0000
    6d61 64000000 0000
    """
    # print(data[0:6].hex())
    return data[4:]


def h_skip(data):
    print("[skipped] %s" % data.hex())
    dataLen = len(data)

    return data[dataLen:]


def h_monster_near(data):
    dataLen = len(data)
    # print("[monster near (%i)] %s" % (dataLen, data.hex()))
    """
    Monster/Actor the item is located when there is a location bundled with it (location 0x6d76d)
    id   ?                                                           sId  itemId
    7073 880e0000 867317c6 01396a47 aae7f444000072dd00006a0088ff0000 6d76 890e0000 ba8d80c57a10ee46dccebc45f010b7ee0000 (Fire Ball)
    7073 880e0000 d2f6f7c5 41468047 bd172445000004230000680079000000 6d76 8a0e0000 66b502c612d01947103cc344ffffffff69fe (White Ball - Item Drop)
    7073 880e0000 80c3dfc5 afee8447 a4c0264500002f280000580085000000 6d76 8d0e0000 90a2fcc57a4e1c479a03c54437fcd42a0000 (Zero Cool)
    """

    # Returns -1 if not found
    # locationInd1 = data.find(bytes.fromhex('6d76'))

    # if locationInd1 == -1:
    #     return data[dataLen:]

    # # print("[monster near (%i)] %s" % (dataLen, data.hex()))
    # position = data[locationInd1:]

    # locationInd2 = 0
    # while locationInd2 > -1:
    #     locationInd2 = position[2:].find(bytes.fromhex('6d76'))
    #     locationInd3 = position[2:].find(bytes.fromhex('7073'))

    #     # position[2:6] is itemId
    #     if (locationInd3 < locationInd2) and locationInd3 > -1 and locationInd2 > -1:
    #         position = position[0:locationInd3+2]
    #         SERVER_QUEUE.append(bytes.fromhex('6565') + position[2:6])
    #     else:
    #         if (locationInd2 > -1):
    #             position = position[0:locationInd2+2]
    #             SERVER_QUEUE.append(bytes.fromhex('6565') + position[2:6])

    #         if (locationInd3 > -1):
    #             position = position[0:locationInd3+2]
    #             SERVER_QUEUE.append(bytes.fromhex('6565') + position[2:6])

    # print('[{}]'.format(', '.join(x.hex() for x in item_pickups)))

    return data[dataLen:]


def h_health_regen(data):
    """
    Player Health Regen:
    id   sId      health   xyz
    2b2b c1060000 62000000 6d762b07000076b8f1467c83664711991a455431581ce35d0000
    2b2b c1060000 63000000 6d762b07000076b8f1467c83664711991a455431581ce35d0000
    2b2b c1060000 64000000 6d762b07000076b8f1467c83664711991a455431581ce35d0000
    """
    # sId, health = struct.unpack('II', data[0:4*2])
    # print(hex(sId), health)

    return data[4*2:]


def h_monster_spawn(data):
    dataLen = len(data)
    # print("[monster spawn (%i)] %s" % (len(data), data.hex()))

    return data[dataLen:]


def h_actors(data):
    dataLen = len(data)
    """
    Weapon Used:
    id   actorId  sId       -+ nLen name                                                                       sid          sid                                                                            
    6d6b 3b100000 1b100000 00 0800 4669726562616c6c               93519a46bd56324710ff24459cf562c9000064000000              6d76 3b100000 a86a9a4644213247031a24459cf562c900000000 (Fire Ball)
    6d6b 40100000 1b100000 00 0800 4669726562616c6c               d99799462951324710ff2445bdf1c1a3000064000000 6d6161000000 6d76 40100000 bc1f9946dd08324733da2245bdf1c1a300000000 (Fire Ball)
    6d6b 42100000 1b100000 00 0800 5a65726f436f6f6c               171f99469f97324710ff244525343b7e000064000000              6d76 42100000 79f09846a2983247c9dd294525343b7e00000000 (Zero Cool)
    6d6b 46100000 1b100000 00 0f00 486f6c7948616e644772656e616465 ec4b9a462c55324710ff2445a9f81fc8000064000000              6d76 45100000 4e28b846401e0c47caaa364518011bcf0000                6d76461000000d9a9a46c9933147b78d2245a9f81fc800000000 (HolyHandGrenade)
    
    Item Dropped:
    6d6b f1180000 00000000 00 0900 576869746544726f70             0f6668c6e92e25471b449e4400000000000064000000 7472e5180000040044656164000000006d613b0000006d613c0000006d613a0000007073ed1800003bc704c652d272476db8174500008c5b00009cff7d0000006d76f11800000f6668c6e92e2547ff629e440000000000007073eb18000034b7c4c53baf924789fa1a4500000fe800000000000000007073ec180000679df2c594b56047c6d9f1440000e61500008900520000007073e91800005ad25ac695df8a47f45c2c450000e6e300000000000000007073ea180000cf75c8c2a4588d47b05238450000a12100000000000000007073e718000014f67fc669566647beb79d44000096010000a000060000007073e818000043a6c744904e6347ebc0154500008295000076ffafff00007073e3180000983867c69bf97a47330ef444000068020000a000090000007073e41800005d7133456f5e784705ad22450000d10f0000c4ff430000007073e618000062a48e4451c336471d3f0745000022a80000a8ff7bff00007073c018000014b467c6fc7370475236d4440000ae74000066ff2c0000007073c21800001f1005c68e18214765bbde440000db7700000000000000007073c3180000c379b2c5eaa7464700f504450000971f00007200700000007073c71800004fde6bc443928b4735ad3c450000e181000060fff9ff00007073f01800002a5d8ac6880d3447684c60440000ab82000088ff320000006d76d4180000bbaa13c67a7f5e4705d3e344aad34c4cf3a27073bf1800004912b1c622ee3747ec62b6430000ee4e0000c7ff950000007073d81800003ae63bc69ae57d47b2570e45000024510000bfff920000007073d9180000f13db945e6d07c47718a1d4500002b9500000000000000007073da180000828c86c4d6312947e9e926450000c4bf0000a1ff7fff00007073db180000f21589c5025744471c8f064500003aa600000000000000007073dc180000b85d8ac6526f60478a3162440000a876000064ff240000007073dd1800003becfa4523a46e47310cf044000092da0000610081ff00007073de1800002ed195c68a3c8c47980cc5440000ffa500000000000000007073df180000ce8b8144240c92476e341d4500001487000062ffe4ff00007073e01800003746ecc5f92c9547b37f23450000d5470000e1ff9d0000007073e1180000157807c6f29d754789a11b4500002a6b000074ff4e0000007073c11800003957f2455957804741ea244500007f94000074ffb3ff00007073c6180000f6a64dc6b2af884716ff2345000037ad00000000000000007073c81800004e1373c504f087476b5737450000cb2f00000000000000007073c4180000d7a136c627575e47c5dbd0440000c9580000a5ff830000007073c5180000c5284145f4875b47589b10450000821d00000000000000000000
    Monster Spawn:
    6d6b 39000000 00000000 01 0400 42656172                       8b4c7ac6750b31479c5e67440000000000007d00000070731f000000af95a244d9ff9047185420450000f3e300007c009aff0000707321000000322418c65bb25847de43eb440000410b00009a002c0000007073200000004a9539c6339583471df01245000057cb00002c0066ff0000707318000000c93141c619868e479e4838450000082d0000000000000000707319000000d0be3d45520c7f47c7cb20450000e3c10000070060ff000070731a000000890188c56f093147e9ea1c45000050e400007c009cff000070731b0000005e7749c6a2bc4847b3d396440000ab920000fdfff5ff000070731c0000008fd733c6df314a475bcbb4440000b1cf000000000000000070731d000000bb42e1c46f9b6747d2e11e450000c8ea0000fffff6ff000070731e0000006b5b55c63b1c81473f4807450000c59e0000000000000000707322000000a9b316c67d962747bfa1f044000010e400007c009bff000070732300000065f259c6a55a7d47d7cb01450000a41100000000030000007073240000003e98af45ed9f724766fa05450000045a0000000000000000707325000000ce9f8ec593393247357619450000d01e000074006e00000070732600000065cc1245b5184647555ce144000016cc00002f0067ff00007073270000001e1a06c64b1b6547447bed4400004c930000000000000000707328000000e9d6dd447a786e478f3716450000ee1500008900520000007073290000008bea51c65ad78147c974094500005f0d000097003400000070732a000000bb684b424e8c8647620b304500001483000060fff4ff000070732f0000002cb696c4ca8882470ffe2a4500001972000069ff350000007073300000003eb61fc6c2953947a6d1d34400007f1400008c004d000000707331000000b318dac563bc4847f917024500006cda00000000000000007073320000009ba643c619684d47c58aa94400009f0900009c0025000000707333000000006c0ec39d346447ad631d450000184a0000d9ff9b0000007073340000000c9f0ac62fff884742771e45000002bc0000f0ff61ff0000707335000000ee737fc5e81e8c477a963b450000bd9c000086ff98ff000070732d000000eb1f8fc6cd272747e5207d440000a5de000000000000000070732e000000e03f57c63ef48647a8281545000071a2000096ff88ff000070732b000000f8aea2c501729247f9bf1c450000d5530000b5ff8d00000070732c00000029423dc6a0c26747cc85d24400001c8b0000000000000000707336000000da7000c6c94f934795291f450000bc790000000000000000707337000000d15006c649007d473704224500008ee10000750093ff00006d7638000000878760c6b69c0c47248b91440bebfc0ab4df7073390000008b4c7ac6750b31479c5e67440000000000000000000000000000
    Item Pickup:
    6565 f1180000 6d768c2968c6f2022547f2649e4414f8392b00007f00

    Location Changed/Initialized:
    id
    6d6b ac10000000000000010400426561728b4c7ac6750b31479c5e67440000000000007d0000006d6bad10000000000000010400426561729b2267c63b607c47bde4f6440000000000007d0000006d6bae10000000000000010400426561725a8b2745af668247fe2e20450000000000007d0000006d6baf1000000000000001040042656172d49bf8c5cb0e3947d5b3f4440000000000007d0000006d6bb01000000000000001040042656172501d0fc5aa474647b17402450000000000007d0000006d6bb110000000000000010400426561728fce6dc612185a476e345f440000000000007d0000006d6bb2100000000000000104004265617277c1ac41bb516947e5291b450000000000007d0000006d6bb310000000000000010400426561721b7953c6b96e8947a73826450000000000007d0000006d6bb410000000000000010400426561725065bdc3c3818947ab5938450000000000007d0000006d6bb510000000000000010400426561720098ebc580038e4707891c450000000000007d0000006d6bb61000000000000001040042656172f39be5c5002f62474cb0f2440000000000007d0000007073b41000005065bdc3c3818947ab5938450000000000000000000000007073b51000000098ebc580038e4707891c450000000000000000000000007073ae1000005a8b2745af668247fe2e20450000000000000000000000007073af100000d49bf8c5cb0e3947d5b3f4440000000000000000000000007073ac1000008b4c7ac6750b31479c5e67440000000000000000000000007073ad1000009b2267c63b607c47bde4f6440000000000000000000000007073b0100000501d0fc5aa474647b17402450000000000000000000000007073b11000008fce6dc612185a476e345f440000000000000000000000007073b210000077c1ac41bb516947e5291b450000000000000000000000007073b31000001b7953c6b96e8947a73826450000000000000000000000007073b6100000f39be5c5002f62474cb0f2440000000000000000000000000000
    6d6b 0100000000000000001000477265617442616c6c734f664669726500872ac7000c5ac70000a143000000800000640000006d6b0200000000000000000c004c6f73744361766542757368002351c700d62cc70000b343000000000000640000006d6b030000000000000000090042656172436865737400b0f6c500e27b470070264523fde67f8100640000006d6b0400000000000000000800436f77436865737400fe764800a16fc80040924422fe088fc5fd640000006d6b05000000000000000009004c617661436865737400bc464700d8a3c50060be440000e3380000640000006d6b0600000000000000000b00426c6f636b79436865737400f03ec500bab34600300e45000000c00000640000006d6b0700000000000000000c0047756e53686f704f776e6572005712c700048dc6000017450000ff7f0000640000006d6b0800000000000000000f004a757374696e546f6c657261626c65007c20c700007ec600e00d450000aa6a0000640000006d6b09000000000000000006004661726d65720062a84600102147005005450000e3380000640000006d6b0a00000000000000000d004d69636861656c416e67656c6fc0277e48c0ba72c800e0b0440000c7510000640000006d6b0b00000000000000000a00476f6c64656e4567673100aac3c6004a8d4600008243000000000000640000006d6b0c00000000000000000a00476f6c64656e45676732007249c7001f6fc700e09c45000000000000640000006d6b0d00000000000000000a00476f6c64656e456767330080bf460019884700302645000000000000640000006d6b0e00000000000000000a00476f6c64656e4567673400256c47000288c600b03745000000000000640000006d6b0f00000000000000000a00476f6c64656e456767350040be4400d869460070db45000000000000640000006d6b1000000000000000000a00476f6c64656e4567673600503546002c4dc60080cd43000000000000640000006d6b1100000000000000000a00476f6c64656e4567673780ed8dc7003f51c700a0cd44000000000000640000006d6b1200000000000000000a00476f6c64656e4567673800143d4700aadb4600003044000000000000640000006d6b1300000000000000000a00476f6c64656e4567673900c97e470060b3c500009a45000000000000640000006d6b1400000000000000000e0042616c6c6d65725065616b45676700a02dc5006c2cc600202446000000000000640000006d6b150000000000000000110042616c6c6d65725065616b506f7374657200a8bec500302bc60030264600000000000064000000e21800ffffffff6d6bdc130000000000000108004769616e745261741604b146263f6a47262428450000000000001e0000006d6bdd130000000000000108004769616e74526174b2efb44675d85d477d7a38450000000000001e0000006d6bde130000000000000108004769616e745261744e80d0468b3f534779af24450000000000001e0000006d6bdf130000000000000108004769616e74526174e569d546059f664702272e450000000000001e0000006d6be0130000000000000108004769616e74526174cab7f446c5436a47eee928450000000000001e0000006d6be1130000000000000108004769616e7452617495a9ee4643e081477a462f450000000000001e0000006d6be2130000000000000108004769616e74526174462cb1460fa5844716df22450000000000001e0000006d6be3130000000000000108004769616e7452617485179b46627c6147381047450000000000001e0000007073e2130000462cb1460fa5844716df22450000000000000000000000007073e313000085179b46627c6147381047450000000000000000000000007073dd130000b2efb44675d85d477d7a38450000000000000000000000007073de1300004e80d0468b3f534779af24450000000000000000000000007073df130000e569d546059f664702272e450000000000000000000000007073e0130000cab7f446c5436a47eee928450000000000000000000000007073e113000095a9ee4643e081477a462f450000000000000000000000007073dc1300001604b146263f6a47262428450000000000000000000000000000
    """

    # print("[actor spawn (%i)] %s" % (dataLen, data.hex()))

    locationInd = data.find(bytes.fromhex('6d76'))

    if locationInd == -1:
        print('Location Initialize')
        newData = bytes.fromhex('6d6b') + data

        actorInd = 0
        while actorInd > -1:
            actor = b''

            # Skip 2B for the 0x6d6b actor id reference
            # Returns -1 if not found
            actorInd = newData[2:].find(bytes.fromhex('6d6b'))

            actor = newData[:actorInd]
            # Get all the rest of data when no more 0x6d6b
            if actorInd == -1:
                actor = newData[:]

            # Modifying the data starts here
            actorId, sId, isMob, nameLen = struct.unpack(
                '<IIBH', actor[2:11+2])
            name = actor[11+2:11+2+nameLen]
            # print(hex(actorId), hex(sId), isMob, nameLen)
            print("Actor %s" % name.decode('utf-8'))

            x, y, z = struct.unpack(
                '<fff', actor[11+2+nameLen:11+2+nameLen+12])
            print(x, y, z)

            newData = newData[actorInd+2:]

    # print("[drop near (%i)] %s" % (dataLen, data.hex()))

    # sId is unknown
    # When sId and isMob are zero then it is a dropped item (guessed)
    actorId, sId, isMob, nameLen = struct.unpack('<IIBH', data[:11])
    name = data[11:11+nameLen]
    # print(hex(actorId), hex(sId), isMob, nameLen)

    # Pickup Item
    if isMob and not sId == 0:
        print("Monster Spawn %s" % name.decode('utf-8'))

    if not isMob and sId == 0:
        pickup = struct.pack('=HI', 0x6565, actorId)
        print("To pick up item %s" % name.decode('utf-8'))

        SERVER_QUEUE.append(pickup)

    return data[dataLen:]


handlers_toServer = {
    0x0000: h_noop,
    0x6d76: h_position,
    0x6a70: h_jumping_hold,
    0x7273: h_spawn,
    # 0x232a: h_chat,
    0x733d: h_weapon_slot_change,
    0x2a69: h_weapon_use,
    0x6672: h_weapon_hold,
    0x6565: h_item_pickup,  # previous was h_npc_talk_start
    0x233e: h_npc_talk_end
}


handlers_toClient = {
    0x0000: h_noop,
    0x6d61: h_mana_regen,
    0x733d: h_weapon_slot_change,  # h_weapon_slot_change,
    0x6d6b: h_actors,  # when using weapon starting, when item drops
    # 0x6d76: h_position,  # when using weapon travels
    # 0x7878: h_skip,  # when using weapon ended
    # 0x0500: h_skip,  # when using weapon ended
    0x2373: h_npc_talk_start,
    0x2366: h_npc_talk_end,
    0x7073: h_monster_near,
    0x2b2b: h_health_regen,
    0x7374: h_monster_spawn,
    # 0x7472: h_skip,  # Mob Attacked the Player
    # 0x2d39: h_skip,  # Player Died

    # Move to the main function
    # 0x6368: h_change_map,
}


def parser(data, port, origin):
    global CLOSE_CLIENT

    unkownShowServer = False
    unkownShowClient = False

    # Check is it master server
    if (port == MASTER_SERVER_PORT):
        pass
    else:
        # Loop through the packets and to process it through the handlers
        # Since the packets are bundled (e.g. jump+playerposition)
        while len(data) > 0:
            # Get the hexadecimal packet id of 2 bytes
            # Then process it by the handlers
            packetId = struct.unpack(">H", data[0:2])[0]

            # Proccess client packets
            # Log input from server
            if (origin == SERVER):
                # print("[server(%i)] %s" % (port, data.hex()))

                # 0x6368 Change Map
                if (data[:2] == b'\x63\x68'):
                    print("Client closing...")
                    CLOSE_CLIENT = port
                    return

                if (packetId not in handlers_toClient and not unkownShowServer):
                    # print("[server unknown] %s" % data.hex())
                    unkownShowServer = True

                # Skip empty bytes
                if (len(data[2:]) <= 2):
                    return

                data = handlers_toClient.get(packetId, h_noop)(data[2:])

            # Log input from client logging
            if (origin == GAME):
                # print("[client(%i)] %s" % (port, data.hex()))

                if (packetId not in handlers_toServer) and not unkownShowClient:
                    print("[game unknown] %s" % data.hex())
                    unkownShowClient = True

                # Skip empty bytes
                if (len(data[2:]) <= 2):
                    return

                data = handlers_toServer.get(packetId, h_noop)(data[2:])


"""
# Player Information
id - 4B
xyz - 8pB; 24B
pprryy - 4pB; 12B
WSAD - 1pB; 2B

Jumping: (spacebar)
               id   +  sId    xyz
[client(3002)] 6a70 01 6d76 37f053c60bb20f47237ab44 bbfc9b0a00000000 (spacebar +)

Player Location: [22B]
               id   x        y        z
[client(3002)] 6d76 37f053c6 0bb20f47 d38bb844 bbfc9b0a00000000
[client(3002)] 6d76 37f053c6 0bb20f47 479abe44 bbfc9b0a00000000
[client(3002)] 6d76 37f053c6 0bb20f47 1883c144 bbfc9b0a00000000
[client(3002)] 6d76 37f053c6 0bb20f47 2be8c144 bbfc9b0a00000000
[client(3002)] 6d76 37f053c6 0bb20f47 5280c144 bbfc9b0a00000000
[client(3002)] 6d76 37f053c6 0bb20f47 a727c044 bbfc9b0a00000000
[client(3002)] 6d76 37f053c6 0bb20f47 6926be44 bbfc9b0a00000000
[client(3002)] 6d76 37f053c6 0bb20f47 5349bb44 bbfc9b0a00000000
[client(3002)] 6d76 37f053c6 0bb20f47 f686b744 bbfc9b0a00000000
[client(3002)] 6d76 37f053c6 0bb20f47 1bedb244 bbfc9b0a00000000
[client(3002)] 6d76 37f053c6 0bb20f47 6749ae44 bbfc9b0a00000000 (landed)
               id   -  sId   xyz
[client(3002)] 6a70 00 6d76 37f053c60bb20f476749ae44 bbfc9b0a00000000 (spacebar -)


Looking Around: (Arrow Right and Arrow Left)
               id   xyz                      pp   yy   rr
[client(3002)] 6d76 fe885ac65d520f47489fa544 3cfb 056e 0000 0000 (arrow left +)
[client(3002)] 6d76 fe885ac65d520f47489fa544 3cfb 1275 0000 0000
[client(3002)] 6d76 fe885ac65d520f47489fa544 3cfb ba7a 0000 0000
[client(3002)] 6d76 fe885ac65d520f47489fa544 3cfb 4181 0000 0000
[client(3002)] 6d76 fe885ac65d520f47489fa544 3cfb 8287 0000 0000
[client(3002)] 6d76 fe885ac65d520f47489fa544 3cfb 948e 0000 0000
[client(3002)] 6d76 fe885ac65d520f47489fa544 3cfb 7094 0000 0000
[client(3002)] 6d76 fe885ac65d520f47489fa544 3cfb cf99 0000 0000
[client(3002)] 6d76 fe885ac65d520f47489fa544 3cfb eca0 0000 0000
[client(3002)] 6d76 fe885ac65d520f47489fa544 3cfb 63a6 0000 0000
[client(3002)] 6d76 fe885ac65d520f47489fa544 3cfb 2bb1 0000 0000 (arrow left -)
[client(3002)] 6d76 fe885ac65d520f47489fa544 3cfb 2bb1 0000 0000
[client(3002)] 6d76 fe885ac65d520f47489fa544 3cfb 24aa 0000 0000 (arrow right +)
[client(3002)] 6d76 fe885ac65d520f47489fa544 3cfb c2a4 0000 0000
[client(3002)] 6d76 fe885ac65d520f47489fa544 3cfb 789f 0000 0000
[client(3002)] 6d76 fe885ac65d520f47489fa544 3cfb 4d93 0000 0000
[client(3002)] 6d76 fe885ac65d520f47489fa544 3cfb e98d 0000 0000
[client(3002)] 6d76 fe885ac65d520f47489fa544 3cfb 7170 0000 0000 (arrow right -)

Moving Around: (WSAD)
               id   xyz                      pprryy       WS AD
[client(3002)] 6d76 3b6a62c6434d1347bc3dab44 74f84d970000 7f 00 (W +)
[client(3002)] 6d76 346563c6e4241347fbd0a844 74f84d970000 7f 00
[client(3002)] 6d76 ff0464c62d0b13475c5ca744 74f84d970000 7f 00
[client(3002)] 6d76 e79864c65ff31247986fa644 74f84d970000 7f 00
[client(3002)] 6d76 273765c6e8d91247d19ca544 74f84d970000 7f 00
[client(3002)] 6d76 85dc65c64bbf1247e79da444 74f84d970000 7f 00
[client(3002)] 6d76 fd8a66c637a312477c84a344 74f84d970000 7f 00
[client(3002)] 6d76 d02b67c6548912474955a244 74f84d970000 00 00 (W -)
[client(3002)] 6d76 921167c68f8d1247c886a244 74f84d970000 81 00 (S +)
[client(3002)] 6d76 89cb66c6d5981247d40aa344 74f84d970000 81 00
[client(3002)] 6d76 005866c66eab1247a3e4a344 74f84d970000 81 00
[client(3002)] 6d76 10c765c6c4c212471cbba444 74f84d970000 81 00
[client(3002)] 6d76 ab1f65c6b5dd124775bea544 74f84d970000 81 00
[client(3002)] 6d76 c97c64c6edf712477097a644 74f84d970000 81 00
[client(3002)] 6d76 dcd163c67113134750cfa744 74f84d970000 81 00
[client(3002)] 6d76 d68c62c6c64713475314ab44 74f84d970000 81 00
[client(3002)] 6d76 0d3662c6bf5513475171ab44 74f84d970000 00 00 (S -)
[client(3002)] 6d76 405d62c668721347fd11ad44 74f84d970000 00 81 (A +)
[client(3002)] 6d76 a0a162c66f8f134723b0ae44 74f84d970000 00 81
[client(3002)] 6d76 410463c600b71347a073af44 74f84d970000 00 81
[client(3002)] 6d76 8ad563c6f808144708ecaf44 74f84d970000 00 81
[client(3002)] 6d76 781764c6a22214478308b044 74f84d970000 00 00
[client(3002)] 6d76 681f64c6b8251447f10bb044 74f84d970000 00 00 (A -)
[client(3002)] 6d76 0f1c64c66b241447820ab044 74f84d970000 00 7f (D +)
[client(3002)] 6d76 7ffd63c68c1814476afdaf44 74f84d970000 00 7f
[client(3002)] 6d76 88c363c60802144790e4af44 74f84d970000 00 7f
[client(3002)] 6d76 4a7c63c65ee6134709c6af44 74f84d970000 00 7f
[client(3002)] 6d76 e2b362c693981347be14af44 74f84d970000 00 7f
[client(3002)] 6d76 614d62c6c570134714e9ac44 74f84d970000 00 7f
[client(3002)] 6d76 b5e761c6484913475cd4aa44 74f84d970000 00 7f
[client(3002)] 6d76 dfc761c6eb3c13473e6baa44 74f84d970000 00 00 (D -)

Player Spawn: (The pitch, roll, yaw are reset to zero) the id is the location
                 id   ??   x        y        z        pp   rr   yy                              
[server unknown] fc04 0000 2f991bc7 5fec9ac6 f3d21945 0000 0000 0000
Player Respawn: (When modifying the respawn location the pprryy should be reset)
               id   sId
[client(3002)] 7273 6d76 1af260c6726213477ee3a144 74f84d970000 0000
[spawn]        7273 6d76 382b72c6c6361a4772bca644 44f8e8380000 0000

Player Chat:
               id   len  chat               playerId?
[client(3002)] 232a 0300 717765             6d76d0e868c6cc131347bbc7a644af0343fb00000000 (qwe)
[client(3002)] 232a 0300 617364             6d76d0e868c6cc131347bbc7a644af0343fb00000000 (asd)
[client(3002)] 232a 0600 717765617364       6d76d0e868c6cc131347bbc7a644af0343fb00000000 (qweasd)
[client(3002)] 232a 0900 7177656173647a7863 6d76d0e868c6cc131347bbc7a644af0343fb00000000 (qweasdzxc)

Player Weapon Change Slot:
[unknown] 733d 00 6d76606851c6f4f30c47a24eac44e4fea72200000000
[unknown] 733d 01 6d76606851c6f4f30c47a24eac44e4fea72200000000
[unknown] 733d 02 6d76606851c6f4f30c47a24eac44e4fea72200000000

Player Weapon Use:
          id   nLen (n) weapon name                     direction                sId  -+
[unknown] 2a69 1000 477265617442616c6c734f6646697265    e08a72c1e01e46c1f771ed34                6d7688225ec61b270c4783239c4438f531f700000000 (Fire Ball)
[unknown] 2a69 0a00 5374617469634c696e6b                e08a72c1e01e46c1f771ed34 6672 01        6d7688225ec61b270c4783239c4438f531f700000000 (Static Link +)
[unknown] 2a69 0a00 5374617469634c696e6b                e08a72c1e01e46c1f771ed34 6672 00        6d7688225ec61b270c4783239c4438f531f700000000 (Static Link -)
[unknown] 2a69 0600 506973746f6c                        e08a72c1e01e46c1f771ed34                6d7688225ec61b270c4783239c4438f531f700000000 (G7 Pistol)
sample when changing direction
[unknown] 2a69 1000 477265617442616c6c734f6646697265 e08a72c1608540c1f771ed34 6d7688225ec61b270c4783239c4438f571f700000000 (Fire Ball)
[unknown] 2a69 1000 477265617442616c6c734f6646697265 a0b438c168912d4200000000 6d7688225ec61b270c4783239c44caf7db1e00000000 (Fire Ball)
"""

"""
# Monster Information

Loot Drop:
    Monster/Actor the item is located when there is a location bundled with it (location 0x6d76d)
    id   ?                                                           sId  itemId
    7073 880e0000 867317c6 01396a47 aae7f444000072dd00006a0088ff0000 6d76 890e0000 ba8d80c57a10ee46dccebc45f010b7ee0000 (Fire Ball)
    7073 880e0000 d2f6f7c5 41468047 bd172445000004230000680079000000 6d76 8a0e0000 66b502c612d01947103cc344ffffffff69fe (White Ball - Item Drop)
    7073 880e0000 80c3dfc5 afee8447 a4c0264500002f280000580085000000 6d76 8d0e0000 90a2fcc57a4e1c479a03c54437fcd42a0000 (Zero Cool)
"""
