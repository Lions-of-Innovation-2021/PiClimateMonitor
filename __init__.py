from pi_bt_server import host_server
from data_reader import DataReader

reader = DataReader()
host_server(reader.read)