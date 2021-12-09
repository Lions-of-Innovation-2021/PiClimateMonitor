import bluetooth

PI_NAME = "MIMS_STEM_RasPi"
PI_ADDRESS = None

def find_pi():
    global PI_ADDRESS
    nearby_devices = bluetooth.discover_devices()
    for bdaddr in nearby_devices:
        bdname = bluetooth.lookup_name(bdaddr)
        print("Found:", bdname)
        if bdname == PI_NAME:
            PI_ADDRESS = bdaddr
            break

def main():
    find_pi()
    if PI_ADDRESS:
        print("Found Raspberry Pi")
        
    else:
        raise Exception("Raspberry PI not found!")

main()