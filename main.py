import sheets_talker
import adafruit_dht
import board
from time import sleep
# from mq import MQ
from mq2 import MQ

#Analyze Data
#Variable values will be replaced by the values from the sensors
temperature = 0 #Fahrenheit
humidity = 0 #We want humidity as a decimal
smoke = 0 #Remember that smoke is measured in output on a 3.3V scale
alert = ""
riskLevel = ""
dhtDevice = adafruit_dht.DHT22(board.D4)
# mq = MQ(analogPin=0)
mq = MQ()

row = sheets_talker.worksheet.row_count - 1

while True:
  try:
    #Read data from DHT22
    temperature_c = dhtDevice.temperature
    temperature_f = temperature_c * (9 / 5) + 32
    humidity = dhtDevice.humidity
    # perc = mq.MQPercentage() #perc["GAS_LPG"] perc["CO"] perc["SMOKE"]
    # smoke = perc["SMOKE"]
    smoke = mq.multisample_read()
    risk = temperature_f - (temperature_f * (humidity / 100))
      
    if risk < 10.5:
      riskLevel = "Very Low"
    elif risk > 10.5 and risk < 40:
      riskLevel = "Low"
    elif risk > 40 and risk < 63:
      riskLevel = "Medium"
    elif risk > 63 and risk < 70:
      riskLevel = "High"
    elif risk > 70:
      riskLevel = "Very High"
      
    if smoke > 10:
      alert = f"Smoke is Present \n {riskLevel}"
    else:
      alert = riskLevel
    
    row += 1

    message = [row, smoke, risk, temperature_f, humidity, alert]
    sheets_talker.worksheet.append_row(message) #add a new row for the box
    print(row, ":", message)

  except RuntimeError as error:
    #If error occurs, print "error" to spreadsheet and continue with code
    print(row, "Error: ", error)
    sheets_talker.worksheet.append_row([row, "error", "error", "error", "error", "error"])
    continue
  except Exception as error:
    dhtDevice.exit()
    raise error
  sleep(0.5) #Takes reading every 5 seconds
