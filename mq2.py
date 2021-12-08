
# adapted from sandboxelectronics.com/?p=165

import math
from MCP3008 import MCP3008
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time
import sys

class MQ():

    ######################### Hardware Related Macros #########################
    MQ_PIN                       = 0        # define which analog input channel you are going to use (MCP3008)
    RL_VALUE                     = 5        # define the load resistance on the board, in kilo ohms
    RO_CLEAN_AIR_FACTOR          = 9.83     # RO_CLEAR_AIR_FACTOR=(Sensor resistance in clean air)/RO,
                                            # which is derived from the chart in datasheet
 
    ######################### Software Related Macros #########################
    CALIBARAION_SAMPLE_TIMES     = 50       # define how many samples you are going to take in the calibration phase
    CALIBRATION_SAMPLE_INTERVAL  = 500      # define the time interval(in milisecond) between each samples in the
                                            # cablibration phase
    READ_SAMPLE_INTERVAL         = 50       # define the time interval(in milisecond) between each samples in
    READ_SAMPLE_TIMES            = 5        # define how many samples you are going to take in normal operation 
                                            # normal operation
 
    ######################### Application Related Macros ######################
    GAS_LPG                      = 0
    GAS_CO                       = 1
    GAS_SMOKE                    = 2

    def __init__(self, Ro=10, mq_pin=0):
        # create the spi bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        # create the cs (chip select)
        cs = digitalio.DigitalInOut(board.D5)
        # create the mcp object
        self.mcp = MCP.MCP3008(spi, cs)

        # create an analog input channel on pin 0
        self.chan = AnalogIn(self.mcp, MCP.P0)

        self.baseline = self.baseline_calibrate()
                
    def read(self):
        return self.chan.voltage/3.3

    def multisample_read(self):
        rs = 0.0

        for i in range(self.READ_SAMPLE_TIMES):
            rs += self.read()
            time.sleep(self.READ_SAMPLE_INTERVAL/1000.0)

        rs = rs/self.READ_SAMPLE_TIMES

        return (rs/self.baseline)*100 #percent change of read from baseline
    
    def baseline_calibrate(self):
        val = 0.0
        for i in range(self.CALIBARAION_SAMPLE_TIMES):          # take multiple samples
            val += self.read()
            time.sleep(self.CALIBRATION_SAMPLE_INTERVAL/1000.0)
            
        val = val/self.CALIBARAION_SAMPLE_TIMES                 # calculate the average value

        return val