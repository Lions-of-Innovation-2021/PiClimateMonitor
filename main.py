import sheets_talker
import adafruit_dht
from gas_detection import GasDetection
import board
from time import sleep

#MQ-2 Calibration 
detection = GasDetection()

#Analyze Data
#Variable values will be replaced by the values from the sensors
temperature = 0 #Fahrenheit
humidity = 0 #We want humidity as a decimal
smoke = 0 #Remember that smoke is measured in output on a 3.3V scale
alert = ""
dhtDevice = adafruit_dht.DHT22(board.D4)
box_id = sheets_talker.worksheet.row_count - 1

while True:
  try:
    #Read data from MQ-2
    ppm = detection.percentage()
    smoke = ppm[detection.SMOKE_GAS]
    #Read data from DHT22
    temperature_c = dhtDevice.temperature
    temperature = temperature_c * (9 / 5) + 32
    humidity = dhtDevice.humidity
    risk = temperature - (temperature * (humidity / 100))
    if smoke > 200 or risk > 10.5:
      alert = "ALERT!"
    else:
      alert = "No Alert"
    box_id += 1
    box_sheet_range = 'A' + str(box_id) + ':B' + str(box_id)  # add one for the column titles
    sheets_talker.worksheet.append_row([str(box_id), str(risk), str(smoke), str(temperature), str(humidity), alert]) #add a new row for the box
    print(box_id, box_sheet_range)
  except RuntimeError as error:
    #If error occurs, print "error" to spreadsheet and continue with code
    print(box_id, box_sheet_range)
    sheets_talker.worksheet.update(box_sheet_range, [[str(box_id), "error"]])
    continue
  except Exception as error:
    dhtDevice.exit()
    raise error
  sleep(2)