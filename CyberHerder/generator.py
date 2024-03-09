from .GenerateMACAddresses import generateMACaddresses
from .GeneratePhoneNumbers import generatePhones
from .GenerateIPv4Addresses import generateIPv4Addresses
from .GenerateIPv6Addresses import generateIPv6Addresses
from .GeneratePostalCodes import generatePostalCodes
from .GenerateUids import generateUids
from .GenerateCreditCards import generateCreditCards
from .GenerateEmails import generateEmails
from .GenerateCompanies import generateCompanies
from .GeneratePins import generatePins
from .GenerateUsernames import generateUsernames
from .GeneratePasswords import generatePasswords
from .GenerateGPS import generateGPS
from .DateRanger import DateRangeGenerator

class Generator:
    def __init__(self):
        pass

    def getIP(self, version: str, amount: int):
        if version == "4":
            return generateIPv4Addresses(amount)
        else:
            return generateIPv6Addresses(amount)

    def getMAC(self, version: str, amount: int):
        if version == "48":
            return generateMACaddresses(amount)
        else:
            return generateMACaddresses(amount, eui48 = False)

    def getPhones(self, amount: int):
        return generatePhones(amount)

    def getDateRange(self, amount: int, day: int, month: int, year: int, forward = True):
        return [str(date) for date in DateRangeGenerator(day, month, year, count = amount, forward = forward)]

    def getPostalCodes(self, amount):
        return generatePostalCodes(amount)

    def getEmails(self, amount):
        return generateEmails(amount)

    def getCompanies(self, amount):
        return generateCompanies(amount)

    def getUids(self, amount):
        return generateUids(amount)

    def getCreditCards(self, amount):
        return generateCreditCards(amount)

    def getPins(self, amount):
        return generatePins(amount)

    def getUsernames(self, amount):
        return generateUsernames(amount)

    def getPasswords(self, amount):
        return generatePasswords(amount)

    def getGPS(self, amount):
        return generateGPS(amount)

# Current Options
options = ["IPv4", "IPv6", "MAC-eui48", "MAC-eui64", "Phones", "DateRange", "Postal Codes", "UIDs", "Credit Cards", "GPS", "Emails", "Pins", "Usernames", "Passwords", "Companies"]
# DateEnd is [day, month, year]
def generate(option: str, amount: int, day: int = 15, month: int = 1, year: int = 2022, forward: bool = True):
    if option not in options:
        raise Exception("Option not listed!")
    
    generator = Generator()
    idx = options.index(option)

    try:
        if idx == 0 or idx == 1:
            return generator.getIP(option[-1], amount)
        elif idx == 2 or idx == 3:
            return generator.getMAC(option[-2:], amount)
        elif idx == 4:
            return generator.getPhones(amount)
        elif idx == 5:
            return generator.getDateRange(amount, day, month, year, forward = forward)
        elif idx == 6:
            return generator.getPostalCodes(amount)
        elif idx == 7:
            return generator.getUids(amount)
        elif idx == 8:
            return generator.getCreditCards(amount)
        elif idx == 9:
            return generator.getGPS(amount)
        elif idx == 10:
            return generator.getEmails(amount)
        elif idx == 11:
            return generator.getPins(amount)
        elif idx == 12:
            return generator.getUsernames(amount)
        elif idx == 13:
            return generator.getPasswords(amount)
        else:
            return generator.getCompanies(amount)
    except:
        print("Guess you offended the system. Try something else!")

if __name__ == "__main__":
    print(generate("IPv4", 10))
    print(generate("IPv6", 10))
    print(generate("MAC-eui48", 10))
    print(generate("MAC-eui64", 10))
    print(generate("Phones", 10))
    print(generate("DateRange", 10, day = 20, month = 2, year = 2020))
    print(generate("DateRange", 10, day = 20, month = 3, year = 2010, forward = False))
    print(generate("Postal Codes", 10))
    print(generate("UIDs", 10))
    print(generate("Credit Cards", 10))
    print(generate("GPS", 10))
    print(generate("Emails", 10))
    print(generate("Pins", 10))
    print(generate("Usernames", 10))
    print(generate("Passwords", 10))
    print(generate("Companies", 10))
