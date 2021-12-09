import bluetooth
import subprocess

def receive_data(client_sock):
    data = client_sock.recv(1024)
    print("Received: [%s]" % data)

def main():
    subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])

    print("Hosting Pi bluetooth server...")
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    port = 1
    server_sock.bind(("",port))

    # begin listening for connection
    print("Lisetning to port [%i]" % port)
    server_sock.listen(port)   # can't find documentation on it

    # wait for a connection from client
    client_sock, address = server_sock.accept()
    print(address)
    device_name = bluetooth.lookup_name(address)
    print(f"Accepted connection from {device_name} ({address})")

    # receive data
    while True:
        receive_data(client_sock)
    
    # cleanup
    client_sock.close()
    server_sock.close()

main()