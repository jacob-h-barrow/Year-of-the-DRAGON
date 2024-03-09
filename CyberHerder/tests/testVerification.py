from NetworkGoldRush import getIt
from verification import terminate

if __name__ == "__main__":
    for ipv4 in getIt("IPv4", 10):
        print(terminate("IPv4", ipv4), "False")
    print(terminate("IPv4", "0.0.0.1.2"), "True")
    print(terminate("IPv4", "260.254.25.25"), "True")
    for ipv6 in getIt("IPv6", 10):
        print(terminate("IPv6", ipv6), "False")
    print(terminate("IPv6", ":::1"), "True")
    print(terminate("IPv6", "TF::FF"), "True")

    for mac48 in getIt("MAC-eui48", 5):
        print(terminate("MAC-eui48", mac48), "False")
    print(terminate("MAC-eui48", "TF:FF:FF:FF:FF:FF"), "True")
    print(terminate("MAC-eui48", "FF:FF:FF:FF:FF:FF:FF"), "True")
    for mac64 in getIt("MAC-eui64", 5):
        print(terminate("MAC-eui64", mac64), "False")
    print(terminate("MAC-eui64", "TF:FF:FF:FF:FF:FF:FF:FF"), "True")
    print(terminate("MAC-eui64", "FF:FF:FF:FF:FF:FF:FF:FF:FF"), "True")
    
    for phone in getIt("Phones", 5):
        print(terminate("Phone", phone), "False")
    print(terminate("Phone", "11111111111"), "True")
    print(terminate("Phone", "111111111A"), "True")

    for zipCode in getIt("Postal Codes", 5):
        print(terminate("Postal Code", zipCode), "False")
    print(terminate("Postal Code", "0112345"), "True")
    print(terminate("Postal Code", "10234A"), "True")
    
    for uid in getIt("UIDs", 5):
        print(terminate("UID", uid), "False")
    print(terminate("UID", "01333333333"), "True")
    print(terminate("UID", "010232123"), "True")
