from random import randint

import datetime

def get_date() -> datetime.datetime:
    return datetime.datetime.now()
    
class Controlled_UUID:
    uuids_given = {}
    
    hexMap = {idx: str(idx) for idx in range(10)}
    hexMap[10] = 'a'
    hexMap[11] = 'b'
    hexMap[12] = 'c'
    hexMap[13] = 'd'
    hexMap[14] = 'e'
    hexMap[15] = 'f'

    def __init__(self, version = 4, n = 4):
        if version > 4 or version < 0:
            raise Exception("Version outside the range!")

        if n > 15 or n < 0:
            raise Exception("Variant amount is outside the range!")

        self.n = n
        self.version = version
        self.uuid = ""

    def getHexRange(self, num):
        return "".join(self.getNextHex() for _ in range(num))

    def getUuid(self):
        for _ in range(10):
            result = self.getHexRange(8) + "-" + self.getHexRange(4)
            result += "-" + self.getNextHex(bitsLeft = 0, val = self.version) + self.getHexRange(3)

            bitAmount = self.n
            count = 1
            while bitAmount > 1:
                bitAmount >>= 1
                count += 1

            result += "-" + self.getNextHex(bitsLeft = 4 - count, val = self.n) + self.getHexRange(3)
            result += "-" + self.getHexRange(12)

            try:
                self.uuids_given[result]
            except:
                self.uuids_given[result] = True
                return result
        return False

    def str2Hex(self, binString):
        hexString = ""

        for idx in range(0, len(binString), 4):
            hexString += self.hexMap[int(binString[idx:idx+4], 2)]

        return hexString

    def getNextHex(self, bitsLeft = 4, val = -1):
        binString = "".join([str(randint(0, 1)) for _ in range(bitsLeft)])
        if val != -1:
            binString = bin(val)[2:] + binString
        return self.str2Hex(binString)

def get_new_uuid() -> str:
    return Controlled_UUID().getUuid()
