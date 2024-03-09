from generator import generate

if __name__ == "__main__":
    try:
        print(generate("IPv5", 0))
    except:
        print("Exception Caught!")
    print(generate("IPv4", 10))
    print(generate("IPv6", 10))
    print(generate("MAC-eui48", 10))
    print(generate("MAC-eui64", 10))
    print(generate("Phones", 10))
    print(generate("DateRange", 10, day = 10, month = 2, year = 2020))
    print(generate("DateRange", 10, day = 10, month = 2, year = 2020, forward = False))
