import bluetooth
import subprocess

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

    # wait for a connection from client
    client_sock, address = server_sock.accept()
    address, port = address[0], address[1]
    device_name = bluetooth.lookup_name(address)
    print(f"Accepted connection from {device_name} ({address})")

    # receive data
    while True:
        msg = client_sock.recv(1024)
        if len(msg) > 0:
            command = msg[0]
            if command == "read":
                client_sock.send(get_data_reading())
    # cleanup
    client_sock.close()
    server_sock.close()