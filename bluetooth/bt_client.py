import bluetooth

PI_NAME = "MIMS_STEM_RasPi"
PI_ADDRESS = None

def find_pi():
    global PI_ADDRESS
    nearby_devices = bluetooth.discover_devices()
    for bdaddr in nearby_devices:
        print(bdaddr)
        bdname = bluetooth.lookup_name(bdaddr)
        print("Found:", bdname)
        if bdname == PI_NAME:
            PI_ADDRESS = bdaddr
            break

def main():
    print("Searching for Pi Bluetooth...")
    find_pi()

    if PI_ADDRESS:
        print("Found Raspberry Pi")

        port = 1

        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((PI_ADDRESS, port))

        sock.send("test data!")

        sock.close()
    else:
        raise Exception("Raspberry PI not found!")

main()