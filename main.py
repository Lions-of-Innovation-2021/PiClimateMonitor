import sheets_talker
import Adafruit_DHT as dht
from time import sleep
 
#Analyze Data
#Variable values will be replaced by the values from the sensors
temperature = 0 #Fahrenheit
humidity = 0 / 100 #We want humidity as a decimal
smoke = 0 #Remember that smoke is measured in output on a 3.3V scale

def init_box():
  box_id = sheets_talker.worksheet.row_count
  box_sheet_range = 'A' + str(box_id+1) + ':B' + str(box_id+1)  # add one for the column titles
  sheets_talker.worksheet.add_rows(1) #add a new row for the box
  return box_id, box_sheet_range
 
def getDHT22Data():
  #Read data from DHT22
  humidity, temperature = dht.read_retry(dht.DHT22, DHT)

#Set data pin for DHT22
DHT = 4
while True:
  getDHT22Data()
  risk = temperature - (temperature * humidity)
  box_id, box_sheet_range = init_box()
  print(box_id, box_sheet_range)
  sheets_talker.worksheet.update(box_sheet_range, [[str(box_id), str(risk)]])
  sleep(5)
