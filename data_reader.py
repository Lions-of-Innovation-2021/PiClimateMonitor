import sheets_talker
import adafruit_dht
import board
from time import sleep
from mq2 import MQ

def get_alert_msg(smoke, risk):
    alert = "None"

    if smoke > 10:
        alert = f"Smoke is Present. Risk: {risk}"
    else:
        if risk < 10.5:
            alert = "Very Low"
        elif risk > 10.5 and risk < 40:
            alert = "Low"
        elif risk > 40 and risk < 63:
            alert = "Medium"
        elif risk > 63 and risk < 70:
            alert = "High"
        elif risk > 70:
            alert = "Very High"
    
    return alert

class DataReader():
    def __init__(self):
        self.dhtDevice = adafruit_dht.DHT22(board.D4)
        self.mq = MQ()

    def read(self):
        msg = ""
        try:
            #Read data from DHT22
            temperature_c = self.dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = self.dhtDevice.humidity
            # perc = mq.MQPercentage() #perc["GAS_LPG"] perc["CO"] perc["SMOKE"]
            # smoke = perc["SMOKE"]
            smoke = self.mq.multisample_read()
            risk = temperature_f - (temperature_f * (humidity / 100))
            alert = get_alert_msg()

            msg = {
                "Temperature": temperature_c,
                "Humidity": humidity,
                "Smoke": smoke,
                "Risk": risk,
                "Alert": alert
            }
        except RuntimeError as error:
            #If error occurs, return "error" message
            msg = "Error"
        except Exception as error:
            self.dhtDevice.exit()
            raise error
        
        return msg