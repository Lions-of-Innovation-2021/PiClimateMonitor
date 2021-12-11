import bluetooth
import time
import sheets_talker
import json

PI_NAME = "MIMS_STEM_RasPi"
PI_SERVICE_UUID = "36263756-593d-11ec-bae7-5f350ed39ff8"

pi_address = None
pi_sock = None

def find_pi():
    global pi_address
    nearby_devices = bluetooth.discover_devices()
    for bdaddr in nearby_devices:
        bdname = bluetooth.lookup_name(bdaddr)
        print("Found:", bdname)
        if bdname == PI_NAME:
            pi_address = bdaddr
            break

def connect_to_pi():
    global pi_sock
    print("Searching for Pi Bluetooth...")
    find_pi()

    if pi_address:
        print("Found Raspberry Pi")

        port = 1

        pi_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        pi_sock.connect((pi_address, port))
    else:
        raise Exception("Raspberry PI not found!")

# def connect_to_pi():
#     service_matches = bluetooth.find_service(uuid = PI_SERVICE_UUID)

#     if len(service_matches) == 0:
#         print("Failed to find Climate Monitor service.")
#         sys.exit(0)

#     first_match = service_matches[0]
#     name = first_match["name"]
#     host = first_match["host"]
#     port = first_match["port"]

#     print(f"Connecting to \"{name}\" on {host}")

#     pi_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
#     pi_sock.connect((host, port))

box_id = sheets_talker.worksheet.row_count - 1

def send_read_request():
    pi_sock.send("read")
    data = pi_sock.recv(1024)
    return data
    
def close_connection():
    pi_sock.close()

connect_to_pi()
while True:
    try:
        box_id += 1
        print("Sending read request...")
        data = send_read_request()
        data = json.loads(data.decode('utf-8'))
        print(data)
        print(f"Data read: {data}")

        # publish data to google sheets
        msg = ""
        if data == "Error":
            msg = [box_id, "Error"]
        else:
            msg = [box_id, data['Smoke'], data['Risk'], data['Temperature'], data['Humidity'], data['Alert']]
        sheets_talker.worksheet.append_row(msg, value_input_option='USER_ENTERED') #add a new row for the box
    except ValueError:
        print("Error fetching and publishing data.")
    except KeyboardInterrupt:
        break

    time.sleep(1)
