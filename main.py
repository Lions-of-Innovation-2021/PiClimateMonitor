import sheets_talker
import adafruit_dht
import board
from time import sleep
from mq import MQ


#Analyze Data
#Variable values will be replaced by the values from the sensors
temperature = 0 #Fahrenheit
humidity = 0 #We want humidity as a decimal
smoke = 0 #Remember that smoke is measured in output on a 3.3V scale
alert = ""
dhtDevice = adafruit_dht.DHT22(board.D4)
mq = MQ()
box_id = sheets_talker.worksheet.row_count - 1

while True:
  try:
    #Read data from DHT22
    temperature_c = dhtDevice.temperature
    temperature = temperature_c * (9 / 5) + 32
    humidity = dhtDevice.humidity
    perc = mq.MQPercentage() #perc["GAS_LPG"] perc["CO"] perc["SMOKE"]
    smoke = perc["SMOKE"]
    risk = temperature - (temperature * (humidity / 100))
    if smoke > 200:
      alert = f"ALERT! Smoke Level is {smoke} \n Fire Risk is {risk}"
    elif risk < 10.5:
      alert = "Fire Risk is very low"
    elif risk > 10.5 and risk < 40:
      alert = "Fire Risk is low"
    elif risk > 40 and risk < 50:
      alert = "Fire Risk is medium"
    elif risk > 50 and risk < 70:
      alert = "Fire Risk is high"
    elif risk > 70:
      alert = "Fire Risk is very high"
    box_id += 1
    box_sheet_range = 'A' + str(box_id) + ':B' + str(box_id)  # add one for the column titles
    sheets_talker.worksheet.append_row([str(box_id), str(risk), str(smoke), str(temperature), str(humidity), alert]) #add a new row for the box
    print(box_id, box_sheet_range)
  except RuntimeError as error:
    #If error occurs, print "error" to spreadsheet and continue with code
    print(box_id, box_sheet_range)
    sheets_talker.worksheet.append_row([str(box_id), "error", "error", "error", "error", "error"])
    continue
  except Exception as error:
    dhtDevice.exit()
    raise error
  sleep(5) #Takes reading every 5 seconds
