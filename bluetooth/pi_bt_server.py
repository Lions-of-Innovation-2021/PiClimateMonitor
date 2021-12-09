import bluetooth
import subprocess

def receive_data(client_sock):
    data = client_sock.recv(1024)
    print("Received: [%s]" % data)

def host_server():
    subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])

    print("Hosting Pi bluetooth server...")
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = bluetooth.get_available_port(bluetooth.RFCOMM)
    server_sock.bind(("",port))
    server_sock.listen(1)   # 1 or port? need documentation
    print("Lisetning to port [%i]" % port)

    #adv service:
    uuid = "36263756-593d-11ec-bae7-5f350ed39ff8"   # randomly generated, consistent in Climate monitor code
    bluetooth.advertise_service(server_sock, "Climate_Monitor", uuid)

    # wait for a connection from client
    client_sock, address = server_sock.accept()
    address, port = address[0], address[1]
    device_name = bluetooth.lookup_name(address)
    print(f"Accepted connection from {device_name} ({address})")

    # receive data
    while True:
        receive_data(client_sock)
    
    # cleanup
    client_sock.close()
    server_sock.close()

host_server()