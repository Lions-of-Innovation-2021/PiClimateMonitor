# Reads sensor data on the Raspberry Pi

import sheets_talker
import adafruit_dht
import board
from time import sleep
from mq2 import MQ

# Formats alert message from smoke & risk.
def get_alert_msg(smoke, risk):
    alert = "None"

    if smoke > 5:
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

# Object for reading data.
class DataReader():
    def __init__(self):
        # Temp/Humidity device.
        self.dhtDevice = adafruit_dht.DHT22(board.D4)
        
        #MQ3008 (analog-digital chip) connection for reading from gas sensor
        self.mq = MQ()

    def read(self):
        msg = ""
        try:
            # Read data from DHT22
            temperature_c = self.dhtDevice.temperature
            humidity = self.dhtDevice.humidity

            # Read data from M3008 SPI
            smoke = self.mq.multisample_read()

            # Formatting, calculations
            temperature_f = temperature_c * (9 / 5) + 32
            risk = temperature_f - (temperature_f * (humidity / 100))
            alert = get_alert_msg(smoke, risk)

            # Final return data
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
            print("Read Error:", error)
        except OverflowError as error:
            # This happens when the DHT is wired incorrectly. Found this out the hard way.
            print("Fatal DHT error")
            raise error
        except Exception as error:
            # Fatal error with dht device
            self.dhtDevice.exit()
            raise error
        
        return msg