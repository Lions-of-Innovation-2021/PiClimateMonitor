import bluetooth
import subprocess

from bluetooth.btcommon import BluetoothError

def host_server(get_data_reading):
    subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])

    print("Hosting Pi bluetooth server...")
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1    # automatically find a port
    server_sock.bind(("",port))
    server_sock.listen(1)   # 1 or port? need documentation
    print("Lisetning to port [%i]" % port)

    #adv service:
    # uuid = "36263756-593d-11ec-bae7-5f350ed39ff8"   # randomly generated, consistent in Climate monitor code
    # bluetooth.advertise_service(server_sock, "Climate_Monitor", uuid)

    client_sock = None
    address = None

    # receive data
    while True:
        try:
            if client_sock:
                msg = client_sock.recv(1024)
                print("Recieved message:", msg)
                if msg and len(msg) > 0:
                    command = msg.decode("utf-8") 
                    print("Command:", command)
                    if command == "read":
                        client_sock.send(get_data_reading())
            else:
                # wait for a connection from client
                client_sock, address = server_sock.accept()
                address, port = address[0], address[1]
                device_name = bluetooth.lookup_name(address)
                print(f"Accepted connection from {device_name} ({address})")
        except KeyboardInterrupt:
            break
        except bluetooth.btcommon.BluetoothError as bterror:
            client_sock = None
            address = None
            print("Disconnected from Bluetooth:", bterror)
        except any as error:
            print("Error processing command:", error)
            
    
    # cleanup
    client_sock.close()
    server_sock.close()