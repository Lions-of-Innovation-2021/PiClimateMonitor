import sys, time, os
sys.path.append('/home/PiClimateMonitor')
print(os.getcwd())
from gas_sensor import mq as mq

try:
    print("Press CTRL+C to abort.")
    
    MQ = mq.MQ()
    while True:
        perc = mq.MQPercentage()
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("LPG: %g ppm, CO: %g ppm, Smoke: %g ppm" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
        sys.stdout.flush()
        time.sleep(0.1)

except:
    print("\nAbort by user")