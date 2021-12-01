import sheets_talker
import adafruit_dht
import board
from time import sleep
 
#Analyze Data
#Variable values will be replaced by the values from the sensors
temperature = 0 #Fahrenheit
humidity = 0 #We want humidity as a decimal
smoke = 0 #Remember that smoke is measured in output on a 3.3V scale
dhtDevice = adafruit_dht.DHT22(board.D4)

def init_box():
  box_id = sheets_talker.worksheet.row_count
  box_sheet_range = 'A' + str(box_id+1) + ':B' + str(box_id+1)  # add one for the column titles
  sheets_talker.worksheet.add_rows(1) #add a new row for the box
  return box_id, box_sheet_range

while True:
  try:
    #Read data from DHT22
    temperature_c = dhtDevice.temperature
    temperature = temperature_c * (9 / 5) + 32
    humidity = dhtDevice.humidity
    risk = temperature - (temperature * (humidity / 100))
    box_id, box_sheet_range = init_box()
    print(box_id, box_sheet_range)
    sheets_talker.worksheet.update(box_sheet_range, [[str(box_id), str(risk)]])
  except RuntimeError as error:
    #If error occurs, print "error" to spreadsheet and continue with code
    box_id, box_sheet_range = init_box()
    print(box_id, box_sheet_range)
    sheets_talker.worksheet.update(box_sheet_range, [[str(box_id), "error"]])
    continue
  except Exception as error:
    dhtDevice.exit()
    raise error
  sleep(5)